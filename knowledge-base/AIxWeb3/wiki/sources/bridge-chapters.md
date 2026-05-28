---
title: "AIxWeb3 Bridge Chapters"
type: source
tags: [aixweb3-bridge, chain-aware-context, web3-tool-use, agent-workflow, agent-wallet, machine-payment, settlement-escrow, agent-identity, agent-trust, ai-oracle, verifiable-ai, ai-security, ai-privacy, ai-sovereignty, governance-ai, decentralized-ai]
source_file: "raw/AIxWeb3 Bridge Chapters.md"
source_hash: "sha256:40836f87f09edea93cb828db7f0330e781701f9da726e73da1a23e5e7542cc06"
date_ingested: "2026-05-28"
---

## Summary

This source aggregates 15 detailed chapters from the AI × Web3 School handbook Bridge section, covering the full stack from on-chain context reading to decentralized AI infrastructure. Each chapter defines the core problem, first principles, sub-concepts with difficulty levels, position in the AI × Web3 ecosystem, and minimal practice exercises. This is the most comprehensive single source in the knowledge base, covering ~70 distinct concepts across the bridge layer.

## Key Concepts (by chapter)

### Chain-aware Context
- [[chain-aware-context]] — AI must read on-chain facts from tools, not guess from language memory
- [[on-chain-data]] — balances, transactions, logs, contract states, block information
- [[contract-docs]] — ABI + documentation + NatSpec fills semantic gaps
- [[transaction-history]] — past user/contract behavior with hash-level evidence
- [[explorer-context]] — verifiable evidence from block explorers
- [[indexing-context]] — product-oriented queryable on-chain events (e.g. The Graph)

### Web3 Tool Use
- [[web3-tool-use]] — read/write separation, structured parameters, auditable logs
- [[rpc-tool]] — chain state queries, gas estimation, broadcast
- [[contract-read]] — view/pure functions, balances, allowances
- [[contract-write]] — state-changing calls requiring simulation + confirmation
- [[wallet-tool]] — signing, transaction generation, authorization management
- [[explorer-tool]] — transaction verification, source code, event queries
- [[defi-tool]] — swap, lending, position queries with protocol whitelist
- [[tool-permission]] — layered rules: auto-allowed, session-key, manual, prohibited
- [[tool-log]] — full audit record per tool call

### Agent Workflow
- [[agent-workflow]] — putting a probabilistic model into a deterministic process
- [[task-graph]] — breaking goals into dependent nodes
- [[state-machine]] — explicit states for on-chain agent execution
- [[human-in-the-loop]] — layered risk-based confirmation
- [[retry-fallback]] — cautious retry patterns for Web3 (broadcast vs. not-yet-sent)
- [[trace]] — full record of input/judgment/tool/result per agent execution
- [[evaluation-harness]] — systematic testing including unauthorized-request rejection
- [[regression-set]] — fixed test cases to prevent safety degradation after updates

### Agent Wallet
- [[agent-wallet]] — verifiable, restricted, revocable action spaces for agents
- [[aa-wallet]] — account abstraction-based wallet with programmable rules
- [[smart-account]] — execution boundary with policy, recovery, automation
- [[session-key]] — time/amount/target-limited temporary key
- [[policy]] — rules the system can check (not just legal text)
- [[guard]] — deterministic pre-execution intercept layer
- [[simulation]] — preview of transaction results before signing
- [[revocation]] — user + automatic permission withdrawal
- [[human-check]] — layered confirmation at key risk points

### Machine Payment
- [[machine-payment]] — limitable, verifiable, traceable agent payments
- [[stablecoin-payment]] — pricing currency vs. settlement currency considerations
- [[budget]] — layered spending limits: global, task, call, provider, emergency stop
- [[quote]] — executable price offer with validity period and refund conditions
- [[payment-intent]] — authorization to pay for a service type, not yet settled
- [[x402]] — HTTP 402 payment flow for per-use API/content payments
- [[mpp]] — Machine Payments Protocol: discovery, quote, auth, settlement, receipt
- [[subscription]] — continuous service payment with cancellation capabilities
- [[micropayment]] — high-frequency small-amount with batching strategies

### Settlement & Escrow
- [[settlement-and-escrow]] — binding task, delivery, acceptance, and payment verifiably
- [[escrow]] — fund locking with state machine until delivery conditions are met
- [[receipt]] — credential recording payment + delivery + acceptance status
- [[delivery-proof]] — file hash, API log, on-chain event, TEE attestation as evidence
- [[acceptance]] — payer or rule system confirming delivery meets requirements
- [[refund]] — fund return on timeout, format error, or cancellation
- [[dispute]] — challenge flow with evidence, arbitrator, cost, appeal
- [[evaluator]] — script/model/human/validator judging delivery qualification
- [[erc-8183]] — draft standard for agent commerce task lifecycle

### Agent Identity
- [[agent-identity]] — discoverable, verifiable, accountable economic participant
- [[agent-profile]] — machine-readable public specification: capabilities, endpoint, price
- [[capability]] — concrete task + input/output/risk level declarations
- [[service-endpoint]] — HTTPS/A2A/MCP entry point with owner-signed updates
- [[registry]] — on-chain/off-chain discovery and continuity anchor
- [[did-vc]] — decentralized identity + verifiable credentials for cross-platform claims
- [[a2a-protocol]] — agent discovery, task negotiation, result exchange
- [[ownership]] — who can update profile/endpoint/payment address

### Agent Trust & Reputation
- [[agent-trust-and-reputation]] — verifiable behavior-based trust signals
- [[reputation]] — collection of historical performance signals by task type
- [[review]] — task-bound feedback with hash evidence
- [[attestation]] — verifiable claim with issuer, subject, expiration, revocation
- [[stake]] — economic guarantee; viewed alongside validation and task history
- [[slashing]] — collateral confiscation for verifiable defaults
- [[validation]] — capability or task result verification with recorded evidence
- [[erc-8004]] — draft standard for agent identity, reputation, verification registry

### AI Oracle
- [[ai-oracle]] — model judgments turned into recordable, verifiable, challengeable inputs
- [[ai-output]] — structured fields for on-chain consumption + human explanation
- [[data-feed]] — continuous AI-processed data requiring version + drift handling
- [[model-result]] — model version + prompt template + input ref + output schema
- [[oracle-risk]] — errors, contamination, prompt injection, economic attacks
- [[proof-of-inference]] — TEE/ZK/signed-log proofs that output came from specific model+input
- [[dispute-challenge]] — optimistic model for challenging AI oracle outputs

### Verifiable AI
- [[verifiable-ai]] — turning "believing the model" into "verifying evidence and constraints"
- [[tee]] — hardware-isolated execution with attestation; lower cost than ZK
- [[zk]] — cryptographic proof without revealing inputs; high cost for large LLMs
- [[zkml]] — ML inference into provable computation; hybrid solutions for LLMs
- [[proof-of-inference]] — TEE/ZK/signed-log proofs (shared with AI Oracle)
- [[verifiable-compute]] — off-chain calculation results verifiable by on-chain/third parties
- [[benchmark]] — task-specific evals including attack/boundary samples
- [[audit-trail]] — most practical verifiable layer: inputs, outputs, model version, confirmations

### AI Security
- [[ai-security]] — untrusted inputs cannot turn into unrestricted execution
- [[prompt-injection]] — malicious content in contracts/web/governance overriding rules
- [[tool-abuse]] — inducing misuse of tool capabilities; anomaly detection required
- [[malicious-context]] — false facts or attack instructions hidden in ordinary content
- [[key-safety]] — secrets never enter model context, logs, or analytics
- [[permission-isolation]] — separate read/write/sign/high-risk into different capabilities
- [[sandbox]] — isolated execution environment preventing secret access
- [[audit-log]] — tamper-evident full chain: context seen, tools called, user confirmed
- [[alert]] — anomaly detection connected to response actions

### AI Privacy
- [[ai-privacy]] — data boundaries between user devices, backends, model services, on-chain
- [[data-boundary]] — explicit flow map: what goes to model, tools, local device
- [[local-ai]] — filter/de-identify locally first, send only summaries to cloud
- [[private-memory]] — manageable long-term agent memory with view/delete/export
- [[secret-management]] — rotation, revocation, isolation of keys from model context
- [[minimal-disclosure]] — prove only what's needed (ZK, summaries, one-time addresses)
- [[encrypted-data]] — combines with access control + TEE; encryption alone doesn't solve inference privacy
- [[user-consent]] — specific, revocable, per-action consent (not blanket agreement)

### AI Sovereignty
- [[ai-sovereignty]] — exit, migrate, choose, and verify capabilities for users
- [[user-control]] — view/modify/revoke permissions, data, session keys, tools
- [[data-portability]] — layered export in machine-readable formats for agent migration
- [[model-choice]] — strategic selection: privacy-first, cost-first, quality-first, open-source-first
- [[local-first-ai]] — hybrid: local for sensitive filtering, cloud for summaries only
- [[censorship-resistance]] — open-source clients, multi-model fallbacks, self-hostable endpoints
- [[dacc]] — defensive accelerationism: accelerate defensive, decentralized, human-enhancement tech
- [[crops]] — Censorship resistance, Open source, Privacy, Security as product checklist

### Governance AI
- [[governance-ai]] — organize information, track contributions, reduce information asymmetry
- [[proposal-summary]] — structured with sources, objections, uncertainty markers
- [[meeting-action]] — executable items with owner, deadline, decision status
- [[contribution-graph]] — visible/invisible contributions across tools with evidence
- [[budget-check]] — completeness, milestones, address ownership, on-chain anomalies
- [[source-traceability]] — every governance summary has clickable source links
- [[deep-funding]] — evidence packages for complex public goods impact allocation
- [[plurality]] — preserve differences, present minority concerns, support negotiation

### Decentralized AI
- [[decentralized-ai]] — redesign of data/model/compute/inference/evaluation/revenue distribution
- [[model-market]] — discovery, evaluation, routing, settlement for model capabilities
- [[data-market]] — verifiable sources, authorization terms, reproducible pipelines
- [[compute-market]] — GPU/CPU/inference as purchasable resources with quality checks
- [[inference-network]] — distributed node execution with routing, versioning, verification
- [[model-routing]] — task/risk/privacy/cost/latency-aware model selection
- [[quality-benchmark]] — stability, reproducibility, gaming-resistance for open networks

## Notable Points

- "The core of Chain-aware Context is turning on-chain facts into context that is readable, referenceable, and verifiable by the model."
- "Models can choose tools, but tools must use deterministic boundaries to limit the model." — Web3 Tool Use
- "The core of Agent Workflow is putting a probabilistic model into a deterministic process."
- "Control cannot be handed over to a probabilistic system. Agents can only be given verifiable, restricted, and revocable action spaces." — Agent Wallet
- "The core of Machine Payment is to decouple payment intent from actual settlement and ensure every step has evidence."
- "Trust is not a single score, but a set of traceable, comparable, and interpretable evidence." — Agent Trust
- "Verification cost must match output impact." — Verifiable AI
- "Everything that enters the model can be an attack surface, and every action that leaves the model must be constrained." — AI Security
- "Models should only see the minimum data required to complete a task." — AI Privacy
- "The closer an AI is to user decisions and assets, the less it should rely solely on platform promises." — AI Sovereignty
- "AI outputs in governance must preserve sources and uncertainties." — Governance AI
- "What AI systems truly need to decentralize is not necessarily the model itself, but the control over critical resources and key decisions." — Decentralized AI
