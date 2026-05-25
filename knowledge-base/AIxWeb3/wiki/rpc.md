---
title: "RPC (Remote Procedure Call)"
type: concept
tags: [web3-foundations, indexing, dev-tooling, network]
source_count: 1
date_updated: "2026-05-25"
---

# RPC (Remote Procedure Call)

## Definition

In Web3, RPC (Remote Procedure Call) refers to the JSON-RPC API exposed by Ethereum nodes (and EVM-compatible chains) for reading chain state and submitting transactions. The `eth_` namespace defines the standard methods. Services like Infura, Alchemy, and QuickNode provide hosted RPC endpoints so developers and applications don't need to run their own nodes.

## Key Points

- **Standard methods**: `eth_call` (read contract state), `eth_sendRawTransaction` (broadcast tx), `eth_getLogs` (fetch event logs), `eth_getBalance`, `eth_blockNumber`, `eth_getTransactionReceipt`
- **HTTP vs WebSocket**: HTTP for one-off reads; WebSocket for subscriptions (`eth_subscribe`) — event-driven updates
- **Rate limits**: free public endpoints (Cloudflare, PublicNode) are heavily rate-limited; production apps use Infura/Alchemy with API keys
- **Archive nodes**: standard nodes keep recent state; archive nodes keep all historical state; needed for `eth_call` at old block numbers
- **RPC providers**: Infura, Alchemy, QuickNode, Ankr, Tenderly — managed node-as-a-service
- **Privacy consideration**: every RPC call reveals the queried address to the provider; privacy-preserving RPC (OHTTP) is emerging
- **AI agent use**: agents use RPC to read on-chain state (balances, prices, contract state) without a wallet or private key

## Related Concepts

- [[blockchain-network]] — RPC is the interface to network nodes
- [[on-chain-indexing]] — RPC provides raw data; indexers structure it
- [[subgraph]] — Subgraph nodes use RPC to scan chain data
- [[viem-wagmi]] — viem abstracts JSON-RPC into typed calls
- [[web3-tool-use]] — AI agents use RPC as a read tool
- [[contract-event]] — `eth_getLogs` is the RPC method to fetch events

## Sources

- [[sources/web3-chapters]] — Chapter: Indexing
