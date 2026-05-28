---
title: "Permission Isolation"
type: concept
tags: [aixweb3-bridge, privacy-security, agent, wallet-permission]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Permission Isolation separates tools, data, and actions of different risk levels into distinct capabilities and environments. Do not give an agent an "all-purpose Web3 tool" — the narrower the interface, the safer the execution boundary.

## Key Points

- Read-only chain queries, transaction drafts, sending transactions, revoking authorizations, and large payments should be separate capabilities
- Environment isolation: browser environment (handling web pages) should not read wallet keys; sandbox (executing code) should not access production databases; document summarization model should not send transactions
- The closer to assets and permissions, the narrower the tool interface should be
- "The safest tool is the one that does exactly the task and cannot exceed boundaries"

## Related Concepts

- [[ai-security]]
- [[tool-permission]]
- [[sandbox]]
- [[guard]]
- [[key-safety]]
- [[wallet-permission-safe-execution]]
- [[least-privilege]]

## Sources

- [[sources/bridge-chapters]]
