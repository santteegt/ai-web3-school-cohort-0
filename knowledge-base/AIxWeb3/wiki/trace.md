---
title: "Trace"
type: concept
tags: [aixweb3-bridge, agent, workflow, observability]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Trace is a record of every input, judgment, tool call, and result of the agent during a task execution. It is the difference between reviewing only chat logs (limited) versus reconstructing the full decision chain (complete).

## Key Points

- Minimum trace fields: user goals, model version, context sources, tool inputs/outputs, policy judgments, simulation results, human confirmation, transaction hashes, and final status
- With traces, post-incident review can determine: model misunderstanding, tool error, policy omission, or user confirming the wrong action
- Without traces, only chat logs exist — insufficient for security review
- Traces should not log secrets (private keys, API keys); use hashes for sensitive values

## Related Concepts

- [[agent-workflow]]
- [[tool-log]]
- [[audit-log]]
- [[audit-trail]]
- [[ai-agent-tracing]]
- [[regression-set]]

## Sources

- [[sources/bridge-chapters]]
