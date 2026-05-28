---
title: "zkML"
type: concept
tags: [aixweb3-bridge, verifiable-ai, frontier]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

zkML is the direction of turning machine learning inference into provable computations using zero-knowledge proofs. It is suitable for scenarios where models are small, structures are fixed, and outputs require strong verification.

## Key Points

- Full ZK proofs for large LLMs are still very expensive — actual systems use hybrid solutions (prove key steps, prove smaller models and post-processing logic)
- Key design questions: is hiding inputs necessary, is on-chain verification needed, can proof latency be accepted, can the model be converted to a circuit?
- Many scenarios that "need trusted AI" are actually more economical with signed logs, TEE, or manual review
- Example tool: EZKL for zkML inference proofs

## Related Concepts

- [[verifiable-ai]]
- [[zk]]
- [[tee]]
- [[proof-of-inference]]
- [[ai-oracle]]
- [[verifiable-compute]]

## Sources

- [[sources/bridge-chapters]]
