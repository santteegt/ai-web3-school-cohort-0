---
title: "Subgraph (The Graph)"
type: concept
tags: [web3-foundations, indexing, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# Subgraph (The Graph)

## Definition

A Subgraph is an indexing unit in The Graph Protocol — a decentralized network for indexing and querying blockchain data. Developers write a Subgraph manifest (defining which contracts/events to index) and mapping handlers (TypeScript/AssemblyScript that transform events into entities). Once deployed, the Subgraph exposes a GraphQL API over the indexed data.

## Key Points

- **Manifest (`subgraph.yaml`)**: specifies which contracts to watch, which events to handle, and the start block
- **Schema (`schema.graphql`)**: defines the entity types that the Subgraph will store and expose
- **Mapping handlers**: event handler functions that receive emitted events and update entity state in the store
- **GraphQL API**: once deployed, query indexed data with standard GraphQL — filters, sorting, pagination
- **Decentralized network**: indexers in The Graph Network are paid in GRT to serve Subgraph queries; curators signal on high-quality Subgraphs
- **Hosted service vs. network**: Graph Studio (hosted) for development; The Graph Network for production decentralization
- **Limitations**: indexing lag (~few seconds per block), complex queries can be expensive, no real-time streaming (use webhooks)

## Related Concepts

- [[on-chain-indexing]] — Subgraph is The Graph's indexing unit
- [[contract-event]] — events are the raw input to Subgraph mappings
- [[rpc]] — Subgraph nodes use RPC to scan blocks
- [[data-pipeline]] — Subgraph is a structured data pipeline
- [[chain-aware-context]] — Subgraph data enriches AI agent context
- [[defi]] — most major DeFi protocols have canonical Subgraphs

## Sources

- [[sources/web3-chapters]] — Chapter: Indexing
