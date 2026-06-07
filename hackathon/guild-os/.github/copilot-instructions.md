# GuildOS — Copilot Instructions (7D Framework Level 4)

You are working on GuildOS, a Python multi-service AI agent coordination application on Base Sepolia testnet. This is a 7-day hackathon build ending June 13.

## Read These Files First

- `docs/PROBLEM.md` — what we're solving
- `docs/TECH_STACK.md` — stack, components, naming conventions
- `docs/MVP_FLOW.md` — the 15-step coordination loop; scope boundary
- `docs/RISKS.md` — fallback decisions already made; read before any integration work

## Component Registry

| Component | File | Do Not Rename |
|-----------|------|---------------|
| OrchestratorServer | `src/orchestrator/server.py` | |
| OrchestratorTools | `src/orchestrator/tools.py` | 7 MCP tools: guild_launch, talent_query, task_invite, task_delegate, deliverable_review, settle, reputation_write |
| SpecialistAgent | `src/specialist/agent.py` | A2A HTTP server on port 10001 |
| A2AClient | `src/shared/a2a.py` | |
| ERC8004 | `src/shared/erc8004.py` | |
| AgentFightClub | `src/shared/agentfightclub.py` | |
| GuildContext | `src/shared/guild_context.py` | |
| HumanGates | `src/cli/gates.py` | |

## Hard Rules

- Base Sepolia testnet only — never mainnet
- No private keys or API keys in source files — use env vars
- Every human gate (0, 0.5, 1, 2) must halt and wait for `y/N` — never auto-proceed
- `giveFeedback()` caller: guild contract or Marco's EOA — NOT the Specialist wallet
- All A2A messages logged to `hackathon/notes/a2a_trace_{date}.json`
- All GLM-5.1 calls logged to `hackathon/notes/glm_trace_{date}.json`

## Sprint

Day 8 (Validation) · Day 9 (Wallets + Identity) · Day 10 (A2A + Execution) · Day 11 (Settlement + Reputation + E2E) · Day 12 (Demo Prep) · Day 13 (Submission by 12:00 UTC+8)
