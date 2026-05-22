---
title: "AI Agent"
type: concept
tags: [ai-foundations, agent]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

An AI agent is a system where a language model plans autonomously, calls tools dynamically, and manages state across turns — as opposed to a prompt (single response) or a workflow (fixed pipeline). Agents are appropriate when goals are open-ended, multiple tools must collaborate, intermediate results determine the next step, or state must persist across sessions.

## Key Points

- **Three architectures on a spectrum**: Prompt (human decides) → Workflow (predefined path) → Agent (model decides dynamically)
- These three differ fundamentally in **failure modes, risk exposure, and debuggability** — choosing the wrong one for a task creates problems that better prompting cannot fix
- **When to use an agent**: open-ended goal, multi-tool collaboration, intermediate results determine next step, state must persist across sessions
- **When NOT to use an agent**: one-off Q&A (use a prompt), fixed process (use a script), strict compliance (use a human review node), deterministic data needs (use a database query)
- "The higher the complexity and risk, the more cautious you should be about over-agentifying"
- Core technical components: [[state-management]], [[agent-memory]], [[mcp]], skills, [[tool-calling]], [[ai-agent-tracing]], [[guardrails]], [[agent-handoff]], error recovery

## Related Concepts

- [[tool-calling]] — the mechanism by which agents act on the world
- [[state-management]] — how agents maintain shared state across nodes
- [[agent-memory]] — how agents persist information across sessions
- [[guardrails]] — safety constraints that must hold regardless of agent decisions
- [[agent-handoff]] — how agents transfer control between subtasks
- [[ai-agent-tracing]] — how agent execution is made observable
- [[mcp]] — the protocol connecting agents to external tools
- [[prompt-workflow-agent-boundary]] — the conceptual boundary between the three architectures
- [[five-layer-agent-context]] — the context model for reliable agents
- [[agent-wallet]] — AI × Web3 extension: giving agents on-chain execution capability
- [[agent-identity]] — AI × Web3 extension: identifying and auditing agents

## Sources

- [[sources/ai-fundamentals-introduction]] — agent definition, components, and when-to-use criteria
