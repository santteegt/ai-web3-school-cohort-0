"""ERC8004 — interface for ERC-8004 IdentityRegistry and ReputationRegistry.

Contract addresses are network-specific and loaded from config/networks.json
via src/shared/network_config.py, keyed by the CHAIN_ID env var — never
hardcode an address or a network name here (see AGENTS.md Don't: "Hardcode
chain_id").

CRITICAL: giveFeedback() MUST be called from the guild contract address
(via DAO proposal execution) — NOT from the Specialist Agent's own wallet,
and not from a raw agent EOA. Calling from the agent's wallet will cause a
silent revert. (See docs/RISKS.md §F2)
"""

from __future__ import annotations

import json
from pathlib import Path

from src.shared import network_config

NOTES_DIR = Path(__file__).parent / "logs"


def _identity_contract() -> str:
    return network_config.get_contract_address("erc8004_identity_registry")


def _reputation_contract() -> str:
    return network_config.get_contract_address("erc8004_reputation_registry")


def read_profile(agent_id: int) -> dict:
    """Read ERC-8004 profile via 8004scan API or cached JSON fallback."""
    # TODO Day 9: call 8004scan API; fallback to cached JSON if unavailable
    raise NotImplementedError


def register(agent_uri: str, signer_private_key: str) -> str:
    """Call IdentityRegistry.register(agentURI). Returns tx hash."""
    # TODO Day 9: build + submit transaction via web3.py
    raise NotImplementedError


def give_feedback(
    caller_private_key: str,
    task_type: str,
    deliverable_hash: str,
    acceptance_timestamp: int,
    payment_wei: int,
    guild_address: str,
    a2a_task_id: str,
) -> str:
    """Call ReputationRegistry.giveFeedback() with 6 fields.

    Caller must be the guild contract (via DAO proposal execution) — never an
    agent EOA, never the Specialist wallet. See docs/RISKS.md §F2.
    Returns DeliveryRecorded event tx hash.
    """
    # TODO Day 11: build + submit transaction via web3.py
    raise NotImplementedError


def capture_snapshot(agent_id: int, filename: str) -> dict:
    """Read and save agent profile to ./logs/{filename}.json."""
    profile = read_profile(agent_id)
    path = NOTES_DIR / f"{filename}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2))
    return profile
