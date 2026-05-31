# AI × Web3 — Problem Space Map

> Visual: [`AIxWeb3-problem-map.html`](./AIxWeb3-problem-map.html)  
> Source: AI × Web3 School Handbook — Bridge Introduction + Problem Space & Direction Map  
> Built: 2026-05-29 | Week 2 Deliverable

---

## Why This Map Exists

A direction is only genuinely AI × Web3 if **both domains are indispensable**: removing AI would leave an unenforceable process; removing Web3 would leave an unverifiable one. This map applies that test to all six foundational directions.

---

## Quick-Reference Table

| # | Direction | Real User | Best Learning Form | Key Standards |
|---|-----------|-----------|-------------------|---------------|
| 1 | **Payment / Commerce** | Developer building autonomous agent services that need to pay for and receive payment for API calls, data, or compute without human approval per transaction | Product demo | x402, MPP, ERC-8183, L2 channels |
| 2 | **Identity / Reputation** | Developer building multi-agent pipelines who needs to discover, evaluate, and compose third-party agents without relying on a single marketplace | Developer tooling | DIDs/VCs, ERC-8004, EAS |
| 3 | **Capability / Interop** | Developer whose system needs agents from different providers or frameworks to interoperate without writing a custom adapter for every combination | Developer tooling | MCP, A2A, ERC-8004, MPP |
| 4 | **Wallet / Permission** | Developer integrating agent execution into a product who needs to grant scoped, revocable on-chain authority — and a clean audit trail when something goes wrong | Risk model → product demo | ERC-4337, Session Keys, EIP-7702 |
| 5 | **Privacy / Security** | Security engineer or developer building agent systems that handle credentials or private keys who needs to define and communicate a threat model before deployment | Risk model | ZKP, TEE, EAS, on-chain logs |
| 6 | **Governance / Coordination** | DAO contributor or core team member managing participation fatigue who needs AI-synthesized governance briefs tied to verifiable on-chain records | Product demo | Snapshot, Governor, Gitcoin |

---

## Direction Breakdowns

### 1 · Payment / Commerce / Settlement

**Core question:** Who initiates, executes, pays, verifies, and carries risk across a machine-to-machine service transaction?

**Real user:** A developer or product builder creating autonomous agent services who needs agents to discover, pay for, and settle machine-to-machine transactions without requiring human approval at each step.

**Best learning form:** **Product demo** — the full payment lifecycle (discovery → quote → escrow → delivery → settlement) is concrete enough to demonstrate end-to-end with x402 + a minimal escrow contract. Developer tooling is a close second if the goal is building reusable payment primitives others can integrate.

**AI role:** Understands the economic flow. Parses user or agent intent into a structured service request, discovers and evaluates providers, verifies delivery quality against acceptance criteria, detects payment anomalies, and reasons about failure modes and dispute resolution. AI turns a vague instruction ("buy me compute for this task") into a complete payment lifecycle.

**Web3 mechanism:** Enforces and settles the flow. Programmable money via x402 (HTTP-level per-call payments) and MPP (discovery → quote → authorization → receipt). Smart-contract escrow (ERC-8183 draft) implements the state machine `pending → locked → delivered → accepted → released`. L2s make micropayment economics viable.

**Why it is not a pure AI problem:** AI can understand service quality and evaluate delivery, but it cannot trustlessly move funds, enforce spending limits, or produce tamper-proof payment records. Without Web3, settlement still depends on a trusted intermediary.

**Why it is not a pure Web3 problem:** Smart contracts can enforce payment conditions and settle funds, but they cannot understand what "delivery" means for a given service, evaluate whether the output is acceptable, or reason about disputes. A dumb escrow with no delivery oracle is just locked money.

**Verification method:** Three-layer chain matching the workflow's verification pattern:
 1. *Delivery proof before release*: the accepted deliverable must be hashed and matched against the hash committed at quote time — file hash, signed API log, or on-chain event.
 3. *On-chain receipt confirmation*: payment transaction hash + emitted ERC event log provides cryptographic proof that funds moved with specific parameters at a specific block height.
 3. *Escrow state audit*: verify the state machine transitioned correctly through each stage (`pending → locked → delivered → accepted → released`) by reading contract storage — a stuck or skipped state is a dispute trigger.

**Risk boundaries:** Payment exploits from an overly broad agent wallet are the primary financial risk
- ERC-4337 session keys with per-transaction spend limits and contract allowlists are the required mitigation, not optional
- Negotiation integrity is the second risk: a malicious provider can present false capability schemas or bait-and-switch pricing before payment; schema validation of the delivered payload against the quoted spec must happen before the acceptance step, not after.
- Prompt injection via the delivered data payload is the third risk — provider output flows into the agent's reasoning context and can embed adversarial instructions; treat provider data as a separate, lower-trust context layer with sanitization before ingestion.
- Irreversible execution applies to any on-chain settlement: simulation before signing and a human gate before irreversible transfers are the hard stops.

---

### 2 · Identity / Reputation / Capability

**Core question:** How are agents discovered, described, invoked, verified, and trusted across an open multi-agent ecosystem?

**Real user:** A developer building multi-agent pipelines who needs to discover, evaluate, and compose third-party agents as open services — without relying on a single marketplace operator to vouch for agent quality or hard-coding agent addresses into every integration.

**Best learning form:** **Developer tooling** — the standards layer (ERC-8004, A2A, DID/VC) is being designed by others; the tractable entry point is the interface layer above it: a tool that takes a user goal, queries a registry, evaluates capability manifests semantically, and returns a ranked shortlist with trust scores. A working implementation of that layer is both a learning artifact and a hackathon deliverable.

**AI role:** Understands what agents can do and how well they do it. Parses capability manifests in natural language, performs semantic matching between agent profiles and user goals, evaluates task completion quality for reputation accumulation, and detects behavioral anomalies across delivery histories.

**Web3 mechanism:** Makes identity and reputation portable and tamper-proof. DIDs and Verifiable Credentials anchor identity to a wallet address. ERC-8004 provides an on-chain agent registry with capability claims. EAS enables verifiable third-party attestations. Immutable delivery records and stake/slashing give reputation economic weight.

**Why it is not a pure AI problem:** AI can infer reputation from behavioral patterns, but those inferences are platform-specific and disappear when the platform changes. Without Web3, there is no portable, tamper-proof record of what an agent has done.

**Why it is not a pure Web3 problem:** Web3 can store attestations on-chain, but cannot understand the semantic content of a capability claim or evaluate whether a task was completed well. An on-chain registry without AI-assisted matching is just a phone book nobody can query intelligently.

**Verification method:**
1. *Registry read at task time, not build time*: re-read the agent's ERC-8004 profile and capability manifest immediately before invoking it — cached context from earlier in the session may be stale if the agent was updated or paused.
2. *Attestation trace*: query EAS for third-party attestations on the agent; trace each attestation back to its attester address and verify the attester's own on-chain credibility (a self-attestation loop with no independent endorsers is a red flag).
3. *Behavioral cross-check*: compare claimed capabilities against verifiable on-chain delivery records — an agent claiming 500 successful completions with zero on-chain delivery logs has unverified reputation.
4. *Semantic round-trip*: after invoking an agent, verify that the output format matches the capability manifest's declared output schema; a mismatch between claim and delivery is a reputation data point.

**Risk boundaries:**
- Reputation gaming via Sybil attacks (fake delivery records, self-attestation loops) is the defining risk of this direction — economic stake/slashing is the required mitigation because social reputation systems can be gamed at near-zero cost.
- False capability claims introduce a misrouting risk: the agent gets invoked for a task it cannot complete, possibly injecting garbage or adversarial content into the calling agent's context (same prompt injection vector).
- Identity spoofing — impersonating another agent's DID or wallet address — is prevented by DID resolution and signature verification, not by registry lookup alone. Stale registry data is a subtler risk: a capability manifest that was accurate at registration time may describe a deprecated API or a model version that no longer exists; always re-verify at invocation time.
- No private keys or funds are at risk at the read-only discovery and matching layer, which keeps the prototype phase risk surface low.

---

### 3 · Capability / Interoperability

**Core question:** How do AI agents, tools, and on-chain systems compose across open interfaces without collapsing into closed ecosystems?

**Real user:** A developer whose system needs agents from different providers or frameworks to interoperate without writing a custom adapter for every combination — and needs those invocations to be auditable and payable without a central broker in the middle.

**Best learning form:** **Developer tooling** — building a reference implementation that shows two heterogeneous agents (e.g., one MCP-based, one A2A-based) composing a task end-to-end, with on-chain provenance, is more instructive than studying the protocol specs in isolation. A protocol/standard contribution is possible if the goal shifts toward proposing a missing interface spec.

**AI role:** Orchestrates across agents and tools. Translates between capability formats (MCP, A2A), composes multi-agent workflows from individual capability primitives, maps natural language goals to structured tool call sequences, and resolves ambiguity when multiple agents could satisfy a sub-task.

**Web3 mechanism:** Provides open, trustless discovery and invocation. On-chain capability registries (ERC-8004) make agent profiles queryable without a central operator. A2A defines agent-to-agent task handoff. MPP provides a payment layer for third-party capability access. Open provenance records make cross-agent invocation chains auditable.

**Why it is not a pure AI problem:** AI can orchestrate agents, but without open registries and payment primitives there is no economic incentive for third parties to expose capabilities, and no trustless way to discover them. Multi-agent coordination defaults to tightly coupled, platform-controlled systems.

**Why it is not a pure Web3 problem:** Web3 can register capabilities and standardize interfaces, but cannot reason about which capabilities to combine for a given goal, resolve semantic ambiguity across different agents' capability descriptions, or handle failures gracefully during composition.

**Verification method:**
1. *Interface conformance test*: after invoking a sub-agent, validate that its response matches the declared MCP or A2A output schema before passing it to the next stage in the composition chain — a schema mismatch at handoff is a failure point, not a recoverable error.
2. *Invocation provenance trace*: each agent-to-agent call should produce an on-chain or log-anchored record of caller identity, tool invoked, input hash, and output hash — this makes the full composition chain auditable after the fact.
3. *End-to-end composition test*: submit a multi-step goal and trace whether each sub-agent's output correctly seeds the next stage's input, including checking that context was not silently truncated or corrupted across the handoff boundary.

**Risk boundaries:**
- Prompt injection through the composition chain is the primary risk unique to this direction: each handoff is a trust boundary where one agent's output becomes another agent's input, and a malicious or misconfigured upstream agent can embed adversarial instructions that manipulate downstream agents.
- Attribution failure is the governance risk — in a multi-agent chain, determining which agent bears responsibility for a bad outcome requires per-step provenance logs; without them, post-incident investigation is impossible.
- Schema mismatch between agents using nominally compatible protocols (e.g., different MCP versions) causes silent data corruption rather than hard failures, making it harder to detect.
- Closed-ecosystem lock-in is the structural risk: any platform-controlled intermediary in the chain can break open composition silently at any step; open registries and direct A2A calls are the mitigation.

---

### 4 · Wallet / Permission / Safe Execution

**Core question:** When an agent holds on-chain authority, what controls prevent unscoped execution, unauthorized signing, and zombie permissions?

**Real user:** A developer integrating agent execution into a product who needs to grant an agent limited, auditable on-chain authority without exposing full wallet control — and needs a reliable revocation path and immutable audit trail when something goes wrong.

**Best learning form:** **Risk model leading to a product demo** — the design decisions (what to scope, what triggers a human gate, how revocation works, what the audit log must contain) are inherently a risk-modeling exercise. Working through the threat model first produces a better implementation than starting with code. The demo then validates the model with a real Pact-style authorization flow on testnet.

**AI role:** Classifies risk and translates intent into permission specifications. Interprets transaction simulation results in plain language, detects spending pattern anomalies, converts natural-language task descriptions into structured authorization scopes, and identifies when a write action crosses a risk threshold requiring human confirmation (the 8-step pattern's Step 7).

**Web3 mechanism:** Enforces permissions at the cryptographic layer. ERC-4337 smart accounts replace simple EOAs with programmable execution logic. Session keys provide task-scoped, time-bounded signing authority. EIP-7702 lets EOAs temporarily gain smart-account behavior. Revocable Pact authorization (Cobo model) binds agent execution to explicit intent + budget + time window + completion conditions. On-chain execution logs are immutable.

**Why it is not a pure AI problem:** AI can model risk and generate permission specs in natural language, but it cannot cryptographically enforce them. Without smart accounts, an agent with a private key can sign anything — "I only intended to authorize X" is not a technical constraint.

**Why it is not a pure Web3 problem:** Smart contracts can enforce permissions at the protocol level, but cannot dynamically assess the semantic risk of a transaction, understand the intent behind a permission request, or detect when an agent's behavior has been manipulated. A policy rule without contextual risk assessment is either too restrictive or too permissive.

**Verification method:** Mirrors the workflow's three-layer chain applied to every write action.
1. *Simulation before signing*: dry-run every candidate transaction via `eth_call` or a simulation API — preview expected state changes, gas cost, and token movements before the human confirmation gate; any simulation failure is a hard stop.
2. *Permission pre-check at execution time, not only at authorization time*: re-verify session key scope against the target contract, function selector, and amount immediately before signing — do not rely on the permission check done when the Pact was first authorized, because on-chain state may have changed.
3. *Immutable audit log read-back*: after execution, read the transaction receipt (status, gas used, emitted events) and compare against the simulated outcome; divergence between simulated and actual state is an investigation trigger.
4. *Revocation test*: periodically verify that the revocation path works — a permission that cannot be revoked in practice is as dangerous as an unbounded permission.

**Risk boundaries:**
- Unscoped authority is the primary risk — an agent wallet without per-transaction spend limits and contract allowlists can be drained or misused beyond the intended task scope; ERC-4337 session keys with explicit allowlists are required, not optional.
- Zombie permissions (stale never-expiring session keys) are the second risk and the hardest to detect: they accumulate silently and become persistent attack surfaces; time-bounded keys with mandatory expiry are the mitigation.
- Shadow operations — agent wallet actions not reflected in any user-visible interface — make it impossible for the user to detect abuse; on-chain audit trail with alerting is the control.
- Prompt injection into the permission specification is a subtle but serious risk: if the agent generates permission scopes from free-form LLM output, an adversarial input can cause over-broad permissions to be requested; permission specs should be generated from structured templates with bounded fields, not arbitrary model output.
- Irreversible execution remains the hard boundary: any on-chain transaction that moves funds or changes ownership cannot be undone; the human gate in Step 7 of the reference workflow is the mandatory control.

---

### 5 · Privacy / Security / Sovereignty

**Core question:** When an agent holds credentials, keys, and budgets, what prevents adversarial input from compromising execution — and what gives users verifiable control over their own data?

**Real user:** A security engineer or developer building agent systems that handle credentials, private keys, or sensitive user data — who needs to define, communicate, and continuously validate the system's threat model before any real assets are involved.

**Best learning form:** **Risk model** — this direction is fundamentally about attack surface mapping and control design before a line of production code is written. A structured risk model (asset inventory → attack surfaces → controls → sovereignty checklist) is the most honest and transferable output. A product demo risks glossing over the hard parts; a research memo that documents the threat model in depth is the form most likely to survive contact with a real system.

**AI role:** Detects semantic and behavioral threats. Identifies prompt injection attempts, classifies attack surfaces (tool call abuse, forged transaction descriptions, phishing links, model hallucinations), monitors audit logs for behavioral anomalies, and builds threat models specific to AI agent workflows. Importantly: AI reflection is a quality mechanism, not a safety mechanism — code-enforced guardrails remain essential.

**Web3 mechanism:** Provides cryptographic proof and sovereign infrastructure. Zero-knowledge proofs enable privacy-preserving computation (prove correctness without revealing inputs). TEEs provide confidential execution environments. On-chain audit trails cannot be retroactively deleted. User key ownership enables full data portability and censorship resistance without vendor dependency.

**Why it is not a pure AI problem:** AI can detect semantic attacks (prompt injection, social engineering), but it cannot provide cryptographic proof that computation was performed correctly, or make data storage sovereign. Without Web3, "trust the AI" is a vendor trust assumption users cannot independently verify.

**Why it is not a pure Web3 problem:** Web3 provides ZKPs and immutable logs, but cannot detect that an agent has been fed adversarial inputs before it reaches the signing step. An on-chain audit trail faithfully records a malicious transaction that the agent was manipulated into producing. Detection requires AI; prevention requires both.

**Verification method:**
1. *Threat model audit*: structured enumeration of asset inventory (what credentials, keys, budgets does the agent hold?), attack surfaces (where can adversarial input enter?), and controls (what stops each attack?) — this is the primary verification artifact for this direction, and it must be produced before any code.
2. *Adversarial input test*: submit known prompt injection payloads (instruction-embedded documents, forged tool return values, phishing-style context injections) and verify that guardrails trigger correctly and no adversarial instruction reaches the signing or execution layer.
3. *Audit trail integrity check*: verify that the on-chain audit log cannot be deleted, modified, or selectively omitted after the fact — an audit trail with gaps is not an audit trail.
4. *Sovereignty checklist*: verify that the user can (a) export all their data, (b) revoke all agent authorizations, (c) switch model providers, and (d) continue operating core assets without the original platform — a system that fails any of these has a sovereignty gap.

**Risk boundaries:**
- Prompt injection via external inputs (web pages, document payloads, tool response values) is the most critical risk class because it bypasses all on-chain controls — it manipulates the reasoning layer before any transaction is formed; input sanitization and lower-trust context layers are the mitigation.
- Sensitive data in the context window (private keys, API keys, session tokens, PII) is the second risk: anything placed in an LLM prompt is potentially logged, cached, or leaked through the model provider's infrastructure; credentials must never enter prompts, only scoped tool calls.
- Provider dependency creates a sovereignty gap: if the user cannot verify what the model did or migrate away, "trust the AI" is a vendor trust assumption with no technical basis; local execution or TEE attestation is the mitigation.
- Least-privilege tool access is not optional — an agent granted more tool access than its current task requires has an expanded attack surface with no benefit; tool permissions should be scoped per-task, not per-session.
- Audit trail gaps make post-incident investigation impossible: if execution is not logged on-chain with sufficient granularity, the only evidence of what the agent did is the agent's own output, which cannot be trusted after a compromise.

---

### 6 · Governance / Coordination / Public Goods

**Core question:** Can AI help DAOs and communities organize information and surface decisions — and can Web3 make those decisions binding, transparent, and trustlessly executable?

**Real user:** A DAO contributor, core team member, or community manager managing governance participation fatigue — someone who needs structured, AI-synthesized governance briefs that link directly to verifiable on-chain records and don't require reading every forum thread to participate meaningfully.

**Best learning form:** **Product demo** — a narrow scope (ingest a Snapshot space + governance forum → output a structured brief with proposal summary, key trade-offs, action items, and vote record links) is buildable in a week, clearly demonstrates both AI and Web3 roles in a single flow, and the hard constraint (AI must not initiate or pass governance actions) writes the risk boundaries almost automatically.

**AI role:** Reduces information overload and surfaces actionable structure. Summarizes governance proposals, synthesizes community sentiment across discussion threads, converts meeting notes into action items with owners and deadlines, models budget impact, and tracks contribution records. Hard boundary: AI can assist deliberation but cannot make value judgments, approve budgets, or initiate irreversible governance actions.

**Web3 mechanism:** Makes governance binding, transparent, and auditable. On-chain voting (Snapshot for off-chain, OpenZeppelin Governor for on-chain execution) produces tamper-proof records of who voted for what. Transparent treasury contracts enforce that funds only move after governance thresholds are met. Contribution records and public goods funding (Gitcoin) create verifiable accountability.

**Why it is not a pure AI problem:** AI can summarize proposals and suggest optimal decisions, but without Web3 those suggestions are advisory only. AI governance without on-chain enforcement is a well-organized document — effective only as long as participants choose to honor it.

**Why it is not a pure Web3 problem:** Web3 can record votes and execute budget transfers on-chain, but it cannot reduce proposal complexity, synthesize community sentiment, or help participants understand the downstream implications of a vote. High participation costs and information overload are the main reasons DAO governance fails — and those require AI to address.

**Verification method:**
1. *Source linkback audit*: every factual claim in an AI-generated governance brief must trace to a specific forum post ID, Snapshot proposal ID, or on-chain transaction — any claim without a source link is unverifiable and should be flagged or omitted.
2. *Diff check against original thread*: compare the AI brief against the source discussion thread and verify that minority views, technical objections, and dissenting arguments are not omitted or misrepresented; selective summarization that only captures the majority view is a failure mode, not a feature.
3. *On-chain ground truth check*: verify vote tallies, treasury execution status, and contributor records directly against chain state (Snapshot GraphQL API, Governor contract read) — do not trust the brief's numbers without an independent chain read.
4. *Staleness check*: governance proposals update continuously; the brief must carry an explicit timestamp and link to the live source, and briefs older than a defined threshold should be invalidated automatically.

**Risk boundaries:**
- Authoritative misrepresentation is the primary risk — an AI-generated brief mistaken for an official community decision or recommendation can distort governance outcomes without any single actor being responsible; every brief must carry an explicit disclaimer and source links.
- AI-initiated governance actions are the hard boundary: the agent must be architecturally read-only — it surfaces and summarizes, never proposes, votes, or executes treasury actions; this constraint should be enforced in code, not just by instruction.
- Selective summarization can suppress minority views or technical objections that ultimately prove correct; structured output formats that require capturing both sides of every proposal are the mitigation.
- Stale governance data produces briefs that misrepresent the current state of a proposal after it has been amended — link to live sources and timestamp every output.
- Identity attribution risk: if AI-generated governance content is published under a specific on-chain identity without that identity holder's explicit consent, it constitutes a form of impersonation with on-chain consequences; all AI-generated content must be explicitly attributed as such and not signed by a user's wallet without review.

---

## The Central Design Test

For any proposed AI × Web3 direction, apply this two-part test:

> 1. **Remove AI.** Does Web3 alone solve the problem? If yes — it's a pure Web3 problem.  
> 2. **Remove Web3.** Does AI alone solve the problem? If yes — it's a pure AI problem.

Only directions that fail *both* tests are genuinely AI × Web3.

The trap most demos fall into: they use AI for a task AI handles fine (summarizing, formatting, routing) and add Web3 for cosmetic reasons (storing the output as an NFT, triggering a wallet signature). The real AI × Web3 problems are at the boundary where **machine reasoning, economic exchange, permission control, and verifiable records** all need to appear in the same flow.

---

*Source: AI × Web3 School Handbook — Bridge Introduction, Problem Space & Direction Map, Unified Evaluation Framework | Built: 2026-05-29*
