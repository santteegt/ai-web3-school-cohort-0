"""A2AClient — send and receive A2A messages between Orchestrator and Specialist.

Message types used in GuildOS:
  task/invite    — Orchestrator → Specialist (Step 4)
  task/quote     — Specialist → Orchestrator (Step 4, response)
  task/send      — Orchestrator → Specialist (Step 6, full delegation)
  task/delivered — Specialist → Orchestrator (Step 9)
  task/accepted  — Orchestrator → Specialist (Step 11)

All messages are logged to hackathon/notes/a2a_trace_{date}.json.
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

TRACE_DIR = Path(__file__).parent.parent.parent.parent.parent / "hackathon" / "notes"


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


def _build_send_request(message: a2a_pb2.Message) -> a2a_pb2.SendMessageRequest:
    """Wrap a Message in a SendMessageRequest."""
    return a2a_pb2.SendMessageRequest(message=message)


async def _send_to_agent(agent_url: str, message: a2a_pb2.Message) -> dict:
    """Send a message to an A2A agent and return the response as a dict.

    Uses the a2a-sdk ClientFactory to resolve the agent card and send
    the message via the configured transport.
    """
    factory = ClientFactory()
    client = await factory.create_from_url(agent_url)
    request = _build_send_request(message)
    responses = []
    async for response in client.send_message(request):
        responses.append(response)
    client.close()

    if not responses:
        return {}

    # Extract the last response content
    resp = responses[-1]
    result = {}
    which = resp.WhichOneof("response")
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
        result = {"task_id": task.id, "status": str(task.status)}
    return result


async def send_invite(specialist_endpoint: str, task_spec: dict) -> str:
    """Send task/invite to Specialist. Returns message ID.

    Args:
        specialist_endpoint: URL of the Specialist A2A agent (e.g. http://localhost:10001).
        task_spec: Task specification dict.

    Returns:
        A2A message ID of the invite.
    """
    payload = {"type": "task/invite", "task_spec": task_spec}
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
    )
    _log_message("outgoing", "task/invite", payload)
    response = await _send_to_agent(specialist_endpoint, message)
    _log_message("incoming", "task/quote", response)
    return message.message_id


async def send_task(specialist_endpoint: str, task: dict) -> str:
    """Send task/send (full delegation) to Specialist. Returns message ID.

    Args:
        specialist_endpoint: URL of the Specialist A2A agent.
        task: Full task payload dict.

    Returns:
        A2A message ID.
    """
    payload = {"type": "task/send", "task": task}
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
    )
    _log_message("outgoing", "task/send", payload)
    response = await _send_to_agent(specialist_endpoint, message)
    _log_message("incoming", "task/delivered", response)
    return message.message_id


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
