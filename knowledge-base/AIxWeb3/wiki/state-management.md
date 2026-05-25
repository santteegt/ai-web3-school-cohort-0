---
title: "State Management (Agent)"
type: concept
tags: [ai-foundations, agent]
source_count: 2
date_updated: "2026-05-24"
---

## Definition

State management in agent systems is the mechanism by which multiple nodes in an agent graph share read/write access to a common State object — enabling coordination, progress tracking, and context passing across the agent's execution steps.

## Key Points

- In multi-agent or multi-node graphs (e.g. LangGraph), all nodes read from and write to the same State object — state is the "whiteboard" the agent uses to pass results between steps
- State management is distinct from [[agent-memory]]: state is within-session shared workspace; memory is cross-session persistence
- State design determines agent debuggability — well-structured state makes [[ai-agent-tracing]] meaningful; flat or opaque state makes debugging impossible
- In AI × Web3, on-chain state (wallet balances, contract storage, transaction status) is a key input to the State object — agents must refresh it rather than caching stale values
- **"Keeping state only in prompt history is not enough"** — production systems need queryable, recoverable, auditable state
- State must include: user goal, completed steps, tool returns, errors, budget consumed, confirmation records, and final output. In external-execution scenarios: environment, version, key parameters, tool-call results, confirmation requests, and revocation events

## Related Concepts

- [[ai-agent]] — state management is a core agent component
- [[agent-memory]] — cross-session persistence, distinct from within-session state
- [[ai-agent-tracing]] — state is what's visualized in execution traces
- [[five-layer-agent-context]] — fact layer stores current tool results; state feeds into it
- [[context-engineering]] — current task state is one of the required elements in a stable agent context

- [[langgraph]] — LangGraph's graph state is the reference implementation for externalized, queryable agent state

## Sources

- [[sources/ai-fundamentals-introduction]] — state management as core agent component
- [[sources/agent]] — state must be externalized, queryable, recoverable, and auditable; state contents
