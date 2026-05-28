---
title: "Audit Trail"
type: concept
tags: [aixweb3-bridge, verifiable-ai, security, observability]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Audit Trail is the most basic and practical verifiable layer for AI × Web3 systems. It records inputs, outputs, model version, tool calls, time, user confirmation, transaction hashes, and errors. Without TEE or ZK, a complete audit trail still supports review, disputes, and improvement.

## Key Points

- Cannot prove a model is absolutely correct, but proves what the system saw, called, and what the user confirmed at the time
- Easiest starting point for landing verifiable AI in production
- Logs must avoid leaking privacy: sensitive original text is stored encrypted; public layer puts only hashes, summaries, and references
- High-value systems can regularly anchor log hashes to the chain or use signatures to record key events (tamper-proof)

## Related Concepts

- [[verifiable-ai]]
- [[trace]]
- [[tool-log]]
- [[audit-log]]
- [[proof-of-inference]]
- [[ai-oracle]]

## Sources

- [[sources/bridge-chapters]]
