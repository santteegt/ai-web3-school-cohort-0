---
title: "Regression Set"
type: concept
tags: [aixweb3-bridge, agent, evaluation]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Regression Set is a fixed set of test cases used to prevent safety degradation after model, prompt, tool, or policy updates. Every time a change is made, this set is run to confirm the agent hasn't regressed from "rejecting dangerous requests" to "looking smoother but being more dangerous."

## Key Points

- Example cases: normal swap, wrong chain request, infinite approval request, malicious document inducement, insufficient balance, stale oracle prices, user refusing to sign, transaction pending timeout
- Safety regression is the primary concern — not just quality regression
- Regression sets are distinct from evals: evals measure general quality; regression sets enforce specific safety boundaries
- Should run before deploying any model, prompt, or tool change to production

## Related Concepts

- [[agent-workflow]]
- [[evaluation-harness]]
- [[evaluation]]
- [[trace]]
- [[golden-set]]
- [[regression-testing]]

## Sources

- [[sources/bridge-chapters]]
