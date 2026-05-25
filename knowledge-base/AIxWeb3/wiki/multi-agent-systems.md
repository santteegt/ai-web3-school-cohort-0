---
title: "Multi-Agent Systems"
type: concept
tags: [ai-foundations, agent]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

A multi-agent system is an architecture where multiple AI agents divide work in complex workflows — each agent handling a sub-task and passing results to others. While this enables parallelism and specialization, it amplifies coordination problems proportional to the number of agents.

## Key Points

- Coordination failure modes in multi-agent systems: lost context during transfers, unclear responsibility boundaries, treating another agent's mistaken output as fact, tool permissions spreading across roles
- "If you only split one unclear process into multiple unclear roles, the system becomes harder to debug" — complexity multiplies, it does not simplify
- Each agent in a multi-agent system needs the same design rigor as a single agent: clear goal, explicit stop conditions, defined tool permissions, and state isolation
- Handoff design is the critical coupling point — the receiving agent must validate inputs from the sending agent, not blindly trust them
- In AI × Web3, multi-agent systems must have explicit responsibility attribution: which agent authorized which action, whose permissions were used, who is accountable for each on-chain outcome

## Related Concepts

- [[ai-agent]] — the individual unit in multi-agent systems
- [[agent-handoff]] — the mechanism by which agents transfer work
- [[state-management]] — each agent needs isolated state; shared state is a coordination risk
- [[guardrails]] — each agent must enforce its own guardrails; they cannot be delegated to other agents
- [[agent-identity]] — AI × Web3 requires clear identity for each agent in a multi-agent system
- [[agent-planning]] — multi-agent orchestration requires a plan-level view across all agents
- [[ai-agent-tracing]] — tracing across agent boundaries is essential for debugging multi-agent failures

## Sources

- [[sources/agent]] — multi-agent coordination problems and design requirements
