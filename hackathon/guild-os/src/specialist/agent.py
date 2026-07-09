"""SpecialistAgent — A2A HTTP server.

Receives task messages from the Orchestrator, executes tasks with GLM-5.1
long-horizon planning, commits deliverable hash to Base mainnet, and sends
task/delivered back via A2A.

Run: python -m src.specialist.agent
A2A endpoint: http://localhost:10001
Agent card: http://localhost:10001/.well-known/agent-card.json
"""

from __future__ import annotations

import hashlib
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

SPECIALIST_PORT = int(os.getenv("SPECIALIST_A2A_PORT", "10001"))
SPECIALIST_BASE_URL = f"http://localhost:{SPECIALIST_PORT}"

# Declared per what add_a2a_routes_to_fastapi() actually mounts below (both
# JSON-RPC and REST, per specs/10-technical-design.md §12) — without this,
# a2a.client.client_factory.ClientFactory.create() raises "no compatible
# transports found" because it has nothing in supported_interfaces to match
# against, regardless of message content.
AGENT_CARD = a2a_pb2.AgentCard(
    name="GuildOS Specialist Agent",
    description="Executes coding and analysis tasks via GLM-5.1 long-horizon planning",
    version="0.1.0",
    supported_interfaces=[
        a2a_pb2.AgentInterface(
            url=f"{SPECIALIST_BASE_URL}{DEFAULT_RPC_URL}",
            protocol_binding=TransportProtocol.JSONRPC,
            protocol_version=PROTOCOL_VERSION_1_0,
        ),
        a2a_pb2.AgentInterface(
            url=SPECIALIST_BASE_URL,
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
            id="code-generation",
            name="Code Generation",
            description="Generates Python code or smart contract specs",
        ),
        a2a_pb2.AgentSkill(
            id="security-analysis",
            name="Security Analysis",
            description="Produces security checklist or audit report",
        ),
    ],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
)


async def handle_task_invite(message: dict) -> dict:
    """Respond to task/invite with a task/quote.

    Returns:
        A2A task/quote message with scope, estimated_cost_wei, deadline_iso.
    """
    from datetime import datetime, timezone

    quote = {
        "type": "task/quote",
        "scope": "Full task execution with GLM-5.1 long-horizon planning",
        "estimated_cost_wei": 1000000000000000,  # 0.001 ETH
        "deadline_iso": (
            datetime.now(timezone.utc).replace(hour=23, minute=59).isoformat()
        ),
    }
    _log_message("outgoing", "task/quote", quote)
    return quote


async def handle_task_send(message: dict) -> dict:
    """Execute the task delegated via task/send.

    Steps:
    1. Parse task payload
    2. Simulate task execution (GLM-5.1 call)
    3. Write deliverable file to disk
    4. Compute SHA-256 of deliverable
    5. Return task/delivered with hash + file path
    """
    from datetime import datetime, timezone
    from pathlib import Path

    task_id = message.get("task_id", str(uuid.uuid4()))

    # Simulate deliverable output
    deliverable_content = json.dumps(
        {
            "task_id": task_id,
            "description": message.get("task", {}).get("task_description", ""),
            "output": "Task executed successfully via GLM-5.1 long-horizon planning",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        indent=2,
    )

    # Write deliverable to disk so Orchestrator pre-check can verify it
    deliverable_dir = Path("output")
    deliverable_dir.mkdir(exist_ok=True)
    deliverable_path = deliverable_dir / f"{task_id}.json"
    deliverable_path.write_text(deliverable_content)
    logger.info("Deliverable written to %s", deliverable_path)

    # Compute SHA-256
    deliverable_hash = "sha256:" + hashlib.sha256(
        deliverable_content.encode()
    ).hexdigest()

    # Commit hash on-chain (Validation plan 5.3 — Basescan tx #1)
    on_chain_tx = None
    try:
        # Get guild address from guild context
        from src.shared import guild_context
        from src.shared.onchain_hash import commit_hash
        ctx = guild_context.load()
        guild_address = ctx.get("guild_address", "")
        if guild_address:
            result = commit_hash(
                deliverable_hash=deliverable_hash,
                guild_address=guild_address,
                task_id=task_id,
            )
            on_chain_tx = result["tx_hash"]
            logger.info(
                "Hash committed on-chain: %s → %s",
                on_chain_tx,
                result["basescan_url"],
            )
        else:
            logger.warning("No guild_address in context — skipping on-chain commit")
    except Exception as e:
        logger.error("On-chain hash commit failed: %s", e)
        on_chain_tx = None

    result = {
        "type": "task/delivered",
        "task_id": task_id,
        "deliverable_reference": str(deliverable_path),
        "deliverable_hash": deliverable_hash,
        "on_chain_tx": on_chain_tx,  # Basescan tx #1
    }
    _log_message("outgoing", "task/delivered", result)
    return result


class SpecialistExecutor(AgentExecutor):
    """AgentExecutor that handles GuildOS task messages."""

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Process incoming A2A messages and respond appropriately."""
        message = context.message
        if not message:
            return

        # Extract text content from parts
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

        if msg_type == "task/invite":
            response = await handle_task_invite(payload)
        elif msg_type == "task/send":
            payload["task_id"] = task_id
            response = await handle_task_send(payload)
        elif msg_type == "task/accepted":
            response = {"type": "task/accepted_ack", "task_id": task_id, "status": "confirmed"}
            _log_message("incoming", "task/accepted", payload)
        else:
            response = {"type": "error", "message": f"Unknown message type: {msg_type}"}

        # Publish response message
        response_msg = a2a_pb2.Message(
            message_id=str(uuid.uuid4()),
            role=a2a_pb2.ROLE_AGENT,
            parts=[a2a_pb2.Part(text=json.dumps(response))],
            task_id=task_id,
            context_id=context.context_id or "",
        )
        event = a2a_pb2.StreamResponse(message=response_msg)
        event_queue.enqueue(event)

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """Handle task cancellation."""
        event = a2a_pb2.StreamResponse(
            task=a2a_pb2.Task(
                id=context.task_id or "",
                status=a2a_pb2.TaskStatus(
                    state=a2a_pb2.TASK_STATE_CANCELED,
                ),
            )
        )
        event_queue.enqueue(event)


def main() -> None:
    """Start the Specialist A2A HTTP server."""
    import uvicorn
    from fastapi import FastAPI

    task_store = InMemoryTaskStore()
    executor = SpecialistExecutor()
    handler = LegacyRequestHandler(
        agent_executor=executor,
        task_store=task_store,
        agent_card=AGENT_CARD,
    )

    app = FastAPI(title="GuildOS Specialist Agent")

    add_a2a_routes_to_fastapi(
        app,
        agent_card_routes=create_agent_card_routes(AGENT_CARD),
        jsonrpc_routes=create_jsonrpc_routes(handler, rpc_url=DEFAULT_RPC_URL),
        rest_routes=create_rest_routes(handler),
    )

    logger.info("SpecialistAgent starting on port %d", SPECIALIST_PORT)
    uvicorn.run(app, host="0.0.0.0", port=SPECIALIST_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
