---
title: "Delivery Proof"
type: concept
tags: [aixweb3-bridge, payment-commerce, verifiable-ai]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Delivery Proof proves that a service provider has indeed delivered a certain result. The proof must correspond to the original task — preventing "the result exists but is unverifiable" situations where a deliverable might have been replaced.

## Key Points

- Proof types by task: API calls → request/response hashes; code tasks → commit hash + test results; data tasks → dataset hash; model tasks → model version + input hash + output hash
- Proof must be traceable to the original task, not just "a result was submitted"
- Without timestamp, hash, and version info, it's hard to prove later whether the deliverable was replaced
- TEE attestations, manual acceptance records, or another agent's verification can also serve as proof

## Related Concepts

- [[settlement-and-escrow]]
- [[escrow]]
- [[receipt]]
- [[acceptance]]
- [[evaluator]]
- [[proof-of-inference]]
- [[attestation]]
- [[tee]]

## Sources

- [[sources/bridge-chapters]]
