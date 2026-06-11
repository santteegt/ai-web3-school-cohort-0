"""OrchestratorTools — 7 MCP tool implementations.

Each tool corresponds to one step in the 15-step MVP flow (docs/MVP_FLOW.md).
Tools are called by the human via Claude Code MCP; they call on-chain contracts,
A2A endpoints, or the ERC-8004 registry.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

from src.shared import a2a as a2a_client
from src.shared import agentfightclub as afc
from src.shared import erc8004
from src.shared import guild_context

logger = logging.getLogger(__name__)

ASSETS_DIR = Path(__file__).parent.parent.parent.parent / "assets"

# Hardcoded Specialist profile for MVP talent_query (see CLAUDE.md: "hardcoded Specialist profile is MVP")
_DEFAULT_SPECIALIST_PROFILE = {
    "name": "Specialist Agent",
    "agent_id": "erc8004:1",
    "capabilities": ["code-generation", "audit", "testing"],
    "a2a_endpoint": "http://localhost:10001",
    "delivery_count": 0,
    "rating": None,
}


async def guild_launch(mandate: str, treasury_address: str) -> dict:
    """Step 1: Deploy guild contract and fund treasury via AgentFightClub.

    Returns:
        dict with guild_address and tx hashes for launch + commit.
    """
    result = await afc.launch(mandate=mandate, treasury_address=treasury_address)
    guild_address = result["guild_address"]
    tx_hash = result["tx_hash"]

    # Fund treasury with 0.001 ETH
    commit_tx = await afc.commit(guild_address, amount_wei=1_000_000_000_000_000)

    # Update guild context
    guild_context.save({
        "guild_address": guild_address,
        "mandate": mandate,
        "treasury_wei": "1000000000000000",
        "member_list": [],
        "task_state": "ACTIVE",
    })

    return {
        "guild_address": guild_address,
        "launch_tx": tx_hash,
        "commit_tx": commit_tx,
    }


async def talent_query(task_type: str) -> list[dict]:
    """Step 3: Return ERC-8004 shortlist of candidate agents.

    MVP: returns hardcoded Specialist profile from assets/erc8004_specialist_profile.json.
    Post-hackathon: live registry query + LLM ranking.
    """
    # Try loading cached profile first
    cached_path = ASSETS_DIR / "erc8004_specialist_profile.json"
    if cached_path.exists():
        try:
            data = json.loads(cached_path.read_text())
            if isinstance(data, list):
                return data
            return [data]
        except (json.JSONDecodeError, OSError):
            logger.warning("Failed to load cached ERC-8004 profile, using default")

    # Fallback to hardcoded profile
    return [_DEFAULT_SPECIALIST_PROFILE]


async def task_invite(specialist_endpoint: str, task_spec: dict) -> str:
    """Step 4 (part 1): Send A2A task/invite to Specialist; receive task/quote.

    Returns:
        A2A message ID of the invite.
    """
    message_id = await a2a_client.send_invite(specialist_endpoint, task_spec)
    return message_id


async def task_delegate(specialist_endpoint: str, full_task: dict) -> str:
    """Step 6: Send A2A task/send with full task payload after Gate 0.5 acceptance.

    Returns:
        A2A message ID.
    """
    message_id = await a2a_client.send_task(specialist_endpoint, full_task)

    # Update guild context with A2A task ID
    try:
        guild_context.update(a2a_task_id=message_id)
    except Exception:
        logger.warning("Could not update guild context with a2a_task_id")

    return message_id


async def deliverable_review(deliverable_reference: str, deliverable_hash: str) -> dict:
    """Step 10: Run automated pre-check on Specialist deliverable.

    Returns:
        dict with hash_match, format_valid, size_check, evaluator_verdict.
    """
    path = Path(deliverable_reference)

    # Check file exists and read content
    if not path.exists():
        return {
            "hash_match": False,
            "format_valid": False,
            "size_check": False,
            "evaluator_verdict": "FAIL",
            "error": f"File not found: {deliverable_reference}",
        }

    content = path.read_bytes()
    size = len(content)

    # Compute SHA-256 hash
    actual_hash = "sha256:" + hashlib.sha256(content).hexdigest()
    hash_match = actual_hash == deliverable_hash

    # Format check: valid JSON or non-empty text
    format_valid = False
    try:
        json.loads(content.decode("utf-8"))
        format_valid = True
    except (json.JSONDecodeError, UnicodeDecodeError):
        format_valid = size > 0  # non-empty file is valid enough

    # Size check: file must be non-zero
    size_check = size > 0

    verdict = "PASS" if (hash_match and format_valid and size_check) else "FAIL"

    return {
        "hash_match": hash_match,
        "format_valid": format_valid,
        "size_check": size_check,
        "evaluator_verdict": verdict,
    }


async def settle(guild_address: str, specialist_wallet: str) -> str:
    """Step 12: Call AgentFightClub settle() to release payment.

    Returns:
        Settlement tx hash (Basescan tx #2).
    """
    tx_hash = await afc.settle(guild_address, specialist_wallet)

    # Update guild context
    try:
        guild_context.update(
            task_state="SETTLED",
            settlement_tx=tx_hash,
        )
    except Exception:
        logger.warning("Could not update guild context with settlement")

    return tx_hash


async def reputation_write(delivery_record: dict) -> str:
    """Step 13: Call ERC-8004 giveFeedback() with 6-field delivery record.

    Caller: guild contract address or Marco's EOA — NOT the Specialist wallet (F2).

    Args:
        delivery_record: {task_type, deliverable_hash, acceptance_timestamp,
                          payment_wei, guild_address, a2a_task_id}

    Returns:
        DeliveryRecorded event tx hash.
    """
    # Use guild contract address or orchestrator EOA as caller (F2 constraint)
    import os
    caller_key = os.getenv("ORCHESTRATOR_PRIVATE_KEY", "")

    tx_hash = erc8004.give_feedback(
        caller_private_key=caller_key,
        task_type=delivery_record["task_type"],
        deliverable_hash=delivery_record["deliverable_hash"],
        acceptance_timestamp=delivery_record.get("acceptance_timestamp", 0),
        payment_wei=delivery_record.get("payment_wei", 0),
        guild_address=delivery_record.get("guild_address", ""),
        a2a_task_id=delivery_record.get("a2a_task_id", ""),
    )

    # Update guild context
    try:
        guild_context.update(reputation_tx=tx_hash)
    except Exception:
        logger.warning("Could not update guild context with reputation tx")

    return tx_hash
