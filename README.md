# AI × Web3 School — Personal Learning Journal

> Personal proof-of-work repository for **Santiago** ([@santteegt](https://github.com/santteegt))  
> Cohort 0 — AI × Web3 School

---

## About This Repo

This is my open learning journal for [AI × Web3 School](https://aiweb3.school/en/handbook/), a co-learning program initiated by LXDAO and ETHPanda that bridges AI engineering and Web3 development.

I use an AI Learning Agent (Claude / Hermes / Openclaw) to maintain this repo, draft daily check-ins, and turn learning questions into indexed, reviewable materials.

## Program Links

| Resource | URL |
|---|---|
| Handbook | https://aiweb3.school/en/handbook/ |
| WCB Program Page | https://web3career.build/programs/AI-Web3-School |
| WCB Learning Page | https://web3career.build/programs/AI-Web3-School#tab=learning |

## Repository Structure

```
README.md              ← this file
AGENTS.md              ← Learning Agent rules (also read as CLAUDE.md)
CLAUDE.md              ← symlink → AGENTS.md
profile.md             ← my learner profile
learning-plan.md       ← personalized learning plan
daily/                 ← daily learning notes + check-in drafts
tasks/                 ← task breakdowns and progress tracking
experiments/           ← code experiments, prototypes (.py, .sol, .ts, etc.)
handbook-feedback/     ← feedback on Handbook pages (blockers, typos, suggestions)
hackathon/             ← hackathon ideation and project notes
submissions/           ← records of submitted check-ins and WCB tasks
templates/             ← templates for daily notes and task notes
prompts/               ← prompts used with Sensei throughout the learning journey
tools/                 ← agent tooling (e.g. wcb_client.py for WCB Agent API)
logs/                  ← logs of tools used, decisions made, and course events
  TOOLS.md             ← master list of all tools adopted during the course
```

## Learning Journey

> Program: May 17 – June 14, 2026 · 3-week bootcamp + 2-week hackathon

### Week 1 — AI and Web3 Foundations (Days 1–7)

**Goal:** Build shared language across LLMs, prompts, agents, tool use, wallets, transactions, and smart contracts — connecting everything into one execution chain.

| Day | Topic | Deliverable |
|---|---|---|
| Day 0 | Setup | Repo, AGENTS.md, learning-plan, Sensei agent ✅ |
| Day 1 | LLM + Prompt | Daily note + first experiment |
| Day 2 | Context + RAG | Experiment: retrieval over on-chain data |
| Day 3 | Agent + Frameworks | Agent practice run |
| Day 4 | MCP + Tool Use | Wire up a simple MCP tool call |
| Day 5 | Wallet + Transaction | Create test wallet, make testnet transaction |
| Day 6 | Smart Contract basics | Deploy or call a minimal contract on testnet |
| Day 7 | Week 1 wrap-up | Document successes, failures, corrections; push to GitHub |

**Milestone:** One end-to-end chain — LLM prompt → agent tool call → wallet sign → testnet transaction → receipt

---

### Week 2 — AI × Web3 Intersection Areas (Days 8–14)

**Goal:** Map the AI × Web3 problem space, select a primary direction, produce deep-dive analyses, and draft an initial hackathon project proposal.

**Deliverables:** [Week 2 Proof-of-Work Pack](submissions/Week2-PoW.md) · [Problem Space Map](tasks/AIxWeb3-problem-map.md) · [Direction Selection](tasks/PROBLEM_MAP_%26_MAIN_DIRECTION_SELECTION.md) · [GuildOS Proposal](hackathon/PROJECT_PROPOSAL.md)

---

### Week 3 — Practice Deepening + Hackathon Kickoff (Days 15–21)

**Goal:** Fill AI × Web3 bridge knowledge gaps, finalize hackathon track and technical architecture, and prepare the build plan.

---

### Weeks 4–5 — Hackathon Sprint + Demo Showcase (Days 22–35)

**Goal:** Build and demo GuildOS — a programmable agent coordination studio demonstrating A2A task delegation, on-chain reputation, and treasury-governed payments.

---

---

## Direction & Hackathon

### Main Direction — Identity / Reputation / Capability / Interoperability

My primary focus is the infrastructure layer that makes open multi-agent ecosystems possible: how agents are discovered, how their capabilities are declared in a machine-readable way, how reputation accumulates from verifiable delivery records, and how agents communicate across heterogeneous stacks via open protocols (A2A, MCP). I merged Identity/Reputation and Capability/Interoperability into a single track because they form a hard dependency chain — capability claims are meaningless without a stable identity to anchor them, and reputation cannot accumulate without that identity persisting across engagements. Every other AI × Web3 direction (payment, governance, wallet permission) assumes this layer exists. It doesn't yet, not in an open, trustless form.

The direction is grounded in emerging standards: **ERC-8004** for on-chain agent identity and reputation registry, **A2A Protocol** for structured agent-to-agent task delegation, **EAS** for third-party attestations, and **MCP** for the agent-to-tool invocation layer. Full analysis: [tasks/directions/01-identity-capability.md](tasks/directions/01-identity-capability.md).

### Secondary Direction — Governance / Coordination / Public Goods

Governance coordination is a natural extension of the identity layer: any multi-agent coordination scenario requires agents with verifiable on-chain identities that participants can inspect before accepting their work or outputs. I chose this as the secondary direction because it reinforces rather than competes with the main track — the identity and reputation infrastructure built in the main direction is exactly what governance participants need to evaluate AI-generated briefs and delegate coordination tasks to agents. In GuildOS specifically, the governance layer (AgentFightClub / Moloch v3) is the economic and decision-making structure that the identity layer plugs into.

Full analysis: [tasks/directions/02-governance-coordination.md](tasks/directions/02-governance-coordination.md).

---

### Hackathon Project — GuildOS

**Status: Proposal complete · Architecture decision pending · Build starts Week 4**

> GuildOS is a programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury, and build verifiable on-chain reputation — no platform, no middleman, no context loss.

**Track:** Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary, pending architecture decision)

**Core loop:** A human founder launches a guild via AgentFightClub with a mandate and funded treasury → a Specialist Agent with an ERC-8004 profile joins via governance vote → the Orchestrator Agent delegates a real task via A2A → the Specialist executes it using GLM-5.1 and commits the deliverable hash on Base testnet → the human accepts → payment is released from the shared treasury → the Specialist's ERC-8004 reputation is updated on-chain.

**Proof of completion:** Two clickable Basescan transaction hashes (deliverable hash commit + AgentFightClub settlement) and the Specialist's ERC-8004 profile showing a before/after reputation delta.

| Document | Link |
|---|---|
| Full proposal | [hackathon/PROJECT_PROPOSAL.md](hackathon/PROJECT_PROPOSAL.md) |
| Pre-analysis | [hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md](hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md) |
| Track selection rationale | [hackathon/TRACK_SELECTION.md](hackathon/TRACK_SELECTION.md) |
| Prototyping resources | [hackathon/PROTOTYPING_RESOURCES.md](hackathon/PROTOTYPING_RESOURCES.md) |

**One-page direction memo** (for team formation and mentor/sponsor discussions): [tasks/directions/DIRECTION_MEMO.md](tasks/directions/DIRECTION_MEMO.md)

---

## ⚠️ Privacy Warning

This is a **public repository**. Do not commit:
- Private keys, seed phrases, or wallet mnemonics
- API keys or access tokens
- Personal contact details or internal meeting links
- Any other person's private information

Secrets belong in `.env.local` (gitignored) or your OS keychain only.

---

*Maintained with [AI × Web3 School Learning Agent — Sensei](https://aiweb3.school/learning-agent.en.txt)*
