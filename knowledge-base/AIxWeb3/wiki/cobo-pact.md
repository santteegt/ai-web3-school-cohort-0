---
title: "Cobo CAW Pact (Task-Level Authorization)"
type: concept
tags: [aixweb3-bridge, wallet-permission, agent, security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Cobo CAW's Pact is a task-level authorization model where, instead of granting an agent a long-term permission, a temporary authorization is generated around one concrete task. The user first confirms the agent's task intent, budget, operation scope, time window, and failure-handling strategy. The agent can only execute within those defined boundaries, and the permission expires when the task ends.

## Key Points

- Replaces long-term persistent permission grants with task-scoped, time-bounded permissions
- User confirmation step includes: task intent, budget ceiling, allowed operations, time window, and failure-handling strategy
- The agent cannot exceed any boundary set in the Pact — scope, amount, or time
- Permission automatically expires at task completion, reducing residual risk from open authorizations
- Represents a practical implementation of the principle "separate steps that can be automated from steps that require human confirmation"

## Related Concepts

- [[wallet-permission-safe-execution]]
- [[agent-wallet]]
- [[policy]]
- [[guard]]
- [[session-key]]
- [[human-in-the-loop]]
- [[revocation]]
- [[budget]]
- [[smart-account]]

## Sources

- [[sources/aixweb3-bridge-introduction]]
