---
title: "Model Result"
type: concept
tags: [aixweb3-bridge, verifiable-ai]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Model Result needs to include the model version, prompt or task template, input references, and output fields — not just the answer. Without generation conditions, the result is difficult to review after model upgrades or disputes.

## Key Points

- Output schema must be documented: is the risk score 0-100 or 0-1? Higher = higher risk or lower? Who defined the threshold?
- In multi-model systems: record routing information (why this model, whether fallback was used, whether human-reviewed)
- The same input may yield different results after a model upgrade — version tracking is essential
- Serves as evidence in dispute resolution

## Related Concepts

- [[ai-oracle]]
- [[ai-output]]
- [[data-feed]]
- [[proof-of-inference]]
- [[audit-trail]]
- [[model-routing]]

## Sources

- [[sources/bridge-chapters]]
