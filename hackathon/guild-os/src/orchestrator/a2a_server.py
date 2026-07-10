"""OrchestratorA2AServer — A2A HTTP server for the Orchestrator.

Receives proactive messages from the Specialist:
  task/delivered    — Specialist → Orchestrator (after harness completes work)
  feedback/request  — Specialist → Orchestrator (after settlement, triggers reputation)

Each inbound message is processed through the A2A task lifecycle (WORKING →
COMPLETED) using an InMemoryTaskStore. Results are pollable via tasks/get on
this endpoint — the server does NOT write to guild_context.json, keeping
inter-agent coordination through A2A only.

Run: python -m src.orchestrator.a2a_server
A2A endpoint: http://localhost:10000
Agent card: http://localhost:10000/.well-known/agent-card.json
"""

from __future__ import annotations

import json
import logging
import os
import uuid

from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.request_handlers.default_request_handler import (
    LegacyRequestHandler,
)
from a2a.server.routes.agent_card_routes import create_agent_card_routes
from a2a.server.routes.fastapi_routes import add_a2a_routes_to_fastapi
from a2a.server.routes.jsonrpc_routes import create_jsonrpc_routes
from a2a.server.routes.rest_routes import create_rest_routes
from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
from a2a.types import a2a_pb2
from a2a.utils.constants import DEFAULT_RPC_URL, PROTOCOL_VERSION_1_0, TransportProtocol

from src.shared.a2a import _log_message

logger = logging.getLogger(__name__)

ORCHESTRATOR_PORT = int(os.getenv("ORCHESTRATOR_A2A_PORT", "10000"))
ORCHESTRATOR_BASE_URL = f"http://localhost:{ORCHESTRATOR_PORT}"

_ALLOWED_INBOUND_TYPES = frozenset({"task/delivered", "feedback/request"})

AGENT_CARD = a2a_pb2.AgentCard(
    name="GuildOS Orchestrator Agent",
    description=(
        "Receives proactive task/delivered and feedback/request messages "
        "from the Specialist Agent"
    ),
    version="0.1.0",
    supported_interfaces=[
        a2a_pb2.AgentInterface(
            url=f"{ORCHESTRATOR_BASE_URL}{DEFAULT_RPC_URL}",
            protocol_binding=TransportProtocol.JSONRPC,
            protocol_version=PROTOCOL_VERSION_1_0,
        ),
        a2a_pb2.AgentInterface(
            url=ORCHESTRATOR_BASE_URL,
            protocol_binding=TransportProtocol.HTTP_JSON,
            protocol_version=PROTOCOL_VERSION_1_0,
        ),
    ],
    capabilities=a2a_pb2.AgentCapabilities(
        streaming=False,
        push_notifications=False,
    ),
    skills=[
        a2a_pb2.AgentSkill(
            id="deliverable-review",
            name="Deliverable Review",
            description="Runs automated pre-check on Specialist deliverable (Gate 2 entry)",
        ),
        a2a_pb2.AgentSkill(
            id="reputation-propose",
            name="Reputation Proposal",
            description="Triggers reputation proposal for completed work (Gate 4 entry)",
        ),
    ],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
)


class OrchestratorExecutor(AgentExecutor):
    """Handle inbound task/delivered and feedback/request from the Specialist."""

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Process an inbound A2A message.

        Validates the message type, emits WORKING, dispatches to the
        appropriate handler, and emits COMPLETED with the result.
        Unknown message types are rejected (fail closed).
        """
        message = context.message
        if not message:
            return

        text_content = ""
        for part in message.parts:
            if part.text:
                text_content += part.text

        if not text_content:
            return

        try:
            payload = json.loads(text_content)
        except (json.JSONDecodeError, ValueError):
            payload = {"type": "unknown", "text": text_content}

        msg_type = payload.get("type", "unknown")
        task_id = context.task_id or str(uuid.uuid4())
        context_id = context.context_id or ""

        await event_queue.enqueue_event(
            a2a_pb2.TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=a2a_pb2.TaskStatus(
                    state=a2a_pb2.TASK_STATE_WORKING,
                ),
            )
        )

        if msg_type not in _ALLOWED_INBOUND_TYPES:
            response = await self._reject_unknown(msg_type, task_id)
        elif msg_type == "task/delivered":
            response = await self._handle_delivered(payload)
        else:
            response = await self._handle_feedback_request(payload)

        response_msg = a2a_pb2.Message(
            message_id=str(uuid.uuid4()),
            role=a2a_pb2.ROLE_AGENT,
            parts=[a2a_pb2.Part(text=json.dumps(response))],
            task_id=task_id,
            context_id=context_id,
        )
        await event_queue.enqueue_event(
            a2a_pb2.TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=a2a_pb2.TaskStatus(
                    state=a2a_pb2.TASK_STATE_COMPLETED,
                    message=response_msg,
                ),
            )
        )

    async def _handle_delivered(self, payload: dict) -> dict:
        """Run the deliverable pre-check (Gate 2 entry point).

        Calls the existing deliverable_review tool — does not redefine it.
        The result is returned in the COMPLETED task status.message, making
        it pollable via tasks/get on this endpoint.
        """
        _log_message("incoming", "task/delivered", payload)

        deliverable_reference = payload.get("deliverable_reference", "")
        deliverable_hash = payload.get("deliverable_hash", "")

        if not deliverable_hash:
            logger.warning("task/delivered missing deliverable_hash")
            return {
                "type": "deliverable_review",
                "status": "rejected",
                "reason": "missing deliverable_hash",
            }

        from src.orchestrator import tools

        pre_check = await tools.deliverable_review(
            deliverable_reference=deliverable_reference,
            deliverable_hash=deliverable_hash,
        )
        logger.info(
            "Deliverable pre-check result: %s",
            pre_check.get("evaluator_verdict"),
        )
        return {
            "type": "deliverable_review",
            "task_id": payload.get("task_id", ""),
            "pre_check": pre_check,
        }

    async def _handle_feedback_request(self, payload: dict) -> dict:
        """Stub reputation_propose trigger (Gate 4 entry point).

        reputation_propose is Phase 3 — this handler logs the receipt and
        returns a stub acknowledgment. The full implementation will call
        tools.reputation_propose() when it exists.
        """
        _log_message("incoming", "feedback/request", payload)

        logger.info(
            "feedback/request received for task %s — reputation_propose stubbed (Phase 3)",
            payload.get("task_id", ""),
        )
        return {
            "type": "reputation_propose",
            "task_id": payload.get("task_id", ""),
            "status": "stubbed",
            "reason": "reputation_propose is Phase 3 — logged for future implementation",
        }

    async def _reject_unknown(self, msg_type: str, task_id: str) -> dict:
        """Reject an unrecognized message type (fail closed)."""
        _log_message(
            "incoming",
            f"rejected:{msg_type}",
            {"task_id": task_id},
        )
        logger.warning("Rejected unknown inbound message type: %s", msg_type)
        return {
            "type": "error",
            "message": (
                f"Unrecognized message type: {msg_type}. "
                f"Expected one of {sorted(_ALLOWED_INBOUND_TYPES)}."
            ),
        }

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Handle task cancellation."""
        await event_queue.enqueue_event(
            a2a_pb2.TaskStatusUpdateEvent(
                task_id=context.task_id or "",
                context_id=context.context_id or "",
                status=a2a_pb2.TaskStatus(
                    state=a2a_pb2.TASK_STATE_CANCELED,
                ),
            )
        )


def create_orchestrator_app():
    """Build the Orchestrator FastAPI app without starting uvicorn.

    Returns (app, task_store) for testing.
    """
    from fastapi import FastAPI

    task_store = InMemoryTaskStore()
    executor = OrchestratorExecutor()
    handler = LegacyRequestHandler(
        agent_executor=executor,
        task_store=task_store,
        agent_card=AGENT_CARD,
    )

    app = FastAPI(title="GuildOS Orchestrator Agent")

    add_a2a_routes_to_fastapi(
        app,
        agent_card_routes=create_agent_card_routes(AGENT_CARD),
        jsonrpc_routes=create_jsonrpc_routes(handler, rpc_url=DEFAULT_RPC_URL),
        rest_routes=create_rest_routes(handler),
    )

    return app, task_store


def main() -> None:
    """Start the Orchestrator A2A HTTP server."""
    import uvicorn

    app, _ = create_orchestrator_app()
    logger.info(
        "OrchestratorA2AServer starting on port %d", ORCHESTRATOR_PORT
    )
    uvicorn.run(app, host="0.0.0.0", port=ORCHESTRATOR_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
