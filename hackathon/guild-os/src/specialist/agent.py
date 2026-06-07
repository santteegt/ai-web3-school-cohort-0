"""SpecialistAgent — A2A HTTP server.

Receives task messages from the Orchestrator, executes tasks with GLM-5.1
long-horizon planning, commits deliverable hash to Base Sepolia, and sends
task/delivered back via A2A.

Run: python -m src.specialist.agent
A2A endpoint: http://localhost:10001
Agent card: http://localhost:10001/.well-known/agent.json
"""

from __future__ import annotations
import os


SPECIALIST_PORT = int(os.getenv("SPECIALIST_A2A_PORT", "10001"))

AGENT_CARD = {
    "name": "GuildOS Specialist Agent",
    "description": "Executes coding and analysis tasks via GLM-5.1 long-horizon planning",
    "url": f"http://localhost:{SPECIALIST_PORT}",
    "version": "0.1.0",
    "capabilities": {
        "tasks": True,
        "streaming": False,
        "pushNotifications": False,
    },
    "skills": [
        {
            "id": "code-generation",
            "name": "Code Generation",
            "description": "Generates Python code or smart contract specs",
        },
        {
            "id": "security-analysis",
            "name": "Security Analysis",
            "description": "Produces security checklist or audit report",
        },
    ],
}


async def handle_task_invite(message: dict) -> dict:
    """Respond to task/invite with a task/quote.

    Returns:
        A2A task/quote message with scope, estimated_cost_wei, deadline_iso.
    """
    # TODO Day 10: parse invite; call GLM-5.1 for cost/time estimate
    raise NotImplementedError


async def handle_task_send(message: dict) -> None:
    """Execute the task delegated via task/send.

    Steps:
    1. Decompose task into ≥ 3-step plan using GLM-5.1
    2. Execute plan (tool use loop)
    3. Compute SHA-256 of output
    4. Commit hash to guild contract on Base Sepolia
    5. Send task/delivered to Orchestrator
    """
    # TODO Day 10: implement full execution loop
    raise NotImplementedError


def main() -> None:
    # TODO Day 9: start A2A HTTP server, register agent card, listen on SPECIALIST_PORT
    print(f"SpecialistAgent starting on port {SPECIALIST_PORT}...")
    raise NotImplementedError("Implement A2A server in Day 9")


if __name__ == "__main__":
    main()
