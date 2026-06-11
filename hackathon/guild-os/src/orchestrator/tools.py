"""OrchestratorTools — 7 MCP tool implementations.

Each tool corresponds to one step in the 15-step MVP flow (docs/MVP_FLOW.md).
Tools are called by the human via Claude Code MCP; they call on-chain contracts,
A2A endpoints, or the ERC-8004 registry.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.shared import a2a as a2a_client
from src.shared import guild_context


async def guild_launch(mandate: str, treasury_address: str) -> dict:
    """Step 1: Deploy guild contract and fund treasury via AgentFightClub.

    Returns:
        dict with guild_address and tx hashes for launch + commit.
    """
    # TODO Issue #1: call AgentFightClub.launch() then commit()
    raise NotImplementedError("guild_launch — implemented in Issue #1")


async def talent_query(task_type: str) -> list[dict]:
    """Step 3: Return ERC-8004 shortlist of candidate agents.

    MVP: returns hardcoded Specialist profile from hackathon/notes/erc8004_specialist_before.json.
    Post-hackathon: live registry query + LLM ranking.
    """
    profile_path = (
        Path(__file__).parent.parent.parent.parent.parent
        / "hackathon"
        / "notes"
        / "erc8004_specialist_before.json"
    )
    if profile_path.exists():
        profile = json.loads(profile_path.read_text())
    else:
        # Hardcoded fallback for MVP
        profile = {
            "name": "GuildOS Specialist Agent",
            "agent_id": 1,
            "capabilities": ["code-generation", "security-analysis"],
            "delivery_count": 0,
            "acceptance_rate": 1.0,
        }
    return [profile]


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
    guild_context.update(a2a_task_id=message_id)
    return message_id


async def deliverable_review(deliverable_reference: str, deliverable_hash: str) -> dict:
    """Step 10: Run automated pre-check on Specialist deliverable.

    Returns:
        dict with hash_match, format_valid, size_check, evaluator_verdict.
    """
    ref_path = Path(deliverable_reference)

    # Check if reference is a readable file
    size_check = ref_path.exists() and ref_path.stat().st_size > 0 if ref_path.exists() else False

    # Format validation — expect JSON or known extension
    format_valid = ref_path.suffix in (".json", ".py", ".md", ".sol", ".txt", "") if ref_path.suffix else True

    # Hash cross-check if file exists
    hash_match = False
    if ref_path.exists():
        content = ref_path.read_bytes()
        computed = "sha256:" + hashlib.sha256(content).hexdigest()
        hash_match = computed == deliverable_hash

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
    # TODO Issue #1: call AgentFightClub.settle()
    raise NotImplementedError("settle — implemented in Issue #1")


async def reputation_write(delivery_record: dict) -> str:
    """Step 13: Call ERC-8004 giveFeedback() with 6-field delivery record.

    Caller: guild contract address or Marco's EOA — NOT the Specialist wallet (F2).

    Args:
        delivery_record: {task_type, deliverable_hash, acceptance_timestamp,
                          payment_wei, guild_address, a2a_task_id}

    Returns:
        DeliveryRecorded event tx hash.
    """
    # TODO Issue #1: call ERC8004.give_feedback() with correct caller
    raise NotImplementedError("reputation_write — implemented in Issue #1")
