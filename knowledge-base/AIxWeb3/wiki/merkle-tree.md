---
title: "Merkle Tree"
type: concept
tags: [web3-foundations, cryptography, data-structures]
source_count: 1
date_updated: "2026-05-25"
---

# Merkle Tree

## Definition

A Merkle tree is a binary tree of cryptographic hashes where each leaf node is the hash of a data item and each internal node is the hash of its two children. The root (Merkle root) compactly represents the entire dataset. A Merkle proof allows verifying that a single item belongs to the set by providing only the sibling hashes along the path to the root — O(log n) data instead of the full dataset.

## Key Points

- **Efficient membership proofs**: verify that a transaction is in a block without downloading all transactions
- **Tamper detection**: changing any leaf changes all ancestor hashes up to the root
- **Used in block headers**: Ethereum stores the Merkle root of all transactions and the state trie in each block header
- **Merkle proof**: a list of sibling hashes sufficient to recompute the root — used in rollup proofs and airdrops
- **Patricia Merkle Trie**: Ethereum's state is stored in a modified Merkle Patricia Trie, enabling efficient state proofs

## Related Concepts

- [[hash-function]] — the underlying primitive
- [[block]] — block header contains Merkle roots
- [[rollup]] — uses Merkle/ZK proofs to commit state to L1
- [[cryptography]] — broader context
- [[on-chain-indexing]] — indexes may verify Merkle proofs

## Sources

- [[sources/web3-chapters]] — Chapter: Cryptography
