"""SpecialistA2AClient — outbound A2A client for proactive Specialist sends.

The Specialist acts as A2A client (not server) when pushing results back to
the Orchestrator after harness work completes. Two proactive message types:

  task/delivered    — sent after the harness produces the deliverable +
                      EAS attestation; carries the deliverable hash and
                      attestation UID/URL
  feedback/request  — sent after settlement; asks the guild to record
                      reputation for the completed work

Both reuse _build_message, _extract_response, _send_to_agent, and
_log_message from src/shared/a2a.py — imported as-is, never modified.

The orchestrator_endpoint comes from the task/send payload field (see
specs/20-api-contracts.md §3) — never resolved independently, never
hardcoded.
"""

from __future__ import annotations

import json
import logging

from a2a.types import a2a_pb2

from src.shared.a2a import (
    _build_message,
    _log_message,
    _send_to_agent,
)

logger = logging.getLogger(__name__)


async def send_delivered(
    orchestrator_endpoint: str,
    task_id: str,
    deliverable_hash: str,
    attestation_uid: str,
    attestation_url: str,
) -> dict:
    """Send a proactive task/delivered to the Orchestrator's A2A server.

    Called by the harness after work completes and the EAS attestation is
    created. The orchestrator_endpoint comes from the task/send payload.

    Args:
        orchestrator_endpoint: URL of the Orchestrator A2A server (port 10000).
        task_id: The A2A task ID from the original task/send.
        deliverable_hash: SHA-256 hash in sha256:hex format.
        attestation_uid: EAS attestation UID.
        attestation_url: Full easscan URL for the attestation.

    Returns:
        Response dict from the Orchestrator's A2A server.

    Raises:
        Exception: If the send fails (unreachable endpoint, network error).
                   The error is logged before re-raising — never silently
                   dropped.
    """
    payload = {
        "type": "task/delivered",
        "task_id": task_id,
        "deliverable_hash": deliverable_hash,
        "attestation_uid": attestation_uid,
        "attestation_url": attestation_url,
    }
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
        task_id=task_id,
    )
    _log_message("outgoing", "task/delivered", payload)

    try:
        response = await _send_to_agent(orchestrator_endpoint, message)
    except Exception:
        logger.exception(
            "Failed to send proactive task/delivered to %s for task %s",
            orchestrator_endpoint,
            task_id,
        )
        raise

    _log_message("incoming", "task/delivered_ack", response)
    return response


async def send_feedback_request(
    orchestrator_endpoint: str,
    task_id: str,
    deliverable_hash: str,
) -> dict:
    """Send a proactive feedback/request to the Orchestrator's A2A server.

    Called by the harness after settlement is recorded. Triggers the
    reputation proposal flow (Gate 4) on the Orchestrator side.

    Args:
        orchestrator_endpoint: URL of the Orchestrator A2A server (port 10000).
        task_id: The A2A task ID for the completed work.
        deliverable_hash: SHA-256 hash of the deliverable.

    Returns:
        Response dict from the Orchestrator's A2A server.

    Raises:
        Exception: If the send fails. The error is logged before re-raising.
    """
    payload = {
        "type": "feedback/request",
        "task_id": task_id,
        "deliverable_hash": deliverable_hash,
    }
    message = _build_message(
        role=a2a_pb2.ROLE_USER,
        text=json.dumps(payload),
        task_id=task_id,
    )
    _log_message("outgoing", "feedback/request", payload)

    try:
        response = await _send_to_agent(orchestrator_endpoint, message)
    except Exception:
        logger.exception(
            "Failed to send proactive feedback/request to %s for task %s",
            orchestrator_endpoint,
            task_id,
        )
        raise

    _log_message("incoming", "feedback/request_ack", response)
    return response
