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
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

TRACE_DIR = Path(__file__).parent.parent.parent.parent.parent / "hackathon" / "notes"


def _log_message(direction: str, msg_type: str, payload: dict) -> None:
    trace_file = TRACE_DIR / f"a2a_trace_{date.today().isoformat()}.json"
    entry = {"direction": direction, "type": msg_type, "payload": payload}
    trace_file.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(trace_file.read_text()) if trace_file.exists() else []
    existing.append(entry)
    trace_file.write_text(json.dumps(existing, indent=2))
    logger.info("A2A %s %s: %s", direction, msg_type, payload.get("task_id", ""))


async def send_invite(specialist_endpoint: str, task_spec: dict) -> str:
    """Send task/invite to Specialist. Returns message ID."""
    # TODO Day 10: use a2a-sdk to send message
    raise NotImplementedError


async def send_task(specialist_endpoint: str, task: dict) -> str:
    """Send task/send (full delegation) to Specialist. Returns message ID."""
    # TODO Day 10: use a2a-sdk to send message
    raise NotImplementedError


async def send_accepted(specialist_endpoint: str, task_id: str) -> None:
    """Send task/accepted to Specialist after human approval at Gate 2."""
    # TODO Day 11: use a2a-sdk to send message
    raise NotImplementedError
