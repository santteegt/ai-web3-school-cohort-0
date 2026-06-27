# Tech Stack — GuildOS

> Stack is locked as of 2026-06-08. Changes require updating this file first and noting the reason in the Decision Log below.

---

## Stack

| Layer | Choice | Version | Notes |
|-------|--------|---------|-------|
| Language | Python | 3.11+ | Primary — agent services, CLI, A2A handlers |
| Agent protocol | A2A SDK | v1.0.0 | `pip install "a2a-sdk[http-server]"` — cross-harness task delegation |
| LLM execution | Z.AI GLM-5.1 | API | Specialist Agent long-horizon planning; task type locked Day 9 |
| Orchestrator harness | Claude Code (MCP server) | — | 8 tools registered; entry point `src/orchestrator/server.py` |
| Agent wallet | Cobo CAW | TSS local node | x402 pipeline working end-to-end; Pact-scoped spending ceiling per task |
| Treasury + governance | AgentFightClub (Moloch v3) | — | ClawBank API (primary — live, timing issue being fixed); DAOhaus SDK (fallback — see RISKS.md F1) |
| Agent identity | ERC-8004 Registry | Base mainnet | IdentityRegistry: `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| Reputation | ERC-8004 ReputationRegistry | Base mainnet | `0x8004B663056A597Dffe9eCcC1965A193B7388713`; caller constraint applies |
| Deliverable attestation | EAS (Ethereum Attestation Service) | v1.0.1 (Base mainnet) | EAS contract: `0x4200000000000000000000000000000000000021`; SchemaRegistry: `0x4200000000000000000000000000000000000020`; called via `web3.py` ABI (no Python SDK); UID links A2A message ↔ ERC-8004 record |
| Chain interaction | `web3.py` | 6.x | All Base mainnet RPC calls; transaction submission and event reads |
| RPC | Alchemy | Base mainnet | Primary; Infura as backup endpoint |
| Network | **Base** (canonical) · Base Sepolia (isolated testing) | 8453 · 84532 | All on-chain evidence must be on Base; Base Sepolia permitted for isolated component tests that support it; controlled by `CHAIN_ID` env var |
| Linting | ruff | latest | `ruff check src/` |
| Testing | pytest | 8.x | `pytest tests/` |
| Identity API | 8004scan API | — | ERC-8004 profile reads; cached JSON fallback if API down |

---

## Project Structure

```
guild-os/
├── src/
│   ├── orchestrator/
│   │   ├── server.py          # MCP server — registers tools, starts listener
│   │   └── tools.py           # 7 MCP tool implementations
│   ├── specialist/
│   │   └── agent.py           # A2A HTTP server — receives tasks, runs GLM-5.1
│   ├── shared/
│   │   ├── a2a.py             # A2A client: send/receive invite, quote, send, delivered, accepted
│   │   ├── eas.py             # EASClient: attest(), get_attestation() — deliverable hash commitment
│   │   ├── erc8004.py         # ERC-8004 interface: register(), giveFeedback(), read profile
│   │   ├── agentfightclub.py  # AgentFightClub interface: launch, commit, propose, vote, settle
│   │   └── guild_context.py   # guild_context.json read/write helper
│   └── cli/
│       └── gates.py           # Human gate CLI prompts (Gate 0, 0.5, 1, 2)
├── tests/                     # pytest test files
├── docs/                      # Architecture docs (this file + others)
├── scripts/
│   └── setup-github.sh        # Create GitHub labels + milestones
├── guild_context.json          # Mock guild state store (one per guild session)
├── requirements.txt
├── .env.example
└── CLAUDE.md
```

---

## Components

### Orchestrator Agent — `src/orchestrator/`

**Harness:** Claude Code (MCP server)  
**Entry point:** `python -m src.orchestrator.server` → listens on localhost:3000  
**Tools exposed as MCP:**

| Tool | Input | Output | On-chain? |
|------|-------|--------|-----------|
| `guild_launch` | mandate string, treasury address | guild contract address + tx hash | Yes |
| `talent_query` | task type | ERC-8004 shortlist JSON | No (mocked) |
| `task_invite` | specialist a2a endpoint, task spec | A2A `task/invite` message ID | No |
| `task_delegate` | specialist endpoint, full task | A2A `task/send` message ID | No |
| `deliverable_review` | deliverable reference, hash | pre-check report: `{hash_match, format_valid, size_check}` | No |
| `settle` | guild address, specialist wallet | settlement tx hash | Yes |
| `reputation_write` | 6-field delivery record | `DeliveryRecorded` event tx hash | Yes |

### Specialist Agent — `src/specialist/`

**Harness:** Python service (Hermes-compatible)  
**Entry point:** `python -m src.specialist.agent` → A2A HTTP server on localhost:10001  
**A2A endpoint:** `http://localhost:10001`  
**Agent card:** `http://localhost:10001/.well-known/agent.json`

Receives: `task/invite` → responds with `task/quote`  
Receives: `task/send` → executes GLM-5.1 plan → commits hash → sends `task/delivered`

### Shared Modules — `src/shared/`

**A2A message types used:**
- `task/invite` — Orchestrator → Specialist
- `task/quote` — Specialist → Orchestrator (fields: `scope`, `estimated_cost_wei`, `deadline_iso`)
- `task/send` — Orchestrator → Specialist (full task payload)
- `task/delivered` — Specialist → Orchestrator (fields: `deliverable_reference`, `deliverable_hash`, `attestation_uid`, `attestation_url`)
- `task/accepted` — Orchestrator → Specialist (closes loop)

**ERC-8004 caller constraint + mechanism:** `giveFeedback()` must NOT be called from the Specialist Agent's own wallet — it will revert (Sybil protection). The correct mechanism is an **executable `submitFeedback` Moloch proposal**: Orchestrator submits `AgentFightClub.propose()` encoding the `giveFeedback()` call; after Gate 3 vote passes, `AgentFightClub.process()` executes the proposal with **`msg.sender = guild contract address`** — never the Orchestrator's or Specialist's EOA. See `docs/RISKS.md §F2`.

### Guild Context Store — `guild_context.json`

```json
{
  "guild_address": "0x...",
  "mandate": "Build GuildOS — coordinate a Specialist to implement its own tickets",
  "treasury_wei": "1000000000000000",
  "member_list": ["0x_orchestrator", "0x_specialist"],
  "task_state": "ACTIVE",
  "deliverable_hash": null,
  "attestation_uid": null,
  "attestation_url": null,
  "a2a_task_id": null,
  "proposal_id": null,
  "reputation_proposal_id": null,
  "reputation_tx": null
}
```

States: `ACTIVE` → `SETTLED` | `DISPUTED`

---

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `CHAIN_ID` | Active network chain ID | `8453` (Base); `84532` for isolated testing |
| `ALCHEMY_API_KEY` | RPC endpoint (Base or Base Sepolia per `CHAIN_ID`) | — |
| `GLM_API_KEY` | Z.AI GLM-5.1 API | — |
| `ORCHESTRATOR_PRIVATE_KEY` | Orchestrator signing key (EOA) | — |
| `SPECIALIST_PRIVATE_KEY` | Specialist signing key (EOA) | — |
| `AGENTFIGHTCLUB_API_KEY` | ClawBank Skill API | Optional |
| `ERC8004_CONTRACT` | IdentityRegistry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| `REPUTATION_CONTRACT` | ReputationRegistry | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| `EAS_CONTRACT` | EAS contract (Base mainnet) | `0x4200000000000000000000000000000000000021` |
| `EAS_SCHEMA_REGISTRY` | EAS SchemaRegistry (Base mainnet) | `0x4200000000000000000000000000000000000020` |
| `DELIVERY_SCHEMA_UID` | Registered GuildOS delivery schema UID | Register once; hardcode in `.env` |
| `ORCHESTRATOR_A2A_PORT` | Orchestrator A2A endpoint port | `10000` |
| `SPECIALIST_A2A_PORT` | Specialist A2A endpoint port | `10001` |

---

## Naming Conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Classes | PascalCase | `OrchestratorServer`, `ERC8004`, `GuildContext` |
| Functions | snake_case | `guild_launch()`, `send_task_invite()` |
| Constants | SCREAMING_SNAKE | `ERC8004_CONTRACT`, `GUILD_CONTEXT_PATH` |
| A2A message types | `noun/verb` | `task/invite`, `task/delivered` |
| Files | snake_case | `agentfightclub.py`, `guild_context.json` |
| Git branches | `feat/`, `fix/`, `chore/` | `feat/a2a-task-flow` |

---

## Decision Log

| Date | Decision | Choice | Reason |
|------|----------|--------|--------|
| 2026-06-06 | Agent wallet provider | ZeroDev Kernel v3.3 (replacing Cobo CAW) | CAW GitHub repo empty, x402 integration broken, signing API broken |
| 2026-06-06 | Testnet | Base Sepolia (chain_id 84532) | ZeroDev confirmed; ERC-8004 deployed; AgentFightClub targets Base |
| 2026-06-07 | Orchestrator harness | Claude Code (MCP server) | Hybrid approach — demo two heterogeneous stacks communicating via A2A |
| 2026-06-07 | A2A SDK version | v1.0.0 (stable, Linux Foundation) | Green from pre-research; not 0.3 |
| 2026-06-08 | Agent wallet provider | **Cobo CAW restored** (replacing ZeroDev) | TSS local node restart fixed signing; full x402 pipeline working end-to-end |
| 2026-06-08 | Network | **Base mainnet (chain_id 8453)** | AFC moloch-agent has no Base Sepolia support — no contracts, no service, no subgraph deployed |
| 2026-06-08 | AgentFightClub API | ✅ Functional (ClawBank API live) | Probe script confirms working; proposal sponsorship timing issue — fix in progress Day 9 |
| 2026-06-17 | GLM-5.1 demo task | **Dogfooding** — Specialist implements a GuildOS component ticket | Self-referential demo threads every component; canonical mandate: "Build GuildOS — coordinate a Specialist to implement its own tickets" |
| — | ZeroDev session keys | Demoted to design exhibit | CAW is primary wallet; ZeroDev kept as fallback reference only |
| 2026-06-11 | Deliverable hash commitment | **EAS attestation replaces raw `eth_sendTransaction`** | EAS `attest()` is cryptographically signed by Specialist, carries a stable UID cross-referenced in A2A message and ERC-8004 record, and is queryable on easscan without ABI parsing — strictly better than a raw event emission at the same gas cost (see `hackathon/research/EAS_ANALYSIS.md`) |
| 2026-06-17 | Reputation write-back mechanism | **Executable `submitFeedback` Moloch proposal** | Orchestrator submits proposal encoding `giveFeedback()` call; on passing vote `AgentFightClub.process()` executes it with `msg.sender = guild contract` — satisfies F2 caller constraint; no single party writes reputation unilaterally |
