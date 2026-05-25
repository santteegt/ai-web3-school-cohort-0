---
title: "LangGraph"
type: concept
tags: [ai-foundations, frameworks, agent]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

LangGraph is a DAG-based workflow and state machine framework that represents agent tasks as graphs — nodes execute actions, edges control flow, and state records the process. It is the preferred choice when a workflow requires multiple tool calls, retries, human confirmation, branching, recovery, and long-running execution.

## Key Points

- LangGraph models workflows explicitly as graphs: nodes = actions, edges = transitions, state = shared workspace
- "An explicit graph is more reliable than a long prompt history" for workflows requiring: multiple tool calls, branching logic, human confirmation points, failure recovery, and long-running execution
- Useful when you need to answer: which step is the task on? Can it recover? Where does it resume after failure?
- LangGraph state is explicit and queryable — unlike LangChain chains where state lives implicitly in prompt history
- LangGraph supports: retries, conditional branching, human-in-the-loop checkpoints, parallel execution paths

## Related Concepts

- [[langchain]] — LangGraph is LangChain's graph/state-machine extension
- [[ai-frameworks-overview]] — LangGraph is the go-to framework for stateful agent workflows
- [[state-management]] — LangGraph's graph state is the model for externalized, queryable agent state
- [[agent-workflow]] — LangGraph implements the concept of agent workflow as explicit DAGs
- [[agent-handoff]] — LangGraph edges model handoffs between agent nodes
- [[guardrails]] — LangGraph supports built-in interrupt/confirmation nodes as guardrails

## Sources

- [[sources/frameworks]] — LangGraph definition and when to use it vs. LangChain
