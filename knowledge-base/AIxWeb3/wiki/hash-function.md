---
title: "Hash Function"
type: concept
tags: [web3-foundations, cryptography]
source_count: 1
date_updated: "2026-05-25"
---

# Hash Function

## Definition

A hash function is a deterministic, one-way mathematical transform that maps any input to a fixed-length output (the digest). In Web3, SHA256 is used in Bitcoin and Keccak256 in Ethereum. The same input always produces the same hash; even a one-bit input change produces a completely different hash (avalanche effect).

## Key Points

- **One-way**: given the hash, you cannot reverse-engineer the input (preimage resistance)
- **Collision-resistant**: it is computationally infeasible to find two different inputs that produce the same hash
- **Used in block linking**: each block stores the hash of the previous block, forming the chain
- **Used in commitments**: you can commit to a value by publishing its hash, then reveal it later
- **Keccak256**: the specific SHA-3 variant used in Ethereum; also used to derive addresses from public keys
- **Not encryption**: hashing is irreversible; encryption is reversible with a key

## Related Concepts

- [[cryptography]] — the broader primitive set
- [[merkle-tree]] — tree of hashes for efficient proofs
- [[block]] — each block's hash links it to the previous
- [[public-key]] — Ethereum address = Keccak256(public key)[last 20 bytes]
- [[smart-contract]] — contract addresses also derived by hashing

## Sources

- [[sources/web3-chapters]] — Chapter: Cryptography
