# GuildOS — Hackathon Project Proposal

> Track: Cobo | Agentic Economy × Cobo Agentic Wallet (primary)
> Directions: Identity / Capability (main) · Governance / Coordination (secondary)
> Built: 2026-06-01 | Cohort 0 · AI × Web3 School
> Prelimary analysis: [Report](./PROJECT_PROPOSAL_PRE_ANALYSIS.md)
> Meeting 2: [Notes](./PROJECT_PROPOSAL_ANALYSIS_2.md)
> Team: Santiago ([@santteegt](https://github.com/santteegt)) — Solo

---

## 1. One-Sentence Pitch

GuildOS is a programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss.

---

## 2. Problem Statement

The coordination infrastructure for AI-augmented knowledge work does not exist yet. Traditional freelance and agency structures are slow and opaque: finding a specialist takes weeks, reputation is locked in platforms you do not own, and every project restarts context from scratch. AI agents can now execute real development work autonomously — writing code, running tests, generating analyses — but without structure they hallucinate, overreach, and leave no verifiable trail. The deeper problem is that neither side is using what the other offers: developers treat agents as tools rather than collaborators, and agents have no economic structure to join that rewards verified delivery with portable reputation. The result is a coordination gap that no existing platform addresses: capable contributors, human and AI, cannot yet form credible, accountable, ephemeral work structures without a rent-extracting intermediary in the middle.

---

## 3. Target Users

**Primary:** Independent developers and small dev shops (1–4 people) who regularly need short-duration specialized expertise — security review, contract audits, frontend work, data analysis, spec writing — and are tired of Upwork's fees, GitHub marketplace's rigidity, and Slack-based coordination that loses context after every project.

**Secondary:** AI agent developers who want their agents to participate in economic structures, accept work, deliver verifiably, and accumulate portable reputation across engagements — rather than being confined to one platform's tool ecosystem.

**Not this hackathon:** Enterprise procurement teams, non-technical clients, anyone who needs a polished consumer UI. The hackathon demo targets a technically fluent audience: developers and judges who can read a Basescan transaction.

---

## 4. Real Scenario

Marco is an independent smart contract developer. He has a client project: build and audit a minimal ERC-20 staking contract in two weeks. He can write the contract himself but does not have a strong audit background. He opens GuildOS, defines a mandate — "build and audit a staking contract for protocol X, budget 0.3 ETH, deliverable: deployed contract + audit report" — and commits capital to a shared guild treasury via AgentFightClub. The club is live: mandate on-chain, treasury open, governance rails active.

A security-specialist agent registered on ERC-8004 discovers the mandate by reading the guild's Orchestrator Agent A2A card. It inspects the Orchestrator's capability manifest, checks the mandate scope, and submits a membership proposal through AgentFightClub. Marco reviews the agent's on-chain profile: twelve prior audit deliveries, 94% acceptance rate, most recent delivery three weeks ago. He votes to approve via AgentFightClub's governance flow. The agent is now a guild member.

The Orchestrator Agent delegates the audit task to the Specialist Agent via a structured A2A task message: contract source, scope boundaries, acceptance criteria (OWASP checklist + no critical findings unmitigated), deadline, and budget. The Specialist Agent decomposes the task using GLM-5.1's long-horizon planning, runs static analysis, writes the audit report, and creates an EAS attestation of the SHA-256 deliverable hash on Base mainnet — embedding the attestation UID in the A2A result message. The result arrives back to the Orchestrator via A2A. Marco reviews the report in the GuildOS interface, accepts the deliverable, and AgentFightClub's `payment` proposal + `process` releases 0.3 ETH from the shared treasury to the Specialist Agent's wallet. The agent's ERC-8004 profile gains a new delivery record: task type, deliverable hash, acceptance timestamp, payment amount, guild address. The reputation is on-chain and portable to the next engagement.

---

## 5. Minimum Demo Loop

A founding agent launches a GuildOS guild via AgentFightClub with a mandate and a funded treasury; a specialist agent with a live ERC-8004 profile joins via a proposal vote; the Orchestrator Agent delegates a real coding or analysis task to the Specialist Agent via A2A; the Specialist executes it using GLM-5.1 and creates an EAS attestation of the deliverable hash on Base mainnet, embedding the UID in the A2A result; the human founder accepts the deliverable; AgentFightClub releases payment from the guild treasury to the Specialist Agent's wallet; and the Specialist's ERC-8004 profile is updated with a verified delivery record — all demonstrable via clickable Basescan transaction hashes.

---

## 6. Feature List

### MVP — Ships in 7 days

- [ ] Guild formation via AgentFightClub: `summon` + `wrap-eth` + `approve-token` + `tribute` (mandate on-chain, treasury open)
- [ ] ERC-8004 profile read for both agents (8004scan API; show profile in demo UI)
- [ ] ERC-8004 talent query — Orchestrator surfaces shortlist of candidate agents for human review (mocked for MVP — hardcoded profile; full semantic ranking is post-hackathon)
- [ ] A2A quote message — Specialist responds to invite with scope, cost, and timeline; human accepts before work begins
- [ ] A2A acceptance message — Orchestrator sends `task/accepted` to Specialist after human approval at Gate 2
- [ ] Automated deliverable pre-check — Orchestrator runs minimal evaluation (hash present, format valid) before presenting to human
- [ ] Dispute stub — Gate 2 rejection records `DISPUTED` state in guild context store; manual ragequit path documented
- [ ] Specialist Agent membership proposal + vote (AgentFightClub `mint-shares` + `sponsor` + `vote` + `process`)
- [ ] A2A task delegation: Orchestrator Agent → Specialist Agent (structured task message)
- [ ] A2A result return: Specialist → Orchestrator (deliverable reference + hash)
- [ ] Real task execution by Specialist Agent using GLM-5.1 long-horizon capability
- [ ] EAS deliverable attestation — Specialist creates EAS attestation of SHA-256 hash on Base mainnet; attestation UID embedded in A2A `task/delivered` message
- [ ] Human review + acceptance (minimal CLI or simple web form)
- [ ] AgentFightClub treasury settlement on acceptance (`payment` proposal → `sponsor` + `vote` + `process`)
- [ ] ERC-8004 reputation write-back after acceptance (on-chain event emitted)
- [ ] Guild context store — mock as JSON file per guild session

### Deferred — Post-hackathon

- Semantic capability matching across multiple candidate agents (full ERC-8004 registry query + LLM ranking)
- Full A2A multi-agent marketplace / discovery
- Shared persistent memory integration (Mem0, LangChain memory, or equivalent OSS)
- Multiple concurrent active tasks per guild
- Guild dissolution mechanic and pro-rata share distribution
- Human-augmented agent profiles (hybrid human + agent contributor)
- AgentFightClub guild-kick and advanced governance features
- Per-capability pricing and per-task escrow (ERC-8183 full lifecycle)
- Cross-guild reputation aggregation and trust graph
- Polished web UI / dashboard

---

## 7. Mock vs. Real

| Component | Status | Justification |
|---|---|---|
| AgentFightClub: `summon` + `wrap-eth` + `approve-token` + `tribute` | **Real** | 4 Moloch v3 operations; core treasury setup |
| AgentFightClub: `mint-shares` + `sponsor` + `vote` + `process` (membership); `payment` + `sponsor` + `vote` + `process` (settlement) | **Real** | Core governance + payment flow; use moloch-agent CLI (direct path) |
| ERC-8004 profile — Orchestrator Agent | **Real** | 8004scan API read; display before state in demo |
| ERC-8004 profile — Specialist Agent | **Real** | 8004scan API read; display before/after states |
| A2A task message (Orchestrator → Specialist) | **Real** | Core interop surface; A2A 1.0 structured message |
| A2A result message (Specialist → Orchestrator) | **Real** | Structured deliverable reference return |
| GLM-5.1 long-horizon task execution | **Real** | Actual output (code / analysis); not simulated |
| EAS deliverable attestation | **Real** | Signed by Specialist; UID cross-references A2A message and ERC-8004 record; queryable on easscan |
| Reputation write-back (on-chain event) | **Real** | Emitted after acceptance; readable from chain |
| Human review + acceptance | **Real (minimal CLI)** | Text interface; sufficient for demo |
| Capability matching across registry | **Mocked** | Hardcoded agent pair; full matching is post-hackathon |
| Guild context store (shared memory) | **Mocked** | JSON file per guild; OSS integration if time allows |
| Agent wallet provider | **Real (Cobo CAW)** | Pact-scoped API key; x402 + ERC-3009; local signer bypass while Cobo node indexing recovers |
| Multiple concurrent guild members | **Mocked** | Demo shows one agent pair; architecture supports N |
| ERC-8004 talent query (capability matching) | **Mocked** | Hardcoded Specialist profile for MVP; full registry query + LLM ranking is post-hackathon |
| A2A quote message (Specialist → Orchestrator) | **Real** | Specialist responds with scope, cost, and timeline before execution |
| A2A acceptance message (Orchestrator → Specialist) | **Real** | Closes A2A transaction loop after human acceptance at Gate 2 |
| Automated evaluator pre-check (Orchestrator) | **Real (minimal)** | Hash present + format check before human review; full third-party evaluator agent is post-hackathon |
| Dispute resolution | **Stub** | Gate 2 rejection → `DISPUTED` state in guild context; manual ragequit exit; automated dispute agent is post-hackathon |

---

## 8. Problem Breakdown

### Stakeholders

| Stakeholder | Role | Type |
|---|---|---|
| **Human Founder (Marco)** | Sets mandate, funds treasury, approves membership, accepts work | Human — initiator and final authority |
| **Guild Orchestrator Agent** | Manages guild; hunts for talent via ERC-8004 registry; delegates tasks via A2A; pre-checks deliverables (automated evaluator); presents results to human | AI agent — coordination layer |
| **Specialist Agent** | Accepts work, executes tasks, delivers verifiably, builds reputation | AI agent — execution layer |
| **AgentFightClub (Moloch v3)** | Manages shared treasury, governance proposals, and settlement | On-chain protocol — economic layer |
| **ERC-8004 Registry** | Stores agent identity, capability claims, delivery records | On-chain data layer — identity/reputation |
| **Base testnet** | Settlement layer for hashes, payments, and reputation events | Blockchain — enforcement layer |

---

### Process Flow

1. **Human founds guild** — Marco calls AgentFightClub `summon`: DAO contract + Gnosis Safe treasury deployed with mandate in metadata. Marco calls `wrap-eth` + `approve-token` + `tribute`: 0.3 ETH enters shared treasury. Guild is live on-chain.
2. **Orchestrator Agent registers** — Orchestrator publishes an ERC-8004 profile on Base testnet (name, capabilities, A2A endpoint, ERC-8004 token minted). Guild is now discoverable.
3. **Orchestrator hunts for talent** — Orchestrator queries the ERC-8004 registry for agents whose capability claims match the mandate's task type. Filters by delivery count, acceptance rate, and recency. Returns a shortlist for human review. (MVP: hardcoded Specialist profile; full semantic LLM ranking is post-hackathon.)
4. **Human reviews shortlist and selects a candidate** — Marco inspects the top-ranked agent's ERC-8004 profile: capability claims, prior deliveries, acceptance rate, most recent activity. Approves the invite. **[HUMAN GATE]**
5. **Orchestrator invites Specialist; Specialist quotes** — Orchestrator sends an A2A invite to the selected Specialist. Specialist confirms availability and responds with a `task/quote`: confirmed scope, estimated cost, and timeline. Orchestrator surfaces the quote to Marco. Marco accepts the quote. **[HUMAN GATE — lightweight]**
6. **Specialist submits membership proposal** — Specialist calls AgentFightClub `mint-shares` with its ERC-8004 profile reference in the proposal description. Proposal recorded on-chain.
7. **Human votes to approve membership** — Marco reads the Specialist's on-chain profile (delivery history, acceptance rate, stake). Calls AgentFightClub `sponsor` + `vote` to approve. After voting and grace period, `process` executes on-chain; Specialist becomes a guild member. **[HUMAN GATE]**
8. **Orchestrator delegates task via A2A** — Orchestrator sends a structured A2A task message to Specialist: task description, input data, acceptance criteria, deadline, and budget.
9. **Specialist executes** — Specialist decomposes the task using GLM-5.1 long-horizon planning. Runs execution loop: plan → tool use → iteration → output.
10. **Specialist delivers** — Specialist hashes the deliverable (SHA-256), creates an EAS attestation of the hash on Base mainnet via `EASClient.attest()`, and sends a `task/delivered` A2A message to Orchestrator with the deliverable reference and attestation UID.
11. **Orchestrator pre-checks deliverable** — Orchestrator acts as automated evaluator: runs a minimal check (hash present, file size non-zero, outputs match declared format). Produces an evaluation report attached to the human review request. (Full third-party evaluator agent is post-hackathon.)
12. **Orchestrator presents to human** — Orchestrator summarizes the delivered work and the evaluation report, and presents it to Marco for review.
13. **Human accepts or rejects** — Marco reviews the deliverable against the acceptance criteria. **[HUMAN GATE]**
    - *On acceptance:* Orchestrator sends a `task/accepted` A2A message to Specialist, triggering the settlement sequence.
    - *On rejection (dispute stub):* Orchestrator records a `DISPUTED` state in the guild context store. Funds remain locked in escrow (AgentFightClub treasury). Human can initiate ragequit to recover funds. Automated dispute agent: post-hackathon.
14. **AgentFightClub settles** — Orchestrator submits a `payment` proposal; after `sponsor` + `vote` + grace period, `process` executes: Moloch v3 contracts release 0.3 ETH from the shared treasury to the Specialist Agent's wallet. Settlement recorded on-chain.
15. **Reputation updated** — Orchestrator calls `ERC-8004.recordDelivery()` with six fields: (1) task type / capability ID, (2) deliverable SHA-256 hash, (3) acceptance block timestamp, (4) payment amount in wei, (5) guild contract address, (6) A2A task message ID. ERC-8004 `DeliveryRecorded` event emitted on-chain. Portable and readable by any subsequent guild or employer.

---

### AI Role

| Agent | AI capability used |
|---|---|
| Orchestrator Agent | Mandate parsing, task decomposition and delegation, A2A message formatting, result summarization for human review |
| Specialist Agent | Long-horizon task execution (GLM-5.1): multi-step planning, tool use across iterations, structured output generation |

AI handles the execution loop completely (Steps 6–9). AI does not make economic decisions: it does not propose its own payment amount, does not trigger settlement, and does not modify the mandate without human approval.

---

### Web3 Mechanism

| Mechanism | What it provides |
|---|---|
| **AgentFightClub (Moloch v3)** | Shared treasury, proposal/vote lifecycle, settlement, ragequit exit — contract-enforced, no trusted party |
| **ERC-8004** | On-chain agent identity, capability claims, portable reputation records that persist across guilds and platforms |
| **Base mainnet** | EAS deliverable attestation (tamper-proof, signed by Specialist), payment settlement transaction, reputation event log |

Without Web3: reputation is a database row on a platform; payment depends on the platform releasing funds; the mandate is a Notion doc anyone can edit. Web3 makes these three properties enforceable at the protocol level, not the platform level.

**ERC-8004 reputation record — six fields written on acceptance:** (1) task type / capability ID matching the mandate category; (2) deliverable SHA-256 hash committed to chain before acceptance; (3) acceptance block timestamp (on-chain, not wall-clock); (4) payment amount in wei; (5) guild contract address providing cross-guild traceability; (6) A2A task message ID for off-chain log linkage. Trigger: Orchestrator calls `ERC-8004.recordDelivery()` after `process` confirms on-chain. Emits `DeliveryRecorded` event readable by any subsequent guild, employer, or reputation aggregator.

---

### Automation Boundaries

| Action | Automated | Human required |
|---|---|---|
| Guild contract deployment | ✅ | — |
| ERC-8004 profile registration | ✅ | — |
| ERC-8004 talent query + shortlist generation | ✅ | — |
| Candidate selection and invite approval | — | ✅ Review profiles + approve invite |
| Quote review and acceptance | — | ✅ Review scope / cost / timeline |
| A2A task delegation | ✅ | — |
| Task execution (GLM-5.1) | ✅ | — |
| Deliverable hashing and chain commit | ✅ | — |
| A2A result return (`task/delivered`) | ✅ | — |
| Automated deliverable pre-check (evaluator) | ✅ | — |
| A2A acceptance message (`task/accepted`) | ✅ | — |
| Reputation write-back | ✅ | — |
| Membership approval | — | ✅ Review Specialist profile + vote |
| Deliverable acceptance | — | ✅ Review work + approve |
| Treasury actions above threshold | — | ✅ Encoded in AgentFightClub governance |

---

### Human Confirmation Points

**Gate 0 — Candidate selection (Step 4):** Human reviews the ERC-8004 shortlist produced by the Orchestrator. Approves the invite to the selected candidate. This gate ensures the human, not the agent, makes the hiring decision.

**Gate 0.5 — Quote acceptance (Step 5):** Human reviews the Specialist's quote (scope, cost, timeline) before work is committed to. This gate locks the economic terms before the task begins. (Lightweight — y/N CLI prompt in MVP.)

**Gate 1 — Membership (Step 7):** Human reviews the candidate Specialist Agent's ERC-8004 profile: delivery history, acceptance rate, task types, most recent activity, stake. Approves or rejects via AgentFightClub `sponsor` + `vote` + `process`. This gate prevents unknown or low-reputation agents from accessing the guild treasury.

**Gate 2 — Deliverable acceptance (Step 13):** Human reviews the delivered work and the Orchestrator's automated evaluation report against the mandate's acceptance criteria. This is the only point where the payment is unlocked. A rejection holds funds in escrow and produces a `DISPUTED` state (manual resolution via ragequit in v1; automated dispute agent is post-hackathon).

---

### Verification Method

1. **EAS deliverable attestation** — Specialist creates an EAS attestation of the SHA-256 deliverable hash on Base mainnet before acceptance. Attestation is cryptographically signed by the Specialist's key, carries a stable UID cross-referenced in the A2A result and ERC-8004 delivery record, and is queryable by judges at `https://base.easscan.org/attestation/{uid}` without ABI parsing.
2. **ERC-8004 reputation delta** — Demo shows the Specialist's profile before (0 delivery records for this task type) and after (1 verified delivery with tx hash, acceptance timestamp, guild address). Reputation is on-chain and readable by anyone.
3. **AgentFightClub settlement transaction** — Treasury release tx hash on Basescan confirms payment moved on acceptance, not on trust.
4. **A2A message log** — Both agents log each A2A message exchange; the task assignment and result can be traced from origination to delivery.

---

### Main Risks

| Risk | Mitigation |
|---|---|
| **AgentFightClub API instability (alpha)** | Fallback: deploy Moloch v3 DAO directly via DAOhaus SDK (open source, audited, 4 years in production); same contract logic, no ClawBank dependency |
| **A2A spec compliance gap** | Build against A2A 1.0 spec; keep the message schema minimal (task, input, result, hash); use the reference implementation as test fixture |
| **GLM-5.1 output quality for the chosen task** | Test 3 representative task types on Day 1; pick the one that produces the most consistent structured output; use it exclusively in the live demo |
| **ERC-8004 registry latency or downtime** | Cache profile response at startup; run demo against cached profiles if API is slow; maintain a fallback JSON profile file |
| **On-chain transaction timing during live demo** | Use Base testnet (fast finality); pre-stage the membership proposal/vote before the demo starts so only Steps 6–12 are live; have pre-recorded tx hashes as fallback screen |

---

### Swimlane Diagram

![GuildOS MVP Workflow](./assets/guildos-workflow.svg)

> 9-step swimlane: Human Founder · Orchestrator Agent · Specialist Agent · AgentFightClub · On-chain/ERC-8004.
> Yellow rows = human confirmation gates. Dashed arrows = cross-lane calls. Solid arrows = adjacent handoffs.

---

## 9. Track Alignment

**Primary: Cobo | Agentic Economy × Cobo Agentic Wallet**

GuildOS's core story is economic coordination at machine speed: a shared treasury funds a mandate, a specialist agent is paid for verified work, and capital moves programmatically on acceptance — not on trust or a platform's release schedule. This maps directly to the Cobo track's "Agentic Economy" framing and explicitly aligns with the track's listed demo directions: "agent-to-agent work protocols" and the "A2A Economy." The individual agent execution wallet (pending architecture decision) will use a scoped smart account enforcing per-task spending limits and contract allowlists — the "controllable" dimension of Cobo's thesis. Z.AI's GLM-5.1 is integrated as the execution engine for the Specialist Agent, but the economic coordination layer — treasury, governance, settlement, and reputation — is the primary demonstration surface.

**Architecture note:** Agent execution wallets use Cobo CAW with pact-scoped API keys enforcing per-task spending limits. Z.AI's GLM-5.1 is integrated as the Specialist Agent's execution engine, making this project eligible for both tracks; Cobo's economic coordination layer (treasury, settlement, reputation) is the primary demonstration surface.

---

## 10. Evaluation Scorecard

*Applied from the AI × Web3 Unified Evaluation Framework.*

| # | Question | Answer |
|---|---|---|
| 1 | **Would this problem exist without AI?** | Yes — but it becomes a DAO for humans (Raid Guild). AI adds: agents as first-class economic members, long-horizon task execution, A2A-based semantic capability matching. AI is necessary for autonomous execution within the guild. |
| 2 | **Would this problem exist without Web3?** | Yes — but reputation is a platform database row, payment depends on a platform releasing funds, and mandate history is editable. Web3 provides: portable on-chain reputation (ERC-8004), contract-enforced treasury (Moloch v3), and tamper-proof delivery records. Web3 is necessary for trustless coordination. |
| 3 | **Who initiates / executes / pays / accepts / bears risk / arbitrates?** | Initiates: Human Founder. Executes: Specialist Agent. Pays: Guild treasury. Accepts: Human Founder. Bears risk: treasury contributors via ragequit. Arbitrates: AgentFightClub governance + human vote. Chain is complete. |
| 4 | **Automated vs. human confirmation?** | Automated: task delegation, execution, EAS attestation, reputation write-back. Human: membership approval and deliverable acceptance. Boundaries are clear and enforceable. |
| 5 | **How is the result verified? Is verification cheaper than coordination?** | Specialist creates an EAS attestation of the deliverable hash before acceptance; attestation UID is embedded in the A2A result and cross-referenced in the ERC-8004 delivery record. Payment only releases after hash match + human approval. Verification cost (one easscan read + hash comparison) is lower than any human-coordination alternative. |
| 6 | **Which layer — application, tooling, protocol, or other?** | Primary: **application layer** (guild formation and operation experience). Secondary: **protocol layer** (coordination primitives — how guilds form, how reputation accumulates). Hackathon targets the application layer. |
| 7 | **Most likely failure mode?** | Interfaces are immature (ERC-8004 is a draft, AgentFightClub is alpha, A2A is new). Mitigation: one integration risk per day, fallback plans defined. Second risk: users unwilling to change workflow — mitigated by targeting technically fluent developers who already use agent tooling. |

**Intersection test:**
| Machine execution | Economic exchange | Permission control | Verifiable records |
|---|---|---|---|
| ✅ GLM-5.1 executes tasks | ✅ Shared treasury, payment on acceptance | ✅ Scoped wallets, human gates, AgentFightClub governance | ✅ EAS delivery attestation, ERC-8004 reputation, settlement tx |

All four dimensions present. Passes the intersection test.

---

## 11. Scoping Answers

**1. Is this an MVP completable in 7 days by one or two developers?**
Yes, with the scope defined above. The key enabling decision was delegating governance and treasury entirely to AgentFightClub (Moloch v3) rather than building it. The remaining core — A2A communication, ERC-8004 reads, GLM-5.1 execution, one EAS attestation, and AgentFightClub `payment` + `process` — is 5 focused integration days with 2 days for wiring and polish.

**2. What is the single minimum loop that must work?**
One founding agent, one specialist agent, one real task executed via A2A + GLM-5.1, one EAS attestation of the deliverable hash on-chain, one payment released from treasury on acceptance.

**3. What must be real vs. mocked?**
Real: AgentFightClub summon/tribute/payment+process, ERC-8004 profile reads, A2A task and result messages, GLM-5.1 task execution, EAS deliverable attestation, payment release, reputation write-back. Mocked: capability matching (hardcoded pair), shared memory (JSON file), multiple concurrent agents.

**4. How will judges know it is actually complete?**
Two verifiable on-chain proofs during the demo: (1) the EAS attestation of the deliverable hash — queryable at `https://base.easscan.org/attestation/{uid}` — and (2) the AgentFightClub treasury settlement tx on Basescan. The Specialist Agent's ERC-8004 profile shows a delivery record delta: before (0 deliveries of this task type) → after (1 verified delivery with attestation UID and timestamp).

**5. Biggest technical risk and fallback?**
Risk: AgentFightClub Skill API is alpha — endpoint may change or be unavailable during the hackathon. Fallback: deploy a Moloch v3 DAO directly using the open-source DAOhaus SDK (audited contracts, 4 years of production use). The treasury mechanics are identical; ClawBank is a convenience layer, not a protocol dependency.

---

## 12. Next Steps (Post-Hackathon Week)

- **Architecture decision:** Finalize agent wallet provider — Cobo CAW vs. others — based on AgentFightClub API experience during the build
- **Shared memory:** Integrate an OSS persistent memory solution (Mem0, LangChain memory, Cognee) to eliminate the guild context store mock. Memory should be member-gated.
- **Capability matching:** Build the semantic ERC-8004 registry query + LLM ranking layer — this is the full Identity/Capability direction entry point
- **Second guild member:** Demo with 2+ specialist agents in the same guild simultaneously
- **Client-facing guild discovery:** A read-only UI showing active guild mandates, member profiles, and open applications
- **ERC-8183 escrow integration:** Replace the simple hash-commit pattern with the full task/payment/dispute lifecycle
- **Guild dissolution:** Implement ragequit-based exit and pro-rata share distribution
- **Week 3 preparation:** Read Agent Identity, Agent Trust, and Verifiable AI handbook chapters before hackathon Day 1

---

---

## 13. Architecture Decision — Harness Design

### Decision: Hybrid Custom Workflow + Tool-Manifest Pack

GuildOS uses a hybrid approach: the core coordination loop is implemented as a custom Python multi-process application, but the Orchestrator Agent's capabilities are packaged as a standard MCP tool manifest — making the Orchestrator installable as a Claude Code MCP server and portable to other harnesses post-hackathon.

### Rationale

A2A protocol already handles harness independence at the communication layer. Because both agents expose A2A-compliant endpoints, which harness runs each agent is invisible to the other. The hybrid approach captures the demonstration value of cross-harness coordination without the over-engineering cost of supporting three harnesses on launch day.

### Agent Split

| Agent | Harness | Implementation |
|---|---|---|
| **Orchestrator Agent** | Claude Code (MCP server) | Tools registered as MCP tool manifest (JSON schema + Python handlers): `guild_summon`, `talent_query`, `task_invite`, `task_delegate`, `deliverable_review`, `guild_settle`, `reputation_write` |
| **Specialist Agent** | Hermes / GLM-5.1 API | Runs as a separate Python service; receives A2A task messages; executes with GLM-5.1 long-horizon planning; returns deliverable via A2A |

### Why This Beats the Alternatives

**vs. pure custom workflow:** The demo runs in two terminal windows — Orchestrator on Claude Code, Specialist on Hermes. Judges see two heterogeneous stacks communicating via A2A and on-chain contracts. This is the GuildOS thesis made visible, not described.

**vs. pure harness-compatible pack:** No need to support all three harnesses upfront. One MCP pack (Claude Code) + one direct integration (Hermes / GLM-5.1) is sufficient for the hackathon. The tool manifests are already written; porting to Openclaw is a packaging exercise post-hackathon.

### Post-Hackathon Path

Because the Orchestrator's tools are defined as MCP schemas, adapting them for Openclaw's skill format or Hermes's tool registration is a packaging exercise. The A2A communication contract and the economic layer (ERC-8004, AgentFightClub) are harness-agnostic by design.

---

## 14. Tech Stack

> ⚠️ Preliminary — to be finalized after deeper exploration and architecture validation during the build sprint.

| Layer | Component | Notes |
|---|---|---|
| Agent frameworks | Claude Code (MCP server), Hermes, GLM-5.1 API | Orchestrator on Claude Code; Specialist on Hermes |
| Agent protocol | A2A SDK v1.0.0 | Cross-harness task delegation + result return |
| On-chain (coordination) | AgentFightClub (Moloch v3) | Guild treasury, governance, settlement |
| On-chain (identity) | ERC-8004 registry (Base Sepolia) | Agent identity, capability claims, reputation |
| On-chain (payment) | Cobo CAW | Pact-scoped API key; per-task spending ceiling; x402 payment protocol |
| Language | Python (primary) | Agent services, CLI tools, A2A handlers |
| Smart contract tooling | Foundry / ethers.py | Contract calls; no custom Solidity for MVP |
| Network | Base Sepolia testnet | All on-chain operations: treasury, deliverable hash, reputation, settlement |
| RPC | Alchemy / Base Sepolia RPC | Transaction submission and event reading |
| Identity API | 8004scan API | ERC-8004 profile reads and registry queries |

---

*Proposal version: 1.1 | Built: 2026-06-01 | Agent: Sensei (Claude via Cowork)*
*Sources: AgentFightClub docs · ERC-8004 EIP · A2A Protocol repo · AIxWeb3 knowledge base · Direction analyses (01, 02)*

---

## Changelog

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-06-01 | Initial proposal |
| 1.1 | 2026-06-07 | Added talent hunting via ERC-8004 pull model (Steps 3–4 expanded); full A2A commerce protocol: quoting, acceptance message, evaluator pre-check, dispute stub; concrete ERC-8004 reputation write (6 fields + trigger); four human confirmation gates (Gate 0, 0.5, 1, 2); harness architecture decision (hybrid MCP pack — Section 13); tech stack placeholder (Section 14); team declared solo; changelog added |
| 1.2 | 2026-06-07 | Tech stack: wallet provider locked to Cobo CAW (Wiretap removed); Base Sepolia added as explicit network row; Track Alignment note updated; Mock vs Real wallet row resolved to Real |
