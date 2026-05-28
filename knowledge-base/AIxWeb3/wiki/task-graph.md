---
title: "Task Graph"
type: concept
tags: [aixweb3-bridge, agent, workflow]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Task Graph breaks down goals into nodes and dependencies rather than letting an agent execute freely all at once. Each node has its own input, output, permissions, and stop conditions. This transforms "help me evaluate and execute a swap" into a sequence of verifiable steps.

## Key Points

- Example breakdown for a swap: read goals → fetch balance/allowance → query price → generate transaction → simulate → display risks → user confirmation → send → track
- Each step has explicit inputs, outputs, available tools, and failure handling
- Task graphs enable parallel processing where dependencies allow, and strict sequencing where they don't
- Foundation for state machines — a task graph defines what the states are

## Related Concepts

- [[agent-workflow]]
- [[state-machine]]
- [[human-in-the-loop]]
- [[trace]]
- [[agent-planning]]
- [[langgraph]]

## Sources

- [[sources/bridge-chapters]]
