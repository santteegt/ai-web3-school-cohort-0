# AI × Web3 — Problem Space Map

> Visual: [`AIxWeb3-problem-map.html`](./AIxWeb3-problem-map.html)  
> Source: AI × Web3 School Handbook — Bridge Introduction + Problem Space & Direction Map  
> Built: 2026-05-29 | Week 2 Deliverable

---

## Why This Map Exists

A direction is only genuinely AI × Web3 if **both domains are indispensable**: removing AI would leave an unenforceable process; removing Web3 would leave an unverifiable one. This map applies that test to all six foundational directions.

---

## Quick-Reference Table

| # | Direction | AI Role | Web3 Mechanism | Key Standards |
|---|-----------|---------|----------------|---------------|
| 1 | **Payment / Commerce** | Intent parsing, delivery verification, dispute reasoning | Programmable escrow, on-chain receipts, L2 micropayments | x402, MPP, ERC-8183, L2 channels |
| 2 | **Identity / Reputation** | Capability matching, quality scoring, behavioral analysis | Portable attestations, tamper-proof delivery records, stake/slash | DIDs/VCs, ERC-8004, EAS |
| 3 | **Capability / Interop** | Goal decomposition, multi-agent orchestration, semantic routing | Open registries, standardized invocation, provenance records | MCP, A2A, ERC-8004, MPP |
| 4 | **Wallet / Permission** | Risk classification, intent → permission spec, anomaly detection | Cryptographic enforcement, revocable delegation, audit logs | ERC-4337, Session Keys, EIP-7702 |
| 5 | **Privacy / Security** | Prompt injection detection, threat modeling, behavioral anomalies | ZKPs, TEEs, on-chain audit trails, sovereign data ownership | ZKP, TEE, EAS, on-chain logs |
| 6 | **Governance / Coordination** | Proposal summarization, sentiment synthesis, action item extraction | Binding on-chain votes, transparent treasury, immutable decision records | Snapshot, Governor, Gitcoin |

---

## Direction Breakdowns

### 1 · Payment / Commerce / Settlement

**Core question:** Who initiates, executes, pays, verifies, and carries risk across a machine-to-machine service transaction?

**AI role:** Understands the economic flow. Parses user or agent intent into a structured service request, discovers and evaluates providers, verifies delivery quality against acceptance criteria, detects payment anomalies, and reasons about failure modes and dispute resolution. AI turns a vague instruction ("buy me compute for this task") into a complete payment lifecycle.

**Web3 mechanism:** Enforces and settles the flow. Programmable money via x402 (HTTP-level per-call payments) and MPP (discovery → quote → authorization → receipt). Smart-contract escrow (ERC-8183 draft) implements the state machine `pending → locked → delivered → accepted → released`. L2s make micropayment economics viable.

**Why it is not a pure AI problem:** AI can understand service quality and evaluate delivery, but it cannot trustlessly move funds, enforce spending limits, or produce tamper-proof payment records. Without Web3, settlement still depends on a trusted intermediary.

**Why it is not a pure Web3 problem:** Smart contracts can enforce payment conditions and settle funds, but they cannot understand what "delivery" means for a given service, evaluate whether the output is acceptable, or reason about disputes. A dumb escrow with no delivery oracle is just locked money.

---

### 2 · Identity / Reputation / Capability

**Core question:** How are agents discovered, described, invoked, verified, and trusted across an open multi-agent ecosystem?

**AI role:** Understands what agents can do and how well they do it. Parses capability manifests in natural language, performs semantic matching between agent profiles and user goals, evaluates task completion quality for reputation accumulation, and detects behavioral anomalies across delivery histories.

**Web3 mechanism:** Makes identity and reputation portable and tamper-proof. DIDs and Verifiable Credentials anchor identity to a wallet address. ERC-8004 provides an on-chain agent registry with capability claims. EAS enables verifiable third-party attestations. Immutable delivery records and stake/slashing give reputation economic weight.

**Why it is not a pure AI problem:** AI can infer reputation from behavioral patterns, but those inferences are platform-specific and disappear when the platform changes. Without Web3, there is no portable, tamper-proof record of what an agent has done.

**Why it is not a pure Web3 problem:** Web3 can store attestations on-chain, but cannot understand the semantic content of a capability claim or evaluate whether a task was completed well. An on-chain registry without AI-assisted matching is just a phone book nobody can query intelligently.

---

### 3 · Capability / Interoperability

**Core question:** How do AI agents, tools, and on-chain systems compose across open interfaces without collapsing into closed ecosystems?

**AI role:** Orchestrates across agents and tools. Translates between capability formats (MCP, A2A), composes multi-agent workflows from individual capability primitives, maps natural language goals to structured tool call sequences, and resolves ambiguity when multiple agents could satisfy a sub-task.

**Web3 mechanism:** Provides open, trustless discovery and invocation. On-chain capability registries (ERC-8004) make agent profiles queryable without a central operator. A2A defines agent-to-agent task handoff. MPP provides a payment layer for third-party capability access. Open provenance records make cross-agent invocation chains auditable.

**Why it is not a pure AI problem:** AI can orchestrate agents, but without open registries and payment primitives there is no economic incentive for third parties to expose capabilities, and no trustless way to discover them. Multi-agent coordination defaults to tightly coupled, platform-controlled systems.

**Why it is not a pure Web3 problem:** Web3 can register capabilities and standardize interfaces, but cannot reason about which capabilities to combine for a given goal, resolve semantic ambiguity across different agents' capability descriptions, or handle failures gracefully during composition.

---

### 4 · Wallet / Permission / Safe Execution

**Core question:** When an agent holds on-chain authority, what controls prevent unscoped execution, unauthorized signing, and zombie permissions?

**AI role:** Classifies risk and translates intent into permission specifications. Interprets transaction simulation results in plain language, detects spending pattern anomalies, converts natural-language task descriptions into structured authorization scopes, and identifies when a write action crosses a risk threshold requiring human confirmation (the 8-step pattern's Step 7).

**Web3 mechanism:** Enforces permissions at the cryptographic layer. ERC-4337 smart accounts replace simple EOAs with programmable execution logic. Session keys provide task-scoped, time-bounded signing authority. EIP-7702 lets EOAs temporarily gain smart-account behavior. Revocable Pact authorization (Cobo model) binds agent execution to explicit intent + budget + time window + completion conditions. On-chain execution logs are immutable.

**Why it is not a pure AI problem:** AI can model risk and generate permission specs in natural language, but it cannot cryptographically enforce them. Without smart accounts, an agent with a private key can sign anything — "I only intended to authorize X" is not a technical constraint.

**Why it is not a pure Web3 problem:** Smart contracts can enforce permissions at the protocol level, but cannot dynamically assess the semantic risk of a transaction, understand the intent behind a permission request, or detect when an agent's behavior has been manipulated. A policy rule without contextual risk assessment is either too restrictive or too permissive.

---

### 5 · Privacy / Security / Sovereignty

**Core question:** When an agent holds credentials, keys, and budgets, what prevents adversarial input from compromising execution — and what gives users verifiable control over their own data?

**AI role:** Detects semantic and behavioral threats. Identifies prompt injection attempts, classifies attack surfaces (tool call abuse, forged transaction descriptions, phishing links, model hallucinations), monitors audit logs for behavioral anomalies, and builds threat models specific to AI agent workflows. Importantly: AI reflection is a quality mechanism, not a safety mechanism — code-enforced guardrails remain essential.

**Web3 mechanism:** Provides cryptographic proof and sovereign infrastructure. Zero-knowledge proofs enable privacy-preserving computation (prove correctness without revealing inputs). TEEs provide confidential execution environments. On-chain audit trails cannot be retroactively deleted. User key ownership enables full data portability and censorship resistance without vendor dependency.

**Why it is not a pure AI problem:** AI can detect semantic attacks (prompt injection, social engineering), but it cannot provide cryptographic proof that computation was performed correctly, or make data storage sovereign. Without Web3, "trust the AI" is a vendor trust assumption users cannot independently verify.

**Why it is not a pure Web3 problem:** Web3 provides ZKPs and immutable logs, but cannot detect that an agent has been fed adversarial inputs before it reaches the signing step. An on-chain audit trail faithfully records a malicious transaction that the agent was manipulated into producing. Detection requires AI; prevention requires both.

---

### 6 · Governance / Coordination / Public Goods

**Core question:** Can AI help DAOs and communities organize information and surface decisions — and can Web3 make those decisions binding, transparent, and trustlessly executable?

**AI role:** Reduces information overload and surfaces actionable structure. Summarizes governance proposals, synthesizes community sentiment across discussion threads, converts meeting notes into action items with owners and deadlines, models budget impact, and tracks contribution records. Hard boundary: AI can assist deliberation but cannot make value judgments, approve budgets, or initiate irreversible governance actions.

**Web3 mechanism:** Makes governance binding, transparent, and auditable. On-chain voting (Snapshot for off-chain, OpenZeppelin Governor for on-chain execution) produces tamper-proof records of who voted for what. Transparent treasury contracts enforce that funds only move after governance thresholds are met. Contribution records and public goods funding (Gitcoin) create verifiable accountability.

**Why it is not a pure AI problem:** AI can summarize proposals and suggest optimal decisions, but without Web3 those suggestions are advisory only. AI governance without on-chain enforcement is a well-organized document — effective only as long as participants choose to honor it.

**Why it is not a pure Web3 problem:** Web3 can record votes and execute budget transfers on-chain, but it cannot reduce proposal complexity, synthesize community sentiment, or help participants understand the downstream implications of a vote. High participation costs and information overload are the main reasons DAO governance fails — and those require AI to address.

---

## The Central Design Test

For any proposed AI × Web3 direction, apply this two-part test:

> 1. **Remove AI.** Does Web3 alone solve the problem? If yes — it's a pure Web3 problem.  
> 2. **Remove Web3.** Does AI alone solve the problem? If yes — it's a pure AI problem.

Only directions that fail *both* tests are genuinely AI × Web3.

The trap most demos fall into: they use AI for a task AI handles fine (summarizing, formatting, routing) and add Web3 for cosmetic reasons (storing the output as an NFT, triggering a wallet signature). The real AI × Web3 problems are at the boundary where **machine reasoning, economic exchange, permission control, and verifiable records** all need to appear in the same flow.

---

*Source: AI × Web3 School Handbook — Bridge Introduction, Problem Space & Direction Map, Unified Evaluation Framework | Built: 2026-05-29*
