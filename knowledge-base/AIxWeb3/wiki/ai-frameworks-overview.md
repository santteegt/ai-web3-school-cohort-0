---
title: "AI Frameworks Overview"
type: topic
tags: [ai-foundations, frameworks]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

AI frameworks organize models, tools, state, retrieval, evaluation, and deployment into maintainable systems. The key selection criterion is understanding which layer of complexity a framework manages vs. hides — choosing the wrong one creates systems that are hard to debug, test, and replace.

## Framework Selection Principles

- "Understand the workflow first, then decide whether to use a framework"
- "Frameworks must be exit-able" — if it makes models, vector DBs, or deployment hard to change, the long-term cost is high
- Keep simple flows simple: single model calls with retrieval and output formatting do not require a framework
- Long workflows need explicit state: multi-step tasks with tool calls, human confirmation, and failure recovery need queryable state — not just chat history
- A framework is not a substitute for permissions, signatures, tx simulation, or account rules in Web3 systems

## Major Frameworks Covered

| Framework | Primary Use | Key Strength |
|---|---|---|
| [[langchain]] | Component composition | Quick prototyping, RAG, learning AI patterns |
| [[langgraph]] | Stateful agent workflows | DAG structure, branching, recovery, explicit state |
| [[openai-agents-sdk]] | Agent engineering primitives | Handoffs, guardrails, tracing, structured output |
| [[dspy]] | Prompt optimization | Metric-driven prompt improvement, repeatable tasks |
| [[hermes]] | Tool-calling reliability | Structured output, function calling format precision |

## The Three-Layer Responsibility Model

**AI Framework layer**: manages prompts, tools, state, evaluation, and traces  
**Web3 infrastructure layer**: manages accounts, signatures, contracts, transactions, and on-chain state  
**Product layer**: defines user goals, permission boundaries, confirmation flows, and failure handling

These layers must not be conflated — a framework cannot take asset risk on behalf of the user.

## Related Concepts

- [[ai-agent]] — frameworks are the infrastructure for building agents
- [[learning-agents]] — a system-level capability some frameworks support
- [[state-management]] — frameworks differ significantly in how they handle state
- [[ai-agent-tracing]] — all production frameworks should include tracing

## Sources

- [[sources/frameworks]] — framework selection criteria and individual framework descriptions
