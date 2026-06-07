# Tools — AI × Web3 School Cohort 0

> Maintained by Sensei. Every time a new tool is adopted during the learning journey, it should be added here immediately.  
> Last updated: 2026-05-20

---

## Coordination Tools

### Zoom
Used for live bootcamp sessions, office hours, mentor check-ins, and the final demo showcase. All scheduled sessions from the program calendar are attended via Zoom.

### Telegram
Primary async channel for the AI × Web3 School community. Used to follow announcements, ask questions between sessions, coordinate with cohort peers, and stay updated on hackathon logistics.

---

## AI Tools

### Claude Code
Terminal-based AI coding agent used for all git operations, repository management, running experiments, executing bash commands, and building code prototypes. Handles anything that requires direct machine access — `gh` CLI, Python scripts, Solidity, etc.

### Cowork (Sensei / Claude)
Learning management layer. Used for daily check-in drafts, scheduling morning/evening/night reminders, updating learning notes, reviewing learning plan progress, and any session that doesn't require terminal access. Sensei's primary home.

### OpenClaw
TBD — role in the course not yet defined. Next steps: clarify intended use case (agent framework, tooling, evaluation?) and add description once confirmed.

### Hermes (Nous Research)
TBD — to be explored during Day 3 (Agent + Frameworks week). Planned use: hands-on practice with a self-improving agent loop to understand persistent memory and skill creation as a contrast to Claude-based agents.

### OpenRouter
Unified LLM API gateway. Used during experiments to test and compare responses across different models (GPT-4o, Gemini, Llama, etc.) without managing multiple API keys. Relevant for evaluation exercises and multi-model agent workflows.

---

## Web3 Tools

TBD — to be decided during Week 1 (Day 5–6) when wallet and smart contract exercises begin. Expected additions: a testnet wallet tool, an RPC provider, and a contract development framework (e.g. Foundry or Hardhat).

---

## Agent & API Tools

### WCB Agent API (`tools/wcb_client.py`)
Custom CLI tool (stdlib only, no dependencies) for programmatic access to the WCB platform. Used by Sensei's scheduled tasks to check daily task status, list pending check-ins, and surface upcoming deadlines. Reads API key from `.claude/settings.local.json` automatically.

### Casual Hackathon API (`tools/casual_hackathon_client.py`)
Custom CLI tool (stdlib only, no dependencies) for managing participation in the AI × Web3 Agentic Builders Hackathon on [Casual Hackathon](https://casualhackathon.com). Supports: registration status check, form schema inspection, registration draft + submit, project creation, and submission management. Reads `CASUAL_HACKATHON_API_KEY` from `.claude/settings.local.json` automatically. Must be run from the local terminal (bash sandbox does not have network access to `casualhackathon.com`).
