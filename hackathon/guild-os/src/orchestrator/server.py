"""OrchestratorServer — MCP server entry point.

Registers 7 tools and starts the MCP listener.
Run: python -m src.orchestrator.server
"""

from src.orchestrator.tools import (
    guild_launch,
    talent_query,
    task_invite,
    task_delegate,
    deliverable_review,
    settle,
    reputation_write,
)

TOOLS = {
    "guild_launch": guild_launch,
    "talent_query": talent_query,
    "task_invite": task_invite,
    "task_delegate": task_delegate,
    "deliverable_review": deliverable_review,
    "settle": settle,
    "reputation_write": reputation_write,
}

__all__ = [
    "guild_launch",
    "talent_query",
    "task_invite",
    "task_delegate",
    "deliverable_review",
    "settle",
    "reputation_write",
    "TOOLS",
]


def main() -> None:
    """Start the Orchestrator MCP server."""
    # Issue #8: wire tools into MCP server framework
    tool_names = ", ".join(TOOLS.keys())
    print(f"OrchestratorServer starting with tools: {tool_names}")
    print("MCP server registration pending — see Issue #8")


if __name__ == "__main__":
    main()
