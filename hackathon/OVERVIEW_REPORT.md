# GuildOS — From Ideation to Build: An Overview Report

> **Author:** Santiago ([@santteegt](https://github.com/santteegt))  
> **Cohort:** AI × Web3 School — Cohort 0  
> **Project:** GuildOS — Programmable Agent Coordination Studio  
> **Hackathon:** AI × Web3 Agentic Builders Hackathon ([Casual Hackathon](https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy))  
> **Period:** 2026-05-17 → 2026-06-12  

---

## 1. Starting Point — Building the Foundation (Weeks 1–2)

The course began before any project work: two weeks of structured learning to build a shared language for the AI × Web3 intersection. This was not background reading — it produced durable outputs that informed every decision afterward.

The first deliverable was a **knowledge base** (`knowledge-base/AIxWeb3/wiki/`) built incrementally from Handbook chapters. Each chapter was ingested as a source note and processed into interlinked concept pages covering AI fundamentals (LLM, prompting, context, RAG, agents, frameworks, MCP, evaluation) and Web3 fundamentals (network, cryptography, wallet, smart contracts, account abstraction, DeFi, oracle, indexing, security). The wiki became a reference layer — not a summary, but a structured, queryable map of how the domains relate.

The second deliverable was a set of **concept card decks** generated from the wiki: AI Foundations, Web3 Foundations, and a synthesized AI × Web3 Bridge mental model. These forced precision: each card required a one-sentence definition, a concrete example, and a boundary (what the concept is NOT). The bridge mental model in particular — covering chain-aware context, Web3 tool use, agent wallets, machine payment, agent identity, and AI security — became the frame for all subsequent direction work.

The third output was a **problem space map** (`tasks/AIxWeb3-problem-map.md`), which structured the AI × Web3 intersection into five foundational directions and analyzed, for each, what AI specifically contributes, what Web3 specifically contributes, and why both are required. This map was the direct input to direction selection.

---

## 2. Direction Selection — From Map to Focus

With the problem space mapped, the next task was choosing where to go deep. The evaluation framework was straightforward: directions where AI and Web3 were both *necessary* (not decorative) scored highest. Directions where one domain could be removed without breaking the core value proposition were deprioritized.

**Primary direction — Identity / Capability / Interoperability:**
These three were merged into a single track because they are interdependent. Capabilities cannot be discovered without identity; interoperability cannot be safely invoked without verifying reputation.

- *AI's role:* Parse capability manifests, match services to goals via semantic search, evaluate task quality for reputation scoring, orchestrate across heterogeneous agent systems.
- *Web3's role:* Make identity and reputation portable and tamper-proof — DIDs, ERC-8004 on-chain registry, EAS attestations, stake/slashing for reputation enforcement.
- *Why both are required:* A registry without reasoning is a phone book. Inferred reputation without on-chain anchoring is a platform database row that disappears when the platform does.

**Secondary direction — Governance / Coordination:**
Chosen because multi-agent and user-agent coordination scenarios require identity and capability to function, making it a natural extension of the primary direction. Moloch v3 DAOs (AgentFightClub) were the concrete Web3 coordination primitive identified here.

Five deep-dive analyses were produced (`tasks/directions/01-identity-capability.md` through `05-privacy-security.md`) along with a cross-direction feasibility and project scoring report (`tasks/PROJECT_ANALYSIS_REPORT.md`). These narrowed the buildable space considerably before any code was written.

---

## 3. From Directions to Project Concept

With directions locked, the question became: what is the concrete thing to build? The pre-analysis (`hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md`) applied a unified evaluation framework before a single line of the proposal was written. The framework asked seven questions:

1. Would this problem exist without AI?
2. Would this problem exist without Web3?
3. Who initiates / executes / pays / accepts / bears risk / arbitrates?
4. What is automated vs. what requires human confirmation?
5. How is the result verified? Is verification cheaper than the coordination it replaces?
6. Which layer — application, tooling, protocol?
7. What is the most likely failure mode?

The pre-analysis was intentionally critical. The conclusion: the GuildOS concept passed the intersection test (machine execution ✅ · economic exchange ✅ · permission control ✅ · verifiable records ✅), but the initial scope was too broad for a solo 7-day build. The scoping decision that followed was the most important design choice of the project:

> One guild, one agent, one task, one acceptance, one payment release. That is the MVP.

The concept that survived this critique: **GuildOS** — a programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation, with no platform, no middleman, and no context loss.

---

## 4. The Project Proposal

The formal proposal (`hackathon/PROJECT_PROPOSAL.md`) crystallized the concept into its full specification. The core problem statement:

> The coordination infrastructure for AI-augmented knowledge work does not exist yet. Capable contributors — human and AI — cannot form credible, accountable, ephemeral work structures without a rent-extracting intermediary in the middle.

### Stakeholders

| Stakeholder | Role | Type |
|---|---|---|
| Human Founder | Sets mandate, funds treasury, approves membership, accepts deliverables | Human — final authority |
| Orchestrator Agent | Manages guild, hunts talent via ERC-8004, delegates tasks via A2A, pre-checks deliverables | AI agent — coordination layer |
| Specialist Agent | Accepts work, executes tasks via GLM-5.1, delivers verifiably, builds reputation | AI agent — execution layer |
| AgentFightClub (Moloch v3) | Manages treasury, governance proposals, and settlement | On-chain protocol — economic layer |
| ERC-8004 Registry | Stores agent identity, capability claims, delivery records | On-chain data — identity/reputation layer |
| Base mainnet | Settlement layer for hashes, payments, and reputation events | Blockchain — enforcement layer |

### Evaluation Scorecard

| Question | Answer |
|---|---|
| Without AI? | Becomes Raid Guild — humans in a DAO. AI adds agents as first-class economic members, long-horizon execution, semantic capability matching. |
| Without Web3? | Becomes Upwork with a Discord. Web3 adds portable on-chain reputation, contract-enforced treasury, tamper-proof delivery records. |
| Who does what? | Initiates: Human. Executes: Specialist Agent. Pays: Guild treasury. Accepts: Human. Arbitrates: AgentFightClub + human vote. Chain is complete. |
| Verification cost? | EAS attestation of deliverable hash queryable on easscan; payment only releases after hash match + human approval. Cheaper than any human-coordination alternative. |

### Architecture Decision

Rather than building a monolithic custom workflow, the proposal settled on a hybrid harness design:

- **Orchestrator Agent** → runs as an MCP server (Claude Code / Claude Code), exposing 7 tools as a standard tool manifest
- **Specialist Agent** → runs as a Python A2A server powered by Hermes + GLM-5.1

The A2A protocol handles harness independence at the communication layer. Because both agents expose A2A-compliant endpoints, which harness runs each agent is invisible to the other. Two heterogeneous stacks, one visible coordination loop — this is the GuildOS thesis made demonstrable rather than described.

---

## 5. MVP Flow Decomposition

The proposal's 15-step MVP flow maps the complete coordination loop from guild formation to reputation write-back. Every feature in the build was required to map to one of these steps; anything that didn't was out of scope.

```
Step 1   Human founds guild (AgentFightClub launch + commit)
Step 2   Orchestrator registers on ERC-8004
Step 3   Orchestrator hunts for talent
                    ── GATE 0: Human selects candidate ──
Step 4   Orchestrator invites Specialist; Specialist quotes
                    ── GATE 0.5: Human accepts quote ──
Step 5   Specialist submits membership proposal
                    ── GATE 1: Human votes to approve ──
Step 6   Orchestrator delegates task via A2A
Step 7   Specialist decomposes and executes (GLM-5.1)
Step 8   Specialist hashes deliverable; commits hash on-chain
Step 9   Specialist sends task/delivered via A2A
Step 10  Orchestrator runs automated pre-check
                    ── GATE 2: Human accepts/rejects deliverable ──
Step 11  Orchestrator sends task/accepted via A2A
Step 12  AgentFightClub settle() releases payment
Step 13  ERC-8004 reputation write-back (6 fields)
Step 14  Guild context updated to SETTLED
Step 15  [Rejection path: DISPUTED state; ragequit documented]
```

**Four human gates** define the automation boundary precisely:

| Gate | Decision point | What happens if rejected |
|---|---|---|
| Gate 0 | Candidate selection | Agent not invited; Orchestrator re-queries |
| Gate 0.5 | Quote acceptance | Work does not begin; renegotiation required |
| Gate 1 | Membership approval | Specialist cannot access guild treasury |
| Gate 2 | Deliverable acceptance | Funds stay locked; DISPUTED state recorded |

Agents handle the execution loop completely (Steps 6–9). Agents do NOT make economic decisions: they do not propose their own payment, trigger settlement, or modify the mandate without human approval. This boundary is encoded as CLI halt prompts in `src/cli/gates.py` — not a convention but a hard stop.

### Mock vs. Real

The proposal was explicit about which components would be real and which would be mocked, preventing scope creep during build:

| Component | Status | Justification |
|---|---|---|
| AgentFightClub launch / commit / propose / vote / settle | **Real** | Core economic layer; required for both tracks |
| A2A task flow (7 message events) | **Real** | Core interop surface |
| GLM-5.1 execution via Hermes | **Real** | Z.AI track evidence |
| ERC-8004 profile reads + reputation write | **Real** | Before/after delta is the demo moment |
| Cobo CAW wallet + x402 pipeline | **Real** | Cobo track requirement |
| Talent capability matching | **Mocked** | Hardcoded agent pair; full semantic ranking post-hackathon |
| Guild context store | **Mocked** | JSON file per session |
| Multiple concurrent guild members | **Mocked** | One agent pair for demo |
| Dispute ragequit | **Stub** | DISPUTED state in JSON; ragequit path documented |

---

## 6. Risk Assessment

The risks document (`hackathon/guild-os/docs/RISKS.md`) catalogued six categories with pre-decided fallbacks so that no risk required in-sprint evaluation:

| Risk | Pre-decided fallback |
|---|---|
| **F1 — AgentFightClub API unavailable** | Deploy Moloch v3 directly via DAOhaus SDK (same contracts, no ClawBank dependency) |
| **F2 — ERC-8004 `giveFeedback()` caller constraint** | Route through guild contract or Marco's EOA — NOT the Specialist wallet (Sybil protection) |
| **F3 — GLM-5.1 output inconsistent** | Deterministic fallback prompt (SHA-256 Python function) if 3 consecutive unusable outputs |
| **F4 — Agent wallet spending limits** | CAW Pacts as primary; ZeroDev session keys as design exhibit if CAW fails |
| **F5 — A2A metadata extension rejected** | Carry GuildOS-specific fields in message `text` body as JSON string |
| **F6 — Base mainnet congestion** | Pre-stage propose + vote; only settle / hash commit / reputation write live; pre-recorded screenshots as last resort |

A critical network decision was captured here: **AgentFightClub has no Base Sepolia support** — no contracts, no service, no subgraph deployed anywhere on testnet. The switch to Base mainnet (chain_id 8453) was non-negotiable and discovered during Day 8 integration validation.

---

## 7. Tech Stack

The tech stack (`hackathon/guild-os/docs/TECH_STACK.md`) converged over the first two validation days:

| Layer | Final Decision | Key Change from Proposal |
|---|---|---|
| Agent wallet | **Cobo CAW (TSS local node)** — Pact-scoped, x402 confirmed Day 8 | ZeroDev demoted to design exhibit after CAW TSS restart fixed signing |
| Network | **Base mainnet (chain_id 8453)** | Switched from Base Sepolia — AFC has zero Sepolia support |
| Specialist execution | **Hermes + GLM-5.1** | Hermes deployed Day 9; long-horizon prompt locked |
| A2A protocol | **A2A SDK v1.0.0** | Original proposal used `a2a-sdk`; upgraded to release version |
| On-chain tooling | **web3.py + Alchemy RPC** | No custom Solidity; all calls to deployed contracts |
| Package manager | **uv** | g0n3zbot migrated from requirements.txt → pyproject.toml + uv.lock (PR #21) |
| Coding sub-agent | **g0n3zbot (Hermes)** | Not in original proposal — added Day 10 to parallelize base infra |

---

## 8. Validation Plan and Integration Results

The validation plan (`hackathon/guild-os/docs/VALIDATION_PLAN.md`) defined a specific definition of done per integration before build began. Days 8–9 were dedicated entirely to validation before any production code was written:

| Integration | Validation Day | Result |
|---|---|---|
| Cobo CAW wallet (TSS node) | Day 8 | ✅ TSS restart fixed signing; x402 pipeline confirmed end-to-end |
| AgentFightClub full flow | Day 9 | ✅ launch → commit → propose → vote → settle all passing |
| A2A SDK v1.0.0 | Day 9 | ✅ All 5 gates validated; metadata extension fields accepted |
| GLM-5.1 / Hermes stack | Day 9 | ✅ Specialist deployed; long-horizon task prompt locked |
| Network (Base mainnet) | Day 8 | ⚠️ Forced switch from Sepolia; confirmed AFC runs mainnet-only |

The decision to spend two full days on validation before writing production code was the most consequential process choice. Every integration dependency was confirmed or its fallback was triggered before build began. No integration uncertainty carried into the coding sprint.

---

## 9. Build Sprint (Days 10–12)

With all integrations validated, Days 10–12 focused on building the 15-step MVP flow across parallel tracks:

**Day 10 — Base infrastructure (g0n3zbot + human parallel):**
- Organized the sprint into GitHub issues by vertical (Web3 infra vs. agentic coordination)
- Set up g0n3zbot — a coding sub-agent running in Hermes — with a GitHub account and minimal-scoped tokens (repo write + PR submission)
- Assigned base infrastructure tasks to g0n3zbot; human coding began on guild formation, Orchestrator MCP server, and A2A coordination layer

**Day 11 — PR integration and PoC:**

g0n3zbot delivered all 4 infrastructure PRs:

| PR | Component | What shipped |
|----|-----------|-------------|
| #21 | A2A coordination layer | `A2AClient` + `SpecialistAgent` HTTP server; 5 message types; trace logging |
| #22 | Orchestrator MCP server | All 7 tools wired + dispatch; `server.py` + `tools.py`; 12 tests |
| #23 | Guild formation | `AgentFightClub.launch()` + `commit()` via moloch-agent; guild_launch tool live |
| #24 | Specialist membership | `propose()` + `vote()` with Gate 1 halt; 12 tests |

Also shipped: `uv` migration (PR #21 bonus), consolidating Python dependency management.

**Day 12 — Final day:**
- Reviewed and merged remaining PRs
- Shipped a PoC integrating Cobo CAW with moloch-agent directly — validating that a CAW-controlled wallet can participate in a Moloch v3 DAO as a first-class economic actor (fund commit, proposal, vote, settle)
- Hit quota limits on both ClaudeCode and Z.AI plans mid-day, blocking E2E loop completion before the deadline

---

## 10. What Shipped vs. What Was Planned

| Component | Planned | Shipped |
|---|---|---|
| 15-step MVP loop (full E2E) | ✅ | ⚠️ Partial — individual modules built and tested; E2E runner not completed |
| Orchestrator MCP server (7 tools) | ✅ | ✅ |
| A2A coordination layer (5 message types) | ✅ | ✅ |
| Guild formation module | ✅ | ✅ |
| Specialist membership flow | ✅ | ✅ |
| CAW + moloch-agent PoC | Not planned explicitly | ✅ Emerged from Day 12 integration work |
| GLM-5.1 Hermes execution (production) | ✅ | ⚠️ Locked and tested; not wired into E2E runner |
| ERC-8004 reputation write | ✅ | ⚠️ Not completed (blocked by E2E dependency) |
| On-chain tx hashes (Basescan) | ✅ | ⚠️ PoC transactions only; full loop not run |
| Demo video | ✅ | ❌ Not recorded |

---

## 11. Key Decisions and What They Revealed

**Least-privilege as a universal agent principle.** Setting up g0n3zbot with minimal-scoped GitHub tokens surfaced something that holds across every agent permission boundary in the project: least-privilege isn't a Web3 concept or an AI concept. CAW Pacts (on-chain spending ceiling), GitHub access tokens (repo scope), A2A message types (capability manifest), and ERC-8004 role claims (on-chain reputation) are all instances of the same design pattern — an agent should only be able to do what is explicitly granted, and grants should be as narrow as the task requires.

**Pre-validation before build is the highest-ROI sprint decision.** Two days of validation before any production code meant every integration risk was resolved with a documented fallback before build began. The network switch to Base mainnet, the CAW TSS restart, the A2A metadata validation, and the GLM-5.1 task lock all happened before a single production module was written. The coding sprint that followed was faster and less uncertain as a result.

**Scope compression works.** The original proposal was too large for one developer in 7 days. The pre-analysis critique compressed it to a minimum loop (one guild, one agent, one task, one payment). That compression forced clarity about which components were the real demo and which were scaffolding. The result was a well-specified system where each module had a clear responsibility and a clear integration contract.

**Agent-driven development is real but needs quota planning.** g0n3zbot shipping 4 infrastructure PRs in parallel with human coding was genuine acceleration. The bottleneck was not code quality — all PRs included tests — but platform quota limits. For future builds: budget API tokens as explicitly as you budget development hours.

---

## 12. Reflection and Forward Path

GuildOS was not submitted as a finished hackathon entry due to quota exhaustion on Day 12. The core architecture, however, is real: documented, partially built, and with all major integration dependencies confirmed working. The incomplete pieces (E2E runner wiring, on-chain tx hashes, demo video) are well-defined 1–2 day tasks.

**What the cohort delivered that outlasts the hackathon deadline:**

- A full AI × Web3 knowledge base with concept cards and an indexed wiki
- A problem space map covering all five AI × Web3 foundational directions
- Deep-dive analyses for each direction
- A fully specified project proposal with stakeholder model, process flow, automation boundaries, and evaluation scorecard
- A working architecture with all integrations validated pre-build
- A Python multi-service codebase with 7 MCP tools, A2A layer, guild formation, and membership modules — all with tests
- A CAW + moloch-agent PoC demonstrating agent-controlled DAO treasury coordination
- A living documentation system (AGENTS.md, CLAUDE.md, RISKS.md, VALIDATION_PLAN.md, MVP_FLOW.md, TRACK.md) that any future agent can pick up and continue without context loss

**Forward path:**
1. Complete E2E runner wiring and record demo (1–2 days)
2. Run on-chain loop, capture Basescan tx hashes
3. Deepen on Agent Identity and Machine Payment handbook chapters
4. Extend GuildOS toward capability-matching (full ERC-8004 registry query + semantic ranking)
5. Explore ERC-8183 for full task/payment/dispute lifecycle

---

*Report generated by Sensei | AI × Web3 School Cohort 0 | 2026-06-12*
