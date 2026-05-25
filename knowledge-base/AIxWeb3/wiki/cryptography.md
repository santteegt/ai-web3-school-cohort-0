---
title: "Cryptography"
type: concept
tags: [web3-foundations, cryptography, security]
source_count: 2
date_updated: "2026-05-25"
---

# Cryptography

## Definition

Cryptography is the mathematical foundation of all Web3 security. It provides the primitives — hashing, asymmetric key pairs, and digital signatures — that enable trustless ownership, tamper-proof data, and verifiable authorization without a central authority.

## Key Points

- **Hash functions**: deterministic, one-way transforms (SHA256, Keccak256) that fingerprint data; used in block linking, commitments, and Merkle trees
- **Asymmetric keys**: a mathematically linked key pair — private key kept secret, public key (and derived address) shared openly
- **Digital signatures**: prove private key ownership without revealing it; every transaction and signed message uses this
- **Merkle trees**: hierarchical hash structures enabling compact membership proofs; used in blocks and state proofs
- **No cryptography = no Web3**: removing any of these primitives collapses the trust model

## Related Concepts

- [[hash-function]] — the specific one-way primitive
- [[public-key]] — shareable output of the key pair
- [[private-key]] — the secret root of all on-chain authority
- [[cryptographic-signature]] — the runtime application of asymmetric keys
- [[merkle-tree]] — hash-based membership proofs
- [[eoa]] — accounts derived from cryptographic key pairs
- [[web3-security]] — the broader defensive context

## Sources

- [[sources/web3-chapters]] — Chapter: Cryptography
- [[sources/web3-fundamentals-introduction]] — Module B overview
