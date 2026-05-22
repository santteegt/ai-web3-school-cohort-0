---
title: "Agent Memory"
type: concept
tags: [ai-foundations, context, agent]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

Agent memory is information retained across requests — user preferences, historical tasks, commonly used wallets, project configuration, and previous analysis results — that allows an agent to behave more smoothly over time without re-establishing context from scratch each session.

## Key Points

- Memory can make an agent smoother to use, but it also introduces **hidden risk**: the system may loosen safety constraints based on remembered preferences (e.g. "user has high risk tolerance → skip confirmation on high-risk transactions")
- **Memory cannot replace real-time authorization** — anything related to identity, permissions, assets, or external side effects must be rebound to the current session and current authorization
- **Memory must be revocable** — user preferences and historical tasks must not become permanent identity assumptions or hidden permissions
- Memory is the fifth layer in the [[five-layer-agent-context]] model — below instruction, task, fact, and knowledge layers
- Long-term memory stores information across sessions; working memory (context window) holds it within a session

## Related Concepts

- [[five-layer-agent-context]] — memory is the fifth layer
- [[context-engineering]] — deciding what memories to retrieve and inject into context
- [[context-window]] — memories retrieved into context consume window budget
- [[ai-agent]] — agents use memory for state continuity across sessions
- [[state-management]] — within-session state vs. cross-session memory
- [[information-governance]] — memory entries require source, age, and revocability tracking
- [[guardrails]] — must apply regardless of what memory says about permissions

## Sources

- [[sources/context]] — memory as cross-request retention; hidden risk and revocability requirement
- [[sources/ai-fundamentals-introduction]] — long-term memory as a core agent component
