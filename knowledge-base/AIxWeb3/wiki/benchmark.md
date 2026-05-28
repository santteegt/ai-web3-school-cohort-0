---
title: "Benchmark (AI × Web3)"
type: concept
tags: [aixweb3-bridge, evaluation, verifiable-ai]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Benchmarks in AI × Web3 contexts are used to compare model or agent capabilities, but they cannot replace task-level verification. AI × Web3 projects should establish their own task-specific benchmarks rather than relying solely on general leaderboards.

## Key Points

- Public benchmarks show general capability but cannot prove a specific output is correct
- AI × Web3 benchmarks need to include: normal samples, boundary samples, and attack samples
- Attack samples include: wrong chains, malicious contexts, expired prices, same-name tokens, revert transactions, fake contract documents
- Benchmarks should feed into routing, pricing, reputation, and settlement — not just leaderboards
- A model might score high on general benchmarks but frequently misread decimals, ignore chain IDs, or misjudge authorization risks on your specific tasks

## Related Concepts

- [[verifiable-ai]]
- [[evaluation-harness]]
- [[regression-set]]
- [[quality-benchmark]]
- [[validation]]
- [[evaluation]]

## Sources

- [[sources/bridge-chapters]]
