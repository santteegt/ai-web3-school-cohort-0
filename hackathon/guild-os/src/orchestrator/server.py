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


def main() -> None:
    # TODO Day 9: wire tools into MCP server (mcp package or a2a-sdk MCP adapter)
    print("OrchestratorServer starting...")
    print("Registered tools: guild_launch, talent_query, task_invite, task_delegate, deliverable_review, settle, reputation_write")
    raise NotImplementedError("Implement MCP server registration in Day 9")


if __name__ == "__main__":
    main()
