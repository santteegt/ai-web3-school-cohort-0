---
title: "OpenAI Agents SDK"
type: concept
tags: [ai-foundations, frameworks, agent]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

The OpenAI Agents SDK is a framework that turns common agent engineering problems into composable structures — organizing agent instructions and tools, handoffs between multiple agents, tool calls and structured output, guardrails, and runtime tracing.

## Key Points

- Designed specifically for agent workflows, not just model integration — its primitives map directly to production agent components
- Core composable structures: agent definition (instructions + tools), handoff between agents, tool calls with structured output, guardrail rules, and execution tracing
- Useful as a reference architecture for what production agent engineering looks like — even if you don't use the SDK itself
- OpenAI-compatible API models benefit from tight integration with the SDK's tool-calling and structured output capabilities
- Contrast with [[langgraph]]: OpenAI Agents SDK is more opinionated about the agent abstraction; LangGraph is more flexible about workflow topology

## Related Concepts

- [[ai-frameworks-overview]] — one of the major frameworks in the AI agent ecosystem
- [[ai-agent]] — the SDK's core abstraction
- [[agent-handoff]] — a first-class SDK primitive
- [[guardrails]] — built-in to the SDK's agent definition
- [[ai-agent-tracing]] — runtime tracing is a core SDK feature
- [[structured-output]] — the SDK integrates function calling/structured output natively

## Sources

- [[sources/frameworks]] — OpenAI Agents SDK overview and composable structures
