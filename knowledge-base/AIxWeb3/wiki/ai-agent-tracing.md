---
title: "Agent Tracing"
type: concept
tags: [ai-foundations, agent]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Agent tracing is the practice of capturing and visualizing the full execution chain of an agent — each tool call, state change, model decision, handoff, and guardrail check — to make agent behavior observable, debuggable, and auditable.

## Key Points

- Without tracing, agent failures are opaque: "the agent did something wrong but we don't know what or why"
- Tracing enables identification of tool misuse (wrong tool, wrong parameters), execution overreach, and reasoning drift
- Traces can be used for: debugging failures, evaluating agent performance, auditing actions for compliance, and generating training data for improvement
- Good traces capture: timestamp, model input, model output, tool called, tool parameters, tool result, state before/after, guardrail outcomes
- In AI × Web3, on-chain tracing complements agent tracing — transaction hashes and event logs provide immutable records of execution

## Related Concepts

- [[ai-agent]] — tracing is a core agent component
- [[state-management]] — state transitions are the primary content of a trace
- [[tool-calling]] — each tool call should be a trace event
- [[guardrails]] — guardrail outcomes should be traced
- [[agent-handoff]] — handoff events are key trace events
- [[hallucination]] — tracing helps detect tool misuse that results from hallucinated parameters

## Sources

- [[sources/ai-fundamentals-introduction]] — tracing as core agent component; visualize execution chain
