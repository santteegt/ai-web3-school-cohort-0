---
title: "Prompt / Workflow / Agent Boundary"
type: concept
tags: [ai-foundations, agent, prompt]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

The Prompt / Workflow / Agent boundary is the conceptual distinction between three architectures for using LLMs, differing in who makes decisions, how flexible the execution path is, and what failure modes arise.

## Key Points

| Architecture | Decision Maker | Execution Path | Failure Mode |
|---|---|---|---|
| **Prompt** | Human | Single LLM call | Hallucination, misunderstanding |
| **Workflow** | Developer (predefined) | Fixed pipeline, model is one node | Pipeline failure, brittle to edge cases |
| **Agent** | Model (autonomous) | Dynamic, tool-driven | Execution overreach, tool misuse, reasoning drift |

- These differ **fundamentally** in failure modes, risk exposure, and debuggability — not just in complexity
- Over-agentifying is a real risk: "the higher the complexity and risk, the more cautious you should be"
- Most production AI systems are workflows, not agents — understanding this boundary prevents misapplied architecture

## Related Concepts

- [[ai-agent]] — the autonomous planning architecture
- [[tool-calling]] — what distinguishes agents from prompts
- [[guardrails]] — necessary specifically because agents have dynamic, risky execution paths
- [[prompt-design]] — the non-agent alternative; human retains decision-making

## Sources

- [[sources/ai-fundamentals-introduction]] — three-way distinction and its failure mode differences
