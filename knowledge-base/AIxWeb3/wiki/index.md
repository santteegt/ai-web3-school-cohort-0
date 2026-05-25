# Wiki Index

_Last updated: 2026-05-25 — 150 pages (134 concept/topic + 16 source)_

---

## Topics (Overview Pages)

- [[ai-foundations-overview]] — Full map of AI Foundations concepts: LLM, Prompt, Context, RAG, Agent, Frameworks, MCP
- [[ai-frameworks-overview]] — Framework selection, LangChain/LangGraph/DSPy/Hermes comparison, three-layer responsibility model
- [[aixweb3-bridge-overview]] — The intersection layer: where AI agents meet on-chain systems
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
- [[sources/fine-tuning]] — Fine-tuning: SFT, LoRA, PEFT, dataset quality, overfitting; what fine-tuning cannot do
- [[sources/inference]] — Inference layer: API vs. local models, quantization, serving, audit requirements
- [[sources/web3-fundamentals-introduction]] — Module B: accounts, wallets, signatures, gas, smart contracts, account abstraction
- [[sources/web3-chapters]] — Comprehensive Web3 handbook: cryptography, wallet, smart contract, dev stack, network, AA, DeFi, oracle, indexing, security

---

## Concepts — AI Foundations: LLM

- [[large-language-model]] — Probabilistic text generator; reasoning layer, not truth source
- [[tokens]] — Processing unit; affects context capacity, cost, and completeness
- [[embeddings]] — Semantic vector representations; good for retrieval, not correctness judgments
- [[transformer-architecture]] — Attention-based architecture; pattern composition without ground-truth authority
- [[hallucination]] — Confident fabrication; requires external verification, not just better prompts
- [[multimodal]] — Models processing text, images, audio, and video
- [[maas]] — API-based model access; per-token billing, no GPU required _(updated)_
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

- [[ai-agent]] — Constrained execution loop: goal, tools, state, permissions, stop conditions _(updated)_
- [[prompt-workflow-agent-boundary]] — Three architectures with different failure modes
- [[tool-calling]] — Model-to-world action mechanism; requires tool design discipline _(updated)_
- [[state-management]] — Externalized, queryable, recoverable, auditable agent state _(updated)_
- [[agent-planning]] — Candidate plan generation; step classification as read/write; not an authorization
- [[agent-reflection]] — Self-checking for intermediate correction; not a substitute for deterministic checks
- [[agent-stop-conditions]] — Explicit halting criteria: goal reached, budget exceeded, risk crossed
- [[multi-agent-systems]] — Coordination patterns; amplifies failures when roles are unclear
- [[mcp]] — Unified tool connectivity protocol; client/server architecture _(updated)_
- [[mcp-server]] — Exposes resources, tools, prompts; defines permission model
- [[mcp-client]] — Connects model to servers; handles discovery, confirmation, session isolation
- [[tool-schema]] — Machine-readable tool declaration; vague schemas cause wrong-parameter calls
- [[mcp-permission-model]] — Permission design per tool risk level; the most underestimated MCP issue
- [[guardrails]] — Hard execution constraints; code-enforced, not prompt-enforced
- [[agent-handoff]] — Control transfer after subtask completes
- [[ai-agent-tracing]] — Execution chain observability; debugging and audit _(updated)_
- [[maas]] — API-based model access; per-token billing, no GPU required _(updated)_
- [[vibe-coding]] — AI-assisted rapid prototyping; requires engineering discipline _(updated)_
- [[ai-coding]] — AI coding in the full engineering flow: issue → branch → commit → test → review → merge

---

## Concepts — AI Foundations: Frameworks

- [[ai-frameworks-overview]] — Selection criteria, three-layer responsibility model
- [[langchain]] — Component library for composing AI capabilities; good for prototyping
- [[langgraph]] — DAG-based stateful workflows; reference for explicit state management
- [[openai-agents-sdk]] — Agent engineering primitives: handoffs, guardrails, tracing, structured output
- [[dspy]] — Metric-driven prompt optimization; treats pipelines as optimizable programs
- [[hermes]] — Tool-calling and structured-output oriented model ecosystem
- [[learning-agents]] — Systems that improve via evaluation loop, not direct online behavior change _(updated)_

---

## Concepts — AI × Web3 Bridge

- [[chain-aware-context]] — Live on-chain state in agent context
- [[web3-tool-use]] — RPC, wallet, contract tools called by agents
- [[agent-workflow]] — Automation boundaries and human-in-the-loop design
- [[agent-wallet]] — Delegated permissions, spending limits, revocation
- [[machine-payment]] — Autonomous micro-payments and on-chain settlement
- [[agent-identity]] — Agent identification, authorization, accountability
- [[verifiable-ai]] — Proving model outputs and execution processes
- [[ai-security]] — Prompt injection defense, tool abuse prevention, permission isolation
- [[aixweb3-agent-architecture]] — 8-step reference pattern: goal → plan → read/write split → policy → simulation → confirmation → execution → log

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
- [[ai-oracle]] — Emerging pattern: verifiable AI model outputs published on-chain for contract use

---

## Concepts — Web3 Foundations: Indexing

- [[on-chain-indexing]] — ETL from raw blockchain events to queryable structured databases
- [[subgraph]] — The Graph's indexing unit; manifest + mappings → GraphQL API over indexed events
- [[rpc]] — JSON-RPC interface to blockchain nodes; `eth_call`, `eth_getLogs`, WebSocket subscriptions
- [[data-pipeline]] — Extract-Transform-Load pipeline from chain events to analytics/AI context

---

## Concepts — Web3 Foundations: Security

- [[web3-security]] — Defensive practices: audits, static analysis, simulation, monitoring, defense-in-depth
- [[reentrancy]] — Recursive call exploiting stale state; fixed by checks-effects-interactions + ReentrancyGuard
- [[access-control]] — Role-based contract permissions; admin key compromise = full takeover
- [[contract-audit]] — Expert security review before deployment; not a guarantee but essential gate
- [[tx-simulation]] — Pre-execution sandbox verification; AI agents should simulate before signing
- [[on-chain-monitoring]] — Real-time anomaly detection post-deployment; Forta, OpenZeppelin Defender
