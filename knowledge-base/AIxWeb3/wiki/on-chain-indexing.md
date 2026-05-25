---
title: "On-Chain Indexing"
type: concept
tags: [web3-foundations, indexing, data]
source_count: 1
date_updated: "2026-05-25"
---

# On-Chain Indexing

## Definition

On-chain indexing is the process of extracting, transforming, and loading blockchain event data into queryable databases, enabling efficient access to historical and current chain state. Raw blockchain data is hard to query directly (no SQL, only RPC calls per block/tx); indexers build structured, searchable representations on top.

## Key Points

- **Why needed**: querying "all ERC-20 transfers to address X in the past month" via raw RPC requires scanning thousands of blocks — indexers pre-compute this
- **Event-driven**: most indexers are built on contract event logs; events are the canonical signal of state changes
- **The Graph**: dominant decentralized indexing protocol; developers write "Subgraphs" (manifest + mappings) that index specific events and expose a GraphQL API
- **Centralized alternatives**: Alchemy, Infura, Moralis, Dune Analytics — offer managed indexing APIs; simpler but centralized trust
- **Dune Analytics**: SQL-based analytics over indexed Ethereum data; collaborative dashboards; used for DeFi analytics and research
- **Neon / Ponder**: emerging lightweight frameworks for custom local indexers
- **AI agent use**: agents can query indexed data (via GraphQL or SQL) to get rich historical context about on-chain state without making hundreds of raw RPC calls

## Related Concepts

- [[contract-event]] — the raw input to indexers
- [[subgraph]] — The Graph's indexing unit
- [[rpc]] — alternative direct access (unindexed)
- [[data-pipeline]] — the ETL process underlying indexers
- [[blockchain-network]] — the data source
- [[chain-aware-context]] — indexed data enables AI agents to reason about chain state

## Sources

- [[sources/web3-chapters]] — Chapter: Indexing
