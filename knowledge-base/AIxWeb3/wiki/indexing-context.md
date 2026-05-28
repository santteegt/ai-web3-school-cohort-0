---
title: "Indexing Context"
type: concept
tags: [web3-foundations, aixweb3-bridge, context]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Indexing Context is on-chain events organized as product-oriented, queryable data. Agents need to answer questions like "what DeFi operations has this user done in the last 30 days" or "what payments has this Agent made" — these require an indexing layer, not raw block queries.

## Key Points

- Indexing context must include timestamps and sync status — results 500 blocks behind should not be treated as current facts
- Use cases: user DeFi operation history, TVL changes, payment history, governance event logs
- Common indexing layers: The Graph subgraphs, custom indexers, protocol APIs
- Queries are product-oriented (user-level, not block-level)

## Related Concepts

- [[chain-aware-context]]
- [[on-chain-data]]
- [[on-chain-indexing]]
- [[subgraph]]
- [[transaction-history]]

## Sources

- [[sources/bridge-chapters]]
