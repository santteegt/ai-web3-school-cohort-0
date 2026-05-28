---
title: "Transaction History"
type: concept
tags: [web3-foundations, aixweb3-bridge, context]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Transaction History helps an Agent understand what a user or contract has done in the past. It is used to determine prior authorizations, executed strategies, high-risk contract interactions, and recent contract upgrades.

## Key Points

- Minimum required fields: transaction hash, block number, from, to, method, value, token transfers, and logs
- Models can summarize transaction history, but evidence must lead back to the chain (hash or explorer link)
- Transaction history cannot be just a natural language summary — it must be verifiable
- Use cases: checking if authorization was already given, whether a strategy was executed, whether an address has interacted with high-risk contracts

## Related Concepts

- [[chain-aware-context]]
- [[on-chain-data]]
- [[explorer-context]]
- [[indexing-context]]
- [[contract-audit]]

## Sources

- [[sources/bridge-chapters]]
