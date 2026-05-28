---
title: "Verifiable AI"
type: concept
tags: [aixweb3-bridge, security, frontier]
source_count: 2
date_updated: "2026-05-28"
---

## Definition

Verifiable AI focuses on: when AI outputs affect assets, permissions, reputation, or governance, can we verify its inputs, models, execution environment, inference process, or at least leave auditable evidence. Core principle: verification cost must match output impact — turning "believing the model" into "verifying evidence and constraints."

## Key Points

- Verification is layered by risk: low-risk scenarios leave logs; high-risk scenarios require TEE, ZK, attestation, audit trails, challenges, or multi-party verification
- Verify source first (inputs, model version, service provider, execution time) → verify process (trusted environment, replayable) → verify result impact (what on-chain state changes, whether challenge period needed)
- A practical matrix: summarization → audit trail; task acceptance → attestation + challenge; fund release → TEE/ZK + multi-evaluator

## Sub-Concepts

- [[tee]] — hardware-isolated execution with attestation; lower cost than ZK; suitable for private inference
- [[zk]] — cryptographic proof without revealing inputs; strong but expensive for LLMs
- [[zkml]] — ML inference into provable computation; hybrid approaches for large models
- [[proof-of-inference]] — TEE/ZK/signed-log proofs that output came from specific model + input
- [[verifiable-compute]] — off-chain calculation results verifiable by on-chain/third parties
- [[benchmark]] — task-specific evals including attack/boundary/wrong-chain samples
- [[audit-trail]] — most practical starting point: log inputs, outputs, model version, user confirmations

## Related Concepts

- [[agent-identity]] — identity is required to attribute verifiable actions
- [[ai-agent-tracing]] — traces are the off-chain equivalent of verifiable execution records
- [[guardrails]] — guardrails generate auditable checkpoints in the execution record
- [[verification-chain]] — the full execution chain that verifiable AI makes auditable
- [[ai-security]] — verifiable AI is a key component of secure AI system design
- [[ai-oracle]] — AI oracle outputs must be verifiable before affecting on-chain state

## Sources

- [[sources/aixweb3-school]] — verifiable AI as AI × Web3 Bridge topic
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
