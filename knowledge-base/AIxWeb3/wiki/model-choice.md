---
title: "Model Choice"
type: concept
tags: [aixweb3-bridge, privacy-security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Model Choice allows users or developers to select different models based on task requirements. Systems should not lock all tasks to a single model and provider — the right model depends on privacy requirements, task complexity, cost constraints, and verifiability needs.

## Key Points

- Strategic selection modes: privacy-first (local model), quality-first (best available), cost-first (small model), open-source-first, verifiability-first
- Users set default preferences; agents explain why a specific model was chosen before execution
- Model switching must enter the evaluation process — changing a model affects rejection strategies, tool-calling styles, and output formats
- High-risk agents cannot "hot-swap" models and continue automatic execution without re-evaluation

## Related Concepts

- [[ai-sovereignty]]
- [[local-first-ai]]
- [[model-routing]]
- [[local-ai]]
- [[decentralized-ai]]
- [[user-control]]

## Sources

- [[sources/bridge-chapters]]
