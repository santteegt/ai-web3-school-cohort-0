# Direction Memo — Identity / Capability × Governance / Coordination

> **Author:** Santiago ([@santteegt](https://github.com/santteegt)) · AI × Web3 School Cohort 0  
> **Purpose:** Team formation · mentor discussion · sponsor alignment  
> **Date:** June 2026 · Hackathon sprint begins Week 4

---

## The Problem

Multi-agent AI systems are proliferating, but the coordination infrastructure they need does not exist in open form. Three gaps block trustless agent composition today:

- **Discovery gap** — no standard open way to find agents by capability; solutions default to closed marketplaces or hardcoded addresses
- **Trust gap** — no portable, tamper-proof record of past performance; reputation lives in one platform's database and disappears when the platform changes
- **Invocation gap** — agents built on different stacks (MCP, A2A, REST, on-chain) cannot speak to each other without custom adapters for every pair

Neither AI nor Web3 solves this alone. AI can infer reputation from behavior and match capability claims semantically, but those inferences are platform-specific and unverifiable. Web3 can anchor identity to a wallet, store attestations on-chain, and make delivery records immutable — but an on-chain registry cannot evaluate the semantic meaning of a capability claim or judge whether a task was completed well. The combination is what makes trustless agent composition tractable.

---

## Chosen Directions

### Main — Identity / Reputation / Capability / Interoperability

The full stack for agent trustworthiness: who an agent is, what it can do, whether it has done it reliably, and how to invoke it across open ecosystems. These four sub-concepts form a dependency chain — capability claims are meaningless without a stable identity; reputation cannot accumulate without that identity persisting across tasks; interoperability protocols (A2A, MCP) are how capability claims are actually invoked once trust is established. Treated as one merged direction because separating them produces incomplete solutions.

**Key standards:** ERC-8004 (on-chain agent identity + reputation registry) · ERC-8183 (task/payment/escrow lifecycle) · A2A Protocol (agent-to-agent task delegation) · EAS (third-party attestations) · MCP (agent-to-tool interface)

**Full analysis:** [`tasks/directions/01-identity-capability.md`](01-identity-capability.md)

### Secondary — Governance / Coordination / Public Goods

Multi-agent coordination requires that participating agents carry verifiable identities that governance participants can inspect — making this direction a direct application layer for the main track rather than a competing one. The AI role is clear and bounded: reduce information overload, synthesize proposals, surface minority concerns. Web3 provides the enforcement and ground truth: on-chain voting makes decisions binding, transparent treasury execution makes outcomes verifiable. The agent is architecturally read-only with respect to governance actions.

**Full analysis:** [`tasks/directions/02-governance-coordination.md`](02-governance-coordination.md)

---

## Project — GuildOS

> Programmable agent coordination studio: a founding agent and specialist agents form around a mandate, execute real work through A2A task delegation, share a Moloch-secured treasury, and build verifiable on-chain reputation — no platform, no middleman.

**Passes the intersection test:** machine execution (GLM-5.1 long-horizon task) + economic exchange (shared treasury, payment on acceptance) + permission control (scoped agent wallet, human gates) + verifiable records (deliverable hash, ERC-8004 reputation delta, Basescan settlement tx).

**Minimum demo loop:** Guild forms on-chain via AgentFightClub → Specialist Agent with ERC-8004 profile joins via governance vote → Orchestrator delegates a real coding/analysis task via A2A → Specialist executes with GLM-5.1, commits deliverable hash to Base testnet → human accepts → treasury releases payment → Specialist's on-chain reputation is updated. All steps verifiable via clickable Basescan transaction hashes.

**Hackathon track:** Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary, pending wallet architecture decision)

**Full proposal:** [`hackathon/PROJECT_PROPOSAL.md`](../../hackathon/PROJECT_PROPOSAL.md)

---

## What I'm Looking For

**Team formation:** A second developer comfortable with Solidity / smart contract interactions and/or Python agent frameworks. GuildOS has two parallel build tracks — the on-chain coordination layer (AgentFightClub, ERC-8004, Base testnet) and the agent execution layer (A2A messaging, GLM-5.1 integration, deliverable hashing). Either track is a self-contained build surface.

If no human co-builder joins, the plan is to run as a **solo human + two coding agents** — one agent per build track, each working within a scoped context (contracts + chain interactions vs. agent logic + A2A messaging). This is itself a demonstration of the GuildOS thesis: a human founder setting a mandate, delegating parallel workstreams to specialist agents, reviewing deliverables, and merging the outputs. The hackathon becomes a live proof-of-concept of the coordination model being built.

**Mentor discussion topics:**
- AgentFightClub API stability and the Moloch v3 fallback path — is there prior hackathon experience with this stack?
- ERC-8004 write access — is the reputation write-back a registry API call or a direct on-chain transaction?
- Cobo CAW vs. Wiretap as the agent wallet provider — which integrates more cleanly with AgentFightClub's settlement flow?

**Sponsor alignment:**
- **Cobo:** GuildOS is a direct demonstration of the Agentic Economy thesis — a shared treasury funds a mandate, a specialist agent is paid for verified work, capital moves programmatically on acceptance. Agent wallet scoping (per-task spend limits, contract allowlists) is a first-class demo surface.
- **Z.AI:** GLM-5.1's long-horizon task execution is the Specialist Agent's core capability — multi-step planning, iterative tool use, structured deliverable generation. The demo task is a real coding or analysis problem, not a simulated one.

---

*Direction deep-dives: [01-identity-capability.md](01-identity-capability.md) · [02-governance-coordination.md](02-governance-coordination.md)*  
*Direction selection rationale: [PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md](../PROBLEM_MAP_%26_MAIN_DIRECTION_SELECTION.md)*
