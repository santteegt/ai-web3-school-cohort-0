# GuildOS

> A programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss.

**Track:** Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary)  
**Event:** [AI × Web3 Agentic Builders Hackathon](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy)  
**Deadline:** 2026-06-13 12:00 UTC+8 · **Demo Day:** 2026-06-14  
**Network:** Base Sepolia testnet  
**Team:** Santiago Hernandez ([@santteegt](https://github.com/santteegt)) — Solo

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

- Python 3.11+
- Node.js 20+ (ZeroDev TypeScript bridge for session key policies)
- [gh CLI](https://cli.github.com/) authenticated to `santteegt/guild-os`
- Base Sepolia RPC (Alchemy recommended)
- Z.AI GLM-5.1 API key

### Install

```bash
git clone https://github.com/santteegt/guild-os
cd guild-os
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — fill in all required variables
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `ALCHEMY_API_KEY` | Base Sepolia RPC | Yes |
| `GLM_API_KEY` | Z.AI GLM-5.1 API | Yes |
| `ORCHESTRATOR_PRIVATE_KEY` | Orchestrator Agent EOA signing key | Yes |
| `SPECIALIST_PRIVATE_KEY` | Specialist Agent EOA signing key | Yes |
| `AGENTFIGHTCLUB_API_KEY` | ClawBank API key | Optional — fallback: DAOhaus SDK |
| `ZERODEV_PROJECT_ID` | ZeroDev for session key policies | Optional — fallback: basic signer |
| `ERC8004_CONTRACT` | IdentityRegistry address on Base Sepolia | Default: `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| `REPUTATION_CONTRACT` | ReputationRegistry address | Default: `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

### Run (Two Terminals)

**Terminal 1 — Orchestrator Agent (MCP server):**
```bash
python -m src.orchestrator.server
# Starts MCP server on localhost:3000
```

**Terminal 2 — Specialist Agent:**
```bash
python -m src.specialist.agent
# Starts A2A HTTP server on localhost:10001
```

Human gate prompts appear in Terminal 1 at Gate 0, 0.5, 1, and 2.

### GitHub Project Board Setup (one-time)

```bash
chmod +x scripts/setup-github.sh
./scripts/setup-github.sh
```

Creates 14 labels and 6 sprint milestones (Day 8–13) in the GitHub repo.  
Then go to `https://github.com/santteegt/guild-os/projects/new` and create a board with columns matching the milestones.

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
| Specialist ERC-8004 before-state | `hackathon/notes/erc8004_specialist_before.json` |
| Specialist ERC-8004 after-state | `hackathon/notes/erc8004_specialist_after.json` |
| A2A message trace (all 7 events) | `hackathon/notes/a2a_trace_*.json` |
| GLM-5.1 execution trace | `hackathon/notes/glm_trace_*.json` |
| Demo video (3–5 min) | _TBD_ |

→ Full evidence checklist: [`../../submissions/tx_hashes.md`](../../submissions/tx_hashes.md)

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
