---
title: "Agent Stop Conditions"
type: concept
tags: [ai-foundations, agent, security]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

Agent stop conditions are the explicit criteria that cause an agent to halt execution — preventing runaway, budget-exceeding, or dangerous autonomous operation. They must be defined before the agent starts, not discovered at runtime.

## Key Points

- "Stop conditions must be explicit" — the five canonical stop conditions: reaching the goal, exceeding budget, lacking information, crossing a risk boundary, or user rejection
- An agent without explicit stop conditions will continue executing indefinitely, accumulating tool calls, costs, and irreversible actions
- Stop conditions are part of the constrained execution loop definition — they are as important as the goal itself
- In AI × Web3: stop conditions should include on-chain thresholds (e.g. stop if simulated transaction loss exceeds X%) and time-based conditions (e.g. stop if no user confirmation within N minutes)
- Stop conditions should be checked by the system, not self-assessed by the model — "I think I'm done" is not a stop condition

## Related Concepts

- [[ai-agent]] — stop conditions are a core agent design element
- [[guardrails]] — stop conditions are implemented as guardrails
- [[agent-planning]] — good plans define stop conditions per step
- [[agent-reflection]] — reflection may trigger a stop condition if recovery is impossible
- [[machine-payment]] — budget stop conditions are especially critical for payment-capable agents
- [[agent-wallet]] — wallet permission limits are a form of stop condition

## Sources

- [[sources/agent]] — stop conditions definition and five canonical triggers
