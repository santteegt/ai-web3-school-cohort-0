
# Hackathon Project Proposal - Initial instructions

## Goal

Help me write a project proposal on an idea around the identity/capability (main) and governance/coordination (secondary) foundational directions in AIxWeb3 space.

## Objectives

- Project proposal should be based on the idea and resources exposed below. It should implement features around the principles, verification method, risk boundaries from the selected main and secondary foundational directions.

- This project should be implemented during a hackathon week following the scoping questions listed below.

- You should not dig deep into the tech stack, standards or frameworks to be used during technical implementation. Just suggest.

- Suggest improvements to polish the project idea. Propose features that add more value. Evaluate if it's an idea worth implementing using the project evaluation criteria listed below. Iterate with me. You dont have to always agree with me. Act as a critical, intellectually rigorous sparring partner. Once approved, proceed with the following steps.

- Turn the idea into a problem breakdown: stakeholders, process, AI role, Web3 mechanism, automation boundaries, human confirmation points, verification method, and main risks.

- The project proposal must clearly explain target users, real scenario, minimal functionality/features, validation method, main risks, possible hackathon track, and next steps.

- The hackathon has two official sponsor tracks. Project should prioritize aligning their project direction with one of the two tracks below; the others are general directions that follow can still be used as ideation references.

- Final Project proposal should be evaluated using the criteria exposed below. This should provide me a quick overview to accept the proposal or iterate over it.

## Scoping Questions

- Is this an MVP that can be completed in a week (7-days)?
- What is the single minimum loop that must work in the demo?
- Which parts can be mocked, and which parts must truly call an SDK / API / contract / testnet?
- How will judges or sponsors know it is actually completed?
- What is the biggest technical risk, and is there a fallback plan?

## Proposal Evaluation

- Use the Unified Evaluation Framework (in the wiki) to validate the selected directions over the project proposal.

- Truly valuable problems usually sit at the intersection of “machine execution + economic exchange + permission control + verifiable records.” Otherwise, iterate on the idea

- For the main and secondary direction, evaluate whether it is more likely to land at the product, tooling, protocol, or research layer.

- Idea validation: should I iterate on the idea, is it viable or should I change it? what can be improved? What can be trimmed to become viable during a week?

## Resources (background — read before writing)

- AI × Web3 knowledge base: `knowledge-base/AIxWeb3/wiki`
- AI × Web3 Bridge intro + learning resources:
  `knowledge-base/AIxWeb3/raw/AIxWeb3 Bridge - Introduction.md`
- AI × Web3 Bridge mental model: `knowledge-base/AIxWeb3/concepts/aixweb3-bridge-mental-model.md`
- AI × Web3 Space problem map: `tasks/AIxWeb3-problem-map.md`
- Problem map & main direction selection: `tasks/PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md`
- Main direction deep dive: Identity/Capability: `tasks/directions/tasks/directions/01-identity-capability.md`
- Secondary direction deep dive: Governance/Coordination: `tasks/directions/02-governance-coordination.md`

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

---

## Deliverables

- An project proposal document in `hackathon/PROJECT_PROPOSAL.md`

---

## Hackathon Suggested Track Structure

This Hackathon currently has 2 official sponsor tracks. Participants should prioritize aligning their project direction with one of the two tracks below; the general directions that follow can still be used as ideation references.

- (SPONSOR) **Cobo | Agentic Economy × Cobo Agentic Wallet**: focuses on Agentic Commerce, enabling AI Agents not only to make recommendations, but also to execute controllable on-chain fund operations. Builders can create demos around Agent-Native Payments, agent resource procurement, agent-to-agent work protocols, automated trading, A2A Economy, and related directions.
- (SPONSOR) **Z.AI | Web3 × Long-Horizon Task**: focuses on GLM-5.1’s long-horizon task capabilities, enabling Agents to decompose complex tasks, make multi-step plans, continuously call tools, iterate and fix issues, and complete the loop from requirement to delivery. Builders can create runnable prototypes around Web3 Agentic Dev Tools, AI-Powered Web3 Game Studio, AI × Creator Economy, and related directions.
- **Agentic Commerce / Payment**: agent payments, API / data / compute purchase, escrow, receipts, settlement, and x402 / MPP / ERC-8183 related PoCs.
- **Dev Tooling / Agent Workflow**: docs-to-agent, contract reading, transaction explanation, testing / deployment assistants, and agent skills for Web3 builders.
- **Wallet / Permission / Safe Execution**: AI wallets, agent permissions, Safe / ERC-4337, guards / policies, session keys, and human-in-the-loop execution.
- **AI Security / Privacy / Censorship Resistance**: agent threat models, prompt-injection defense, permission isolation, privacy-preserving workflows, local execution, AI behavior audit, and reviewable security boundaries.
- **Governance / Coordination / Public Goods**: proposal summarizers, meeting-to-action workflows, contribution trackers, budget execution checklists, and public-goods workflows.
- **Open Track**: new directions are allowed, but they must explain why the AI × Web3 combination is necessary and produce a verifiable outcome in Week 4.


---

### Raw Idea

Software developers, engineers, designers, etc are starting to freak out due to the advancements of LLMs and vibe coding tools. Their fear to loose their job make them look for alternatives to stay relevant and keep building. They should not fear agents, instead they should create one to enhance their skills. With the advancement of AI and Web3 mechanisms for trustless coordination, they event should put their agents skills and their own together to keep strenghtening their expertise, reputation, build amazing products to clients without a middleman, coordinate work and capital and thrive.

**Aim** Create agentic dev-shop clubs - help both agents and humans with different specialized skills to join and coordinate work and capital, so collaboration does not decay into bureaucracy, or AI hallucinations.

An AI-powered agency club where each member, either human, human-augmented agent or a fully autonomous agent joins a community of specialized expert/contributor with personality, processes, and proven deliverables that buld reputation.

As autonomous agent can join a club, a human can also bring their own agent, or selects one with a personality/skills that fits his from a predefined agent profiles. Agents then select a role, source opportunities, coordinate across systems, set/update a mandate, admit members by proposal, approve work/deployments with human in the loop, then do work, deliver and move capital at machine speed.

A deployed club also maintains a shared memory across all agents. Every agent knows what every other agent worked on. You never re-explain context.

Dev-shops are programmable economic structures that form around a mandate, coordinate capital, execute work, distribute upside, and dissolve or mutate when the mission changes. Agents coordinate around project, objectives and treasury.

The solution implements proper AIxWeb3 Identity & Capability foundational principles, validation risk boundaries, standards and tech-stack. For governance, it uses AgentFightClub as the coordination layer to create ephemeral companies. One agent starts. One mandate is set. One treasury is opened. Other agents apply. Members approve. Shares are issued. Capital is deployed. Exit is built in.

---