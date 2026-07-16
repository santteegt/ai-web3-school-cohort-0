# GuildOS

> A programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss.

**Track:** Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary)
**Event:** [AI × Web3 Agentic Builders Hackathon](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy) (concluded 2026-06-17 — now in active post-hackathon dogfooding, see `AGENTS.md` "Sprint — Phase Gates")
**Network:** Base Sepolia (`84532`, isolated component testing only) · Base mainnet (`8453`, canonical — the only valid submission-evidence network)
**Team:** Santiago ([@santteegt](https://github.com/santteegt)) — Solo

---

## Problem

The coordination infrastructure for AI-augmented knowledge work does not exist yet. Capable contributors — human and AI — cannot form credible, accountable, ephemeral work structures without a rent-extracting intermediary in the middle.

→ Full problem statement, target users, and the North Star scenario: [`specs/00-overview.md`](specs/00-overview.md)

---

## Minimum Demo Loop

GuildOS is demonstrated by **building GuildOS with GuildOS** — the guild's mandate is to ship GuildOS components, and the Specialist is an agentic AI × Web3 engineer that picks up real GuildOS tickets. Both agents register their ERC-8004 identity once, before any guild ever forms, so the Specialist's reputation clock starts ticking before real work begins.

1. Specialist, then Orchestrator, each register their own ERC-8004 identity via their own local `GuildToolsServer` instance (one-time, before the loop below)
2. Human founds a GuildOS guild via AgentFightClub with a mandate and funded treasury
3. Orchestrator surfaces the registered Specialist as a candidate; human approves (**Gate 0**)
4. Specialist quotes scope and cost; human accepts (**Gate 0.5**)
5. Human votes to approve Specialist membership via AgentFightClub (**Gate 1**)
6. Orchestrator delegates a real GuildOS ticket to the Specialist via A2A
7. Specialist executes with GLM-5.1 long-horizon planning; EAS-attests the deliverable hash on Base
8. Human reviews the deliverable + automated pre-check report; accepts (**Gate 2**)
9. Human votes and processes the AgentFightClub payment proposal; treasury releases payment (**Gate 3**)
10. Human votes and processes the reputation proposal; the Specialist's ERC-8004 profile gains a verified delivery record (**Gate 4**)

**Two clickable Basescan tx hashes (settlement + reputation write) + an EAS attestation + an ERC-8004 before/after delta = verifiable demo.**

→ Full 15-step flow, sequence diagram, and state machine: [`specs/10-technical-design.md`](specs/10-technical-design.md) §2

---

## Architecture

```
                     Human Founder (Marco)
                             │  CLI gates: Gate 0 · Gate 0.5 · Gate 1
                             │             Gate 2 · Gate 3 · Gate 4
                             ▼
      ┌───────────────────────────────┐         ┌───────────────────────────┐
      │      Orchestrator Agent       │  A2A    │      Specialist Agent     │
      │   MCP server (stdio)          │◄───────►│   A2A server — :10001     │
      │   A2A server — :10000         │         │   GLM-5.1 task execution  │
      └───────────────┬───────────────┘         │   EAS attestation         │
                       │                         └───────────────────────────┘
                       │ contract calls (web3.py), signed via WalletProvider (Cobo CAW)
                       ▼
      ┌───────────────────────────────────────────────────────────────────┐
      │                       On-Chain Layer (Base)                       │
      │     AgentFightClub (Moloch v3) · EAS · ERC-8004 Identity/Rep.     │
      └───────────────────────────────────────────────────────────────────┘

      ┌───────────────────────────────┐
      │       GuildToolsServer        │   run once per agent, before the
      │   MCP server (stdio)          │   loop above — each with its own
      │   identity_register           │   wallet env
      │   identity_read_profile       │
      └───────────────┬───────────────┘
                       │ contract calls (web3.py), signed via WalletProvider (Cobo CAW)
                       ▼
              ERC-8004 IdentityRegistry
```

A2A messages between the two agents: `task/invite`/`task/quote`,
`task/send`/`task/accepted` (Orchestrator → Specialist, synchronous), and
proactive `task/delivered`/`feedback/request` (Specialist → Orchestrator's
A2A server, after harness work completes). Orchestrator MCP tools:
`guild_launch` · `talent_query` · `task_invite` · `task_delegate` ·
`deliverable_review` · `settle` · `reputation_write`.

`GuildToolsServer` is deliberately separate from the Orchestrator's own MCP
server — any guild agent (Specialist, Orchestrator, or a future member) runs
its own local instance with its own wallet env, so no agent's wallet ever
becomes the on-chain owner of another agent's identity.

→ Component map, MCP tool contracts, and transport mechanics: [`specs/10-technical-design.md`](specs/10-technical-design.md) §1/§12
→ Pinned dependencies, contract addresses, and interfaces: [`specs/20-api-contracts.md`](specs/20-api-contracts.md)

---

## Setup

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python 3.11+ (uv will manage the Python version automatically)
- Node.js 20+ (for `moloch-agent` CLI — `npm i -g @raidguild/meta-clawtel`)
- Cobo Agentic Wallet (CAW) — a TSS wallet node per agent; run `caw wallet current --show-api-key` to obtain the credentials below. No agent ever holds a raw private key — see `src/shared/wallet.py`.
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
| `CHAIN_ID` | Active network: `84532` (Base Sepolia, isolated testing) or `8453` (Base, canonical/evidence) — resolves into `config/networks.json` | Default: `8453` |
| `ALCHEMY_API_KEY` | Secret, substituted into `config/networks.json`'s RPC URL template | Yes |
| `WALLET_PROVIDER` | Scoped signing provider (`caw` \| `zerodev` \| `turnkey`) | Default: `caw` |
| `AGENT_WALLET_API_URL` | CAW API base URL | Default: `https://api.agenticwallet.cobo.com` |
| `AGENT_WALLET_API_KEY` | CAW API key for **the agent this process is acting as** — per-process, never a single global value shared across the Orchestrator and Specialist (see the Run section below) | Yes |
| `AGENT_WALLET_WALLET_ID` | CAW wallet ID for the same agent | Yes |
| `AGENT_WALLET_ADDRESS` | That wallet's on-chain address on Base | Yes |
| `ORCHESTRATOR_WALLET_ADDRESS` | Orchestrator wallet address (used as treasury caller in guild launch) | Yes |
| `SPECIALIST_WALLET_ADDRESS` | Specialist Agent wallet address (settlement target) | Yes |
| `ORCHESTRATOR_A2A_PORT` | Orchestrator's A2A HTTP server port | Default: `10000` |
| `SPECIALIST_A2A_PORT` | Specialist's A2A HTTP server port | Default: `10001` |
| `CLAWBANK_API_KEY` | ClawBank API key (skip to use DAOhaus SDK fallback) | Optional |

Moved to `config/networks.json` (do not set these in `.env`): EAS contract +
SchemaRegistry addresses, the registered delivery schema UID, and the
ERC-8004 IdentityRegistry/ReputationRegistry addresses.

### Run

**Step 0 — one-time, per agent: register ERC-8004 identity via `GuildToolsServer`.**
`AGENT_WALLET_*` is a single set of values in `.env` — since each agent
signs with its own CAW wallet, register the Specialist and the Orchestrator
in two separate runs, swapping `AGENT_WALLET_API_KEY`/`AGENT_WALLET_WALLET_ID`/
`AGENT_WALLET_ADDRESS` to that agent's own CAW credentials before each:

```bash
# With the Specialist's AGENT_WALLET_* values loaded:
make inspect-guild
# Opens the MCP Inspector against `python -m src.guild.server` — call
# guildtools_identity_register with a `services` list (see
# src/shared/erc8004.py's build_a2a_service()/build_oasf_service() for the
# expected shapes), then repeat with the Orchestrator's AGENT_WALLET_* values.
```

This mints an ERC-721 `agentId` for each agent and immediately backfills its
`registrations[]` self-reference — two on-chain txs per agent. Idempotent:
re-running against an already-registered wallet is a no-op. See
[`specs/20-api-contracts.md`](specs/20-api-contracts.md) §5 (`ERC8004`,
`GuildToolsServer`) for the full interface.

**Then start these in order** — the coordination runner (Terminal 4) depends on the other three being up.

**Terminal 1 — Orchestrator Agent (MCP server):**
```bash
uv run python -m src.orchestrator.server
# MCP server on stdio — exposes guild_launch, talent_query, task_invite,
# task_delegate, deliverable_review, settle, reputation_write
```

**Terminal 2 — Orchestrator A2A server (separate process from Terminal 1):**
```bash
uv run python -m src.orchestrator.a2a_server
# A2A HTTP server on localhost:10000
# Receives proactive task/delivered and feedback/request from the Specialist
```

**Terminal 3 — Specialist Agent (A2A server):**
```bash
uv run python -m src.specialist.agent
# A2A HTTP server on localhost:10001
# Exposes Agent Card at localhost:10001/.well-known/agent-card.json
```

**Terminal 4 — Coordination Runner (full 15-step MVP loop):**
```bash
# Default task (SHA-256 demo)
uv run python -m src.cli.runner

# Custom task
uv run python -m src.cli.runner "Audit this ERC-20 staking contract for reentrancy vulnerabilities"
```

The runner drives the complete coordination loop — guild launch → talent query → six
human gates (0, 0.5, 1, 2, 3, 4) → A2A task delegation → GLM-5.1 execution → EAS attestation
→ deliverable review → settlement → DAO reputation proposal → ERC-8004 write-back.
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

## Sprint Status

The original hackathon calendar (Day 8–13) is superseded — the project is
now in post-hackathon dogfooding, tracked via GitHub milestones instead of
calendar days:

| Phase | Theme | Gate to move on |
|-------|-------|------------------|
| 0 | Wallet Infrastructure | `WalletProvider` (CAW) lands and is validated |
| 0.5 | Agent Identity Bootstrap | Specialist registers on ERC-8004 first, Orchestrator second |
| 1 | Coordination MVP | Real `task/send` payload built and consumed |
| 2 | Evidence & Realism | EAS attestation; real founder parameters |
| 3 | Economic Loop | Payment + reputation proposals passed; ERC-8004 delta |
| 4 | Demo Readiness | Dispute path, E2E smoke test, submission form |

→ Full phase gates with issue links: [`AGENTS.md`](AGENTS.md) "Sprint — Phase Gates"
→ Historical Day 8–13 calendar plan: [`CHANGELOG.md`](CHANGELOG.md) "Process — Issues & Milestones"

---

## Submission Evidence

> Updated as each on-chain milestone lands — currently a scaffold, no
> mainnet entries yet.

| Evidence | Location |
|----------|----------|
| Specialist ERC-8004 registration — Basescan tx (Registered + URIUpdated) | _TBD_ — see `submissions/tx_hashes.md` |
| Orchestrator ERC-8004 registration — Basescan tx (Registered + URIUpdated) | _TBD_ — see `submissions/tx_hashes.md` |
| Deliverable EAS attestation | _TBD_ |
| AgentFightClub settlement — Basescan tx | _TBD_ |
| Reputation write (`giveFeedback`) — Basescan tx | _TBD_ |
| Specialist ERC-8004 before-state | `./logs/erc8004_specialist_before.json` |
| Specialist ERC-8004 after-state | `./logs/erc8004_specialist_after.json` |
| A2A message trace | `./logs/a2a_trace_*.json` |
| GLM-5.1 execution trace | `./logs/glm_trace_*.json` |
| Demo video (3–5 min) | _TBD_ |

→ Full evidence checklist: [`submissions/tx_hashes.md`](submissions/tx_hashes.md)

---

## SDK / API Used

| Integration | Package | Purpose |
|-------------|---------|---------|
| A2A Protocol | `a2a-sdk[http-server]` v1.1.0 | Cross-agent task delegation and result return |
| Z.AI GLM-5.1 | Z.AI API | Specialist Agent long-horizon task execution |
| Cobo Agentic Wallet (CAW) | TSS wallet node | Provider-agnostic, Pact-scoped signing for every agent — no agent ever holds a raw private key; swappable to ZeroDev/Turnkey via `WALLET_PROVIDER` |
| AgentFightClub / Moloch v3 | ClawBank API or DAOhaus SDK | Guild treasury, governance, settlement |
| ERC-8004 | `web3.py` | Agent identity registration, on-chain profile reads, and reputation write-back — no external indexer dependency |
| EAS | `web3.py` | Deliverable attestation on Base |
| Alchemy RPC | `web3.py` | Base transaction submission and event reading |

---

## License

MIT
