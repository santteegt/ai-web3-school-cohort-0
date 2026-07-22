---
okf_version: "0.1"
---

# Wiki Index

_Last updated: 2026-07-21 — 269 pages (249 concept/topic + 20 source)_

---

## Topics (Overview Pages)

- [AI Foundations Overview](ai-foundations-overview.md) — Full map of AI Foundations concepts: LLM, Prompt, Context, RAG, Agent, Frameworks, MCP
- [AI Frameworks Overview](ai-frameworks-overview.md) — Framework selection, LangChain/LangGraph/DSPy/Hermes comparison, three-layer responsibility model
- [AI × Web3 Bridge Overview](aixweb3-bridge-overview.md) — The intersection layer: where AI agents meet on-chain systems; 15 bridge chapters
- [Frontier Exploration Overview](frontier-exploration-overview.md) — Hackathon tracks: Agentic Commerce, Wallet/Permission, AI Security, Governance, Dev Tooling

---

## Sources

- [AI Fundamentals - Introduction](sources/ai-fundamentals-introduction.md) — Module A bootcamp notes: LLM basics, control layers, agent components
- [LLMs](sources/llms.md) — LLMs mental model: tokens, embeddings, transformers, hallucination
- [Context](sources/context.md) — Context as information governance: five-layer model, context engineering
- [Prompt](sources/prompt.md) — Prompt as communication protocol: four-segment structure, security principles
- [RAG](sources/rag.md) — RAG as evidence chain: chunking, vector DB, retrieval, citations
- [AIxWeb3 School](sources/aixweb3-school.md) — Handbook outline: four-layer learning map
- [Program Structure](sources/program-structure.md) — Four-week bootcamp structure and deliverables
- [Agent](sources/agent.md) — Agent as constrained execution loop: planning, state, reflection, AI × Web3 architecture
- [Frameworks](sources/frameworks.md) — Framework selection, LangChain/LangGraph/OpenAI SDK/DSPy/Hermes, learning agents
- [MCP](sources/mcp.md) — MCP architecture: client/server split, tool schemas, permission model
- [Vibe Coding](sources/vibe-coding.md) — AI coding as disciplined human-AI iteration; engineering discipline requirements
- [Evaluation](sources/evaluation.md) — Eval pipeline: harness, golden set, LLM-as-judge, regression, observability; AI × Web3 eval requirements
- [Fine Tuning](sources/fine-tuning.md) — Fine-tuning: SFT, LoRA, PEFT, dataset quality, overfitting; AI × Web3 use cases
- [Inference](sources/inference.md) — Inference layer: API vs. local models, quantization, serving, audit requirements
- [Web3 Fundamentals - Introduction](sources/web3-fundamentals-introduction.md) — Module B: accounts, wallets, signatures, gas, smart contracts, account abstraction
- [Web3 Chapters](sources/web3-chapters.md) — Comprehensive Web3 handbook: cryptography, wallet, smart contract, dev stack, network, AA, DeFi, oracle, indexing, security
- [AIxWeb3 Bridge - Introduction](sources/aixweb3-bridge-introduction.md) — AI × Web3 Bridge introduction: 6 directions, 15 chapters, protocols (x402, MPP, ERC-8004, ERC-8183, ERC-7702, MCP, A2A)
- [AIxWeb3 - Problem Space & Direction Map](sources/aixweb3-problem-space-direction-map.md) — Direction evaluation matrix, deep exploration paths, counterexamples per direction
- [AIxWeb3 Project - Unified Evaluation Framework](sources/aixweb3-unified-evaluation-framework.md) — 7-question cross-direction evaluation standard for any AI × Web3 project
- [AIxWeb3 Bridge Chapters](sources/bridge-chapters.md) — 15 detailed handbook chapters: full AI × Web3 Bridge stack from on-chain context to decentralized AI

---

## Concepts — AI Foundations: LLM

- [Large Language Model (LLM)](large-language-model.md) — Probabilistic text generator; reasoning layer, not truth source
- [Tokens](tokens.md) — Processing unit; affects context capacity, cost, and completeness
- [Embeddings](embeddings.md) — Semantic vector representations; good for retrieval, not correctness judgments
- [Transformer Architecture](transformer-architecture.md) — Attention-based architecture; pattern composition without ground-truth authority
- [Hallucination](hallucination.md) — Confident fabrication; requires external verification, not just better prompts
- [Multimodal](multimodal.md) — Models processing text, images, audio, and video
- [MaaS (Model-as-a-Service)](maas.md) — API-based model access; per-token billing, no GPU required
- [Fine-Tuning](fine-tuning.md) — Adapting a pre-trained model for a class of tasks; not a first resort
- [Supervised Fine-Tuning (SFT)](supervised-fine-tuning.md) — SFT: input/output pair training for fixed-format tasks
- [LoRA (Low-Rank Adaptation)](lora.md) — Low-Rank Adaptation: parameter-efficient fine-tuning via adapter matrices
- [PEFT (Parameter-Efficient Fine-Tuning)](peft.md) — Parameter-Efficient Fine-Tuning: class of methods adapting models with minimal parameter changes
- [Overfitting](overfitting.md) — Model memorizes training data; detected by eval on held-out test sets
- [Inference](inference.md) — Production layer delivering model outputs under latency, cost, and quality constraints
- [Local Model](local-model.md) — Self-hosted model weights for privacy, cost control, or customization
- [Quantization](quantization.md) — Reducing weight precision to lower VRAM and latency; quality tradeoff
- [Model Serving](model-serving.md) — Infrastructure for production model inference: queuing, batching, monitoring, scaling

---

## Concepts — AI Foundations: Context

- [Context Window](context-window.md) — Token-bounded working memory; longer ≠ better focus
- [Context Engineering](context-engineering.md) — Designing what information enters the model at the right layer
- [Five-Layer Agent Context](five-layer-agent-context.md) — Instruction / Task / Fact / Knowledge / Memory layers
- [Information Governance](information-governance.md) — Labeling context by source, freshness, permission, trust level
- [Agent Memory](agent-memory.md) — Cross-session persistence; must be revocable; cannot replace authorization
- [Knowledge Base (AI)](knowledge-base.md) — External knowledge repository; requires source, version, deprecation tracking

---

## Concepts — AI Foundations: Prompt

- [Prompt Design](prompt-design.md) — Interface between user and model; executable communication protocol
- [Instruction (Prompt Design)](instruction.md) — Task rule for model: role, goal, prohibitions, uncertainty, format
- [Four-Segment Prompt Structure](four-segment-prompt.md) — Task Goal / Available Inputs / Prohibited Behaviors / Output Format
- [Four Control Layers](four-control-layers.md) — Context window, system instructions, prompt, tool calling
- [Few-Shot Prompting](few-shot-prompting.md) — Example-based guidance; carries maintenance cost
- [Structured Output](structured-output.md) — Schema-constrained output; makes LLM output machine-processable
- [Prompt Injection](prompt-injection.md) — Adversarial content overriding system instructions; defense via zone isolation
- [Verification Chain](verification-chain.md) — Six-layer defense: prompt → context → model → code → guard → human

---

## Concepts — AI Foundations: RAG

- [Retrieval-Augmented Generation (RAG)](retrieval-augmented-generation.md) — Evidence chain: retrieve, filter, cite, bound answers to sources
- [Chunking](chunking.md) — Document splitting; preserve source URL, heading path, version per chunk
- [Vector Database](vector-database.md) — Embedding storage + metadata; filter first, then rank
- [Retriever](retriever.md) — Candidate selection; hybrid approaches outperform pure vector search
- [Re-ranking](re-ranking.md) — Post-retrieval quality ordering; adds latency/cost tradeoff
- [Citations (RAG)](citations.md) — Source traceability; user verification entry point

---

## Concepts — AI Foundations: Evaluation

- [Evaluation (AI Systems)](evaluation.md) — Disciplined practice of measuring AI system reliability with samples, metrics, and regression
- [Eval Harness](eval-harness.md) — Repeatable framework feeding samples, calling system, running graders, recording results
- [Golden Set](golden-set.md) — Curated sample set covering real tasks, boundary cases, and historical bugs
- [LLM-as-Judge](llm-as-judge.md) — LLM grading open-ended outputs; useful but requires calibration against human scoring
- [Regression Testing (AI)](regression-testing.md) — Converting known bugs into tests that rerun before every release
- [Observability (AI Systems)](observability.md) — Recording real-user behavior at runtime to feed back into the eval pipeline

---

## Concepts — AI Foundations: Agent

- [AI Agent](ai-agent.md) — Constrained execution loop: goal, tools, state, permissions, stop conditions
- [Prompt / Workflow / Agent Boundary](prompt-workflow-agent-boundary.md) — Three architectures with different failure modes
- [Tool Calling](tool-calling.md) — Model-to-world action mechanism; requires tool design discipline
- [State Management (Agent)](state-management.md) — Externalized, queryable, recoverable, auditable agent state
- [Agent Planning](agent-planning.md) — Candidate plan generation; step classification as read/write; not an authorization
- [Agent Reflection](agent-reflection.md) — Self-checking for intermediate correction; not a substitute for deterministic checks
- [Agent Stop Conditions](agent-stop-conditions.md) — Explicit halting criteria: goal reached, budget exceeded, risk crossed
- [Multi-Agent Systems](multi-agent-systems.md) — Coordination patterns; amplifies failures when roles are unclear
- [MCP (Model Context Protocol)](mcp.md) — Unified tool connectivity protocol; client/server architecture
- [MCP Server](mcp-server.md) — Exposes resources, tools, prompts; defines permission model
- [MCP Client](mcp-client.md) — Connects model to servers; handles discovery, confirmation, session isolation
- [Tool Schema](tool-schema.md) — Machine-readable tool declaration; vague schemas cause wrong-parameter calls
- [MCP Permission Model](mcp-permission-model.md) — Permission design per tool risk level; the most underestimated MCP issue
- [Guardrails](guardrails.md) — Hard execution constraints; code-enforced, not prompt-enforced
- [Agent Handoff](agent-handoff.md) — Control transfer after subtask completes
- [Agent Tracing](ai-agent-tracing.md) — Execution chain observability; debugging and audit
- [Vibe Coding](vibe-coding.md) — AI-assisted rapid prototyping; requires engineering discipline
- [AI Coding](ai-coding.md) — AI coding in the full engineering flow: issue → branch → commit → test → review → merge

---

## Concepts — AI Foundations: Frameworks

- [LangChain](langchain.md) — Component library for composing AI capabilities; good for prototyping
- [LangGraph](langgraph.md) — DAG-based stateful workflows; reference for explicit state management
- [OpenAI Agents SDK](openai-agents-sdk.md) — Agent engineering primitives: handoffs, guardrails, tracing, structured output
- [DSPy](dspy.md) — Metric-driven prompt optimization; treats pipelines as optimizable programs
- [Hermes](hermes.md) — Tool-calling and structured-output oriented model ecosystem
- [Learning Agents](learning-agents.md) — Systems that improve via evaluation loop, not direct online behavior change

---

## Concepts — AI × Web3 Bridge: Directions & Framework

- [Direction Evaluation Matrix](direction-evaluation-matrix.md) — 5-criteria matrix for bridge direction selection: structural demand, verifiability, minimal entry point, risk boundaries, follow-through
- [Deep Exploration Paths](deep-exploration-paths.md) — Structured decomposition templates per bridge direction (Payment→Protocol, Identity→Collaboration, Wallet→Recoverable Execution, Privacy→Security Boundaries, Governance→Verifiable Coordination)
- [Unified Evaluation Framework (AI × Web3 Projects)](unified-evaluation-framework.md) — 7 cross-direction evaluation questions applied to any AI × Web3 project direction
- [Payment and Commerce (AI × Web3)](payment-and-commerce.md) — Full commercial loop direction: pricing, payment, settlement, subscription, receipt on-chain
- [Identity, Reputation, and Capability (AI × Web3)](identity-reputation-capability.md) — Agent authentication, capability registration, and cross-service trust direction (MCP, A2A, ERC-8004)
- [Wallet, Permission, and Safe Execution (AI × Web3)](wallet-permission-safe-execution.md) — Delegated signing with bounded authority: session keys, policy guards, ERC-7702, Cobo CAW Pact
- [Privacy, Security, and Sovereignty (AI × Web3)](privacy-security-sovereignty.md) — AI data boundary design combined with Web3 cryptographic guarantees: ZK, TEE, minimal disclosure
- [Dev Tooling and Agent Workflow (AI × Web3)](dev-tooling-agent-workflow.md) — AI improving Web3 developer workflows: code generation, audit, simulation, deployment automation
- [Governance, Coordination, and Public Goods (AI × Web3)](governance-coordination-public-goods.md) — DAO participation + contribution intelligence: proposal summaries, voting assistance, budget verification
- [Cobo CAW Pact (Task-Level Authorization)](cobo-pact.md) — Task-level authorization model: temporary bounded permissions (budget + scope + time window + failure handling)

---

## Concepts — AI × Web3 Bridge: Overview & Standards

- [AI × Web3 Bridge Overview](aixweb3-bridge-overview.md) — Bridge intersection layer overview; 15 chapters; 6 directions
- [AI × Web3 Agent Architecture](aixweb3-agent-architecture.md) — 8-step reference pattern: goal → plan → read/write split → policy → simulation → confirmation → execution → log
- [ERC-7702](erc-7702.md) — EIP allowing EOAs to temporarily adopt smart-account capabilities for one transaction
- [ERC-8183](erc-8183.md) — Payment channel standard for AI agent on-chain micropayments and subscriptions
- [ERC-8004](erc-8004.md) — On-chain agent capability registry: verifiable service endpoints and capability declarations

---

## Concepts — AI × Web3 Bridge: Chain-aware Context

- [Chain-aware Context](chain-aware-context.md) — Live on-chain state, contract metadata, and transaction history in agent context
- [On-chain Data](on-chain-data.md) — Raw blockchain state: balances, storage, logs, events used as agent context
- [Contract Docs](contract-docs.md) — ABI, NatSpec comments, and parameter explanations injected into agent context
- [Transaction History](transaction-history.md) — Historical wallet activity providing behavioral patterns for agent reasoning
- [Explorer Context](explorer-context.md) — Block explorer data (Etherscan/Blockscout) formatted for agent consumption
- [Indexing Context](indexing-context.md) — Subgraph and indexed event data enabling rich semantic queries from agents

---

## Concepts — AI × Web3 Bridge: Web3 Tool Use

- [Web3 Tool Use](web3-tool-use.md) — RPC, wallet, contract, and DeFi tools called by AI agents
- [RPC Tool](rpc-tool.md) — JSON-RPC call wrapper exposing eth_call, eth_getLogs, and related reads to agents
- [Contract Read](contract-read.md) — Read-only contract call tool: view/pure functions, no gas, no signing required
- [Contract Write](contract-write.md) — State-changing contract call tool: requires signing, simulation, and confirmation
- [Wallet Tool](wallet-tool.md) — Wallet balance, token holdings, and allowance query tools for agent context
- [DeFi Tool](defi-tool.md) — DeFi protocol interaction tools: swap quotes, lending positions, liquidity data
- [Tool Permission](tool-permission.md) — Per-tool risk classification and access control; narrow interfaces reduce blast radius
- [Tool Log](tool-log.md) — Structured logging of all tool inputs, outputs, and errors for audit and debugging

---

## Concepts — AI × Web3 Bridge: Agent Workflow

- [Agent Workflow](agent-workflow.md) — Automation boundaries, human-in-the-loop design, and execution orchestration
- [Task Graph](task-graph.md) — Directed acyclic graph of subtasks with dependencies; enables parallel and conditional execution
- [Human-in-the-loop](human-in-the-loop.md) — Mandatory human confirmation gates for irreversible, high-value, or ambiguous actions
- [Retry / Fallback](retry-fallback.md) — Error recovery logic: retry with backoff, degrade gracefully, or escalate to human
- [Trace](trace.md) — Per-task execution record: steps, tool calls, decisions, timing; primary debugging artifact
- [Regression Set](regression-set.md) — Curated failure cases that are re-run after every system change to prevent regressions

---

## Concepts — AI × Web3 Bridge: Agent Wallet

- [Agent Wallet](agent-wallet.md) — Delegated wallet with spending limits, session keys, policy guards, and revocation
- [AA Wallet (Account Abstraction Wallet)](aa-wallet.md) — Account-abstraction wallet used by AI agents: programmable auth, gas sponsorship
- [Policy (Agent Wallet)](policy.md) — Rule set attached to agent wallet: allowed contracts, amount limits, time windows
- [Guard (Agent Wallet)](guard.md) — On-chain or off-chain enforcement point that rejects policy-violating transactions
- [Simulation (Transaction)](simulation.md) — Pre-execution sandbox run of a transaction to verify outcome before signing
- [Revocation](revocation.md) — Mechanism to cancel session keys, permissions, or approvals; critical for agent safety
- [Human Check](human-check.md) — Explicit human approval step for transactions above risk threshold

---

## Concepts — AI × Web3 Bridge: Machine Payment

- [Machine Payment](machine-payment.md) — Autonomous micropayments and on-chain settlement for agent-to-agent commerce
- [Stablecoin Payment](stablecoin-payment.md) — Using USDC/USDT/DAI for AI agent payments; avoids volatility risk
- [Budget (Agent Payment)](budget.md) — Allocated spending limit for an agent task; prevents runaway costs
- [Quote (Machine Payment)](quote.md) — Price estimate returned before execution; agent accepts or rejects before spending
- [Payment Intent](payment-intent.md) — Off-chain payment commitment that becomes binding once signed
- [x402](x402.md) — HTTP 402-based payment protocol for AI agents to pay API calls inline
- [MPP (Machine Payments Protocol)](mpp.md) — Machine Payment Protocol: open standard for agent-to-agent micropayments
- [Subscription (Machine Payment)](subscription.md) — Recurring on-chain payment stream for agent services; time or usage based
- [Micropayment](micropayment.md) — Sub-cent payments enabled by L2s and payment channels; viable for per-call billing

---

## Concepts — AI × Web3 Bridge: Settlement & Escrow

- [Settlement & Escrow](settlement-and-escrow.md) — Completing the payment loop: delivery proof, dispute resolution, fund release
- [Escrow](escrow.md) — Smart contract holding funds until delivery conditions are met
- [Receipt](receipt.md) — On-chain or signed record of completed payment and service delivery
- [Delivery Proof](delivery-proof.md) — Verifiable evidence that a service was delivered as specified (hash, signature, log)
- [Acceptance](acceptance.md) — Buyer confirmation that delivery meets spec; triggers fund release from escrow
- [Refund](refund.md) — Return of escrowed funds when delivery fails, times out, or dispute is resolved for buyer
- [Dispute](dispute.md) — Challenge mechanism when acceptance is withheld; requires arbitration or on-chain resolution
- [Evaluator](evaluator.md) — Third-party or automated system judging whether delivery meets acceptance criteria

---

## Concepts — AI × Web3 Bridge: Agent Identity

- [Agent Identity](agent-identity.md) — Agent identification, authentication, authorization, and accountability
- [Agent Profile](agent-profile.md) — Structured description of an agent: name, capabilities, endpoints, public key
- [Capability (Agent)](capability.md) — Declared service an agent can perform; referenced in identity and trust contexts
- [Service Endpoint](service-endpoint.md) — URL or on-chain address where an agent's capabilities are accessible
- [Registry (Agent)](registry.md) — On-chain or off-chain catalog mapping agent identities to profiles and capabilities
- [DID / VC (Decentralized Identity & Verifiable Credentials)](did-vc.md) — Decentralized Identifiers and Verifiable Credentials for agent authentication
- [A2A Protocol (Agent-to-Agent)](a2a-protocol.md) — Agent-to-Agent protocol for cross-service agent discovery and task handoff
- [Ownership (Agent Identity)](ownership.md) — Attribution of agent actions to a human or organization; liability and accountability

---

## Concepts — AI × Web3 Bridge: Agent Trust & Reputation

- [Agent Trust & Reputation](agent-trust-and-reputation.md) — Verifiable behavior-based trust: not a single score but layered evidence bound to identity
- [Reputation (Agent)](reputation.md) — Aggregated past-behavior signal used to inform task delegation and risk assessment
- [Review (Agent Reputation)](review.md) — Structured post-task evaluation by service consumer; input to reputation systems
- [Attestation](attestation.md) — Cryptographic statement by a verifier about an agent's capability or behavior
- [Stake (Agent Reputation)](stake.md) — Deposited collateral that creates skin-in-the-game for honest agent behavior
- [Slashing](slashing.md) — Penalty mechanism that burns stake when provably malicious behavior is detected
- [Validation (Agent)](validation.md) — Independent verification of agent output before it affects on-chain state

---

## Concepts — AI × Web3 Bridge: AI Oracle

- [AI Oracle](ai-oracle.md) — AI model outputs published on-chain for contract use; requires verifiability
- [AI Output (Oracle)](ai-output.md) — Raw LLM inference result before on-chain publishing; needs format + proof wrapper
- [Data Feed (AI Oracle)](data-feed.md) — Structured on-chain data stream (prices, events, scores) from AI oracle systems
- [Model Result](model-result.md) — Specific AI inference outcome (classification, score, summary) for on-chain use
- [Proof of Inference](proof-of-inference.md) — Cryptographic proof that output came from a specific model and input (TEE/ZK/signed log)
- [Dispute / Challenge (AI Oracle)](dispute-challenge.md) — On-chain mechanism to challenge an oracle result within a time window

---

## Concepts — AI × Web3 Bridge: Verifiable AI

- [Verifiable AI](verifiable-ai.md) — Proving model inputs, execution environment, and outputs when they affect on-chain state
- [TEE (Trusted Execution Environment)](tee.md) — Trusted Execution Environment: hardware-isolated inference with remote attestation
- [ZK (Zero-Knowledge Proofs)](zk.md) — Zero-knowledge proofs: verifiable computation without revealing inputs
- [zkML](zkml.md) — ZK applied to ML inference: proving model execution; hybrid approaches for large models
- [Verifiable Compute](verifiable-compute.md) — Off-chain computation whose results can be verified by on-chain or third parties
- [Benchmark (AI × Web3)](benchmark.md) — Task-specific eval set including attack, boundary, and wrong-chain samples for model comparison
- [Audit Trail](audit-trail.md) — Persistent, tamper-evident log of inputs, outputs, model version, and confirmations

---

## Concepts — AI × Web3 Bridge: AI Security

- [AI Security](ai-security.md) — Defense against prompt injection, tool abuse, permission escalation, and key exposure
- [Tool Abuse](tool-abuse.md) — Misuse of agent tools by malicious input or confused-deputy attacks
- [Malicious Context](malicious-context.md) — Attacker-controlled data in agent context that attempts to hijack behavior
- [Key Safety](key-safety.md) — Practices ensuring private keys and seed phrases never reach AI agent context
- [Permission Isolation](permission-isolation.md) — Separating read/write/sign capabilities into distinct, narrowly scoped tools
- [Sandbox](sandbox.md) — Isolated execution environment preventing malicious input from accessing secrets
- [Audit Log](audit-log.md) — Security-oriented persistent record of agent decisions, tool calls, and confirmations
- [Alert (Agent Security)](alert.md) — Real-time notification of anomalous agent behavior or policy violations

---

## Concepts — AI × Web3 Bridge: AI Privacy

- [AI Privacy](ai-privacy.md) — Data boundary design, minimal disclosure, local-first processing, private memory management
- [Data Boundary](data-boundary.md) — Explicit rules about what data can flow into AI context and what must stay local
- [Local AI](local-ai.md) — Running models on-device or in private infrastructure to prevent data leaving the boundary
- [Private Memory](private-memory.md) — Agent memory partitioned by user; not shared across users or sessions
- [Secret Management](secret-management.md) — Secure storage and retrieval of credentials, keys, and sensitive config for agents
- [Minimal Disclosure](minimal-disclosure.md) — Sharing only the data required for a task; ZK and selective disclosure enable this
- [Encrypted Data](encrypted-data.md) — Data encrypted before entering AI pipelines; agent works on ciphertext or TEE
- [User Consent](user-consent.md) — Explicit approval before agent accesses, stores, or transmits personal data

---

## Concepts — AI × Web3 Bridge: AI Sovereignty

- [AI Sovereignty](ai-sovereignty.md) — User control over AI models, data, and execution; resistance to platform lock-in
- [User Control](user-control.md) — User ability to inspect, modify, pause, or delete agent behavior and stored data
- [Data Portability](data-portability.md) — Right and ability to export personal data and agent memory to other systems
- [Model Choice](model-choice.md) — User selection of model provider, version, or local deployment without lock-in
- [Local-first AI](local-first-ai.md) — Processing and storing data locally before any cloud sync; privacy-preserving default
- [Censorship Resistance](censorship-resistance.md) — Architectural resistance to being shut down, blocked, or deplatformed
- [d/acc (Defensive Accelerationism)](dacc.md) — Defensive Accelerationism: open-source, distributed development as sovereignty strategy
- [CROPS](crops.md) — Cryptographic Rights and Ownership for Personal Sovereignty; on-chain data rights framework

---

## Concepts — AI × Web3 Bridge: Governance AI

- [Governance AI](governance-ai.md) — AI improving proposal analysis, contribution tracking, and budget verification in DAOs
- [Proposal Summary (Governance AI)](proposal-summary.md) — AI-generated summary of governance proposals with source links for human verification
- [Meeting Action](meeting-action.md) — AI extraction of action items from meeting transcripts with attribution and due dates
- [Contribution Graph](contribution-graph.md) — Verified record of contributor participation, output, and impact over time
- [Budget Check (Governance AI)](budget-check.md) — Automated verification that proposed spending aligns with on-chain treasury and prior votes
- [Source Traceability](source-traceability.md) — Linking every AI governance claim back to the original on-chain or off-chain source
- [Deep Funding](deep-funding.md) — Retroactive public goods funding informed by verifiable contribution data
- [Plurality](plurality.md) — Governance mechanism combining quadratic voting, identity, and consent for fair resource allocation

---

## Concepts — AI × Web3 Bridge: Decentralized AI

- [Decentralized AI](decentralized-ai.md) — Open markets for models, data, and compute; inference networks without central control
- [Model Market](model-market.md) — Marketplace for discovering, comparing, and licensing AI models on-chain
- [Data Market](data-market.md) — Marketplace for buying, selling, and licensing training or inference data with provenance
- [Compute Market](compute-market.md) — Decentralized GPU/compute marketplace for running AI inference and training jobs
- [Inference Network](inference-network.md) — Distributed network of nodes serving AI model inference with verifiable outputs
- [Model Routing](model-routing.md) — Dynamic selection of the best model for a task based on cost, quality, and latency
- [Quality Benchmark (Decentralized AI)](quality-benchmark.md) — Standardized performance comparison enabling trustless model selection in markets

---

## Concepts — Web3 Foundations: Cryptography

- [Cryptography](cryptography.md) — Mathematical foundation of all Web3 security: hashing, asymmetric keys, signatures
- [Hash Function](hash-function.md) — One-way deterministic transform (SHA256/Keccak256); collision-resistant fingerprint
- [Public Key](public-key.md) — Shareable key derived from private key; Ethereum address = Keccak256(pubkey)[-20 bytes]
- [Private Key](private-key.md) — Root secret of a blockchain account; must never be exposed or given to AI agents
- [Cryptographic Signature](cryptographic-signature.md) — Proves key ownership without revealing it; authorizes specific on-chain actions
- [Merkle Tree](merkle-tree.md) — Binary hash tree enabling compact membership proofs; used in blocks and rollup proofs

---

## Concepts — Web3 Foundations: Wallet

- [Externally Owned Account (EOA)](eoa.md) — Externally Owned Account; key-pair controlled, no code, full control with private key
- [Mnemonic (Seed Phrase)](mnemonic.md) — BIP-39 seed phrase; generates all private keys in an HD wallet; never share
- [Web3 Transaction](web3-transaction.md) — Signed data package that changes on-chain state; 8-step execution flow
- [Gas](gas.md) — EVM computation unit; fees paid in ETH/gwei; EIP-1559 model; L2s dramatically cheaper
- [Block Explorer](block-explorer.md) — Read-only on-chain data interface; Etherscan for transactions, contracts, events

---

## Concepts — Web3 Foundations: Smart Contracts

- [Smart Contract](smart-contract.md) — Self-executing on-chain code; state and execution are public; immutable by default
- [Solidity](solidity.md) — Primary EVM smart contract language; compiled to bytecode; statically typed
- [EVM (Ethereum Virtual Machine)](evm.md) — Ethereum Virtual Machine; deterministic sandboxed runtime; basis for EVM-compatible chains
- [ABI (Application Binary Interface)](abi.md) — Application Binary Interface; JSON spec for encoding/decoding contract calls and events
- [Contract Event](contract-event.md) — Emitted logs in transaction receipts; primary input for indexers and frontends
- [Contract Upgrade](contract-upgrade.md) — Proxy patterns (transparent, UUPS) for replacing contract logic while preserving state

---

## Concepts — Web3 Foundations: Dev Stack

- [Web3 Dev Stack](web3-dev-stack.md) — Full toolchain: Remix → Hardhat/Foundry → OpenZeppelin → viem/wagmi
- [Remix IDE](remix-ide.md) — Browser-based Solidity IDE; fastest path from code to on-chain; no setup required
- [Hardhat](hardhat.md) — Node.js dev framework; compile, test (Chai/Mocha), deploy, verify; Hardhat Network
- [Foundry](foundry.md) — Rust-based dev framework; Forge (tests), Cast (CLI), Anvil (local node), fuzz testing
- [OpenZeppelin Contracts](openzeppelin.md) — Audited Solidity library: ERC-20, ERC-721, AccessControl, upgradeable proxies
- [viem / wagmi](viem-wagmi.md) — TypeScript/React libraries for on-chain reads and writes; modern ethers.js replacement

---

## Concepts — Web3 Foundations: Network

- [Blockchain Network](blockchain-network.md) — Distributed peer-to-peer ledger; canonical state via consensus; permissionless
- [Block](block.md) — Batch of transactions linked by parent hash; 12-second slot time on Ethereum PoS
- [Consensus](consensus.md) — Agreement mechanism for canonical chain state; PoW → PoS post-Merge
- [Proof of Stake (PoS)](proof-of-stake.md) — Ethereum's consensus: validators stake 32 ETH; randomly selected to propose blocks
- [Testnet](testnet.md) — Test network with valueless tokens; Sepolia/Holesky; always test here before mainnet
- [Layer 2 (L2)](layer-2.md) — Off-chain execution inheriting L1 security; 10–100x cheaper gas; Arbitrum, Base, zkSync
- [Rollup](rollup.md) — Dominant L2 architecture: batch transactions, post data + validity proof to L1

---

## Concepts — Web3 Foundations: Account Abstraction

- [ERC-4337 (Account Abstraction)](erc-4337.md) — Account abstraction standard: UserOperation mempool, EntryPoint, no protocol change
- [Smart Account](smart-account.md) — Contract wallet with programmable auth: multisig, social recovery, session keys
- [Bundler](bundler.md) — Collects UserOperations from alt mempool; submits batched EntryPoint transaction
- [Paymaster](paymaster.md) — Sponsors gas on behalf of users/agents; enables gasless UX or ERC-20 gas payments
- [Session Key](session-key.md) — Limited-scope key for AI agents: contract-scoped, amount-capped, time-bounded

---

## Concepts — Web3 Foundations: DeFi

- [DeFi (Decentralized Finance)](defi.md) — Permissionless on-chain financial protocols; composable, non-custodial, auditable
- [ERC-20 Token](erc20-token.md) — Standard fungible token interface; transfer, approve, allowance; EIP-2612 permit
- [AMM (Automated Market Maker)](amm.md) — Automated Market Maker; liquidity pool trading; introduces slippage, MEV, impermanent loss
- [DeFi Lending](defi-lending.md) — Over-collateralized borrowing/lending (Aave, Compound); liquidation risk
- [Stablecoin](stablecoin.md) — Price-pegged asset: fiat-backed (USDC), crypto-collateralized (DAI), algorithmic (FRAX)
- [Liquidity](liquidity.md) — Capital in pools enabling trades; LPs earn fees, bear impermanent loss

---

## Concepts — Web3 Foundations: Oracle

- [Oracle](oracle.md) — Bridge from off-chain data to on-chain contracts; decentralized networks solve trust
- [Price Feed](price-feed.md) — Real-time asset prices on-chain (Chainlink, Pyth); freshness verification critical
- [Oracle Risk](oracle-risk.md) — Manipulation, stale price, centralization risks; oracle attacks drain DeFi protocols

---

## Concepts — Web3 Foundations: Indexing

- [On-Chain Indexing](on-chain-indexing.md) — ETL from raw blockchain events to queryable structured databases
- [Subgraph (The Graph)](subgraph.md) — The Graph's indexing unit; manifest + mappings → GraphQL API over indexed events
- [RPC (Remote Procedure Call)](rpc.md) — JSON-RPC interface to blockchain nodes; `eth_call`, `eth_getLogs`, WebSocket subscriptions
- [Data Pipeline](data-pipeline.md) — Extract-Transform-Load pipeline from chain events to analytics/AI context
- [On-Chain Monitoring](on-chain-monitoring.md) — Real-time anomaly detection post-deployment; Forta, OpenZeppelin Defender

---

## Concepts — Web3 Foundations: Security

- [Web3 Security](web3-security.md) — Defensive practices: audits, static analysis, simulation, monitoring, defense-in-depth
- [Reentrancy](reentrancy.md) — Recursive call exploiting stale state; fixed by checks-effects-interactions + ReentrancyGuard
- [Access Control](access-control.md) — Role-based contract permissions; admin key compromise = full takeover
- [Contract Audit](contract-audit.md) — Expert security review before deployment; not a guarantee but essential gate
- [Transaction Simulation](tx-simulation.md) — Pre-execution sandbox verification; AI agents should simulate before signing

---

## Generated Outputs

- [concepts/](../concepts/) — filed-back Marp decks, diagrams, and other query outputs (not hash-tracked; see AGENTS.md's "answers can be filed back" idea)
