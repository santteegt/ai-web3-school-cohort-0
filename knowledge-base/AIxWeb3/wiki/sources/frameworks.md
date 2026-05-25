---
title: "Frameworks"
type: source
tags: [ai-foundations, agent, frameworks, langchain, langgraph, dspy]
source_file: "raw/Frameworks.md"
source_hash: "sha256:1dcc052435fe93bd6538a760ddd9a8a589722a32cd90b8107adb04362cac2641"
date_ingested: "2026-05-24"
---

## Summary

This source covers AI orchestration frameworks — what they are for, how to choose between them, and their failure modes. Its core argument is that the most important selection criterion is understanding which layer of complexity a framework manages vs. hides. The source surveys LangChain, LangGraph, OpenAI Agents SDK, DSPy, and Hermes, and introduces the concept of learning agents — systems that improve from feedback through an evaluation loop rather than direct online behavior change.

## Key Concepts

- [[ai-frameworks-overview]] — frameworks organize model, tools, state, retrieval, evaluation, and deployment into maintainable systems
- [[langchain]] — component library for composing model capabilities; good for learning; may create abstraction traps in production
- [[langgraph]] — DAG-based workflows and state machines; more reliable than prompt history for multi-step tasks with branching and recovery
- [[openai-agents-sdk]] — turns common agent engineering problems (handoffs, tools, guardrails, tracing) into composable structures
- [[dspy]] — prompt optimization framework; writes prompts as optimizable programs; requires dataset and evaluation metrics
- [[hermes]] — tool-calling and structured-output oriented model/agent ecosystem
- [[learning-agents]] — systems that improve from feedback via evaluation loop; direct online behavior change introduces data pollution risk
- [[state-management]] — multi-step tasks need queryable state, not only chat history
- [[ai-agent-tracing]] — online behavior needs tracing in all production frameworks

## Notable Points

- "The most important judgment when choosing a framework is: which layer of complexity does it help you manage, and which complexity does it hide?"
- "Understand the workflow first, then decide whether to use a framework. The major mistake is bending product logic around a framework."
- Frameworks manage prompts, tools, state, eval, and traces. Web3 infra manages accounts, signatures, contracts, and on-chain state. Product layer defines user goals, permissions, and confirmation flows. These three layers must not be conflated.
