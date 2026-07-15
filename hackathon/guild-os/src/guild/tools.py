"""GuildTools — agent-agnostic tool implementations shared by any guild agent.

Unlike OrchestratorTools (which is bound to the Orchestrator's own process
and its own WalletProvider env), these tools carry no assumption about which
agent is calling — a wallet's own AGENT_WALLET_* env determines whose
identity gets registered or read. Each agent runs its own local instance of
GuildToolsServer (src/guild/server.py) with its own env; there is no shared
process and no cross-agent credential handling.
"""

from __future__ import annotations

from src.shared import erc8004


async def identity_register(
    name: str,
    description: str,
    services: list[dict],
    wallet_address: str,
    image: str | None = None,
    x402_support: bool | None = None,
    active: bool = True,
    registrations: list[dict] | None = None,
    supported_trust: list[str] | None = None,
) -> dict:
    """Register the calling agent's own ERC-8004 identity from
    caller-supplied services (and optional profile fields).

    wallet_address identifies the calling agent's own wallet — resolved by
    the MCP server (src/guild/server.py) from its own environment, not read
    here; this module and erc8004.py stay env-agnostic, plain functions of
    their inputs.

    Idempotent — a wallet that already owns an agentId returns the cached
    registration instead of minting a second one. On a fresh mint,
    immediately backfills the registrations[] self-reference via a
    setAgentURI follow-up. Signs with whichever WalletProvider is
    configured in the calling process's own environment.
    """
    return await erc8004.register_agent(
        name=name,
        description=description,
        services=services,
        wallet_address=wallet_address,
        image=image,
        x402_support=x402_support,
        active=active,
        registrations=registrations,
        supported_trust=supported_trust,
    )


async def identity_read_profile(agent_id: int) -> dict:
    """Read an ERC-8004 profile: name, capabilities, domains, delivery_count,
    a2a_endpoint."""
    return erc8004.read_profile(agent_id)
