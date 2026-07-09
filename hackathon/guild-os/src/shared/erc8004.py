"""ERC8004 — interface for ERC-8004 IdentityRegistry and ReputationRegistry.

Contract addresses are network-specific and loaded from config/networks.json
via src/shared/network_config.py, keyed by the CHAIN_ID env var — never
hardcode an address or a network name here.

register() signs through WalletProvider (CAW TSS) — no raw EOA key is ever
read. The Pact allowlist covers the IdentityRegistry's register() selector
exactly (see config/pact.json).

CRITICAL: giveFeedback() MUST be called from the guild contract address
(via DAO proposal execution) — NOT from the Specialist Agent's own wallet,
and not from a raw agent EOA. Calling from the agent's wallet will cause a
silent revert (specs/10-technical-design.md §8 F2).
"""

from __future__ import annotations

import json
from pathlib import Path

from src.shared import network_config
from src.shared.wallet import UnsignedTx, get_wallet_provider

NOTES_DIR = Path(__file__).parent / "logs"


def _identity_contract() -> str:
    return network_config.get_contract_address("erc8004_identity_registry")


def _reputation_contract() -> str:
    return network_config.get_contract_address("erc8004_reputation_registry")


def read_profile(agent_id: int) -> dict:
    """Read ERC-8004 profile via 8004scan API or cached JSON fallback."""
    raise NotImplementedError


async def register(agent_uri: str) -> str:
    """Call IdentityRegistry.register(agentURI) through WalletProvider.

    Builds the register calldata (selector + ABI-encoded agentURI), then
    signs through the scoped WalletProvider. The Pact authorizes this
    call because register() is on the ERC-8004 allowlist.

    The full broadcast + confirmation path lands in issue #5; this scaffold
    wires the WalletProvider seam so register() never touches a raw key.

    Returns:
        Transaction hash once confirmed on-chain.
    """
    wallet = get_wallet_provider()
    identity_addr = _identity_contract()

    from eth_abi import encode

    register_selector = "0xf2c298be"
    calldata = register_selector + encode(
        ["string"], [agent_uri]
    ).hex()

    tx: UnsignedTx = {
        "to": identity_addr,
        "data": calldata,
        "value": "0",
        "chainId": int(network_config.get_chain_id()),
    }

    result = await wallet.sign(tx)
    return result.tx_hash or ""


def give_feedback(
    task_type: str,
    deliverable_hash: str,
    acceptance_timestamp: int,
    payment_wei: int,
    guild_address: str,
    a2a_task_id: str,
) -> str:
    """Call ReputationRegistry.giveFeedback() with 6 fields.

    Caller must be the guild contract (via DAO proposal execution) — never
    an agent EOA, never the Specialist wallet (specs/10-technical-design.md
    §8 F2). Returns DeliveryRecorded event tx hash.

    The full flow is: reputation_propose submits an executable Moloch
    proposal encoding giveFeedback(); Gate 4 halts for human vote; on
    passing vote AgentFightClub.process(proposal_id) executes it with
    msg.sender = guild contract. This function is the stub seam for the
    final on-chain call — no raw private key is ever accepted.
    """
    raise NotImplementedError


def capture_snapshot(agent_id: int, filename: str) -> dict:
    """Read and save agent profile to ./logs/{filename}.json."""
    profile = read_profile(agent_id)
    path = NOTES_DIR / f"{filename}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2))
    return profile
