---
title: "Model Routing"
type: concept
tags: [aixweb3-bridge, decentralized-ai, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Model Routing makes choices among multiple models, nodes, or services. It is an often underestimated layer in decentralized AI — the routing layer is essentially the scheduler of an AI application, determining when to pursue cost-efficiency, reliability, or when to refuse execution.

## Key Points

- Routing dimensions: task type (summarization/code/on-chain analysis), risk level, data sensitivity, cost budget, latency requirements, evaluation feedback (historical success rates, user feedback, error types)
- Determines: cost-efficiency vs. reliability trade-off per task
- Also determines: when the system must refuse to execute (no suitable model available or risk level too high)
- Routing decisions should be explainable and logged

## Related Concepts

- [[decentralized-ai]]
- [[inference-network]]
- [[model-market]]
- [[model-choice]]
- [[quality-benchmark]]
- [[agent-workflow]]

## Sources

- [[sources/bridge-chapters]]
