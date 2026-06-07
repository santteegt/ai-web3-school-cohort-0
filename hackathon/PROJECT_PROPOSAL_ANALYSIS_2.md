Here's the full proposal analysis with gap check and recommended additions.

---

## Part 1 — Completeness Check

**Project name** ✅ GuildOS — clearly stated throughout.

**Track** ✅ Cobo | Agentic Economy × Cobo Agentic Wallet (primary), Z.AI (secondary), with architecture-contingent note.

**Target user** ✅ Section 3 — independent devs + small dev shops (primary), AI agent developers (secondary). Well-scoped with an explicit "not this hackathon" boundary.

**Problem** ✅ Section 2 — coordination gap in AI-augmented knowledge work. Strong.

**Minimum feature** ✅ Section 5 (Minimum Demo Loop) and Section 11 (#2). One loop, clearly stated.

**Teammates/roles** ❌ **MISSING.** Registered solo. The proposal has no section for team composition. For submission this is required. Either add a "Solo / looking for teammate" note, or if a teammate joins, define their role (Specialist Agent implementation is the natural split).

**Tech stack** ⚠️ **SCATTERED.** Components are mentioned across sections but there is no single reference table. Judges and teammates need to find it in one place. Should be added as a dedicated section.

**Risks** ✅ Section 9 (Main Risks table) — good coverage across five risk areas.

**Biggest technical risk** ✅ Section 11 (#5) — AgentFightClub Skill API alpha instability, with fallback to DAOhaus SDK. Clear and actionable.

**Fallback plan** ✅ Answered in Section 11. DAOhaus fallback is well-reasoned.

---

## Part 2 — Feature Additions

### Talent Hunting via ERC-8004

The current proposal has the Specialist Agent passively "discover" the guild's mandate and self-submit a proposal. That's a push model — the agent finds you. Talent hunting is the pull model: the Orchestrator actively queries the ERC-8004 registry for agents whose capability claims match the task type, ranks them by delivery history and acceptance rate, and presents a shortlist to the human founder before Step 4 (membership proposal).

**What to add to the proposal:**

Rename Step 3 in the Process Flow from "Specialist Agent discovers mandate" to two steps: (3a) Orchestrator queries ERC-8004 registry for agents with matching capability claims; (3b) Human reviews ranked shortlist and selects a candidate to invite; Specialist receives invite and confirms via A2A before submitting the AgentFightClub membership proposal.

In the Feature List, add to MVP: "ERC-8004 registry capability query — Orchestrator reads candidate agent profiles and surfaces a shortlist for human review before the membership vote." Add to Mock vs Real: "ERC-8004 registry talent query | Mocked — hardcoded candidate for MVP; semantic LLM ranking is post-hackathon."

The reason this matters for the demo: it shows that ERC-8004 is not just a record-keeping layer but a *discovery* layer. The before/after story becomes: "Here is the registry. The mandate required a security auditor. Here are the three agents that match. Marco selected this one based on 12 prior deliveries and a 94% acceptance rate." That is a significantly stronger demo moment than "an agent appeared and applied."

---

### A2A Commerce Protocol (Quoting, Delivery, Acceptance, Escrow, Evaluators, Reputation, Dispute Resolution)

The current A2A treatment covers task delegation and result return. The full commerce loop needs seven named stages. Here is how each maps to what's already in the proposal vs. what needs to be added:

**Quoting** — Not currently in the proposal. Before executing, the Specialist Agent should respond to the A2A task message with a quote: estimated cost, timeline confirmation, and scope boundary acknowledgment. Orchestrator (or human) accepts the quote before work starts. This creates a binding agreement traceable in the A2A message log. For MVP, quote acceptance can be a simple y/N CLI prompt. New A2A message types: `task/quote-request` (Orchestrator → Specialist) and `task/quote` (Specialist → Orchestrator).

**Delivery** — Already in the proposal. Specialist hashes the deliverable, commits on-chain, returns via A2A. Solid.

**Acceptance** — Human Gate 2 is in the proposal. What's missing is the corresponding A2A signal: after the human accepts, the Orchestrator should send a `task/accepted` message back to the Specialist. This closes the A2A transaction loop and triggers both payment and reputation write-back. Without it, the Specialist has no protocol-level confirmation of acceptance — it only knows payment was released.

**Escrow** — The funds are already locked in the AgentFightClub treasury from Step 1, but the proposal doesn't explicitly frame this as escrow. Add one sentence in the Web3 Mechanism section: "From the moment the guild treasury is funded, capital is in escrow — locked by Moloch's ragequit protection, inaccessible to anyone until either `settle()` is called on acceptance or a rage-quit exit is triggered on rejection."

**Evaluators** — Not currently in the proposal. For MVP, the Orchestrator plays an automated evaluator role before presenting the deliverable to the human: it runs a minimal automated check (deliverable hash present, file size non-zero, outputs match declared format) and produces an evaluation report that accompanies the human review request. The evaluation is advisory, not binding — Gate 2 remains with the human. Add to Stakeholders table: "Orchestrator-as-Evaluator | Runs automated pre-check before human review; passes or flags the deliverable." Real third-party evaluator agents are post-hackathon.

**Reputation** — Already in the proposal. See next section for the specific fields to make explicit.

**Dispute Resolution** — Currently explicitly deferred. For the hackathon, add a stub: Gate 2 rejection holds funds in escrow (no `settle()` called), produces a `DISPUTED` state in the guild context store, and the only resolution path is human-initiated ragequit via AgentFightClub (funds returned to the treasury contributor proportionally). Document this stub explicitly in the proposal so judges see the path exists — even if the automated dispute agent is post-hackathon.

**Where to add this in the proposal:** Insert a new sub-section "A2A Commerce Protocol" between the Process Flow and AI Role sections in Section 8. Map each stage to the step number where it occurs in the Process Flow. Update the Mock vs Real table with three new rows: `A2A quote message (Orchestrator ↔ Specialist) | Real`, `A2A acceptance message (Orchestrator → Specialist) | Real`, `Automated evaluator pre-check | Real (minimal — Orchestrator runs hash + format check)`.

---

### On-Chain Reputation Recording

This is already in the proposal but needs to be made more concrete. The current language — "ERC-8004 reputation write-back after acceptance" — is correct but underspecified. Add a dedicated paragraph to the Web3 Mechanism section naming the five fields written to the ERC-8004 contract on acceptance: (1) task type / capability ID, (2) deliverable hash (SHA-256), (3) acceptance timestamp (block timestamp), (4) payment amount in wei, (5) guild contract address. Optionally a sixth: A2A task message ID for off-chain traceability.

Also clarify the trigger: in v1, the Orchestrator Agent calls the ERC-8004 registry contract directly after receiving human acceptance. The call is part of the `settle` flow — the Orchestrator sequences: (a) call AgentFightClub `settle()`, (b) wait for tx confirmation, (c) call ERC-8004 `recordDelivery()` with the five fields. Both transactions produce Basescan links. In v2, a settlement hook on AgentFightClub triggers the reputation write automatically.

This matters for the demo because "here is the on-chain record of this specific delivery, with the deliverable hash and the timestamp, readable by anyone" is one of the two main proof points. Make sure the proposal spells out exactly which contract method is called and what the emitted event contains.

---

### Harness Architecture: Custom Workflow vs. Harness-Compatible Pack

**My recommendation: Hybrid — custom workflow for the core loop, tool-manifest packaging for the Orchestrator.**

Here is the reasoning:

A pure custom workflow (both agents as standalone Python services, direct HTTP between them) is the fastest path to a working demo. Nothing wrong with it. But it doesn't show the harness-diversity story that is the actual GuildOS thesis: that any agent, running on any harness, can participate in a guild as long as it speaks A2A and holds an ERC-8004 identity.

A pure harness-compatible pack (build everything as installable skill packs for Openclaw, Hermes, and Claude Code) is over-engineered for a 7-day build. Each harness has its own tool registration format, memory model, and invocation pattern. Supporting all three upfront is scope creep.

The hybrid path captures the value of both: build the core loop as custom Python services (Orchestrator + Specialist as two async processes), but define the Orchestrator's capabilities as a standard MCP tool manifest (JSON schema + Python handlers), and package it as a Claude Code MCP server. The Specialist runs on Hermes or directly via GLM-5.1 API — whichever is easier to wire A2A into. The two agents communicate via A2A; neither knows or cares what harness the other uses.

**Specific split for the hackathon demo:**
- Orchestrator Agent: Claude Code as the harness. Tools registered as an MCP server: `guild_launch`, `task_delegate`, `deliverable_review`, `settle`, `reputation_write`. Santiago runs the Orchestrator from his Claude Code terminal session.
- Specialist Agent: Hermes as the harness (or raw GLM-5.1 API call from a Python service if Hermes A2A integration is unclear). Receives A2A task messages, executes using GLM-5.1 long-horizon mode, returns deliverable via A2A.

Why this is the right choice: the demo can show two terminal windows — one running the Orchestrator on Claude Code, one running the Specialist on Hermes — and judges can see the A2A messages flowing between them. That is a stronger demo than one agent pair running in the same Python process. It also directly demonstrates GuildOS's interoperability claim without requiring all three harnesses on launch day.

**Post-hackathon path:** because the Orchestrator's tools are already defined as MCP schemas, packaging them for Openclaw is a packaging exercise (adapt the tool manifest format), not a redesign. Same for Hermes if it has an MCP-compatible tool registration system.

**Add to the proposal as a new Section 13: Architecture Decision — Harness Design.** State the decision, the rationale (A2A as harness-independence layer), and the specific split. Update the Mock vs Real table: "Orchestrator harness (Claude Code MCP pack) | Real" and "Specialist harness (Hermes / GLM-5.1) | Real."

---

## Summary of Required Changes

Three additions are blocking (missing from current proposal):
1. **Teammates/roles section** — even if solo, state it explicitly
2. **Dedicated tech stack table** — one place listing: Python, Claude Code MCP, Hermes, GLM-5.1, A2A SDK, Base Sepolia, AgentFightClub/Moloch v3, ERC-8004, Cobo CAW/Wiretap (TBD), Foundry, 8004scan API
3. **Section 13: Harness Architecture Decision** — document the hybrid decision

Three additions strengthen the proposal significantly:
4. **Talent hunting step** in Process Flow + Mock vs Real row
5. **A2A Commerce Protocol sub-section** with all seven stages mapped to process steps
6. **Concrete ERC-8004 write fields** in Web3 Mechanism section (five fields + trigger sequence)

Want me to apply all of these to `hackathon/PROJECT_PROPOSAL.md` now?