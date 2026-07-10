"""A2AClient — send and receive A2A messages between Orchestrator and Specialist.

Message types used in GuildOS:
  task/invite    — Orchestrator → Specialist (Step 4, synchronous)
  task/quote     — Specialist → Orchestrator (Step 4, response)
  task/send      — Orchestrator → Specialist (Step 6, non-blocking return_immediately)
  task/delivered — Specialist → Orchestrator (Step 9, proactive push via SpecialistA2AClient)
  task/accepted  — Orchestrator → Specialist (Step 11, synchronous)
  feedback/request — Specialist → Orchestrator (Step 13, proactive push via SpecialistA2AClient)

All messages are logged to logs/a2a_trace_{date}.json.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

from a2a.client.client_factory import ClientFactory
from a2a.types import a2a_pb2

logger = logging.getLogger(__name__)

TRACE_DIR = Path(__file__).parent.parent.parent.parent / "logs"


def _log_message(direction: str, msg_type: str, payload: dict) -> None:
    """Log an A2A message to the trace file."""
    trace_file = TRACE_DIR / f"a2a_trace_{date.today().isoformat()}.json"
    entry = {
        "direction": direction,
        "type": msg_type,
        "payload": payload,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(trace_file.read_text()) if trace_file.exists() else []
    existing.append(entry)
    trace_file.write_text(json.dumps(existing, indent=2))
    logger.info("A2A %s %s: %s", direction, msg_type, payload.get("task_id", ""))


def _build_message(role: int, text: str, task_id: str | None = None) -> a2a_pb2.Message:
    """Build an A2A Message with a text part."""
    return a2a_pb2.Message(
        message_id=str(uuid.uuid4()),
        role=role,
        parts=[a2a_pb2.Part(text=text)],
        task_id=task_id or "",
    )


def _build_send_request(
    message: a2a_pb2.Message,
    configuration: a2a_pb2.SendMessageConfiguration | None = None,
) -> a2a_pb2.SendMessageRequest:
    """Wrap a Message in a SendMessageRequest.

    Args:
        message: The A2A Message to send.
        configuration: Optional SendMessageConfiguration (e.g. return_immediately).
    """
    if configuration is not None:
        return a2a_pb2.SendMessageRequest(
            message=message, configuration=configuration
        )
    return a2a_pb2.SendMessageRequest(message=message)


def _extract_response(resp: a2a_pb2.StreamResponse) -> dict:
    """Extract the GuildOS payload from a single A2A StreamResponse.

    Handles both the 'message' oneof (immediate response) and the 'task'
    oneof (async Task lifecycle, payload in task.status.message).
    """
    result = {}
    which = resp.WhichOneof("payload")
    if which == "message":
        msg = resp.message
        for part in msg.parts:
            if part.text:
                try:
                    result = json.loads(part.text)
                except (json.JSONDecodeError, ValueError):
                    result = {"text": part.text}
        result["message_id"] = msg.message_id
        result["task_id"] = msg.task_id
    elif which == "task":
        task = resp.task
        if task.status.HasField("message"):
            msg = task.status.message
            for part in msg.parts:
                if part.text:
                    try:
                        result = json.loads(part.text)
                    except (json.JSONDecodeError, ValueError):
                        result = {"text": part.text}
            result["message_id"] = msg.message_id
        result["task_id"] = task.id
        result["task_state"] = a2a_pb2.TaskState.Name(task.status.state)
    return result


async def _send_to_agent(
    agent_url: str,
    message: a2a_pb2.Message,
    configuration: a2a_pb2.SendMessageConfiguration | None = None,
) -> dict:
    """Send a message to an A2A agent and return the response as a dict.

    Uses the a2a-sdk ClientFactory to resolve the agent card and send
    the message via the configured transport.

    Args:
        agent_url: URL of the target A2A agent.
        message: The A2A Message to send.
        configuration: Optional SendMessageConfiguration (e.g. return_immediately
                       for non-blocking task/send).
    """
    factory = ClientFactory()
    client = await factory.create_from_url(agent_url)
    request = _build_send_request(message, configuration)
    responses = []
    async for response in client.send_message(request):
        responses.append(response)
    client.close()

    if not responses:
        return {}

    return _extract_response(responses[-1])


async def send_invite(specialist_endpoint: str, task_spec: dict) -> dict:
    """Send task/invite to Specialist. Returns the full A2A response dict.

    The response dict contains the quote fields (scope, estimated_cost_wei,
    deadline_iso) from the Specialist, plus message_id and task_id from
    the A2A transport.

    Args:
        specialist_endpoint: URL of the Specialist A2A agent (e.g. http://localhost:10001).
        task_spec: Task specification dict.

    Returns:
        Response dict containing the quote and transport metadata.
    """
    payload = {"type": "task/invite", "task_spec": task_spec}
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
    )
    _log_message("outgoing", "task/invite", payload)
    response = await _send_to_agent(specialist_endpoint, message)
    _log_message("incoming", "task/quote", response)
    return response


async def send_task(specialist_endpoint: str, task: dict) -> str:
    """Send task/send (non-blocking) to Specialist. Returns the task_id.

    Sets return_immediately=True in the SendMessageConfiguration so the
    Specialist returns WORKING immediately — the harness does the actual
    work outside the A2A thread. The Orchestrator polls via poll_task()
    or receives a proactive task/delivered push later.

    The task payload must include orchestrator_endpoint — without it,
    the Specialist has nowhere to push the proactive result, so the task
    is rejected as under-specified (specs/scenarios/05_task_delegation.feature).

    Args:
        specialist_endpoint: URL of the Specialist A2A agent.
        task: Full task payload dict (must include orchestrator_endpoint).

    Returns:
        The A2A task_id from the WORKING response.

    Raises:
        ValueError: If task.orchestrator_endpoint is missing.
    """
    if not task.get("orchestrator_endpoint"):
        raise ValueError(
            "task.orchestrator_endpoint is required — the Specialist needs "
            "it to push proactive results back to the Orchestrator"
        )

    payload = {"type": "task/send", "task": task}
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
    )
    configuration = a2a_pb2.SendMessageConfiguration(
        return_immediately=True,
    )
    _log_message("outgoing", "task/send", payload)
    response = await _send_to_agent(specialist_endpoint, message, configuration)
    _log_message("incoming", "task/send_response", response)
    return response.get("task_id", message.message_id)


async def send_accepted(specialist_endpoint: str, task_id: str) -> None:
    """Send task/accepted to Specialist after human approval at Gate 2.

    Args:
        specialist_endpoint: URL of the Specialist A2A agent.
        task_id: The A2A task ID to confirm.
    """
    payload = {"type": "task/accepted", "task_id": task_id}
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
        task_id=task_id,
    )
    _log_message("outgoing", "task/accepted", payload)
    await _send_to_agent(specialist_endpoint, message)


async def poll_task(endpoint: str, task_id: str) -> dict:
    """Poll an A2A agent's task state via tasks/get.

    Returns the current task state (WORKING, COMPLETED, etc.) plus any
    payload embedded in the task's status.message (e.g. the deliverable
    hash and reference from a COMPLETED Specialist task).

    Args:
        endpoint: URL of the A2A agent whose task store to poll.
        task_id: The task ID returned by send_task().

    Returns:
        Dict with task_id, task_state, and any fields from status.message.
    """
    factory = ClientFactory()
    client = await factory.create_from_url(endpoint)
    request = a2a_pb2.GetTaskRequest(id=task_id)
    task = await client.get_task(request)
    client.close()

    result = {
        "task_id": task.id,
        "task_state": a2a_pb2.TaskState.Name(task.status.state),
    }
    if task.status.HasField("message"):
        msg = task.status.message
        for part in msg.parts:
            if part.text:
                try:
                    result.update(json.loads(part.text))
                except (json.JSONDecodeError, ValueError):
                    result["text"] = part.text
    return result
