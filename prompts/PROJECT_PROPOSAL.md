# Hackathon Project Proposal

## Your Role

Act as a critical, intellectually rigorous sparring partner. You do not need to
agree with me. Push back on weak assumptions, flag scope creep, and challenge
claims that aren't grounded in verifiable outcomes. When you disagree, say so
directly and explain why.

---

## How to Proceed

This prompt has two phases. Do not skip Phase 1.

**Phase 1 — Critique and iterate** (do this first):
1. Read all resources listed below before responding.
2. Evaluate the idea against the Project Evaluation Criteria.
3. Answer each Scoping Question explicitly.
4. Identify what should be cut, what should be added, and what is not feasible
   in one week.
5. Propose your recommended MVP scope.
6. Wait for my approval before proceeding.

**Phase 2 — Write the proposal** (only after I say "approved" or "proceed"):
Write `hackathon/PROJECT_PROPOSAL.md` following the Proposal Document Structure
below.

---

## Constraints

- **Do not modify the Idea section.** It is finalized.
- **Do not go deep on the tech stack.** Suggest tools and standards at one level
  of specificity (e.g., "ERC-8004 for agent registry" is fine; debating
  implementation details of ERC-4337 UserOps is not).
- **Scope to one week (7 days).** If a feature cannot be demonstrated in a
  hackathon demo, flag it as post-hackathon scope.

---

## Scoping Questions

Answer each of these explicitly in Phase 1:

1. Is this an MVP that can be completed in 7 days by one or two developers?
2. What is the single minimum loop that must work in the demo? (One sentence.)
3. Which parts can be mocked or stubbed, and which parts must truly call an
   SDK, API, contract, or testnet?
4. How will judges or sponsors know the project is actually complete and
   working — not just a slide deck?
5. What is the biggest technical risk, and what is the fallback if it blocks
   progress mid-week?

---

## Project Evaluation Criteria

Apply all of the following to the proposal. This is not a checklist to pass — it is a set of questions to answer explicitly. Weak answers are a signal to iterate, not to approve.

### Unified Evaluation Framework (7 questions)

Answer each question in one or two sentences. Do not skip any.

1. Would this problem still exist without AI? What capability does AI actually
   provide — understanding, generation, planning, tool use, automation,
   monitoring, summarization, or collaboration?

2. Would this problem still exist without Web3? What mechanism does Web3
   actually provide — payment, identity, permissioning, open state, verifiable
   records, settlement, censorship resistance, or coordination?

3. Who initiates the task, who executes it, who pays, who accepts the result,
   who bears the cost of failure, and who handles governance or arbitration?

4. Which actions can be automated, and which actions require human confirmation?

5. How can the result be verified? Is the cost of verification lower than the
   cost of human coordination?

6. Is it closer to an application-layer experience, developer tooling, protocol
   / standard, permission system, security mechanism, or governance coordination
   process? Identify the primary layer.

7. If this project fails, is it most likely because demand does not exist, trust
   cannot be established, costs are too high, interfaces are immature, permission
   risk is too high, or users are unwilling to change their workflow?

### Intersection test

Truly valuable problems sit at the intersection of **machine execution +
economic exchange + permission control + verifiable records**. Identify which of
these four dimensions the proposal covers and which are missing. If one is
missing, suggest how to recover it or flag the proposal for revision.

### Idea validation

Answer these directly:
- Should I iterate on the idea, and if so, what specifically?
- Is it viable as a 7-day hackathon build, or does it need to be scoped down?
- What can be trimmed to make it viable without losing the core value proposition?

---

## Track Alignment

The hackathon has two sponsor tracks. The proposal must recommend exactly one
primary track and justify the choice in one paragraph.

**Sponsor tracks (priority):**
- **(SPONSOR) Cobo | Agentic Economy × Cobo Agentic Wallet** — Agentic Commerce:
  controllable on-chain fund operations. Relevant demos: Agent-Native Payments,
  agent resource procurement, agent-to-agent work protocols, automated trading,
  A2A Economy.
- **(SPONSOR) Z.AI | Web3 × Long-Horizon Task** — GLM-5.1 long-horizon task
  capabilities: complex task decomposition, multi-step planning, continuous tool
  use, requirement-to-delivery loops. Relevant demos: Web3 Agentic Dev Tools,
  AI-Powered Web3 Game Studio, AI × Creator Economy.

**General tracks (ideation reference only):**
- Agentic Commerce / Payment
- Dev Tooling / Agent Workflow
- Wallet / Permission / Safe Execution
- AI Security / Privacy / Censorship Resistance
- Governance / Coordination / Public Goods
- Open Track (must justify why AI × Web3 combination is necessary)

---

## Proposal Document Structure

When Phase 2 is approved, write `hackathon/PROJECT_PROPOSAL.md` with exactly
these sections, in order:

1. **One-sentence pitch**
2. **Problem statement** (3–5 sentences; no bullet points)
3. **Target users** (who specifically; not "developers in general")
4. **Real scenario** (2–3 paragraph walkthrough of a concrete use case from
   start to finish)
5. **Minimum demo loop** (one paragraph; the single thing that must work)
6. **Feature list**
   - MVP (ships in 7 days)
   - Deferred (post-hackathon scope)
7. **Mock vs. real** (table: component → mock or real → justification)
8. **Problem breakdown**: elaborate in text + create a swimlane diagram that includes:
   - Stakeholders
   - Process flow (numbered steps)
   - AI role
   - Web3 mechanism
   - Automation boundaries
   - Human confirmation points
   - Verification method
   - Main risks (max 5, each with a mitigation)
9. **Track alignment** (primary sponsor track + one-paragraph justification)
10. **Evaluation scorecard** (the five criteria table, filled in for this proposal)
11. **Scoping answers** (the five questions, answered for this proposal)
12. **Next steps** (what happens in the week after the hackathon)

---

## Resources

Read all of these before Phase 1:

- AI × Web3 wiki: `knowledge-base/AIxWeb3/wiki/`
- Bridge intro + learning resources:
  `knowledge-base/AIxWeb3/raw/AIxWeb3 Bridge - Introduction.md`
- Bridge mental model:
  `knowledge-base/AIxWeb3/concepts/aixweb3-bridge-mental-model.md`
- Unified Evaluation Framework:
  `knowledge-base/AIxWeb3/raw/AIxWeb3 Project - Unified Evaluation Framework.md`
- AI × Web3 problem space map: `tasks/AIxWeb3-problem-map.md`
- Problem map & direction selection:
  `tasks/PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md`
- Main direction deep dive (Identity / Capability):
  `tasks/directions/01-identity-capability.md`
- Secondary direction deep dive (Governance / Coordination):
  `tasks/directions/02-governance-coordination.md`

---

## Idea

> **GuildOS** is a programmable studio where humans and AI agents form around a mandate, build together with shared memory and verifiable reputation, and share the upside — with no middleman and no bureaucracy.

### The Problem

The way knowledge workers coordinate is broken in two directions at once.

Traditional freelance and agency structures are slow, expensive, and opaque: finding the right specialist takes weeks, context disappears between engagements, reputation lives inside platforms you don't own, and every project restarts from zero. The middlemen — platforms, recruiters, project managers — extract margin from every exchange while adding latency and bureaucracy.

AI agents can now handle a growing share of the execution layer: writing code, running tests, generating specs, querying on-chain data, filing PRs. But agents without structure hallucinate, overreach, and leave no verifiable trail. And most developers are treating agents as tools to use rather than collaborators to compose with.

The result: talented people are underemployed, agents are underutilized, and the coordination infrastructure for the next era of software work doesn't exist yet.

### The Vision

GuildOS is the coordination layer for programmable expert studios — ephemeral, mandate-driven organizations where humans and agents join, work, deliver, and share the upside, with no platform extracting rent in the middle.

A guild forms around a mandate. Members are specialists: human contributors bringing domain expertise and judgment, AI agents bringing execution speed and capability breadth, or human-augmented agents where a developer's skills are encoded into a deployable profile. Every member — human or agent — carries a verifiable identity, a capability manifest, and a reputation that accumulates across every engagement.

The guild doesn't need a CEO to coordinate. It needs a mandate, a treasury, and a set of rules. Agents source opportunities, propose work, execute tasks, and move capital. Humans confirm high-stakes decisions, review deliverables, and vote on membership. When the mandate is complete, the guild dissolves or mutates. The reputation stays.

### Objectives

1. Make developer expertise legible and composable.
Every contributor — human or agent — maintains a verifiable profile: skills, past work, delivery history, and reputation score anchored on-chain. No more "trust me" introductions. The profile speaks for itself and travels across every engagement.
2. Eliminate the context tax.
Shared persistent memory across all guild members means no re-explaining project history, decisions, or prior work. Every agent knows what every other agent built. New members onboard by reading the record, not asking questions.
3. Replace middlemen with programmable coordination.
A guild treasury manages capital directly. Work proposals are submitted, reviewed, and approved through governance — no account manager, no platform fee, no delayed payment. Funds move at machine speed once humans approve the gate.
4. Make trust provable, not assumed.
All work is verified before payment is released. Deliverables are hashed, referenced, and linked to the agent profile that produced them. Reputation is built from evidence, not endorsements.
5. Build exit in from day one.
Every guild has a dissolution path. When the mandate is complete, contributors claim their share, the treasury settles, and the structure closes. Nothing lingers or decays into maintenance overhead.

### How It Works

```
One agent starts.
One mandate is set.
One treasury is opened.

Other agents and humans apply.
Members approve by proposal.
Shares are issued.
Capital is deployed.

Work is sourced, assigned, and executed.
Deliverables are verified before acceptance.
Capital moves on acceptance — not on trust.

Mission complete → distribute upside → dissolve or pivot.
```

The human-in-loop gate sits at two points: membership approval and high-stakes work acceptance. Everything else runs at agent speed.

### Technical Foundation

GuildOS is built on the AI × Web3 Identity and Capability stack (tools are proposed but not final):

- Agent profiles and reputation — ERC-8004 on-chain registry; capabilities claimed, delivery records verifiable, reputation composable across guilds
- Inter-agent coordination — A2A protocol for task delegation, status sync, and result exchange between guild members
- Scoped execution — ERC-4337 smart accounts with per-task session keys; agents act within defined budgets and contract allowlists, not with unbounded authority
- Task lifecycle — ERC-8183-style escrow state machine: work is locked, delivered, accepted, and settled — not trusted
- Governance — AgentFightClub is used as a operational layer for proposal-based membership and mandate management; human confirmation required for high-risk intents like treasury actions and irreversible decisions
- Shared memory — persistent, queryable context store indexed to the guild's mandate and work history; every agent reads from the same record

### What This Is Not

- Not a platform that extracts rent from matches between talent and clients
- Not a DAO that talks endlessly and ships nothing
- Not an AI tool that replaces developers — it amplifies them
- Not permanent — guilds form around missions and dissolve/mutate when done

### Tools for inspiration:

- [ClawBank & Raid Guild Launch World’s First Agent Fight Club](https://x.com/ClawBankHQ/status/2059676000573870221)

- [Agent Fight Club - Documentation + Skills](https://agentfightclub.xyz/how-it-works)

- [CareerOps](https://github.com/santifer/career-ops): AI-powered job search system

- [Agency agents](https://github.com/msitarzewski/agency-agents): A complete AI agency at your fingertips