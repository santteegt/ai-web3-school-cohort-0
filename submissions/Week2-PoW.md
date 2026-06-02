# Week 2 Proof-of-Work Pack

> **AI × Web3 School — Cohort 0**
> [GitHub Repo](https://github.com/santteegt/ai-web3-school-cohort-0)
> Covering: Days 8–14 (May 27 – June 2, 2026)
> Track: Direction Deep-Dive Pack + Initial Project Proposal

---

## 1. AI × Web3 Problem Space Map

**Report:** [AIxWeb3-problem-map.md](/tasks/AIxWeb3-problem-map.md) | **HTML diagram:** [AIxWeb3-problem-map.html](/tasks/AIxWeb3-problem-map.html)

The AI × Web3 problem space was mapped across five foundational directions, each representing a distinct coordination failure that requires both AI reasoning and Web3 enforcement to address. The five directions are: **Identity / Reputation / Capability / Interoperability** — the infrastructure layer for discovering and trusting agents across open ecosystems; **Governance / Coordination / Public Goods** — reducing information overload in DAO decision-making while keeping governance binding and transparent; **Payment / Commerce / Settlement** — enabling autonomous machine-to-machine economic exchange with tamper-proof receipts; **Wallet / Permission / Safe Execution** — scoping agent authority so autonomous agents cannot exceed human-authorized boundaries; and **Privacy / Security / Sovereignty** — protecting agent workflows from adversarial inputs and preserving user control over inference and data.

**Each direction was evaluated against five criteria**: structural demand, verifiability, minimal entry point, risk boundaries, and follow-through potential.

A key insight from the mapping exercise is that these five directions are not independent. Identity and reputation are prerequisites for every other direction — payment flows require knowing which agent to pay, governance coordination requires knowing which agents to trust as participants, and safe execution requires knowing what a given agent is authorized to do. The mapping also surfaces the core AI × Web3 thesis: in each direction, AI alone produces inferences that are platform-locked and unverifiable, while Web3 alone produces tamper-proof records that no one can query intelligently. **The combination — AI for semantics and reasoning, Web3 for portable enforcement** — is what makes each direction tractable. The full problem map is available in the HTML diagram and summarized in the report file linked above.

---

## 2. Direction Selection

**Selection document:** [PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md](/tasks/PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md)

The **main direction** selected is **Identity / Reputation / Capability / Interoperability**, treated as a single merged track rather than two separate directions because they form a tight dependency chain: capabilities cannot be discovered without a stable identity to attach them to, and reputation cannot accumulate without that same identity persisting across tasks. *Interoperability protocols (MCP, A2A) are how capability claims are actually invoked once identity and trust are established*. This direction was chosen for its infrastructure-level structural demand — every multi-agent system, regardless of framework or chain, faces the same underlying question of how to find, evaluate, and invoke third-party agents trustlessly — and for its clear minimal entry point: a working prototype can query an open registry, perform semantic capability matching, and return a ranked trust-scored shortlist without deploying new contracts or handling private keys. Among all five directions, it also has the strongest follow-through path into a Hackathon build and longer-term research contributions.

The **secondary direction** is **Governance / Coordination / Public Goods**, selected because coordination is a natural extension of the identity and reputation infrastructure: any multi-agent governance scenario requires agents with verifiable identities that community participants can inspect before accepting their outputs. This creates a reinforcing relationship rather than a competing one — the main direction builds the identity layer, and the secondary direction demonstrates a high-value use case for it. Governance was also chosen because it has the lowest barrier to a working prototype (Snapshot GraphQL requires no authentication and no contract deployment) and the most self-evident human/AI division of labor: AI reduces information overload, Web3 makes decisions binding and transparent, and the agent is architecturally read-only with respect to governance actions.

---

## 3. Problem Breakdown

**Reference:** [AIxWeb3_WORKFLOW.md](/tasks/AIxWeb3_WORKFLOW.md) | **Diagram (SVG):** [agentic-commerce-workflow.svg](/tasks/agentic-commerce-workflow.svg)

Mapping a Minimal AI × Web3 Agentic Commerce Workflow helped me visualize a canonical multi-agent commerce scenario with four stakeholders: a **Human Operator** who issues a high-level intent and holds final approval authority; a **Requester Agent** that orchestrates the workflow end-to-end; a **Data Provider Agent** acting as an autonomous external service; and the **On-chain / L2 layer** that enforces payment, settlement, and intent execution.

The process runs in nine sequential steps: intent issuance → task receipt and agent discovery → negotiation → micro-payment and receipt verification → data delivery and context building → intent proposal → human approval → on-chain execution → state verification.

**AI drives steps 1b–6 and 7b–8**: parsing natural-language intent, querying service registries, negotiating terms, signing the micro-payment, ingesting delivered data into a chain-aware reasoning context, and proposing the final on-chain action.

On the other hand, **Web3 provides the enforcement layer** throughout: an ERC-4337 scoped wallet with per-transaction spend limits and contract allowlists prevents the agent from exceeding its authority; the on-chain payment receipt is cryptographic proof of the agent-to-agent exchange; and the final intent is settled on an L2 with an immutable transaction record.

The workflow enforces **exactly one human confirmation gate**: Step 7, where the Requester Agent presents the human with a dry-run simulation of the proposed on-chain intent (expected state changes, gas cost, token movements) before any irreversible transaction is signed. This gate is a hard code constraint, not a prompt instruction — the agent cannot bypass it.

**Verification** is distributed across three layers: simulation before signing, on-chain receipt confirmation after execution, and a post-execution state re-read via RPC to confirm actual outcome matches simulated outcome.

The **five main risks** are: *negotiation integrity* (a malicious Data Provider presenting false capability schemas), *payment exploits* (overly broad agent wallet authority enabling fund drain), *prompt injection* via the delivered dataset entering the agent's reasoning context, irreversible intent execution from *hallucinated or stale inputs*, and *MEV/frontrunning* of the submitted transaction in the public mempool. IN the report, each risk has a defined mitigation — schema validation, wallet scope limits, input sanitization, the human gate + simulation, and private mempool routing respectively.

---

## 4. Initial Project Proposal — GuildOS

**Proposal document:** [hackathon/PROJECT_PROPOSAL.md](/hackathon/PROJECT_PROPOSAL.md) | **Pre-analysis:** [hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md](/hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md)

**GuildOS** is a programmable coordination studio where a founding agent and one or more specialist agents form around a mandate, execute real work through A2A task delegation, and build verifiable on-chain reputation — with a human-in-loop at two explicit gates and no platform extracting rent in the middle. The core problem it addresses is the absence of coordination infrastructure for AI-augmented knowledge work: **AI agents can now execute real development tasks autonomously, but without economic structure, verifiable identity, and scoped authority, they hallucinate, overreach, and leave no auditable trail**. GuildOS answers this by combining ERC-8004 agent identity and reputation, A2A protocol for structured task delegation, AgentFightClub (Moloch v3) for shared treasury and governance, and GLM-5.1 long-horizon task execution for the Specialist Agent. The result is a coordination loop that is entirely automated except at two human gates: membership approval (reviewing the Specialist's ERC-8004 profile before accepting them into the guild) and deliverable acceptance (reviewing the completed work before releasing payment). The hackathon MVP targets the Cobo | Agentic Economy × Cobo Agentic Wallet track as primary and Z.AI | Web3 × Long-Horizon Task as secondary.

The minimum demo loop is fully defined: a founding agent launches a guild via AgentFightClub with a mandate and funded treasury; a Specialist Agent with a live ERC-8004 profile joins via a proposal vote; the Orchestrator delegates a real task via A2A; the Specialist executes it using GLM-5.1 and commits the deliverable hash to the guild contract on Base testnet; the human accepts; AgentFightClub releases payment; and the Specialist's ERC-8004 profile is updated with a verified delivery record — all demonstrable via clickable Basescan transaction hashes. The proposal scopes what is real vs. mocked: AgentFightClub treasury operations, ERC-8004 profile reads/writes, A2A task messages, GLM-5.1 execution, on-chain deliverable hash, and reputation write-back are all real; capability matching (hardcoded agent pair) and shared memory (JSON file) are mocked. The biggest technical risk is AgentFightClub API instability (alpha software), with a fallback to deploying Moloch v3 directly via the open-source DAOhaus SDK.

---

## 5. Prototyping Resources

**Reference document:** [hackathon/PROTOTYPING_RESOURCES.md](/hackathon/PROTOTYPING_RESOURCES.md)

Eight projects, standards, and tools reviewed before the hackathon build week, each with documentation links and a per-resource explanation of what it helps evaluate. Covers: AgentFightClub + Moloch v3 (DAOhaus SDK fallback), ERC-8004 + ERC-8183, A2A Protocol (0.3.0), GLM-5.1 / Z.AI API, Cobo Agentkit / Cobo Agentic Wallet, Base / Basescan, EAS (Ethereum Attestation Service), and Snapshot GraphQL + OpenZeppelin Governor (secondary direction reference). Each entry includes a reading priority note mapped to the build-week day it should be reviewed.

---

## 6. Direction Deep-Dive Pack

### Main Direction — Identity / Capability

**Deep-dive document:** [tasks/directions/01-identity-capability.md](/tasks/directions/01-identity-capability.md)

The main direction deep-dive covers the full dependency chain connecting identity, reputation, capability, and interoperability as a single infrastructure layer. It includes: a framing of the three core gaps (discovery, trust, invocation) that make multi-agent composition impossible in open ecosystems today; a Mermaid flowchart of the complete agent registration → discovery → trust evaluation → invocation → delivery → reputation update cycle; a worked scenario routing a governance summarization task through a third-party agent with full ERC-8004, A2A, and EAS integration; a counterexample showing how DID-as-avatar misses the point; a five-risk inventory (Sybil attacks, stale capability claims, identity spoofing, schema mismatch, adversarial agent routing); a one-week validation plan; and a reference section covering ERC-8004, A2A, MCP, MPP, and EAS with a protocol comparison table and MCP vs. A2A head-to-head analysis.

### Secondary Direction — Governance / Coordination

**Deep-dive document:** [tasks/directions/02-governance-coordination.md](/tasks/directions/02-governance-coordination.md)

The secondary direction analysis covers governance brief generation as the entry-point use case: using AI to reduce proposal reading costs while Web3 provides the on-chain ground truth that makes the brief trustworthy enough to act on. It includes the full governance brief workflow flowchart (AI-assisted ingest and summarization → human review → on-chain execution), a step-by-step scenario for a public goods DAO grant proposal, a counterexample showing how an agent with write access crosses the hard governance boundary, and a five-risk inventory (authoritative misrepresentation, selective summarization, stale data, AI-initiated governance actions, identity attribution). The two directions are structurally connected: governance in multi-agent systems requires that participating agents have verifiable identities and portable reputation records — the exact infrastructure the main direction builds. Governance is therefore the clearest application-layer proof point for Identity / Capability: once agents have trustless ERC-8004 profiles, governance communities can reason about which agents to accept as contributors and what weight to give their outputs. GuildOS exercises this relationship directly — the membership approval gate requires reading the Specialist Agent's ERC-8004 profile and making a governance vote before that agent can access the guild treasury.

---

## 7. Direction Backlog

The following three directions were analyzed but not selected as primary or secondary targets for the hackathon project.

**Deeper analyses:** [tasks/directions/03-payment-commerce.md](/tasks/directions/03-payment-commerce.md) · [tasks/directions/04-wallet-permission.md](/tasks/directions/04-wallet-permission.md) · [tasks/directions/05-privacy-security.md](/tasks/directions/05-privacy-security.md)

**Direction 3 — Payment / Commerce / Settlement** was not selected as a standalone direction because its core mechanisms (escrow, machine-to-machine payment, receipt verification) are present in GuildOS as infrastructure rather than as the primary demo surface. AgentFightClub provides the treasury and settlement layer; ERC-8183 defines the task/payment lifecycle; and the deliverable hash + `settle()` call demonstrates verifiable payment-on-acceptance. Payment is therefore embedded throughout GuildOS's flow rather than being the subject of the prototype. Standalone payment direction work (x402, MPP, per-API-call micropayments) is relevant post-hackathon when the guild's capability matching layer is extended to third-party paid services.

**Direction 4 — Wallet / Permission / Safe Execution** was not selected as a primary direction because, like payment, it is present in GuildOS as a constraint layer rather than a demo surface. The agent wallet (Cobo CAW or Wiretap via AgentFightClub) is scoped to the specific AgentFightClub contracts and Base testnet operations — enforcing the "controllable" dimension of the Cobo track. ERC-4337 session keys and contract allowlists are the mitigation for unbounded payment risk. However, the interesting research questions in this direction (how tightly can session key permissions be scoped, what is the standard ABI for permission predicates, how does revocation work for long-running sessions) remain open questions in the backlog rather than primary demo targets. A standalone wallet/permission prototype would focus on the permission policy design itself rather than the coordination layer GuildOS is building.

**Direction 5 — Privacy / Security / Sovereignty** was not selected because GuildOS operates on public testnets with transparent on-chain records — transparency is a feature, not a risk. The relevant security concerns for GuildOS (prompt injection via delivered data, stale capability claims, identity spoofing) are addressed through architectural constraints (read-only agent context for untrusted inputs, ERC-8004 re-validation at invocation time, DID resolution and signature verification) rather than through cryptographic privacy primitives. A privacy-first prototype would look significantly different from GuildOS: private execution environments, ZK proofs for verifiable inference, or censorship-resistant agent identity — important problems, but orthogonal to the coordination and reputation focus of the hackathon build.

---

## 8. Open Questions & Blockers

1. **AgentFightClub API stability** — The alpha API endpoint may change or be rate-limited during the build week. Fallback path (DAOhaus SDK + direct Moloch v3 deployment) is defined but needs to be validated before Day 1 of the hackathon.

2. **ERC-8004 registry write access** — The MVP requires writing a reputation record after deliverable acceptance. Is the 8004scan registry writable via a standard API call, or does the write require a direct on-chain transaction? The answer determines whether the reputation write-back is a registry API call or an `eth_sendTransaction` to Base testnet.

3. **GLM-5.1 structured output consistency** — Long-horizon task execution needs to produce a structured, hashable deliverable. Testing three task types on Day 1 (as planned) is the validation method — but if none produce consistent structured output, the fallback task type needs to be defined in advance.

4. **A2A payment intent field in 0.3.0** — The proposal requires the A2A task message to carry a payment intent reference so the task delegation and AgentFightClub settlement are traceable to the same exchange. Confirming this field exists in A2A 0.3.0 (and not in a later version only) must happen before building the task message schema.

5. **Cobo CAW vs. Wiretap wallet decision** — The wallet architecture decision is explicitly deferred in the proposal. It affects the primary hackathon track claim (Cobo vs. Z.AI as primary) and the on-chain transaction signing flow for both agents. This must be decided before Day 1.

---

*Built: 2026-06-02 | Agent: Sensei (Claude via Cowork)*
*Sources: PROJECT_PROPOSAL.md · AIxWeb3_WORKFLOW.md · PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md · directions/01-identity-capability.md · directions/02-governance-coordination.md · PROTOTYPING_RESOURCES.md · directions/03,04,05*
