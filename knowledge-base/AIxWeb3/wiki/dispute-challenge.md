---
title: "Dispute / Challenge (AI Oracle)"
type: concept
tags: [aixweb3-bridge, verifiable-ai, payment-commerce]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Dispute/Challenge is a mechanism for raising objections to AI Oracle outputs. It uses an optimistic model: accept the result first with a challenge window; if someone submits evidence, enter review, arbitration, or multi-party verification. An AI oracle without challenge mechanism risks hardcoding model errors into on-chain states.

## Key Points

- Challenge window balance: too short → users can't find errors; too long → low settlement efficiency
- Challenge cost balance: too low → spam; too high → victims can't appeal
- Practical layering: short window for small tasks, longer for high-value, human/multi-party evaluators for high-dispute
- Relates to both AI Oracle disputes and Settlement & Escrow disputes — same underlying challenge mechanism pattern

## Related Concepts

- [[ai-oracle]]
- [[oracle-risk]]
- [[evaluator]]
- [[dispute]]
- [[attestation]]
- [[settlement-and-escrow]]

## Sources

- [[sources/bridge-chapters]]
