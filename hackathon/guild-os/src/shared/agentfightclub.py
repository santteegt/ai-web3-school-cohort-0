"""AgentFightClub — interface for Moloch v3 guild treasury and governance.

Primary: AgentFightClub ClawBank Skill API
Fallback: DAOhaus SDK direct Moloch v3 deploy (see docs/RISKS.md §F1)

Decision is recorded in docs/TECH_STACK.md Decision Log on Day 8.
"""

from __future__ import annotations
import os

API_KEY = os.getenv("AGENTFIGHTCLUB_API_KEY", "")
USE_DAOHUAS_FALLBACK = not API_KEY


async def launch(mandate: str, treasury_address: str) -> dict:
    """Deploy guild contract with mandate string.

    Returns:
        dict with guild_address and tx_hash.
    """
    # TODO Day 9: ClawBank API call or DAOhaus SDK deploy based on Day 8 decision
    raise NotImplementedError


async def commit(guild_address: str, amount_wei: int) -> str:
    """Fund treasury. Returns tx hash."""
    # TODO Day 9
    raise NotImplementedError


async def propose(guild_address: str, specialist_erc8004_id: int) -> str:
    """Submit Specialist membership proposal. Returns proposal ID."""
    # TODO Day 9
    raise NotImplementedError


async def vote(guild_address: str, proposal_id: str, approve: bool) -> str:
    """Cast membership vote. Returns tx hash."""
    # TODO Day 9
    raise NotImplementedError


async def settle(guild_address: str, specialist_wallet: str) -> str:
    """Release treasury payment to Specialist wallet.

    This is Basescan tx #2 — the settlement transaction.
    Returns tx hash; save to ../../submissions/tx_hashes.md.
    """
    # TODO Day 11
    raise NotImplementedError
