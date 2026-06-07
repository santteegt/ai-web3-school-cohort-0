"""ERC8004 — interface for ERC-8004 IdentityRegistry and ReputationRegistry.

Contracts on Base Sepolia (chain_id 84532):
  IdentityRegistry:   0x8004A818BFB912233c491871b3d84c89A494BD9e
  ReputationRegistry: 0x8004B663056A597Dffe9eCcC1965A193B7388713

CRITICAL: giveFeedback() MUST be called from the guild contract address
or Marco's EOA — NOT from the Specialist Agent's own wallet. Calling
from the agent's wallet will cause a silent revert. (See docs/RISKS.md §F2)
"""

from __future__ import annotations
import json
import os
from pathlib import Path

IDENTITY_CONTRACT = os.getenv("ERC8004_CONTRACT", "0x8004A818BFB912233c491871b3d84c89A494BD9e")
REPUTATION_CONTRACT = os.getenv("REPUTATION_CONTRACT", "0x8004B663056A597Dffe9eCcC1965A193B7388713")

NOTES_DIR = Path(__file__).parent.parent.parent.parent.parent / "hackathon" / "notes"


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

    Caller must be guild contract or Marco's EOA — NOT the Specialist wallet.
    Returns DeliveryRecorded event tx hash.
    """
    # TODO Day 11: build + submit transaction via web3.py
    raise NotImplementedError


def capture_snapshot(agent_id: int, filename: str) -> dict:
    """Read and save agent profile to hackathon/notes/{filename}.json."""
    profile = read_profile(agent_id)
    path = NOTES_DIR / f"{filename}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2))
    return profile
