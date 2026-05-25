---
title: "Block Explorer"
type: concept
tags: [web3-foundations, tooling, network]
source_count: 2
date_updated: "2026-05-25"
---

# Block Explorer

## Definition

A block explorer is a read-only web interface that provides human-readable access to all on-chain data: transactions, blocks, addresses, contract code, events, and token balances. Etherscan is the canonical Ethereum explorer; each chain typically has its own (Arbiscan, Basescan, etc.).

## Key Points

- **Transaction status**: see if a tx succeeded, failed, or is pending; view gas used and logs
- **Address inspection**: view transaction history, token balances, contract code for any address
- **Contract verification**: upload Solidity source code to prove the deployed bytecode matches → enables human-readable ABI interaction
- **Event logs**: view all emitted events from contract transactions — crucial for debugging and indexing
- **AI agent use**: agents can use explorer APIs or RPC to read on-chain state without a wallet
- **Testnet explorers**: Sepolia Etherscan, Holesky Etherscan — same interface for test networks
- **Blockscan / API**: programmatic access to explorer data via REST API (requires API key)

## Related Concepts

- [[web3-transaction]] — the primary data unit explorers display
- [[contract-event]] — event logs visible in explorers
- [[abi]] — explorer uses ABI to decode function calls and events
- [[block]] — organized by block number and hash
- [[rpc]] — alternative programmatic data access
- [[on-chain-indexing]] — explorers are a type of indexing service
- [[testnet]] — each testnet has its own explorer

## Sources

- [[sources/web3-chapters]] — Chapter: Wallet
- [[sources/web3-fundamentals-introduction]] — Module B: block explorers and receipts
