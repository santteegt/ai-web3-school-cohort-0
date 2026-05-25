---
title: "AI Agent"
type: concept
tags: [ai-foundations, agent]
source_count: 2
date_updated: "2026-05-24"
---

## Definition

An AI agent is a **constrained execution loop** — a system where a language model plans autonomously, calls tools dynamically, and manages state across turns, operating within explicitly defined goals, tools, permissions, and stop conditions. Agents are appropriate when goals are open-ended, multiple tools must collaborate, intermediate results determine the next step, or state must persist across sessions.

## Key Points

- **Three architectures on a spectrum**: Prompt (human decides) → Workflow (predefined path) → Agent (model decides dynamically)
- These three differ fundamentally in **failure modes, risk exposure, and debuggability** — choosing the wrong one for a task creates problems that better prompting cannot fix
- **When to use an agent**: open-ended goal, multi-tool collaboration, intermediate results determine next step, state must persist across sessions
- **When NOT to use an agent**: one-off Q&A (use a prompt), fixed process (use a script), strict compliance (use a human review node), deterministic data needs (use a database query)
- "The higher the complexity and risk, the more cautious you should be about over-agentifying"
- Core technical components: [[state-management]], [[agent-memory]], [[mcp]], [[agent-planning]], [[tool-calling]], [[ai-agent-tracing]], [[guardrails]], [[agent-handoff]], [[agent-reflection]], [[agent-stop-conditions]], error recovery
- **Division of labor**: the model proposes candidate actions, the system limits the action space, the user approves high-risk boundaries — the model never authorizes its own actions
- "The most dangerous design is giving an Agent vague goals, broad tools, long-term memory, and large-asset permissions at the same time"
- A usable agent must know: what it can do / cannot do, how to verify completion, how to stop on failure, and who can audit what it has done
- **Tools are more dangerous than answers** — a wrong action creates real-world consequences; errors are no longer just wrong text

## Related Concepts

- [[tool-calling]] — the mechanism by which agents act on the world
- [[state-management]] — how agents maintain shared state across nodes
- [[agent-memory]] — how agents persist information across sessions
- [[agent-planning]] — breaking goals into verifiable, classified steps
- [[agent-reflection]] — self-checking mechanism for intermediate correction
- [[agent-stop-conditions]] — explicit halting criteria to prevent runaway execution
- [[guardrails]] — safety constraints that must hold regardless of agent decisions
- [[agent-handoff]] — how agents transfer control between subtasks
- [[ai-agent-tracing]] — how agent execution is made observable
- [[multi-agent-systems]] — multiple agents coordinating on complex workflows
- [[mcp]] — the protocol connecting agents to external tools
- [[prompt-workflow-agent-boundary]] — the conceptual boundary between the three architectures
- [[five-layer-agent-context]] — the context model for reliable agents
- [[ai-frameworks-overview]] — the frameworks used to build agents
- [[aixweb3-agent-architecture]] — the 8-step reference pattern for AI × Web3 agents
- [[agent-wallet]] — AI × Web3 extension: giving agents on-chain execution capability
- [[agent-identity]] — AI × Web3 extension: identifying and auditing agents

## Sources

- [[sources/ai-fundamentals-introduction]] — agent definition, components, and when-to-use criteria
- [[sources/agent]] — constrained execution loop framing, division of labor, stop conditions, AI × Web3 architecture
