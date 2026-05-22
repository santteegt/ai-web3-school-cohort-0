---
title: "Agent Handoff"
type: concept
tags: [ai-foundations, agent]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Agent handoff is the mechanism by which control is transferred from one agent (or agent node) to another after a subtask completes — enabling multi-agent systems where specialized agents handle different parts of a workflow.

## Key Points

- Handoff occurs when an agent determines it has completed its scope and the next step requires a different capability or context
- Handoffs must be explicit and auditable — the receiving agent should know exactly what state, results, and context it is receiving
- The handoff boundary is where error recovery logic engages — if a subtask failed, the system must decide to retry, rollback, or escalate before handing off
- In multi-agent architectures (orchestrator + specialist agents), the orchestrator decides when and to whom to hand off based on task progress
- Handoffs are related to [[agent-workflow]] decisions: which steps should be automated vs. require human-in-the-loop before proceeding

## Related Concepts

- [[ai-agent]] — handoff is a core agent component
- [[state-management]] — the state object is what's shared across a handoff
- [[agent-workflow]] — workflow design determines handoff points
- [[guardrails]] — handoff should only occur after guardrails pass on the completed subtask
- [[ai-agent-tracing]] — handoff events should be logged for observability

## Sources

- [[sources/ai-fundamentals-introduction]] — handoff as core agent component; transfer control after subtask completes
