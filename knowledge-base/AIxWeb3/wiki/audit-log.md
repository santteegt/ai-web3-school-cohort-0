---
title: "Audit Log"
type: concept
tags: [aixweb3-bridge, privacy-security, observability]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Audit Log records the agent's context, decisions, tool calls, and execution results. Without logs, reviewing security incidents is impossible. What's truly useful is the full chain: context seen → tool chosen → tool returned → policy passed → user confirmed.

## Key Points

- Critical fields: user requests, model version, reference sources, tool inputs/outputs, policy judgments, transaction hashes, user confirmations, and errors
- Don't just record the "final answer" — log the full decision chain
- Must be tamper-proof for high-value systems: anchor log hashes on-chain or use signatures for key events
- Distinct from trace: trace is per-task execution record; audit log is the persistent security-oriented record store

## Related Concepts

- [[ai-security]]
- [[trace]]
- [[tool-log]]
- [[audit-trail]]
- [[alert]]
- [[observability]]

## Sources

- [[sources/bridge-chapters]]
