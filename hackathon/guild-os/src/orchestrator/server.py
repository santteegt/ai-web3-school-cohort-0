"""OrchestratorServer — MCP server entry point (FastMCP).

Exposes 7 tools over stdio to drive the GuildOS coordination
loop. Run: python -m src.orchestrator.server

Server name: guildos_mcp  (follows the {service}_mcp convention)
Transport:   stdio (JSON-RPC 2.0) — specs/10-technical-design.md §12

Tools (all prefixed guildos_ to avoid collisions with other MCP servers):
  1. guildos_guild_launch        — Deploy guild contract + fund treasury
  2. guildos_talent_query        — Return ERC-8004 shortlist (hardcoded MVP)
  3. guildos_task_invite         — Send A2A task/invite to Specialist
  4. guildos_task_delegate       — Send A2A task/send to Specialist
  5. guildos_deliverable_review  — Run pre-check on deliverable
  6. guildos_settle              — Release payment (stub for Issue #1)
  7. guildos_reputation_write    — Call ERC-8004 giveFeedback (stub)

DRIFT NOTE: AGENTS.md Component Map and specs/10-technical-design.md §6 list
9 tools (adds payment_propose, reputation_propose). tools.py implements 2
extra functions (membership_propose, membership_vote) that are neither in the
spec's 9 nor registered here. This is mid-migration — reconcile before Phase 3
(payment_propose / reputation_propose must exist for the economic loop).
"""

from __future__ import annotations

import json
import logging
from functools import wraps
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

from src.orchestrator import tools as orchestrator_tools

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pydantic input models — validated before the tool body runs
# ---------------------------------------------------------------------------

class TechnicalConstraints(BaseModel):
    """The box the deliverable work must stay in."""

    model_config = ConfigDict(extra="forbid")

    repo_branch: str | None = Field(default=None, description="Working branch")
    library_versions: list[str] = Field(
        default_factory=list,
        description="Pinned versions the deliverable must use",
    )
    env_vars: list[str] = Field(
        default_factory=list,
        description="Required environment variable names",
    )


class AgBOM(BaseModel):
    """Agent Bill of Materials — what the agent may use."""

    model_config = ConfigDict(extra="forbid")

    tools: list[str] = Field(default_factory=list)
    mcp_servers: list[str] = Field(default_factory=list)
    data_sources: list[str] = Field(default_factory=list)


class TaskPayload(BaseModel):
    """Full task/send payload — see specs/20-api-contracts.md §3.

    Pydantic validates required fields and the deliverable_format enum at the
    MCP boundary; tools.py retains defense-in-depth checks (UnderspecifiedTaskError)
    for direct callers that bypass the server.
    """

    model_config = ConfigDict(extra="forbid")

    task_id: str = Field(..., description="Unique task identifier")
    task_description: str = Field(
        ...,
        description="e.g. 'Implement the EAS attestation module (EASClient)'",
    )
    github_issue_url: str = Field(
        ..., description="The ticket the Specialist reads and works from"
    )
    input_data: str | None = Field(
        default=None, description="Ticket body / spec excerpt / repo ref"
    )
    technical_constraints: TechnicalConstraints | None = None
    agbom: AgBOM | None = None
    acceptance_criteria: list[str] = Field(
        ..., min_length=1, description="List of BDD tests that must pass"
    )
    deliverable_format: Literal["zip+hash", "github_commit"] = Field(
        ..., description="Deliverable format"
    )
    deadline: str = Field(..., description="ISO-8601 deadline")
    budget_wei: str = Field(..., description="Numeric string (wei)")


class DeliveryRecord(BaseModel):
    """6-field ERC-8004 delivery record."""

    model_config = ConfigDict(extra="forbid")

    task_type: str = Field(..., description="Type of task completed")
    deliverable_hash: str = Field(
        ..., description="SHA-256 hash in sha256:hex format"
    )
    acceptance_timestamp: int = Field(
        default=0, description="Unix timestamp of acceptance"
    )
    payment_wei: int = Field(default=0, description="Payment amount in wei")
    guild_address: str = Field(default="", description="Guild contract address")
    a2a_task_id: str = Field(default="", description="A2A message ID")


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP("guildos_mcp")


def _handle_errors(func):
    """Wrap a tool function with STUB convention + JSON serialization.

    NotImplementedError (unimplemented integrations) is caught and returned
    as a STUB message so the agent knows to skip the step. All other
    exceptions propagate — FastMCP's Tool.run() catches them and the MCP
    protocol layer marks the CallToolResult ``isError=True``, surfacing
    the message to the agent for corrective action.
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> str:
        try:
            result = await func(*args, **kwargs)
        except NotImplementedError as e:
            return (
                f"STUB: {e}. This integration is not yet built — see Issue #1."
            )
        return _to_json(result)

    return wrapper


def _to_json(result: Any) -> str:
    """Serialize a tool result to JSON text."""
    if isinstance(result, str):
        return result
    return json.dumps(result, indent=2, default=str)


# --- Tool 1: guild_launch ----------------------------------------------------

@mcp.tool(
    name="guildos_guild_launch",
    title="Guild Launch",
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildos_guild_launch(
    mandate: str = Field(..., description="Guild mandate / mission statement"),
    treasury_address: str = Field(
        ..., description="Address to receive initial treasury funding"
    ),
) -> str:
    """Deploy guild contract via AgentFightClub and fund treasury.

    Step 1 of the 15-step MVP flow. Deploys the Moloch v3 guild contract,
    commits 0.001 ETH to the treasury, and records the guild address in
    guild_context.json.

    Args:
        mandate: Guild mandate / mission statement.
        treasury_address: Address to receive initial treasury funding.

    Returns:
        JSON with guild_address, launch_tx, and commit_tx.
    """
    return await orchestrator_tools.guild_launch(
        mandate=mandate, treasury_address=treasury_address
    )


# --- Tool 2: talent_query ----------------------------------------------------

@mcp.tool(
    name="guildos_talent_query",
    title="Talent Query",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
@_handle_errors
async def guildos_talent_query(
    task_type: str = Field(..., description="Type of task to match agents for"),
) -> str:
    """Return ERC-8004 shortlist of candidate agents.

    Step 3 of the MVP flow. MVP returns a hardcoded Specialist profile from
    assets/erc8004_specialist_profile.json (live registry query + LLM ranking
    is post-hackathon).

    Args:
        task_type: Type of task to match agents for.

    Returns:
        JSON list of candidate agent profiles.
    """
    return await orchestrator_tools.talent_query(task_type=task_type)


# --- Tool 3: task_invite -----------------------------------------------------

@mcp.tool(
    name="guildos_task_invite",
    title="Task Invite",
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildos_task_invite(
    specialist_endpoint: str = Field(
        ..., description="A2A endpoint URL (e.g. http://localhost:10001)"
    ),
    task_spec: dict[str, Any] = Field(
        ..., description="Task specification to send"
    ),
) -> str:
    """Send A2A task/invite to Specialist; receive task/quote response.

    Step 4 (part 1) of the MVP flow. Sends an A2A invite message to the
    Specialist agent and returns the A2A message ID.

    Args:
        specialist_endpoint: A2A endpoint URL of the Specialist.
        task_spec: Task specification object to send.

    Returns:
        A2A message ID of the invite.
    """
    return await orchestrator_tools.task_invite(
        specialist_endpoint=specialist_endpoint, task_spec=task_spec
    )


# --- Tool 4: task_delegate ---------------------------------------------------

@mcp.tool(
    name="guildos_task_delegate",
    title="Task Delegate",
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildos_task_delegate(
    specialist_endpoint: str = Field(
        ..., description="A2A endpoint URL (e.g. http://localhost:10001)"
    ),
    full_task: TaskPayload = Field(
        ..., description="Full task/send payload — see specs/20-api-contracts.md §3"
    ),
) -> str:
    """Send A2A task/send with the full GuildOS task payload to the Specialist.

    Step 6 of the MVP flow. Rejects (before sending) a payload missing
    acceptance_criteria, missing github_issue_url, or carrying an unrecognized
    deliverable_format.

    Args:
        specialist_endpoint: A2A endpoint URL of the Specialist.
        full_task: Validated task payload (TaskPayload model).

    Returns:
        A2A message ID.
    """
    return await orchestrator_tools.task_delegate(
        specialist_endpoint=specialist_endpoint,
        full_task=full_task.model_dump(),
    )


# --- Tool 5: deliverable_review ----------------------------------------------

@mcp.tool(
    name="guildos_deliverable_review",
    title="Deliverable Review",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
@_handle_errors
async def guildos_deliverable_review(
    deliverable_reference: str = Field(
        ..., description="Path to the deliverable file"
    ),
    deliverable_hash: str = Field(
        ..., description="Expected SHA-256 hash (sha256:hex format)"
    ),
) -> str:
    """Run automated pre-check on Specialist deliverable (hash, format, size).

    Step 10 of the MVP flow. Reads the deliverable file (paths outside the
    working directory or system temp are rejected), computes its SHA-256 hash,
    and verifies format and non-zero size.

    Args:
        deliverable_reference: Path to the deliverable file.
        deliverable_hash: Expected SHA-256 hash (sha256:hex format).

    Returns:
        JSON with hash_match, format_valid, size_check, evaluator_verdict.
    """
    return await orchestrator_tools.deliverable_review(
        deliverable_reference=deliverable_reference,
        deliverable_hash=deliverable_hash,
    )


# --- Tool 6: settle ----------------------------------------------------------

@mcp.tool(
    name="guildos_settle",
    title="Settle",
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildos_settle(
    guild_address: str = Field(..., description="Guild contract address"),
    specialist_wallet: str = Field(
        ..., description="Specialist wallet address for payment"
    ),
) -> str:
    """Release payment to Specialist via AgentFightClub settle().

    Step 12 of the MVP flow. Processes the passed payment proposal and sends
    the settlement transaction. Returns the settlement tx hash (Basescan tx #2).

    Args:
        guild_address: Guild contract address.
        specialist_wallet: Specialist wallet address for payment.

    Returns:
        Settlement tx hash.
    """
    return await orchestrator_tools.settle(
        guild_address=guild_address, specialist_wallet=specialist_wallet
    )


# --- Tool 7: reputation_write ------------------------------------------------

@mcp.tool(
    name="guildos_reputation_write",
    title="Reputation Write",
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=True,
        idempotentHint=False,
        openWorldHint=True,
    ),
)
@_handle_errors
async def guildos_reputation_write(
    delivery_record: DeliveryRecord = Field(
        ..., description="6-field delivery record"
    ),
) -> str:
    """Call ERC-8004 giveFeedback() with delivery record.

    Step 13 of the MVP flow. The caller is the guild contract (msg.sender)
    via DAO proposal execution — never an agent EOA, never the Specialist
    wallet (F2). No private key is read; the eventual implementation signs
    through WalletProvider. Currently a stub.

    Args:
        delivery_record: 6-field delivery record (DeliveryRecord model).

    Returns:
        DeliveryRecorded event tx hash.
    """
    return await orchestrator_tools.reputation_write(
        delivery_record=delivery_record.model_dump(),
    )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for ``python -m src.orchestrator.server``."""
    mcp.run()


__all__ = [
    "mcp",
    "main",
    "guildos_guild_launch",
    "guildos_talent_query",
    "guildos_task_invite",
    "guildos_task_delegate",
    "guildos_deliverable_review",
    "guildos_settle",
    "guildos_reputation_write",
]


if __name__ == "__main__":
    main()
