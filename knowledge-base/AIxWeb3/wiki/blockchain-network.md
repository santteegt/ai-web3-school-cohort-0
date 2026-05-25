---
title: "Blockchain Network"
type: concept
tags: [web3-foundations, network]
source_count: 1
date_updated: "2026-05-25"
---

# Blockchain Network

## Definition

A blockchain network is a peer-to-peer distributed system where nodes agree on a single canonical sequence of blocks (the chain) via a consensus mechanism. The chain stores all transactions ever made; its state (account balances, contract storage) is derived by replaying all transactions from genesis. No single party controls it.

## Key Points

- **Nodes**: any participant running the client software; each holds a full copy of the chain
- **Canonical chain**: nodes converge on the same chain via consensus rules (longest chain, heaviest chain, etc.)
- **Permissionless**: anyone can join, deploy contracts, or send transactions without approval
- **Immutability**: once a block is sufficiently deep, reversing it requires rewriting the majority of the chain (economically infeasible on secured networks)
- **L1 vs L2**: L1 = the base chain (Ethereum); L2 = chains that inherit L1 security while scaling throughput
- **EVM chains**: Ethereum, Polygon, Arbitrum, Optimism, Base, Avalanche C-Chain — all share the EVM execution environment
- **Mainnets vs testnets**: mainnets use real value; testnets (Sepolia, Holesky) use valueless test tokens

## Related Concepts

- [[block]] — the unit of chain state advancement
- [[consensus]] — the agreement mechanism
- [[proof-of-stake]] — Ethereum's consensus
- [[layer-2]] — scaling on top of L1
- [[rollup]] — the dominant L2 architecture
- [[testnet]] — safe practice environment
- [[evm]] — the shared execution environment across many chains

## Sources

- [[sources/web3-chapters]] — Chapter: Network
