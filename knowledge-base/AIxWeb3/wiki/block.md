---
title: "Block"
type: concept
tags: [web3-foundations, network]
source_count: 1
date_updated: "2026-05-25"
---

# Block

## Definition

A block is the fundamental unit of chain state advancement. It is a batched, ordered collection of transactions, together with metadata (parent hash, timestamp, validator, gas limit, Merkle roots of state and transactions). Blocks are linked by their parent hash — each block commits to the previous block, forming the "chain."

## Key Points

- **Contents**: transaction list, block header (parent hash, timestamp, beneficiary, stateRoot, txRoot, receiptsRoot, gasLimit, gasUsed, baseFeePerGas, etc.)
- **Block time**: Ethereum ~12 seconds per slot; L2s often faster (1–2 seconds or faster)
- **Slot vs epoch**: PoS divides time into slots (12s); 32 slots = 1 epoch; finality takes ~2 epochs (~13 minutes)
- **Block producer**: in PoS, a randomly selected validator proposes the block; attestors vote to confirm
- **Block reorganization ("reorg")**: when a competing chain branch temporarily replaces recent blocks; short reorgs are normal
- **Transaction ordering**: validators have discretion over ordering → MEV extraction
- **Finality**: after 2 epochs, a block is considered finalized; practically irreversible

## Related Concepts

- [[blockchain-network]] — blocks form the chain
- [[consensus]] — mechanism for agreeing on which block is canonical
- [[proof-of-stake]] — Ethereum's block proposal mechanism
- [[web3-transaction]] — transactions are batched into blocks
- [[merkle-tree]] — block header contains Merkle roots
- [[hash-function]] — parent hash links blocks
- [[gas]] — each block has a gas limit

## Sources

- [[sources/web3-chapters]] — Chapter: Network
