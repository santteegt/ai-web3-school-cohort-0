---
title: "Layer 2 (L2)"
type: concept
tags: [web3-foundations, network, scaling]
source_count: 2
date_updated: "2026-05-25"
---

# Layer 2 (L2)

## Definition

Layer 2 refers to blockchain scaling solutions that execute transactions off the main chain (Layer 1) but inherit its security by posting proofs or data back to L1. The goal is to increase throughput and reduce costs while preserving the trust model of the underlying L1.

## Key Points

- **Why L2**: Ethereum L1 handles ~15 TPS; gas fees spike to $50+ during congestion; L2s achieve thousands of TPS at cents per transaction
- **Rollups**: the dominant L2 architecture; batch thousands of transactions, post compressed data + validity proof to L1
- **Optimistic rollups**: Arbitrum, Optimism, Base — assume transactions are valid by default; fraud proofs if challenged; 7-day withdrawal window
- **ZK rollups**: Starknet, zkSync, Polygon zkEVM — post zero-knowledge validity proofs; fast finality; harder to build
- **EVM compatibility**: most L2s are EVM-compatible; deploy same contracts, same tooling
- **Data availability**: L2 security depends on L1 storing enough data to reconstruct L2 state if sequencer fails
- **EIP-4844 (blobs)**: introduced cheaper DA for rollups by adding blob-carrying transactions to L1
- **AI × Web3**: lower gas makes agent micro-payments and frequent on-chain actions economically viable

## Related Concepts

- [[rollup]] — the primary L2 architecture
- [[blockchain-network]] — L2 inherits L1 security
- [[gas]] — L2 reduces gas costs dramatically
- [[evm]] — most L2s are EVM-compatible
- [[consensus]] — L2 sequencer for ordering; L1 for finality
- [[machine-payment]] — L2 gas economics enable agent micro-payments

## Sources

- [[sources/web3-chapters]] — Chapter: Network
- [[sources/web3-fundamentals-introduction]] — Module B: L1/L2 and execution costs
