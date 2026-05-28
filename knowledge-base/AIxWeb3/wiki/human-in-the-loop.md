---
title: "Human-in-the-loop"
type: concept
tags: [aixweb3-bridge, agent, workflow, wallet-permission]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Human-in-the-loop places humans at critical risk points in agent workflows rather than requiring confirmation for every low-risk step. The goal is layered risk-based confirmation: let agents automate what's safe, and escalate only what requires human judgment.

## Key Points

- Layered confirmation model: read-only analysis (automatic) → transaction drafts (automatic generation) → small whitelisted operations (session key) → high-risk transactions (manual confirm required) → policy violations (reject directly)
- The point is not whether there is human confirmation, but whether humans can understand asset changes, permission changes, and failure risks when they confirm
- Human check should show: what will this action change, where is the risk, and why is confirmation needed now
- Does not mean throwing everything back to the user — that defeats the purpose of an agent

## Related Concepts

- [[agent-workflow]]
- [[human-check]]
- [[agent-wallet]]
- [[policy]]
- [[guard]]
- [[session-key]]
- [[wallet-permission-safe-execution]]
- [[cobo-pact]]

## Sources

- [[sources/bridge-chapters]]
