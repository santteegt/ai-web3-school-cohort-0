---
title: "Data Pipeline"
type: concept
tags: [web3-foundations, indexing, data]
source_count: 1
date_updated: "2026-05-25"
---

# Data Pipeline

## Definition

A data pipeline in the Web3 context is an Extract-Transform-Load (ETL) process that reads raw blockchain data (transactions, events, state), transforms it into structured, queryable form, and loads it into a database or analytics system. Data pipelines power block explorers, DeFi dashboards, protocol analytics, and AI agent context systems.

## Key Points

- **Extraction**: subscribe to new blocks/events via RPC WebSocket subscriptions or batch-scan historical blocks
- **Transformation**: decode ABI-encoded calldata and event logs; join with reference data; compute derived metrics
- **Loading**: write to PostgreSQL, ClickHouse, BigQuery, or a vector database for AI retrieval
- **Latency tiers**: real-time (< 1 block, via WebSocket); near-real-time (1–10 blocks, batch); historical (full re-index)
- **Backfill**: initial load of all historical data from genesis block; can take days on large chains
- **Forks / reorgs**: pipeline must handle chain reorganizations — revert processed blocks, reapply canonical blocks
- **AI × Web3**: data pipelines feed AI agents with structured on-chain context — positions, protocol state, event history

## Related Concepts

- [[on-chain-indexing]] — data pipelines implement the indexing step
- [[subgraph]] — a declarative data pipeline framework
- [[contract-event]] — raw ETL source
- [[rpc]] — extraction layer for chain data
- [[chain-aware-context]] — the AI × Web3 concept powered by data pipelines
- [[knowledge-base]] — structured on-chain data is a form of knowledge base for agents

## Sources

- [[sources/web3-chapters]] — Chapter: Indexing
