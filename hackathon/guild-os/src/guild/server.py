"""GuildToolsServer — shared MCP server entry point (FastMCP).

Exposes identity-registration and identity-read tools over stdio to any
agent joining the guild — not just the Orchestrator. Run:
python -m src.guild.server

Server name: guildtools_mcp (follows the {service}_mcp convention)
Transport:   stdio (JSON-RPC 2.0) — specs/10-technical-design.md §12

Each agent runs its own local instance of this server, configured with its
own AGENT_WALLET_* env (WalletProvider resolves whichever wallet is
configured in the process it's running in) — there is no shared process and
no cross-agent credential handling. Using the Orchestrator's own MCP server
(guildos_mcp) to register the Specialist would make the Orchestrator's
wallet the on-chain owner of the Specialist's agentId, which breaks the
"an agent only ever registers its own identity" guardrail
(specs/scenarios/12_scoped_spending.feature) — this server exists precisely
to avoid that.

Tools (prefixed guildtools_ to avoid collisions with other MCP servers):
  1. guildtools_identity_register       — Register the calling agent's own ERC-8004 profile
  2. guildtools_identity_read_profile   — Read an ERC-8004 profile by agentId

This is the one place AGENT_WALLET_ADDRESS is read from the environment —
src/shared/erc8004.py and src/guild/tools.py take it as an explicit
wallet_address parameter instead of reading env vars themselves, so they
stay plain, testable functions of their inputs.
"""

from __future__ import annotations

import json
import logging
import os
from functools import wraps
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field

from src.guild import tools as guild_tools

logger = logging.getLogger(__name__)

mcp = FastMCP("guildtools_mcp")


def _handle_errors(func):
    """Wrap a tool function with STUB convention + JSON serialization.

    Mirrors src/orchestrator/server.py's _handle_errors — kept local rather
    than imported so this server has no dependency on the Orchestrator's
    module (it must run standalone in any agent's own process).
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            result = await func(*args, **kwargs)
        except NotImplementedError as e:
            return f"STUB: {e}."
        return _to_json(result)

    return wrapper


def _to_json(result: Any) -> str:
    """Serialize a tool result to JSON text."""
    if isinstance(result, str):
        return result
    return json.dumps(result, indent=2, default=str)


# --- Tool 1: identity_register ----------------------------------------------

@mcp.tool(
    name="guildtools_identity_register",
    title="Identity Register",
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=True,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildtools_identity_register(
    name: str = Field(..., description="Agent display name"),
    description: str = Field(..., description="Agent description"),
    services: list[dict] = Field(
        ...,
        description=(
            "List of services[] entries — fully caller-defined, per "
            "https://github.com/erc-8004/best-practices. Capabilities/skills "
            "belong here, not as top-level fields. Common shapes:\n"
            '  A2A: {"name": "A2A", "endpoint": "http://host:port/.well-known/agent-card.json", '
            '"version": "0.3.0", "a2aSkills": ["..."] (optional)}\n'
            '  MCP: {"name": "MCP", "endpoint": "...", "version": "2025-06-18", '
            '"mcpTools": [...], "mcpPrompts": [...], "mcpResources": [...], "capabilities": [...] (all optional)}\n'
            '  OASF (general capabilities/domains): {"name": "OASF", "endpoint": "", '
            '"version": "0.8", "skills": ["code-generation", "audit"], "domains": [...]} (both optional)\n'
            "Any other well-formed service entry (web, ENS, email, ...) is also accepted."
        ),
    ),
    image: str | None = Field(default=None, description="Optional agent image/logo URL"),
    x402_support: bool | None = Field(default=None, description="Optional x402 payment support flag"),
    active: bool = Field(default=True, description="Whether the agent is production-ready"),
    registrations: list[dict] | None = Field(
        default=None,
        description=(
            "Optional list of {agentId, agentRegistry} cross-registry links "
            "for other registries this same agent identity is already known "
            "on. The self-reference for THIS registry is added automatically "
            "after minting — do not include it here."
        ),
    ),
    supported_trust: list[str] | None = Field(
        default=None, description='Optional trust models, e.g. ["reputation", "crypto-economic"]'
    ),
) -> str:
    """Register the calling agent's own profile on ERC-8004.

    Builds a registration file from the caller-supplied services (and any
    optional profile fields), base64-encodes it as a fully on-chain data:
    URI, and registers it through this process's own WalletProvider.
    Idempotent — re-calling for an already-registered wallet returns the
    cached registration instead of minting a second agentId. On a fresh
    mint, immediately follows up with a setAgentURI() call that backfills
    the registrations[] self-reference ({agentId, agentRegistry}) — two
    on-chain transactions, not one.

    Returns:
        JSON with agent_id, agent_uri (final), register_tx_hash,
        update_tx_hash (null if this was an idempotent no-op), and minted.
    """
    wallet_address = os.getenv("AGENT_WALLET_ADDRESS", "")
    return await guild_tools.identity_register(
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


# --- Tool 2: identity_read_profile ------------------------------------------

@mcp.tool(
    name="guildtools_identity_read_profile",
    title="Identity Read Profile",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildtools_identity_read_profile(
    agent_id: int = Field(..., description="ERC-8004 agentId to read"),
) -> str:
    """Read an ERC-8004 profile: name, capabilities, domains, delivery_count,
    a2a_endpoint.

    Returns:
        JSON with name, capabilities, domains, delivery_count, a2a_endpoint,
        agent_uri.
    """
    return await guild_tools.identity_read_profile(agent_id=agent_id)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for ``python -m src.guild.server``."""
    mcp.run()


__all__ = [
    "mcp",
    "main",
    "guildtools_identity_register",
    "guildtools_identity_read_profile",
]


if __name__ == "__main__":
    main()
