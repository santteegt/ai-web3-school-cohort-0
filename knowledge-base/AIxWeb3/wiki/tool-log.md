---
title: "Tool Log"
type: concept
tags: [aixweb3-bridge, tool-use, security, observability]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Tool Log is the foundation for agent behavior auditability. Every tool call records at minimum: user goal, tool name, input parameters, output result, error, time, chain ID, block number, transaction hash, confirmer, and policy judgment.

## Key Points

- When an agent makes a mistake, logs answer: what the model saw, what it called, what the tool returned, whether the system intercepted it, and what the user confirmed
- Logs cannot be omitted — every tool call must be recorded
- Tool logs + trace together form the full audit chain for post-incident review
- Categorized as Intermediate difficulty

## Related Concepts

- [[web3-tool-use]]
- [[trace]]
- [[audit-log]]
- [[audit-trail]]
- [[tool-permission]]
- [[observability]]

## Sources

- [[sources/bridge-chapters]]
