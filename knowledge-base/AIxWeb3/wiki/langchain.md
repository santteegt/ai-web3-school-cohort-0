---
title: "LangChain"
type: concept
tags: [ai-foundations, frameworks]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

LangChain is a component library for composing AI application capabilities — covering model integration, prompts, tool calls, retrievers, agents, and output parsers. It is useful for quickly connecting model capabilities to external systems and for learning common AI application components.

## Key Points

- LangChain helps compose capabilities quickly; it is a good entry point for learning RAG, tool use, and agent patterns
- Risk in production: LangChain's abstraction layer can hide complexity rather than managing it — debugging becomes harder when abstractions break
- "The major mistake is bending product logic around a framework" — LangChain should express your workflow, not define it
- LangChain works well for: simple model calls with retrieval and output formatting; learning how components connect
- LangChain works less well for: complex multi-step workflows needing explicit state, branching, and recovery — use [[langgraph]] instead for those
- Abstraction exit: ensure the system can replace LangChain components (models, vector DBs, deployment) without architectural surgery

## Related Concepts

- [[ai-frameworks-overview]] — LangChain is one of the main frameworks in the AI orchestration landscape
- [[langgraph]] — LangChain's graph/state-machine extension for stateful workflows
- [[retrieval-augmented-generation]] — LangChain has built-in RAG component support
- [[tool-calling]] — LangChain organizes tool calls as composable modules
- [[state-management]] — LangChain's chain-based approach is weaker than LangGraph's explicit state for complex tasks

## Sources

- [[sources/frameworks]] — LangChain description, use cases, and production tradeoffs
