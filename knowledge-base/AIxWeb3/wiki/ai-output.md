---
title: "AI Output (Oracle)"
type: concept
tags: [aixweb3-bridge, verifiable-ai]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

AI Output is the result given by a model for use in an on-chain or system context. On-chain systems should consume only structured outputs (e.g., `accepted: true`, `riskScore: 72`), not long text. Long text is stored off-chain as evidence and associated via hashes.

## Key Points

- Split into two layers: "machine fields" (enters contracts or backend rules) and "human explanation" (UI, reports, dispute materials)
- Don't let a contract depend on natural language text for critical judgments
- For outputs affecting funds or permissions: record confidence, model version, input hash, output hash, generation time
- Without these fields, post-hoc review of why the model gave a specific result is impossible

## Related Concepts

- [[ai-oracle]]
- [[model-result]]
- [[proof-of-inference]]
- [[attestation]]
- [[audit-trail]]
- [[verifiable-ai]]

## Sources

- [[sources/bridge-chapters]]
