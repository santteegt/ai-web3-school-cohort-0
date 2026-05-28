---
title: "ZK (Zero-Knowledge Proofs)"
type: concept
tags: [web3-foundations, aixweb3-bridge, verifiable-ai, frontier]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Zero-Knowledge proofs allow proving that a calculation meets conditions without revealing all inputs or re-executing the entire calculation. ZK provides strong cryptographic verification but generating proofs is costly and engineering-complex — not all AI models are suitable for direct ZK proofs.

## Key Points

- Best suited for tasks with clear boundaries and controllable computation scale
- For AI: more practical to prove key parts rather than the entire model (e.g., small classifier, post-processing rule, data aggregation constraint)
- Fully proving LLM inference tokens is not yet realistic for production
- Stronger than TEE in terms of trust assumptions but significantly more expensive
- Examples suitable for ZK: small risk models, eligibility judgments, threshold classifications, simple inferences on private data

## Related Concepts

- [[verifiable-ai]]
- [[zkml]]
- [[tee]]
- [[proof-of-inference]]
- [[verifiable-compute]]
- [[cryptography]]

## Sources

- [[sources/bridge-chapters]]
