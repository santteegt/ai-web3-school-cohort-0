---
title: "Tool Permission"
type: concept
tags: [aixweb3-bridge, tool-use, security, wallet-permission]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Tool Permission defines which tools an agent can call, under what conditions, and what parameters it can pass. Permissions can be layered by tool, contract, method, amount, time, frequency, and user confirmation level.

## Key Points

- Layered example: query balance (auto-allowed) → generate transaction draft (auto-allowed) → small whitelist payment (session key) → large transfer or authorization (manual confirmation required) → arbitrary contract call (prohibited by default)
- Tool permissions are distinct from wallet permissions but should align with them
- Read-write separation at the tool level is the foundation of secure agent design
- Categorized as Advanced difficulty

## Related Concepts

- [[web3-tool-use]]
- [[policy]]
- [[guard]]
- [[session-key]]
- [[wallet-permission-safe-execution]]
- [[agent-wallet]]
- [[human-check]]

## Sources

- [[sources/bridge-chapters]]
