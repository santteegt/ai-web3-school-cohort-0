# Wiki Index

_Last updated: 2026-05-28 — 269 pages (249 concept/topic + 20 source)_

---

## Topics (Overview Pages)

- [[ai-foundations-overview]] — Full map of AI Foundations concepts: LLM, Prompt, Context, RAG, Agent, Frameworks, MCP
- [[ai-frameworks-overview]] — Framework selection, LangChain/LangGraph/DSPy/Hermes comparison, three-layer responsibility model
- [[aixweb3-bridge-overview]] — The intersection layer: where AI agents meet on-chain systems; 15 bridge chapters
- [[frontier-exploration-overview]] — Hackathon tracks: Agentic Commerce, Wallet/Permission, AI Security, Governance, Dev Tooling

---

## Sources

- [[sources/ai-fundamentals-introduction]] — Module A bootcamp notes: LLM basics, control layers, agent components
- [[sources/llms]] — LLMs mental model: tokens, embeddings, transformers, hallucination
- [[sources/context]] — Context as information governance: five-layer model, context engineering
- [[sources/prompt]] — Prompt as communication protocol: four-segment structure, security principles
- [[sources/rag]] — RAG as evidence chain: chunking, vector DB, retrieval, citations
- [[sources/aixweb3-school]] — Handbook outline: four-layer learning map
- [[sources/program-structure]] — Four-week bootcamp structure and deliverables
- [[sources/agent]] — Agent as constrained execution loop: planning, state, reflection, AI × Web3 architecture
- [[sources/frameworks]] — Framework selection, LangChain/LangGraph/OpenAI SDK/DSPy/Hermes, learning agents
- [[sources/mcp]] — MCP architecture: client/server split, tool schemas, permission model
- [[sources/vibe-coding]] — AI coding as disciplined human-AI iteration; engineering discipline requirements
- [[sources/evaluation]] — Eval pipeline: harness, golden set, LLM-as-judge, regression, observability; AI × Web3 eval requirements
- [[sources/fine-tuning]] — Fine-tuning: SFT, LoRA, PEFT, dataset quality, overfitting; AI × Web3 use cases
- [[sources/inference]] — Inference layer: API vs. local models, quantization, serving, audit requirements
- [[sources/web3-fundamentals-introduction]] — Module B: accounts, wallets, signatures, gas, smart contracts, account abstraction
- [[sources/web3-chapters]] — Comprehensive Web3 handbook: cryptography, wallet, smart contract, dev stack, network, AA, DeFi, oracle, indexing, security
- [[sources/aixweb3-bridge-introduction]] — AI × Web3 Bridge introduction: 6 directions, 15 chapters, protocols (x402, MPP, ERC-8004, ERC-8183, ERC-7702, MCP, A2A)
- [[sources/aixweb3-problem-space-direction-map]] — Direction evaluation matrix, deep exploration paths, counterexamples per direction
- [[sources/aixweb3-unified-evaluation-framework]] — 7-question cross-direction evaluation standard for any AI × Web3 project
- [[sources/bridge-chapters]] — 15 detailed handbook chapters: full AI × Web3 Bridge stack from on-chain context to decentralized AI

---

## Concepts — AI Foundations: LLM

- [[large-language-model]] — Probabilistic text generator; reasoning layer, not truth source
- [[tokens]] — Processing unit; affects context capacity, cost, and completeness
- [[embeddings]] — Semantic vector representations; good for retrieval, not correctness judgments
- [[transformer-architecture]] — Attention-based architecture; pattern composition without ground-truth authority
- [[hallucination]] — Confident fabrication; requires external verification, not just better prompts
- [[multimodal]] — Models processing text, images, audio, and video
- [[maas]] — API-based model access; per-token billing, no GPU required
- [[fine-tuning]] — Adapting a pre-trained model for a class of tasks; not a first resort
- [[supervised-fine-tuning]] — SFT: input/output pair training for fixed-format tasks
- [[lora]] — Low-Rank Adaptation: parameter-efficient fine-tuning via adapter matrices
- [[peft]] — Parameter-Efficient Fine-Tuning: class of methods adapting models with minimal parameter changes
- [[overfitting]] — Model memorizes training data; detected by eval on held-out test sets
- [[inference]] — Production layer delivering model outputs under latency, cost, and quality constraints
- [[local-model]] — Self-hosted model weights for privacy, cost control, or customization
- [[quantization]] — Reducing weight precision to lower VRAM and latency; quality tradeoff
- [[model-serving]] — Infrastructure for production model inference: queuing, batching, monitoring, scaling

---

## Concepts — AI Foundations: Context

- [[context-window]] — Token-bounded working memory; longer ≠ better focus
- [[context-engineering]] — Designing what information enters the model at the right layer
- [[five-layer-agent-context]] — Instruction / Task / Fact / Knowledge / Memory layers
- [[information-governance]] — Labeling context by source, freshness, permission, trust level
- [[agent-memory]] — Cross-session persistence; must be revocable; cannot replace authorization
- [[knowledge-base]] — External knowledge repository; requires source, version, deprecation tracking

---

## Concepts — AI Foundations: Prompt

- [[prompt-design]] — Interface between user and model; executable communication protocol
- [[instruction]] — Task rule for model: role, goal, prohibitions, uncertainty, format
- [[four-segment-prompt]] — Task Goal / Available Inputs / Prohibited Behaviors / Output Format
- [[four-control-layers]] — Context window, system instructions, prompt, tool calling
- [[few-shot-prompting]] — Example-based guidance; carries maintenance cost
- [[structured-output]] — Schema-constrained output; makes LLM output machine-processable
- [[prompt-injection]] — Adversarial content overriding system instructions; defense via zone isolation
- [[verification-chain]] — Six-layer defense: prompt → context → model → code → guard → human

---

## Concepts — AI Foundations: RAG

- [[retrieval-augmented-generation]] — Evidence chain: retrieve, filter, cite, bound answers to sources
- [[chunking]] — Document splitting; preserve source URL, heading path, version per chunk
- [[vector-database]] — Embedding storage + metadata; filter first, then rank
- [[retriever]] — Candidate selection; hybrid approaches outperform pure vector search
- [[re-ranking]] — Post-retrieval quality ordering; adds latency/cost tradeoff
- [[citations]] — Source traceability; user verification entry point

---

## Concepts — AI Foundations: Evaluation

- [[evaluation]] — Disciplined practice of measuring AI system reliability with samples, metrics, and regression
- [[eval-harness]] — Repeatable framework feeding samples, calling system, running graders, recording results
- [[golden-set]] — Curated sample set covering real tasks, boundary cases, and historical bugs
- [[llm-as-judge]] — LLM grading open-ended outputs; useful but requires calibration against human scoring
- [[regression-testing]] — Converting known bugs into tests that rerun before every release
- [[observability]] — Recording real-user behavior at runtime to feed back into the eval pipeline

---

## Concepts — AI Foundations: Agent

- [[ai-agent]] — Constrained execution loop: goal, tools, state, permissions, stop conditions
- [[prompt-workflow-agent-boundary]] — Three architectures with different failure modes
- [[tool-calling]] — Model-to-world action mechanism; requires tool design discipline
- [[state-management]] — Externalized, queryable, recoverable, auditable agent state
- [[agent-planning]] — Candidate plan generation; step classification as read/write; not an authorization
- [[agent-reflection]] — Self-checking for intermediate correction; not a substitute for deterministic checks
- [[agent-stop-conditions]] — Explicit halting criteria: goal reached, budget exceeded, risk crossed
- [[multi-agent-systems]] — Coordination patterns; amplifies failures when roles are unclear
- [[mcp]] — Unified tool connectivity protocol; client/server architecture
- [[mcp-server]] — Exposes resources, tools, prompts; defines permission model
- [[mcp-client]] — Connects model to servers; handles discovery, confirmation, session isolation
- [[tool-schema]] — Machine-readable tool declaration; vague schemas cause wrong-parameter calls
- [[mcp-permission-model]] — Permission design per tool risk level; the most underestimated MCP issue
- [[guardrails]] — Hard execution constraints; code-enforced, not prompt-enforced
- [[agent-handoff]] — Control transfer after subtask completes
- [[ai-agent-tracing]] — Execution chain observability; debugging and audit
- [[vibe-coding]] — AI-assisted rapid prototyping; requires engineering discipline
- [[ai-coding]] — AI coding in the full engineering flow: issue → branch → commit → test → review → merge

---

## Concepts — AI Foundations: Frameworks

- [[langchain]] — Component library for composing AI capabilities; good for prototyping
- [[langgraph]] — DAG-based stateful workflows; reference for explicit state management
- [[openai-agents-sdk]] — Agent engineering primitives: handoffs, guardrails, tracing, structured output
- [[dspy]] — Metric-driven prompt optimization; treats pipelines as optimizable programs
- [[hermes]] — Tool-calling and structured-output oriented model ecosystem
- [[learning-agents]] — Systems that improve via evaluation loop, not direct online behavior change

---

## Concepts — AI × Web3 Bridge: Directions & Framework

- [[direction-evaluation-matrix]] — 5-criteria matrix for bridge direction selection: structural demand, verifiability, minimal entry point, risk boundaries, follow-through
- [[deep-exploration-paths]] — Structured decomposition templates per bridge direction (Payment→Protocol, Identity→Collaboration, Wallet→Recoverable Execution, Privacy→Security Boundaries, Governance→Verifiable Coordination)
- [[unified-evaluation-framework]] — 7 cross-direction evaluation questions applied to any AI × Web3 project direction
- [[payment-and-commerce]] — Full commercial loop direction: pricing, payment, settlement, subscription, receipt on-chain
- [[identity-reputation-capability]] — Agent authentication, capability registration, and cross-service trust direction (MCP, A2A, ERC-8004)
- [[wallet-permission-safe-execution]] — Delegated signing with bounded authority: session keys, policy guards, ERC-7702, Cobo CAW Pact
- [[privacy-security-sovereignty]] — AI data boundary design combined with Web3 cryptographic guarantees: ZK, TEE, minimal disclosure
- [[dev-tooling-agent-workflow]] — AI improving Web3 developer workflows: code generation, audit, simulation, deployment automation
- [[governance-coordination-public-goods]] — DAO participation + contribution intelligence: proposal summaries, voting assistance, budget verification
- [[cobo-pact]] — Task-level authorization model: temporary bounded permissions (budget + scope + time window + failure handling)

---

## Concepts — AI × Web3 Bridge: Overview & Standards

- [[aixweb3-bridge-overview]] — Bridge intersection layer overview; 15 chapters; 6 directions
- [[aixweb3-agent-architecture]] — 8-step reference pattern: goal → plan → read/write split → policy → simulation → confirmation → execution → log
- [[erc-7702]] — EIP allowing EOAs to temporarily adopt smart-account capabilities for one transaction
- [[erc-8183]] — Payment channel standard for AI agent on-chain micropayments and subscriptions
- [[erc-8004]] — On-chain agent capability registry: verifiable service endpoints and capability declarations

---

## Concepts — AI × Web3 Bridge: Chain-aware Context

- [[chain-aware-context]] — Live on-chain state, contract metadata, and transaction history in agent context
- [[on-chain-data]] — Raw blockchain state: balances, storage, logs, events used as agent context
- [[contract-docs]] — ABI, NatSpec comments, and parameter explanations injected into agent context
- [[transaction-history]] — Historical wallet activity providing behavioral patterns for agent reasoning
- [[explorer-context]] — Block explorer data (Etherscan/Blockscout) formatted for agent consumption
- [[indexing-context]] — Subgraph and indexed event data enabling rich semantic queries from agents

---

## Concepts — AI × Web3 Bridge: Web3 Tool Use

- [[web3-tool-use]] — RPC, wallet, contract, and DeFi tools called by AI agents
- [[rpc-tool]] — JSON-RPC call wrapper exposing eth_call, eth_getLogs, and related reads to agents
- [[contract-read]] — Read-only contract call tool: view/pure functions, no gas, no signing required
- [[contract-write]] — State-changing contract call tool: requires signing, simulation, and confirmation
- [[wallet-tool]] — Wallet balance, token holdings, and allowance query tools for agent context
- [[defi-tool]] — DeFi protocol interaction tools: swap quotes, lending positions, liquidity data
- [[tool-permission]] — Per-tool risk classification and access control; narrow interfaces reduce blast radius
- [[tool-log]] — Structured logging of all tool inputs, outputs, and errors for audit and debugging

---

## Concepts — AI × Web3 Bridge: Agent Workflow

- [[agent-workflow]] — Automation boundaries, human-in-the-loop design, and execution orchestration
- [[task-graph]] — Directed acyclic graph of subtasks with dependencies; enables parallel and conditional execution
- [[human-in-the-loop]] — Mandatory human confirmation gates for irreversible, high-value, or ambiguous actions
- [[retry-fallback]] — Error recovery logic: retry with backoff, degrade gracefully, or escalate to human
- [[trace]] — Per-task execution record: steps, tool calls, decisions, timing; primary debugging artifact
- [[regression-set]] — Curated failure cases that are re-run after every system change to prevent regressions

---

## Concepts — AI × Web3 Bridge: Agent Wallet

- [[agent-wallet]] — Delegated wallet with spending limits, session keys, policy guards, and revocation
- [[aa-wallet]] — Account-abstraction wallet used by AI agents: programmable auth, gas sponsorship
- [[policy]] — Rule set attached to agent wallet: allowed contracts, amount limits, time windows
- [[guard]] — On-chain or off-chain enforcement point that rejects policy-violating transactions
- [[simulation]] — Pre-execution sandbox run of a transaction to verify outcome before signing
- [[revocation]] — Mechanism to cancel session keys, permissions, or approvals; critical for agent safety
- [[human-check]] — Explicit human approval step for transactions above risk threshold

---

## Concepts — AI × Web3 Bridge: Machine Payment

- [[machine-payment]] — Autonomous micropayments and on-chain settlement for agent-to-agent commerce
- [[stablecoin-payment]] — Using USDC/USDT/DAI for AI agent payments; avoids volatility risk
- [[budget]] — Allocated spending limit for an agent task; prevents runaway costs
- [[quote]] — Price estimate returned before execution; agent accepts or rejects before spending
- [[payment-intent]] — Off-chain payment commitment that becomes binding once signed
- [[x402]] — HTTP 402-based payment protocol for AI agents to pay API calls inline
- [[mpp]] — Machine Payment Protocol: open standard for agent-to-agent micropayments
- [[subscription]] — Recurring on-chain payment stream for agent services; time or usage based
- [[micropayment]] — Sub-cent payments enabled by L2s and payment channels; viable for per-call billing

---

## Concepts — AI × Web3 Bridge: Settlement & Escrow

- [[settlement-and-escrow]] — Completing the payment loop: delivery proof, dispute resolution, fund release
- [[escrow]] — Smart contract holding funds until delivery conditions are met
- [[receipt]] — On-chain or signed record of completed payment and service delivery
- [[delivery-proof]] — Verifiable evidence that a service was delivered as specified (hash, signature, log)
- [[acceptance]] — Buyer confirmation that delivery meets spec; triggers fund release from escrow
- [[refund]] — Return of escrowed funds when delivery fails, times out, or dispute is resolved for buyer
- [[dispute]] — Challenge mechanism when acceptance is withheld; requires arbitration or on-chain resolution
- [[evaluator]] — Third-party or automated system judging whether delivery meets acceptance criteria

---

## Concepts — AI × Web3 Bridge: Agent Identity

- [[agent-identity]] — Agent identification, authentication, authorization, and accountability
- [[agent-profile]] — Structured description of an agent: name, capabilities, endpoints, public key
- [[capability]] — Declared service an agent can perform; referenced in identity and trust contexts
- [[service-endpoint]] — URL or on-chain address where an agent's capabilities are accessible
- [[registry]] — On-chain or off-chain catalog mapping agent identities to profiles and capabilities
- [[did-vc]] — Decentralized Identifiers and Verifiable Credentials for agent authentication
- [[a2a-protocol]] — Agent-to-Agent protocol for cross-service agent discovery and task handoff
- [[ownership]] — Attribution of agent actions to a human or organization; liability and accountability

---

## Concepts — AI × Web3 Bridge: Agent Trust & Reputation

- [[agent-trust-and-reputation]] — Verifiable behavior-based trust: not a single score but layered evidence bound to identity
- [[reputation]] — Aggregated past-behavior signal used to inform task delegation and risk assessment
- [[review]] — Structured post-task evaluation by service consumer; input to reputation systems
- [[attestation]] — Cryptographic statement by a verifier about an agent's capability or behavior
- [[stake]] — Deposited collateral that creates skin-in-the-game for honest agent behavior
- [[slashing]] — Penalty mechanism that burns stake when provably malicious behavior is detected
- [[validation]] — Independent verification of agent output before it affects on-chain state

---

## Concepts — AI × Web3 Bridge: AI Oracle

- [[ai-oracle]] — AI model outputs published on-chain for contract use; requires verifiability
- [[ai-output]] — Raw LLM inference result before on-chain publishing; needs format + proof wrapper
- [[data-feed]] — Structured on-chain data stream (prices, events, scores) from AI oracle systems
- [[model-result]] — Specific AI inference outcome (classification, score, summary) for on-chain use
- [[proof-of-inference]] — Cryptographic proof that output came from a specific model and input (TEE/ZK/signed log)
- [[dispute-challenge]] — On-chain mechanism to challenge an oracle result within a time window

---

## Concepts — AI × Web3 Bridge: Verifiable AI

- [[verifiable-ai]] — Proving model inputs, execution environment, and outputs when they affect on-chain state
- [[tee]] — Trusted Execution Environment: hardware-isolated inference with remote attestation
- [[zk]] — Zero-knowledge proofs: verifiable computation without revealing inputs
- [[zkml]] — ZK applied to ML inference: proving model execution; hybrid approaches for large models
- [[verifiable-compute]] — Off-chain computation whose results can be verified by on-chain or third parties
- [[benchmark]] — Task-specific eval set including attack, boundary, and wrong-chain samples for model comparison
- [[audit-trail]] — Persistent, tamper-evident log of inputs, outputs, model version, and confirmations

---

## Concepts — AI × Web3 Bridge: AI Security

- [[ai-security]] — Defense against prompt injection, tool abuse, permission escalation, and key exposure
- [[tool-abuse]] — Misuse of agent tools by malicious input or confused-deputy attacks
- [[malicious-context]] — Attacker-controlled data in agent context that attempts to hijack behavior
- [[key-safety]] — Practices ensuring private keys and seed phrases never reach AI agent context
- [[permission-isolation]] — Separating read/write/sign capabilities into distinct, narrowly scoped tools
- [[sandbox]] — Isolated execution environment preventing malicious input from accessing secrets
- [[audit-log]] — Security-oriented persistent record of agent decisions, tool calls, and confirmations
- [[alert]] — Real-time notification of anomalous agent behavior or policy violations

---

## Concepts — AI × Web3 Bridge: AI Privacy

- [[ai-privacy]] — Data boundary design, minimal disclosure, local-first processing, private memory management
- [[data-boundary]] — Explicit rules about what data can flow into AI context and what must stay local
- [[local-ai]] — Running models on-device or in private infrastructure to prevent data leaving the boundary
- [[private-memory]] — Agent memory partitioned by user; not shared across users or sessions
- [[secret-management]] — Secure storage and retrieval of credentials, keys, and sensitive config for agents
- [[minimal-disclosure]] — Sharing only the data required for a task; ZK and selective disclosure enable this
- [[encrypted-data]] — Data encrypted before entering AI pipelines; agent works on ciphertext or TEE
- [[user-consent]] — Explicit approval before agent accesses, stores, or transmits personal data

---

## Concepts — AI × Web3 Bridge: AI Sovereignty

- [[ai-sovereignty]] — User control over AI models, data, and execution; resistance to platform lock-in
- [[user-control]] — User ability to inspect, modify, pause, or delete agent behavior and stored data
- [[data-portability]] — Right and ability to export personal data and agent memory to other systems
- [[model-choice]] — User selection of model provider, version, or local deployment without lock-in
- [[local-first-ai]] — Processing and storing data locally before any cloud sync; privacy-preserving default
- [[censorship-resistance]] — Architectural resistance to being shut down, blocked, or deplatformed
- [[dacc]] — Defensive Accelerationism: open-source, distributed development as sovereignty strategy
- [[crops]] — Cryptographic Rights and Ownership for Personal Sovereignty; on-chain data rights framework

---

## Concepts — AI × Web3 Bridge: Governance AI

- [[governance-ai]] — AI improving proposal analysis, contribution tracking, and budget verification in DAOs
- [[proposal-summary]] — AI-generated summary of governance proposals with source links for human verification
- [[meeting-action]] — AI extraction of action items from meeting transcripts with attribution and due dates
- [[contribution-graph]] — Verified record of contributor participation, output, and impact over time
- [[budget-check]] — Automated verification that proposed spending aligns with on-chain treasury and prior votes
- [[source-traceability]] — Linking every AI governance claim back to the original on-chain or off-chain source
- [[deep-funding]] — Retroactive public goods funding informed by verifiable contribution data
- [[plurality]] — Governance mechanism combining quadratic voting, identity, and consent for fair resource allocation

---

## Concepts — AI × Web3 Bridge: Decentralized AI

- [[decentralized-ai]] — Open markets for models, data, and compute; inference networks without central control
- [[model-market]] — Marketplace for discovering, comparing, and licensing AI models on-chain
- [[data-market]] — Marketplace for buying, selling, and licensing training or inference data with provenance
- [[compute-market]] — Decentralized GPU/compute marketplace for running AI inference and training jobs
- [[inference-network]] — Distributed network of nodes serving AI model inference with verifiable outputs
- [[model-routing]] — Dynamic selection of the best model for a task based on cost, quality, and latency
- [[quality-benchmark]] — Standardized performance comparison enabling trustless model selection in markets

---

## Concepts — Web3 Foundations: Cryptography

- [[cryptography]] — Mathematical foundation of all Web3 security: hashing, asymmetric keys, signatures
- [[hash-function]] — One-way deterministic transform (SHA256/Keccak256); collision-resistant fingerprint
- [[public-key]] — Shareable key derived from private key; Ethereum address = Keccak256(pubkey)[-20 bytes]
- [[private-key]] — Root secret of a blockchain account; must never be exposed or given to AI agents
- [[cryptographic-signature]] — Proves key ownership without revealing it; authorizes specific on-chain actions
- [[merkle-tree]] — Binary hash tree enabling compact membership proofs; used in blocks and rollup proofs

---

## Concepts — Web3 Foundations: Wallet

- [[eoa]] — Externally Owned Account; key-pair controlled, no code, full control with private key
- [[mnemonic]] — BIP-39 seed phrase; generates all private keys in an HD wallet; never share
- [[web3-transaction]] — Signed data package that changes on-chain state; 8-step execution flow
- [[gas]] — EVM computation unit; fees paid in ETH/gwei; EIP-1559 model; L2s dramatically cheaper
- [[block-explorer]] — Read-only on-chain data interface; Etherscan for transactions, contracts, events

---

## Concepts — Web3 Foundations: Smart Contracts

- [[smart-contract]] — Self-executing on-chain code; state and execution are public; immutable by default
- [[solidity]] — Primary EVM smart contract language; compiled to bytecode; statically typed
- [[evm]] — Ethereum Virtual Machine; deterministic sandboxed runtime; basis for EVM-compatible chains
- [[abi]] — Application Binary Interface; JSON spec for encoding/decoding contract calls and events
- [[contract-event]] — Emitted logs in transaction receipts; primary input for indexers and frontends
- [[contract-upgrade]] — Proxy patterns (transparent, UUPS) for replacing contract logic while preserving state

---

## Concepts — Web3 Foundations: Dev Stack

- [[web3-dev-stack]] — Full toolchain: Remix → Hardhat/Foundry → OpenZeppelin → viem/wagmi
- [[remix-ide]] — Browser-based Solidity IDE; fastest path from code to on-chain; no setup required
- [[hardhat]] — Node.js dev framework; compile, test (Chai/Mocha), deploy, verify; Hardhat Network
- [[foundry]] — Rust-based dev framework; Forge (tests), Cast (CLI), Anvil (local node), fuzz testing
- [[openzeppelin]] — Audited Solidity library: ERC-20, ERC-721, AccessControl, upgradeable proxies
- [[viem-wagmi]] — TypeScript/React libraries for on-chain reads and writes; modern ethers.js replacement

---

## Concepts — Web3 Foundations: Network

- [[blockchain-network]] — Distributed peer-to-peer ledger; canonical state via consensus; permissionless
- [[block]] — Batch of transactions linked by parent hash; 12-second slot time on Ethereum PoS
- [[consensus]] — Agreement mechanism for canonical chain state; PoW → PoS post-Merge
- [[proof-of-stake]] — Ethereum's consensus: validators stake 32 ETH; randomly selected to propose blocks
- [[testnet]] — Test network with valueless tokens; Sepolia/Holesky; always test here before mainnet
- [[layer-2]] — Off-chain execution inheriting L1 security; 10–100x cheaper gas; Arbitrum, Base, zkSync
- [[rollup]] — Dominant L2 architecture: batch transactions, post data + validity proof to L1

---

## Concepts — Web3 Foundations: Account Abstraction

- [[erc-4337]] — Account abstraction standard: UserOperation mempool, EntryPoint, no protocol change
- [[smart-account]] — Contract wallet with programmable auth: multisig, social recovery, session keys
- [[bundler]] — Collects UserOperations from alt mempool; submits batched EntryPoint transaction
- [[paymaster]] — Sponsors gas on behalf of users/agents; enables gasless UX or ERC-20 gas payments
- [[session-key]] — Limited-scope key for AI agents: contract-scoped, amount-capped, time-bounded

---

## Concepts — Web3 Foundations: DeFi

- [[defi]] — Permissionless on-chain financial protocols; composable, non-custodial, auditable
- [[erc20-token]] — Standard fungible token interface; transfer, approve, allowance; EIP-2612 permit
- [[amm]] — Automated Market Maker; liquidity pool trading; introduces slippage, MEV, impermanent loss
- [[defi-lending]] — Over-collateralized borrowing/lending (Aave, Compound); liquidation risk
- [[stablecoin]] — Price-pegged asset: fiat-backed (USDC), crypto-collateralized (DAI), algorithmic (FRAX)
- [[liquidity]] — Capital in pools enabling trades; LPs earn fees, bear impermanent loss

---

## Concepts — Web3 Foundations: Oracle

- [[oracle]] — Bridge from off-chain data to on-chain contracts; decentralized networks solve trust
- [[price-feed]] — Real-time asset prices on-chain (Chainlink, Pyth); freshness verification critical
- [[oracle-risk]] — Manipulation, stale price, centralization risks; oracle attacks drain DeFi protocols

---

## Concepts — Web3 Foundations: Indexing

- [[on-chain-indexing]] — ETL from raw blockchain events to queryable structured databases
- [[subgraph]] — The Graph's indexing unit; manifest + mappings → GraphQL API over indexed events
- [[rpc]] — JSON-RPC interface to blockchain nodes; `eth_call`, `eth_getLogs`, WebSocket subscriptions
- [[data-pipeline]] — Extract-Transform-Load pipeline from chain events to analytics/AI context
- [[on-chain-monitoring]] — Real-time anomaly detection post-deployment; Forta, OpenZeppelin Defender

---

## Concepts — Web3 Foundations: Security

- [[web3-security]] — Defensive practices: audits, static analysis, simulation, monitoring, defense-in-depth
- [[reentrancy]] — Recursive call exploiting stale state; fixed by checks-effects-interactions + ReentrancyGuard
- [[access-control]] — Role-based contract permissions; admin key compromise = full takeover
- [[contract-audit]] — Expert security review before deployment; not a guarantee but essential gate
- [[tx-simulation]] — Pre-execution sandbox verification; AI agents should simulate before signing
