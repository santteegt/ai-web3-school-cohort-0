"""OrchestratorTools — 7 MCP tool implementations.

Each tool corresponds to one step in the 15-step MVP flow (docs/MVP_FLOW.md).
Tools are called by the human via Claude Code MCP; they call on-chain contracts,
A2A endpoints, or the ERC-8004 registry.
"""

from __future__ import annotations


async def guild_launch(mandate: str, treasury_address: str) -> dict:
    """Step 1: Deploy guild contract and fund treasury via AgentFightClub.

    Returns:
        dict with guild_address and tx hashes for launch + commit.
    """
    # TODO Day 9: call AgentFightClub.launch() then commit()
    raise NotImplementedError


async def talent_query(task_type: str) -> list[dict]:
    """Step 3: Return ERC-8004 shortlist of candidate agents.

    MVP: returns hardcoded Specialist profile from hackathon/notes/erc8004_specialist_before.json.
    Post-hackathon: live registry query + LLM ranking.
    """
    # TODO Day 9: load cached profile JSON
    raise NotImplementedError


async def task_invite(specialist_endpoint: str, task_spec: dict) -> str:
    """Step 4 (part 1): Send A2A task/invite to Specialist; receive task/quote.

    Returns:
        A2A message ID of the invite.
    """
    # TODO Day 10: call A2AClient.send_invite()
    raise NotImplementedError


async def task_delegate(specialist_endpoint: str, full_task: dict) -> str:
    """Step 6: Send A2A task/send with full task payload after Gate 0.5 acceptance.

    Returns:
        A2A message ID.
    """
    # TODO Day 10: call A2AClient.send_task()
    raise NotImplementedError


async def deliverable_review(deliverable_reference: str, deliverable_hash: str) -> dict:
    """Step 10: Run automated pre-check on Specialist deliverable.

    Returns:
        dict with hash_match, format_valid, size_check, evaluator_verdict.
    """
    # TODO Day 10: implement hash verification + format check
    raise NotImplementedError


async def settle(guild_address: str, specialist_wallet: str) -> str:
    """Step 12: Call AgentFightClub settle() to release payment.

    Returns:
        Settlement tx hash (Basescan tx #2).
    """
    # TODO Day 11: call AgentFightClub.settle()
    raise NotImplementedError


async def reputation_write(delivery_record: dict) -> str:
    """Step 13: Call ERC-8004 giveFeedback() with 6-field delivery record.

    Caller: guild contract address or Marco's EOA — NOT the Specialist wallet (F2).

    Args:
        delivery_record: {task_type, deliverable_hash, acceptance_timestamp,
                          payment_wei, guild_address, a2a_task_id}

    Returns:
        DeliveryRecorded event tx hash.
    """
    # TODO Day 11: call ERC8004.give_feedback() with correct caller
    raise NotImplementedError
