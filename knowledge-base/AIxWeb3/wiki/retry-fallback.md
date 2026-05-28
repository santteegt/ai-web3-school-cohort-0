---
title: "Retry / Fallback"
type: concept
tags: [aixweb3-bridge, agent, workflow]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Retry/Fallback handles tool failures, network anomalies, unqualified model outputs, and uncertain transaction states in Web3 agent workflows. Web3 agents cannot retry blindly — the broadcast state of a transaction changes whether retrying is safe.

## Key Points

- Balance read failure → safe to retry
- Failed transaction send → check if already broadcast before retrying (cannot re-send a pending transaction)
- Pending transaction → do not simply re-send; track and wait
- RPC anomaly → can trigger provider switch, but data source changes must be logged
- Fallback must be cautious: when a model is unavailable, degrade to read-only mode; do not auto-switch to an unevaluated model for transactions

## Related Concepts

- [[agent-workflow]]
- [[state-machine]]
- [[trace]]
- [[rpc-tool]]
- [[tool-log]]
- [[regression-set]]

## Sources

- [[sources/bridge-chapters]]
