---
title: "Contract Event"
type: concept
tags: [web3-foundations, smart-contracts, indexing]
source_count: 1
date_updated: "2026-05-25"
---

# Contract Event

## Definition

A contract event is a log entry emitted during smart contract execution. Events are stored in the transaction receipt (not in contract storage) and are the primary mechanism by which off-chain systems observe on-chain state changes. Indexers, frontends, and data pipelines subscribe to events to build responsive dApps.

## Key Points

- **Emitted with `emit`** in Solidity: `emit Transfer(from, to, amount)`
- **Stored in receipts, not storage**: events don't change contract state; they are logs attached to transaction receipts
- **Indexed topics**: up to 3 event parameters can be declared `indexed`, making them efficiently filterable by RPC
- **Event signature**: first topic = Keccak256(event signature); identifies the event type
- **Gas efficient**: logging is cheaper than storage; used for auditing and off-chain integration
- **Immutable**: once in a transaction receipt, events cannot be changed or deleted
- **Primary input to indexers**: The Graph's Subgraphs are built by processing event logs

## Related Concepts

- [[smart-contract]] — emits events during execution
- [[abi]] — events are described in the ABI
- [[web3-transaction]] — events appear in transaction receipts
- [[on-chain-indexing]] — events are the raw material for indexers
- [[subgraph]] — GraphQL APIs built on event indexing
- [[block-explorer]] — events visible in the "Logs" tab of a transaction
- [[rpc]] — `eth_getLogs` RPC method retrieves events

## Sources

- [[sources/web3-chapters]] — Chapter: Smart Contract, Indexing
