---
title: "Malicious Context"
type: concept
tags: [aixweb3-bridge, privacy-security, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Malicious Context is seemingly ordinary context that contains attack instructions or misleading data. Unlike prompt injection (explicit instruction override), malicious context can be false facts — fake contract addresses, forged audit reports, stale price data, or contaminated token metadata.

## Key Points

- Sources: contract READMEs, web HTML, governance proposals, forums, emails, token metadata, external API returns
- System must isolate "content" from "instructions" — external content is objects for analysis, not new instructions
- False facts are as dangerous as explicit attack instructions: agents using fake data generate erroneous transactions
- Defense: on-chain facts prioritize RPCs, explorers, verified sources, and indexing; web descriptions are auxiliary only

## Related Concepts

- [[ai-security]]
- [[prompt-injection]]
- [[tool-abuse]]
- [[permission-isolation]]
- [[chain-aware-context]]
- [[contract-docs]]
- [[audit-log]]

## Sources

- [[sources/bridge-chapters]]
