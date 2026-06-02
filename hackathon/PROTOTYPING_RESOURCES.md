# GuildOS — Prototyping Resources

> Track: Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary)  
> Directions: Identity / Capability (main) · Governance / Coordination (secondary)  
> Built: 2026-06-02 | Cohort 0 · AI × Web3 School

This document lists the key projects, standards, protocols, and tools that must be reviewed before and during GuildOS prototyping. Each entry maps to a specific component of the MVP, lists concrete learning resources, and explains what each source helps you evaluate or validate during the build week.

---

## 1. AgentFightClub + Moloch v3 (DAOhaus SDK)

**Role in GuildOS:** The governance and treasury layer. AgentFightClub wraps Moloch v3 to provide: guild formation (`launch` + `commit`), membership proposals (`propose` + `vote`), and payment settlement (`settle`). It is the on-chain enforcement layer that removes the need for a trusted intermediary — treasury is collective, capital only moves after an approved governance action.

**Why it belongs here:** AgentFightClub is the primary technical risk in the MVP. It is alpha software. Reviewing it early validates whether the API is stable enough to build against, and identifies which Moloch v3 operations map to the GuildOS workflow. The DAOhaus fallback (deploy Moloch v3 directly) must be understood before Day 1 so it can be activated without losing time.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| AgentFightClub — How It Works | https://agentfightclub.xyz/how-it-works | Maps the full `launch → propose → vote → settle` lifecycle to GuildOS's guild formation and payment flow. Read this to confirm which operations are available via Skill API vs. requiring direct contract calls. |
| ClawBank + Raid Guild announcement | https://x.com/ClawBankHQ/status/2059676000573870221 | Shows how a working "Agent Fight Club" instance was deployed end-to-end — useful for understanding what the live demo was and what "ships in production" looks like for this stack. |
| Moloch v3 — DAOhaus Documentation | https://docs.daohaus.club/contracts | Covers the Moloch v3 contract architecture: `Baal.sol` (governance), `BaalVault.sol` (treasury), and the proposal lifecycle state machine. Read this to understand the fallback path: deploying Moloch v3 directly if AgentFightClub's Skill API is unavailable during the hackathon. |
| Moloch v3 GitHub (open source, audited) | https://github.com/HausDAO/Baal | The source contracts. Review `Baal.sol` for the exact ABI and event signatures used by `launch`, `commit`, `propose`, `vote`, and `settle`. Knowing the event signatures lets you verify each operation on Basescan during the demo. |
| Moloch v3 Tutorial — DAOhaus | https://docs.daohaus.club/quickstart | Step-by-step guide for spinning up a Moloch v3 DAO. Run through this to validate the fallback path works before the hackathon begins. |

---

## 2. ERC-8004 — Agent Identity, Capability, and Reputation Registry

**Role in GuildOS:** The identity and reputation data layer for both agents (Orchestrator and Specialist). ERC-8004 stores: agent name, owner, capabilities, A2A endpoint, and task delivery records. The MVP reads ERC-8004 profiles to display the Specialist Agent's delivery history before membership approval, and writes a new delivery record after the accepted task. The before/after delta of the Specialist's profile is one of the two primary demo proof points.

**Why it belongs here:** ERC-8004 is a draft standard with an active API (8004scan). Understanding its schema is required to design the agent profile, to know what fields are readable from the API, and to plan the reputation write-back. The companion standard ERC-8183 defines the task/payment/escrow lifecycle that feeds into the reputation record — reading both together is essential.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| ERC-8004 EIP | https://eips.ethereum.org/EIPS/eip-8004 | The canonical schema: identity fields, capability manifest format, reputation records, attestation references. Read the full EIP before designing the agent profile data structure — the demo profile must conform to this schema or the read/write cycle will not match what 8004scan returns. |
| 8004scan API | https://8004scan.xyz (or linked from EIP) | The live registry reader. Test a real agent profile read against this API before the hackathon. This validates whether the API is stable, what fields are actually populated in deployed profiles, and how to handle missing or null fields in the demo UI. |
| ERC-8183 EIP | https://eips.ethereum.org/EIPS/eip-8183 | The task/payment/escrow lifecycle companion to ERC-8004. Defines how a task is authorized, how the escrow state machine works (locked → delivered → accepted/disputed → settled), and how settlement feeds back into the reputation record. Read alongside ERC-8004 to understand the boundary between "who is this agent" and "how does this specific task get settled." |
| MetaMask — Design Server Wallets for AI Agents with ERC-8004 | https://docs.metamask.io/tutorials/design-server-wallets/ | A production architecture tutorial that combines agent identity (ERC-8004), backend signer, and wallet execution. Useful for understanding how an agent's identity anchors to a wallet key and how the signing flow works for reputation write-backs — directly relevant to the GuildOS on-chain deliverable hash commit. |

---

## 3. A2A Protocol — Agent-to-Agent Communication

**Role in GuildOS:** The communication layer between the Orchestrator Agent and Specialist Agent. A2A carries the structured task message (task description, input data, acceptance criteria, deadline, budget) from Orchestrator to Specialist, and the result message (deliverable reference + hash) back from Specialist to Orchestrator. Both A2A messages are core demo artifacts — they appear in the agent message log that proves task delegation happened.

**Why it belongs here:** A2A is the primary interoperability surface. Getting the message schema right determines whether the task delegation is legible to judges and whether the result carries the deliverable reference correctly. A2A 0.3.0 is the target spec — reviewing the reference implementation and examples before building prevents format drift.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| A2A Official Repository | https://github.com/a2aproject/A2A | The spec and reference implementation. Read the spec alongside the examples to understand the minimum required message fields for a task request (task ID, caller identity, input, acceptance criteria, payment intent reference) and a result (status, deliverable reference, hash). Focus on the message schema, not the transport layer — GuildOS needs the schema right, not a full transport implementation. |
| A2A Specification (0.3.0) | https://github.com/a2aproject/A2A/blob/main/spec/A2A_spec.md | The versioned spec document. Pin to 0.3.0 for the hackathon build to avoid schema drift. Evaluate whether the payment intent association field is present in 0.3.0 — the GuildOS task message must carry a payment intent reference so the A2A exchange and the AgentFightClub settlement are traceable to the same task. |
| A2A Examples | https://github.com/a2aproject/A2A/tree/main/examples | Working code examples of A2A task messages. Run the examples before building to confirm the message format produces valid JSON that passes schema validation. This is the fastest way to validate that your A2A implementation is spec-compliant. |
| A2A vs. MCP explainer (Direction 1 deep-dive) | `tasks/directions/01-identity-capability.md` (Section 12) | The protocol comparison table and head-to-head analysis from the direction deep-dive. Use this to confirm which protocol belongs at which layer: A2A for agent-to-agent task delegation (Orchestrator ↔ Specialist), MCP for tool calls within a single agent. The boundary matters for the demo architecture. |

---

## 4. GLM-5.1 — Long-Horizon Task Execution (Z.AI)

**Role in GuildOS:** The LLM powering the Specialist Agent's execution loop. GLM-5.1 handles multi-step planning, tool use across iterations, and structured output generation for the assigned task. It is the AI execution engine that produces the deliverable — the actual code, analysis, or audit report — that gets hashed and committed on-chain. The Specialist Agent is the Z.AI track's primary demo surface.

**Why it belongs here:** GLM-5.1's long-horizon task capability is the hackathon track differentiator. Reviewing the API and evaluating task type performance before Day 1 is essential: the proposal explicitly calls for testing three representative task types on Day 1 and picking the one that produces the most consistent structured output for the live demo. Understanding the API's tool calling and structured output format is a prerequisite for that evaluation.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| Z.AI (ZhipuAI) API Documentation | https://open.bigmodel.cn/dev/api | Full API reference for GLM-5.1. Review the tool calling API, the structured output format, and the long-horizon task completion parameters. Evaluate whether GLM-5.1 accepts a task with explicit acceptance criteria and produces a verifiable structured output — this is required for the deliverable hash step. |
| ZhipuAI Python SDK | https://github.com/zhipuai/zhipuai-sdk-python-v4 | The official Python client. Set up a working GLM-5.1 API call before Day 1 of the hackathon. Test the tool calling loop on a representative task (code generation, contract audit, analysis) to confirm the output is structured enough to hash consistently. |
| GLM-5.1 Long-Horizon Task Demo | https://open.bigmodel.cn/dev/api#long-chain (check Z.AI docs for latest) | Official examples of multi-step long-horizon task execution. Review these to understand how to structure the initial task prompt so GLM-5.1 decomposes it into a plan, executes steps, and produces a final structured output rather than a raw conversational response. |
| Z.AI Hackathon Track Brief | (provided in hackathon materials) | Explains what judges expect from the Z.AI track: a runnable prototype that uses GLM-5.1's long-horizon capability, with a real task executed from requirement to delivery. Use this to confirm the demo task type matches the track's stated directions and that GLM-5.1's output quality will satisfy the acceptance criteria. |

---

## 5. Cobo Agentkit / Cobo Agentic Wallet

**Role in GuildOS:** The agent execution wallet — the smart account that each agent uses to sign transactions, commit deliverable hashes, and receive payment. The Cobo track requires demonstrating "controllable on-chain fund operations": scoped wallets where an agent can only act within predefined spending limits and contract allowlists. This is the primary hackathon track's evaluation surface.

**Why it belongs here:** The wallet architecture decision (Cobo CAW vs. Wiretap) is explicitly deferred in the proposal but must be finalized before Day 1. Reviewing Cobo Agentkit's API and the CAW (Cobo Agentic Wallet) design determines whether the wallet can be scoped to the specific AgentFightClub contracts and Base testnet transactions required by the demo, and whether the API is stable enough for the hackathon timeline.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| Cobo Agentkit Documentation | https://www.cobo.com/developers/v2/developer-tools/agentkit/overview | Overview of the Agentkit: what operations it supports, how wallet scoping works (contract allowlists, spending limits, session keys), and how to initialize a Cobo Agentic Wallet for a specific agent. Evaluate whether the wallet can be configured to only authorize calls to the AgentFightClub contracts and Base testnet. |
| Cobo Agentkit GitHub | https://github.com/CoboGlobal/cobo-agentkit | The SDK source and examples. Run the quickstart example to confirm API access and evaluate the transaction signing flow. Check whether the wallet creation API supports a "scoped to contract X" initialization that matches GuildOS's per-agent authorization model. |
| Cobo Developer Portal | https://portal.cobo.com/developer | The portal for API keys and testnet wallet setup. Set this up before the hackathon. Evaluate whether testnet (Base Sepolia) is supported, and whether the portal provides a wallet dashboard for tracking agent transaction history — useful for the demo's Basescan link requirement. |
| Cobo Hackathon Track Brief | (provided in hackathon materials) | Defines the Cobo track's evaluation criteria: what "controllable on-chain fund operations" means in judging terms, which demo directions score highest, and whether the A2A Economy framing of GuildOS maps to the track's stated goals. Use this to confirm the demo scope matches what judges will be evaluating. |

---

## 6. Base / Basescan (Deployment Chain)

**Role in GuildOS:** The L2 settlement chain for all on-chain operations: AgentFightClub treasury (`launch`, `commit`, `settle`), deliverable hash commitment, ERC-8004 reputation write-back. Base testnet (Base Sepolia) is the target for the hackathon demo. Clickable Basescan transaction hashes are the primary proof-of-completion evidence for judges.

**Why it belongs here:** Every on-chain demo proof — the deliverable hash commit, the AgentFightClub settlement tx, the ERC-8004 reputation event — must be visible and verifiable on Basescan during the live demo. Understanding how Base works, how to fund a testnet wallet, and how to read contract events on Basescan is required before Day 1.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| Base Documentation | https://docs.base.org | Overview of Base: network parameters, JSON-RPC endpoint, EVM compatibility, and testnet configuration. Evaluate whether all AgentFightClub contracts and ERC-8004 registry operations are EVM-compatible on Base Sepolia — a prerequisite before deciding the deployment chain is settled. |
| Base Sepolia Testnet Faucet | https://docs.base.org/docs/tools/network-faucets | How to fund a Base Sepolia wallet for testing. Set up funded testnet wallets for both the Orchestrator and Specialist agents before the hackathon. Evaluate whether the faucet provides enough ETH for the full demo loop (formation + membership vote + deliverable hash + settlement). |
| Basescan (Base Sepolia) | https://sepolia.basescan.org | The block explorer for Base Sepolia. Evaluate what a transaction looks like from the judge's perspective: can the deliverable hash commit, the settlement tx, and the ERC-8004 reputation event all be verified from a single Basescan address view? The answer to this determines how the demo's "clickable tx hashes" proof structure should be organized. |
| Base Smart Contract Deployment Guide | https://docs.base.org/docs/getting-started/deploy-smart-contract | If deploying the Moloch v3 fallback or any custom guild contract, this guide covers the deployment flow (Hardhat / Foundry + Base RPC). Evaluate before Day 1 to confirm the fallback path (deploying Moloch v3 directly) works end-to-end on Base Sepolia. |

---

## 7. EAS — Ethereum Attestation Service

**Role in GuildOS:** The third-party attestation layer for agent reputation. EAS allows independent verifiers to publish on-chain claims about an agent's delivery history, identity, or capability quality — claims that are more trustworthy than self-declared reputation. In the Identity / Capability direction, EAS attestations are one of the multi-signal inputs to agent trust evaluation. In the MVP, EAS is used for the Specialist Agent's reputation read; in post-hackathon iterations it becomes the mechanism for independent auditors to attest to delivered work.

**Why it belongs here:** EAS is directly referenced in the direction deep-dive as the attestation infrastructure that distinguishes verified reputation from self-declared reputation. The Specialist Agent's ERC-8004 profile may reference EAS attestations. Reviewing the EAS schema and read API is required to understand what "verified reputation" looks like in practice — even if EAS writes are deferred to post-hackathon.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| EAS Documentation | https://docs.attest.org | Overview of the EAS schema model, attestation creation, and revocation. Evaluate how an attestation schema for a GuildOS delivery record would be structured: issuer (guild contract), subject (agent address), claim (task type, deliverable hash, acceptance timestamp). |
| EAS Explorer (Base) | https://base.easscan.org | The live attestation explorer for Base. Search for existing agent-related attestation schemas to evaluate whether compatible schemas already exist that GuildOS can read — avoiding the need to deploy a new schema during the hackathon. |
| EAS SDK | https://github.com/ethereum-attestation-service/eas-sdk | The TypeScript SDK for reading and creating attestations. Run a read query against an existing schema to validate that EAS on Base is live and queryable before building the reputation display in the demo UI. |
| EAS Attestation in agent-trust-and-reputation wiki | `knowledge-base/AIxWeb3/wiki/agent-trust-and-reputation.md` | The wiki page covering how EAS attestations feed into agent trust scoring: evaluator trustworthiness, task-type-specific reputation, and the difference between self-declared and third-party-verified reputation. Use this to design the trust display logic in the demo UI — what to show, how to weight it, and what absence of attestations means. |

---

## 8. Snapshot GraphQL API (Governance Integration — Secondary Direction)

**Role in GuildOS:** Secondary direction reference. GuildOS's primary governance layer is AgentFightClub (Moloch v3). Snapshot is relevant as an extension path: once a guild is operating, a governance brief agent for the guild's own decision-making (member approval rationale, mandate amendments, dispute resolution briefs) maps directly to the Governance / Coordination secondary direction. For the MVP, Snapshot is the prototype entry point for any governance summarization feature.

**Why it belongs here:** The Governance direction deep-dive establishes Snapshot as the lowest-barrier entry point for a working governance tool — no contracts to deploy, public GraphQL API, no authentication required. If any governance-facing feature needs to be demonstrated in the hackathon (even as an extension), Snapshot is the data source. Reviewing the API before the build week confirms what is achievable without additional setup time.

### Resources

| Resource | URL | What it helps you evaluate |
|---|---|---|
| Snapshot GraphQL API | https://docs.snapshot.box/graphql | The full API reference for querying proposals, vote tallies, spaces, and strategies. Evaluate whether the three most relevant data fields for a governance brief (proposal body, current vote tally, discussion thread link) are all accessible without authentication — they are, which confirms Snapshot as a zero-setup data source. |
| Snapshot Docs | https://docs.snapshot.box/ | Overview of spaces, proposals, strategies, and delegation. Evaluate how Snapshot's off-chain voting model connects to on-chain execution via Governor contracts — the boundary between Snapshot (off-chain signal) and Governor (on-chain enforcement) is the key design question for any governance feature in GuildOS. |
| OpenZeppelin Governor Documentation | https://docs.openzeppelin.com/contracts/5.x/api/governance | On-chain governance contract architecture. Relevant for understanding the proposal lifecycle state machine (`Pending → Active → Succeeded → Queued → Executed`) and the timelock pattern that enforces a human confirmation delay between vote success and treasury execution. This is the on-chain equivalent of AgentFightClub's `vote → settle` confirmation gate. |
| Governance direction deep-dive | `tasks/directions/02-governance-coordination.md` | The full governance direction analysis: flowchart, scenario, counterexample, risk inventory, and one-week validation plan. Use this as the design reference for any governance brief feature added to GuildOS — it defines the mandatory output schema fields (summary, for/against arguments, open questions, source tags) and the read-only architectural constraint that prevents the agent from initiating governance actions. |

---

## Reading Priority for Build Week

| Day | Resource to review |
|---|---|
| Pre-hackathon | AgentFightClub how-it-works + Moloch v3 quickstart (validate API stability) |
| Pre-hackathon | GLM-5.1 API quickstart + run 3 test tasks (pick the best-performing task type) |
| Pre-hackathon | Cobo Agentkit quickstart + fund Base Sepolia wallets |
| Day 1 | ERC-8004 EIP + 8004scan API (design agent profiles, validate read API) |
| Day 1 | A2A spec 0.3.0 + run reference examples (lock down the task message schema) |
| Day 2 | ERC-8183 EIP (design the deliverable hash → settlement flow) |
| Day 3 | Base Sepolia deployment + Basescan verification (validate the on-chain proof loop) |
| Day 4+ | EAS SDK read queries (populate trust display; defer write attestations to post-hackathon) |
| If needed | Snapshot GraphQL (governance brief extension, if time allows) |

---

*Built: 2026-06-02 | Agent: Sensei (Claude via Cowork) | Sources: PROJECT_PROPOSAL.md · directions/01-identity-capability.md · directions/02-governance-coordination.md · PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md · TRACK_SELECTION.md*
