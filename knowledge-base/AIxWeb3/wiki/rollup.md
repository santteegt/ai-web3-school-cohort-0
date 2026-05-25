---
title: "Rollup"
type: concept
tags: [web3-foundations, network, scaling]
source_count: 1
date_updated: "2026-05-25"
---

# Rollup

## Definition

A rollup is a Layer 2 scaling architecture that executes transactions off-chain and posts compressed transaction data (plus a validity proof) to the Layer 1 chain. By batching thousands of transactions into one L1 submission, rollups reduce per-transaction costs by 10–100x while inheriting L1's security guarantees.

## Key Points

- **Sequencer**: collects user transactions, orders them, executes them in a local EVM, produces a new state root
- **Data posting**: compresses transaction data (calldata or EIP-4844 blobs) and posts to L1; needed so anyone can reconstruct L2 state
- **Optimistic rollups**: post state roots without proof; dispute window (7 days) allows fraud proofs; Arbitrum, Optimism, Base
- **ZK rollups**: post cryptographic validity proofs (ZK-SNARK or STARK) with each batch; no dispute window; fast finality; zkSync, Starknet
- **Withdrawal delay**: optimistic rollups require 7-day exit window; bridges provide faster exits at a fee
- **EIP-4844 blobs**: separate blob-carrying transactions reduce DA costs ~10x; adopted by most rollups in 2024
- **Decentralized sequencer**: most rollups currently have a centralized sequencer; decentralization is active research area

## Related Concepts

- [[layer-2]] — rollup is the dominant L2 architecture
- [[evm]] — rollup executes EVM transactions off-chain
- [[merkle-tree]] — state roots and proofs use Merkle structures
- [[block]] — rollup batches correspond to L1 blocks or blob-carrying transactions
- [[consensus]] — L1 consensus provides finality for rollup data
- [[gas]] — rollup amortizes L1 gas over many transactions

## Sources

- [[sources/web3-chapters]] — Chapter: Network
