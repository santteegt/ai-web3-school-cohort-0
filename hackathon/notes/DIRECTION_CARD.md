# GuildOS — Hackathon Direction Card

> Quick-reference card for build decisions. Canonical detail lives in [PROJECT_PROPOSAL.md](../PROJECT_PROPOSAL.md).
> Last updated: 2026-06-07

---

## Track

**Primary:** Cobo | Agentic Economy × Cobo Agentic Wallet  
**Secondary (eligible):** Z.AI | Web3 × Long-Horizon Task (GLM-5.1 is the Specialist Agent's execution engine)

---

## Project Name

**GuildOS**

*A programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss.*

---

## Target Users

| Segment | Who | Pain |
|---|---|---|
| **Primary** | Independent developers / small dev shops (1–4 people) | Upwork fees, GitHub marketplace rigidity, Slack coordination that loses context after every project |
| **Secondary** | AI agent developers | Agents confined to one platform's tool ecosystem; no portable economic identity |
| **Not this hackathon** | Enterprise procurement, non-technical clients | Out of scope; demo targets technically fluent audience (developers + judges who can read Basescan) |

---

## Problem

The coordination infrastructure for AI-augmented knowledge work does not exist yet.

- Finding a specialist takes weeks; reputation is locked in platforms you do not own
- AI agents can execute real work autonomously but have no economic structure to join that rewards verified delivery
- Neither side uses what the other offers: developers treat agents as tools, agents have no credible way to join accountable work structures

**Root gap:** capable contributors — human and AI — cannot form credible, ephemeral work structures without a rent-extracting intermediary.

---

## Minimal Feature (MVP Demo Loop)

> One founding agent + one specialist agent + one real task + one payment + one reputation record.

1. Founding agent launches guild via AgentFightClub (`launch` + `commit`) — mandate on-chain, treasury funded
2. Specialist Agent (with live ERC-8004 profile) submits membership proposal; human votes to approve
3. Orchestrator delegates a real coding/analysis task to Specialist via A2A structured message
4. Specialist executes task using GLM-5.1; commits deliverable SHA-256 hash to guild contract on Base Sepolia
5. Human reviews work + Orchestrator's automated pre-check report; accepts deliverable
6. AgentFightClub `settle()` releases payment from treasury to Specialist's wallet
7. Orchestrator calls `ERC-8004.recordDelivery()` — Specialist's profile gains one verified delivery record

**Proof:** Two clickable Basescan tx hashes (deliverable hash commit + treasury settlement) + ERC-8004 profile delta (0 → 1 verified delivery).

---

## Technical Path

| Layer | Component | Notes |
|---|---|---|
| Agent frameworks | Claude Code (MCP server) + Hermes + GLM-5.1 API | Orchestrator on Claude Code; Specialist on Hermes |
| Agent protocol | A2A SDK v1.0.0 | Cross-harness task delegation + result return |
| On-chain coordination | AgentFightClub (Moloch v3) | Guild treasury, governance, settlement |
| On-chain identity | ERC-8004 registry (Base Sepolia) | Agent identity, capability claims, portable reputation |
| Agent wallet | Cobo CAW | Pact-scoped API key; per-task spending ceiling; x402 payment protocol |
| Language | Python (primary) | Agent services, CLI tools, A2A handlers |
| Smart contract tooling | Foundry / ethers.py | Contract calls; no custom Solidity for MVP |
| Network | Base Sepolia testnet | All on-chain ops: treasury, deliverable hash, reputation, settlement |
| Identity API | 8004scan API | ERC-8004 profile reads |

**Architecture pattern:** Hybrid custom workflow + MCP tool-manifest pack. Orchestrator's tools are packaged as MCP schemas (`guild_launch`, `talent_query`, `task_invite`, `task_delegate`, `deliverable_review`, `settle`, `reputation_write`) — portable to other harnesses post-hackathon.

**What is mocked:** capability matching (hardcoded agent pair), guild context store (JSON file per session), multiple concurrent agents.

---

## Major Risks

| Risk | Mitigation |
|---|---|
| **AgentFightClub API instability (alpha)** | Fallback: deploy Moloch v3 DAO directly via DAOhaus SDK (audited, 4 years production); same contract logic, no ClawBank dependency |
| **A2A spec compliance gap** | Build against A2A v1.0.0 spec; keep message schema minimal; use reference implementation as test fixture |
| **GLM-5.1 output quality for chosen task** | Test 3 representative task types on Day 1; pick the one with most consistent structured output; use exclusively in live demo |
| **ERC-8004 registry latency / downtime** | Cache profile at startup; run demo against cached profiles if API is slow; maintain fallback JSON profile file |
| **On-chain tx timing during live demo** | Pre-stage membership proposal/vote before demo; have pre-recorded tx hashes as fallback screen |

---

## Human Confirmation Gates

| Gate | Step | What human decides |
|---|---|---|
| Gate 0 | Candidate selection | Approve invite to Specialist Agent from ERC-8004 shortlist |
| Gate 0.5 | Quote acceptance | Confirm scope / cost / timeline before work starts |
| Gate 1 | Membership | Vote to admit Specialist Agent into guild via AgentFightClub |
| Gate 2 | Deliverable acceptance | Review work + auto-evaluator report; unlock payment |

---

## Submission Deadline

**2026-06-13 12:00 UTC+8 (04:00 UTC)** · Demo Day: 2026-06-14 · Results: 2026-06-17
