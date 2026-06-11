"""OrchestratorServer — MCP server entry point.

Registers 7 tools and starts the MCP listener on stdio.
Run: python -m src.orchestrator.server

Tools:
  1. guild_launch       — Deploy guild contract + fund treasury (stub for Issue #1)
  2. talent_query       — Return ERC-8004 shortlist (hardcoded MVP)
  3. task_invite        — Send A2A task/invite to Specialist
  4. task_delegate      — Send A2A task/send to Specialist
  5. deliverable_review — Run pre-check on deliverable
  6. settle             — Release payment (stub for Issue #1)
  7. reputation_write   — Call ERC-8004 giveFeedback (stub for Issue #1)
"""

from __future__ import annotations

import json

import anyio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.orchestrator import tools as orchestrator_tools

# Tool definitions — input schemas for each of the 7 MCP tools
TOOL_DEFINITIONS: list[types.Tool] = [
    types.Tool(
        name="guild_launch",
        description="Deploy guild contract via AgentFightClub and fund treasury. Returns guild_address + 2 tx hashes.",
        inputSchema={
            "type": "object",
            "properties": {
                "mandate": {
                    "type": "string",
                    "description": "Guild mandate / mission statement",
                },
                "treasury_address": {
                    "type": "string",
                    "description": "Address to receive initial treasury funding",
                },
            },
            "required": ["mandate", "treasury_address"],
        },
    ),
    types.Tool(
        name="talent_query",
        description="Return ERC-8004 shortlist of candidate agents. MVP: returns hardcoded Specialist profile.",
        inputSchema={
            "type": "object",
            "properties": {
                "task_type": {
                    "type": "string",
                    "description": "Type of task to match agents for",
                },
            },
            "required": ["task_type"],
        },
    ),
    types.Tool(
        name="task_invite",
        description="Send A2A task/invite to Specialist; receive task/quote response.",
        inputSchema={
            "type": "object",
            "properties": {
                "specialist_endpoint": {
                    "type": "string",
                    "description": "A2A endpoint URL of the Specialist (e.g. http://localhost:10001)",
                },
                "task_spec": {
                    "type": "object",
                    "description": "Task specification to send",
                },
            },
            "required": ["specialist_endpoint", "task_spec"],
        },
    ),
    types.Tool(
        name="task_delegate",
        description="Send A2A task/send with full task payload to Specialist.",
        inputSchema={
            "type": "object",
            "properties": {
                "specialist_endpoint": {
                    "type": "string",
                    "description": "A2A endpoint URL of the Specialist",
                },
                "full_task": {
                    "type": "object",
                    "description": "Full task payload to delegate",
                },
            },
            "required": ["specialist_endpoint", "full_task"],
        },
    ),
    types.Tool(
        name="deliverable_review",
        description="Run automated pre-check on Specialist deliverable (hash, format, size).",
        inputSchema={
            "type": "object",
            "properties": {
                "deliverable_reference": {
                    "type": "string",
                    "description": "Path to the deliverable file",
                },
                "deliverable_hash": {
                    "type": "string",
                    "description": "Expected SHA-256 hash (sha256:hex format)",
                },
            },
            "required": ["deliverable_reference", "deliverable_hash"],
        },
    ),
    types.Tool(
        name="settle",
        description="Release payment to Specialist via AgentFightClub settle(). Returns settlement tx hash.",
        inputSchema={
            "type": "object",
            "properties": {
                "guild_address": {
                    "type": "string",
                    "description": "Guild contract address",
                },
                "specialist_wallet": {
                    "type": "string",
                    "description": "Specialist wallet address for payment",
                },
            },
            "required": ["guild_address", "specialist_wallet"],
        },
    ),
    types.Tool(
        name="reputation_write",
        description="Call ERC-8004 giveFeedback() with delivery record. Routes via guild contract (not Specialist wallet).",
        inputSchema={
            "type": "object",
            "properties": {
                "delivery_record": {
                    "type": "object",
                    "description": "6-field delivery record",
                },
            },
            "required": ["delivery_record"],
        },
    ),
]


def create_server() -> Server:
    """Create and configure the MCP server with all 7 tools."""
    server = Server("guildos-orchestrator")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        """Return all 7 registered tools."""
        return TOOL_DEFINITIONS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        """Dispatch tool calls to the appropriate handler."""
        try:
            if name == "guild_launch":
                result = await orchestrator_tools.guild_launch(
                    mandate=arguments["mandate"],
                    treasury_address=arguments["treasury_address"],
                )
            elif name == "talent_query":
                result = await orchestrator_tools.talent_query(
                    task_type=arguments["task_type"],
                )
            elif name == "task_invite":
                result = await orchestrator_tools.task_invite(
                    specialist_endpoint=arguments["specialist_endpoint"],
                    task_spec=arguments["task_spec"],
                )
            elif name == "task_delegate":
                result = await orchestrator_tools.task_delegate(
                    specialist_endpoint=arguments["specialist_endpoint"],
                    full_task=arguments["full_task"],
                )
            elif name == "deliverable_review":
                result = await orchestrator_tools.deliverable_review(
                    deliverable_reference=arguments["deliverable_reference"],
                    deliverable_hash=arguments["deliverable_hash"],
                )
            elif name == "settle":
                result = await orchestrator_tools.settle(
                    guild_address=arguments["guild_address"],
                    specialist_wallet=arguments["specialist_wallet"],
                )
            elif name == "reputation_write":
                result = await orchestrator_tools.reputation_write(
                    delivery_record=arguments["delivery_record"],
                )
            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

            # Serialize result
            if isinstance(result, str):
                text = result
            elif isinstance(result, list):
                text = json.dumps(result, indent=2)
            else:
                text = json.dumps(result, indent=2, default=str)

            return [types.TextContent(type="text", text=text)]

        except NotImplementedError as e:
            return [types.TextContent(
                type="text",
                text=f"STUB: {e}. This integration is not yet built — see Issue #1.",
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"ERROR: {type(e).__name__}: {e}",
            )]

    return server


async def run_server() -> None:
    """Start the MCP server on stdio."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

TOOLS = {
    "guild_launch": orchestrator_tools.guild_launch,
    "talent_query": orchestrator_tools.talent_query,
    "task_invite": orchestrator_tools.task_invite,
    "task_delegate": orchestrator_tools.task_delegate,
    "deliverable_review": orchestrator_tools.deliverable_review,
    "settle": orchestrator_tools.settle,
    "reputation_write": orchestrator_tools.reputation_write,
}

__all__ = [
    "create_server",
    "run_server",
    "TOOLS",
]


def main() -> None:
    """Entry point for `python -m src.orchestrator.server`."""
    anyio.run(run_server)


if __name__ == "__main__":
    main()
