# CLAUDE.md — GuildOS

You are building **GuildOS**, a Python multi-service application that coordinates AI agents through the A2A protocol, on-chain treasury (AgentFightClub / Moloch v3), and verifiable reputation (ERC-8004) on **Base mainnet (chain_id 8453)**. This is a **7-day hackathon build** ending June 13. Scope is locked — every file in `docs/` defines the boundaries.

## Files — Read Before Coding

| File | Read When |
|------|-----------|
| `docs/PROBLEM.md` | Before any new feature — understand what we're solving |
| `docs/TECH_STACK.md` | Before adding imports or calling external services |
| `docs/MVP_FLOW.md` | Before any change to agent coordination logic |
| `docs/RISKS.md` | Before touching AgentFightClub, ERC-8004, or ZeroDev — fallbacks are already decided |
| `docs/VALIDATION_PLAN.md` | Definition of done per integration |
| `guild_context.json` | Current guild state (mock store — one JSON file per session) |

## Component Map — Use These Names, Never Invent New Ones

| Component | Location | What It Does |
|-----------|----------|--------------|
| `OrchestratorServer` | `src/orchestrator/server.py` | MCP server entry point; registers all tools |
| `OrchestratorTools` | `src/orchestrator/tools.py` | 7 tools: `guild_launch`, `talent_query`, `task_invite`, `task_delegate`, `deliverable_review`, `settle`, `reputation_write` |
| `SpecialistAgent` | `src/specialist/agent.py` | Python A2A server; runs GLM-5.1 long-horizon tasks; responds to task messages |
| `A2AClient` | `src/shared/a2a.py` | Sends/receives A2A messages (invite, quote, send, delivered, accepted) |
| `ERC8004` | `src/shared/erc8004.py` | `register()` and `giveFeedback()` — caller constraint: NOT the agent's own wallet |
| `AgentFightClub` | `src/shared/agentfightclub.py` | `launch`, `commit`, `propose`, `vote`, `settle` — ClawBank API or DAOhaus SDK fallback |
| `GuildContext` | `src/shared/guild_context.py` | Read/write `guild_context.json`; the mock guild state store |
| `HumanGates` | `src/cli/gates.py` | Gate 0, 0.5, 1, 2 — CLI `y/N` prompts; always halt execution and wait |

## Before Building

1. Read `docs/TECH_STACK.md` — versions and library choices are locked
2. Read `docs/RISKS.md` Decision Log — fallbacks are already decided; don't re-evaluate
3. Check the Component Map above — use existing module names and class names exactly
4. Confirm which sprint Day (8–13) the task belongs to; match that Day's P0 gate

## While Building

- All A2A messages must be logged to `hackathon/notes/a2a_trace_{date}.json`
- All GLM-5.1 calls must log plan + tool calls + output to `hackathon/notes/glm_trace_{date}.json`
- Every human gate (0, 0.5, 1, 2) must halt execution and wait for explicit `y` — never skip or auto-proceed
- All on-chain calls must log the tx hash and print the Base mainnet Basescan URL (https://basescan.org/tx/...)
- Guild state transitions must update `guild_context.json` immediately after the on-chain event

## After Building

- Run `pytest tests/` — all tests must pass
- Run `ruff check src/` — no lint errors
- Log any new on-chain tx hashes to `../../submissions/tx_hashes.md`
- Add new error patterns to `docs/VALIDATION_PLAN.md` under the relevant section

## When Unsure

- **Which library for Base mainnet calls?** → `web3.py` with Alchemy RPC; see `docs/TECH_STACK.md`
- **AgentFightClub API or DAOhaus SDK?** → Check `docs/RISKS.md` § Decision Log; ClawBank API confirmed working Day 9
- **Which wallet calls `giveFeedback()`?** → Guild contract address or Marco's EOA — NOT the Specialist wallet (see `docs/RISKS.md §F2`)
- **New A2A message type needed?** → Check `src/shared/a2a.py` for the established pattern; don't invent new types without updating `docs/MVP_FLOW.md`
- **Is this feature in scope?** → Check `docs/MVP_FLOW.md`; if not in the 15 steps, it's out of scope

## Don't

- Run any transaction on Ethereum mainnet — Base mainnet (chain_id 8453) only; never Base Sepolia
- Hardcode private keys, API keys, or seed phrases in source files
- Skip human gate prompts — every gate must halt and wait; use `src/cli/gates.py`
- Add Python packages without updating `requirements.txt`
- Call `giveFeedback()` from the Specialist Agent's wallet — it will revert (F2)
- Build UI components — two terminal windows are the demo surface
- Query the live ERC-8004 registry for talent matching — hardcoded Specialist profile is MVP
- Implement ragequit on-chain — document the path only
- Add features not in the 15-step MVP flow

## Sprint — Day Gates

| Day | Date | Theme | P0 Gate |
|-----|------|-------|---------|
| 8 | Jun 8 | Validation | `launch` live · A2A test green · GLM-5.1 task locked |
| 9 | Jun 9 | Wallets + Identity | Both wallets on-chain · ERC-8004 agentIds · Guild funded |
| 10 | Jun 10 | A2A + Execution | Hash on Base mainnet · Basescan tx #1 saved |
| 11 | Jun 11 | Settlement + Reputation + E2E | `settle()` tx · ERC-8004 delta · Smoke test passes |
| 12 | Jun 12 | Demo Prep | README, demo script, all artifacts — repo clean |
| 13 | Jun 13 | Submission | Submitted before 12:00 UTC+8 (04:00 UTC) |

## Customizing This File

Add new components to the Component Map when they are created. Update Don't rules when a fallback is triggered. Add Day-specific guidance before each morning session starts.
