---
title: "Observability (AI Systems)"
type: concept
tags: [ai-foundations, evaluation, agent]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Observability is the ability to monitor AI system behavior during real use — recording inputs, retrieval results, tool calls, outputs, errors, and user feedback so that real-world failures can be detected and fed back into the evaluation pipeline. While evals happen before release, observability happens during production.

## Key Points

- Observability is what connects production reality to the eval pipeline — it is how you discover what real users actually fail at, which is often different from what you anticipated in the golden set
- Minimum observability records: (1) input type and source, (2) retrieval results, (3) tool calls, (4) model output, (5) errors and retries, (6) user feedback, (7) cost and latency
- Observability without evaluation is monitoring — useful but not actionable for improvement. Evaluation without observability means your golden set goes stale
- In AI × Web3: observability is also a compliance and audit requirement — on-chain actions require records of which model was used, what inputs it received, what output it produced, and whether any tool was triggered
- The observability pipeline should be designed to protect user privacy — inputs may contain wallet addresses, transaction intents, and sensitive financial data that require redaction before logging

## Related Concepts

- [[evaluation]] — observability feeds real failure data into the eval pipeline
- [[golden-set]] — real user failures from observability are the source of new golden set entries
- [[ai-agent-tracing]] — agent tracing is the agent-specific form of observability; both record execution chains
- [[regression-testing]] — observed failures become regression test cases
- [[information-governance]] — observability logs must follow the same information governance rules as other data (source, freshness, permission, trust)
- [[verifiable-ai]] — audit-grade observability supports verifiability claims in AI × Web3 systems

## Sources

- [[sources/evaluation]] — observability definition, minimum records, and relation to eval
- [[sources/inference]] — inference audit records as a form of observability in AI × Web3
