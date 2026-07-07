# GuildOS

> A programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss.

**Track:** Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary)  
**Event:** [AI × Web3 Agentic Builders Hackathon](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy)  
**Deadline:** 2026-06-13 12:00 UTC+8 · **Demo Day:** 2026-06-14  
**Network:** Base Sepolia (testing) · Base (deployment / full integration)  
**Team:** Santiago ([@santteegt](https://github.com/santteegt)) — Solo

---

## Problem

The coordination infrastructure for AI-augmented knowledge work does not exist yet. Capable contributors — human and AI — cannot form credible, accountable, ephemeral work structures without a rent-extracting intermediary in the middle.

→ Full problem statement: [docs/PROBLEM.md](docs/PROBLEM.md)

---

## Minimum Demo Loop

1. Human founds a GuildOS guild via AgentFightClub with a mandate and funded treasury
2. Orchestrator Agent queries ERC-8004 registry and surfaces Specialist candidate
3. Human approves candidate; Specialist quotes scope and cost
4. Human votes to approve Specialist membership via AgentFightClub
5. Orchestrator delegates a real coding/analysis task to Specialist via A2A
6. Specialist executes task with GLM-5.1 long-horizon planning; commits deliverable hash to Base Sepolia
7. Human reviews deliverable + automated pre-check report; accepts
8. AgentFightClub releases payment from treasury to Specialist wallet
9. Specialist's ERC-8004 profile gains a verified delivery record (6 fields on-chain)

**Two clickable Basescan tx hashes + ERC-8004 before/after delta = verifiable demo.**

→ Full 15-step flow: [docs/MVP_FLOW.md](docs/MVP_FLOW.md)

---

## Architecture

```
Human Founder (Marco)
       │  CLI gates: Gate 0 · Gate 0.5 · Gate 1 · Gate 2
       ▼
┌──────────────────────────────────────────────────────────┐
│              Orchestrator Agent  (MCP server)             │
│  guild_launch · talent_query · task_invite               │
│  task_delegate · deliverable_review · settle             │
│  reputation_write                                        │
└──────┬─────────────────────────────┬────────────────────┘
       │ A2A v1.0.0                  │ contract calls (web3.py)
       ▼                             ▼
┌─────────────────────┐   ┌────────────────────────────────┐
│   Specialist Agent  │   │        On-Chain Layer           │
│  (Python / GLM-5.1) │   │  AgentFightClub (Moloch v3)    │
│  task execution     │   │  ERC-8004 Registry (Base Sep.) │
│  deliverable hash   │   │  ZeroDev Kernel v3.3 (ERC-4337)│
└─────────────────────┘   └────────────────────────────────┘
```

→ Full tech stack: [docs/TECH_STACK.md](docs/TECH_STACK.md)  
→ Risks and fallbacks: [docs/RISKS.md](docs/RISKS.md)  
→ Track alignment: [docs/TRACK.md](docs/TRACK.md)

---

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.11+ (uv will manage the Python version automatically)
- Node.js 20+ (for `moloch-agent` CLI — `npm i -g @raidguild/meta-clawtel`)
- Base mainnet RPC (Alchemy recommended)
- Z.AI GLM-5.1 API key

### Install

```bash
git clone https://github.com/santteegt/ai-web3-school-cohort-0
cd hackathon/guild-os

# Install all dependencies (uv creates .venv automatically)
uv sync

# Copy environment template
cp .env.example .env
# Edit .env — fill in all required variables
```

### Environment Variables

`.env` holds only the network **selector** and **secrets**. Every
network-specific value (contract addresses, RPC URL, explorer links, the
registered delivery schema UID) lives in `config/networks.json`, keyed by
`CHAIN_ID`, and is resolved through `src/shared/network_config.py` — not
read from an env var. See that file before adding a new on-chain address
anywhere in the code.

| Variable | Purpose | Required |
|----------|---------|----------|
| `ORCHESTRATOR_WALLET_ADDRESS` | Orchestrator wallet address (used as treasury in guild launch) | Yes |
| `SPECIALIST_WALLET_ADDRESS` | Specialist Agent wallet address (settlement target) | Yes |
| `CHAIN_ID` | Active network: `84532` (Base Sepolia, isolated testing) or `8453` (Base, canonical/evidence) — resolves into `config/networks.json` | Default: `8453` |
| `ALCHEMY_API_KEY` | Secret, substituted into `config/networks.json`'s RPC URL template | Yes |
| `WALLET_PROVIDER` | Scoped signing provider (`caw` \| `zerodev` \| `turnkey`) | Default: `caw` |
| `CLAWBANK_API_KEY` | ClawBank API key (skip to use DAOhaus SDK fallback) | Optional |

Moved to `config/networks.json` (do not set these in `.env`): EAS contract +
SchemaRegistry addresses, the registered delivery schema UID, and the
ERC-8004 IdentityRegistry/ReputationRegistry addresses.

### Run

Start services in this order — the coordination runner depends on both agents being up.

**Terminal 1 — Orchestrator Agent (MCP server):**
```bash
uv run python -m src.orchestrator.server
# MCP server on stdio — exposes guild_launch, talent_query, task_invite,
# task_delegate, deliverable_review, settle, reputation_propose, reputation_write
# Acts as A2A client: sends task messages to the Specialist; receives responses synchronously
```

**Terminal 2 — Specialist Agent (A2A server):**
```bash
uv run python -m src.specialist.agent
# A2A HTTP server on localhost:10001
# Exposes Agent Card at localhost:10001/.well-known/agent.json
```

**Terminal 3 — Coordination Runner (full 15-step MVP loop):**
```bash
# Default task (SHA-256 demo)
uv run python -m src.cli.runner

# Custom task
uv run python -m src.cli.runner "Audit this ERC-20 staking contract for reentrancy vulnerabilities"
```

The runner drives the complete coordination loop — guild launch → talent query → four
human gates (0, 0.5, 1, 2) → A2A task delegation → GLM-5.1 execution → EAS attestation
→ deliverable review → settlement → DAO reputation proposal (Gate 3) → ERC-8004 write-back.
Each gate halts at a `[y/N]` prompt; the loop stops if any gate is rejected.

> **Network:** set `CHAIN_ID=84532` for isolated testing on Base Sepolia, or leave the
> default (`8453`) for full integration on Base. Tx hashes submitted as evidence must
> be on Base.

### Tests & Lint

```bash
make test   # uv run pytest tests/
make lint   # uv run ruff check src/ tests/
```

---

## Sprint Plan

| Day | Date | Theme | P0 Gate |
|-----|------|-------|---------|
| Day 8 | Jun 8 | Validation | AgentFightClub `launch` live · A2A green · GLM-5.1 task locked |
| Day 9 | Jun 9 | Wallets + Identity | Both agents on-chain · Guild funded · ERC-8004 registered |
| Day 10 | Jun 10 | A2A + Execution | Hash committed to Base Sepolia · Basescan tx #1 saved |
| Day 11 | Jun 11 | Settlement + Reputation + E2E | `settle()` tx · ERC-8004 delta visible · Smoke test passes |
| Day 12 | Jun 12 | Demo Prep | README, demo script, submission artifacts — repo clean |
| Day 13 | Jun 13 | Submission | Submitted before 12:00 UTC+8 (04:00 UTC) |

→ Full sprint plan: [`hackathon/notes/WEEK4_SPRINT_PLAN.md`](../notes/WEEK4_SPRINT_PLAN.md)

---

## Submission Evidence

> Updated after build sprint.

| Evidence | Location |
|----------|----------|
| Deliverable hash commit — Basescan tx #1 | _TBD_ |
| AgentFightClub settlement — Basescan tx #2 | _TBD_ |
| Specialist ERC-8004 before-state | `./logs/erc8004_specialist_before.json` |
| Specialist ERC-8004 after-state | `./logs/erc8004_specialist_after.json` |
| A2A message trace (all 7 events) | `./logs/a2a_trace_*.json` |
| GLM-5.1 execution trace | `./logs/glm_trace_*.json` |
| Demo video (3–5 min) | _TBD_ |

→ Full evidence checklist: [`./logs/tx_hashes.md`](./logs/tx_hashes.md)

---

## SDK / API Used

| Integration | Package | Purpose |
|-------------|---------|---------|
| A2A Protocol | `a2a-sdk[http-server]` v1.0.0 | Cross-agent task delegation and result return |
| Z.AI GLM-5.1 | Z.AI API | Specialist Agent long-horizon task execution |
| ZeroDev Kernel | `@zerodev/sdk` v5.x (TypeScript) | ERC-4337 smart accounts + session key policies |
| AgentFightClub / Moloch v3 | ClawBank API or DAOhaus SDK | Guild treasury, governance, settlement |
| ERC-8004 | `web3.py` + 8004scan API | Agent identity registration and reputation read/write |
| Alchemy RPC | `web3.py` | Base Sepolia transaction submission and event reading |

---

## License

MIT
