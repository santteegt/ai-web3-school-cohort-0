---
trigger: always_on
---

# GuildOS — 7D Framework

Python multi-service AI agent coordination app on Base Sepolia. 7-day hackathon build, scope locked June 13.

## Read Before Coding

- `docs/TECH_STACK.md` — stack, component names
- `docs/MVP_FLOW.md` — 15-step loop (scope boundary)
- `docs/RISKS.md` — fallback decisions are final

## Components (never rename or invent new ones)

- OrchestratorServer → `src/orchestrator/server.py`
- OrchestratorTools → `src/orchestrator/tools.py` (7 MCP tools)
- SpecialistAgent → `src/specialist/agent.py`
- A2AClient → `src/shared/a2a.py`
- ERC8004 → `src/shared/erc8004.py`
- AgentFightClub → `src/shared/agentfightclub.py`
- GuildContext → `src/shared/guild_context.py`
- HumanGates → `src/cli/gates.py`

## Hard Rules

- Base Sepolia only — never mainnet
- No keys in source — env vars only
- Human gates halt execution; wait for `y/N`
- `giveFeedback()`: guild contract or Marco's EOA — NOT Specialist wallet
- Log A2A to `./logs/a2a_trace_{date}.json`
- Log GLM-5.1 to `./logs/glm_trace_{date}.json`
- Run `pytest tests/` and `ruff check src/` before marking done
