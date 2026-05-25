---
title: "Public Key"
type: concept
tags: [web3-foundations, cryptography]
source_count: 1
date_updated: "2026-05-25"
---

# Public Key

## Definition

A public key is the shareable output of an asymmetric cryptographic key pair. In Ethereum, public keys are derived from private keys using elliptic curve multiplication (secp256k1). Your wallet address is the last 20 bytes of the Keccak256 hash of your public key. Public keys can be shared freely — they reveal nothing about the private key.

## Key Points

- **Derived from private key**: private key → elliptic curve multiply → public key (one-way)
- **Address derivation**: Ethereum address = `0x` + last 20 bytes of Keccak256(public key)
- **Used for signature verification**: others use your public key to verify that a message was signed by your private key
- **Safe to share**: exposing a public key or address does not compromise security
- **Not pseudonymous**: an address can be linked to real identity through on-chain behavior analysis

## Related Concepts

- [[private-key]] — the secret that generates this key
- [[hash-function]] — used to derive address from public key
- [[cryptographic-signature]] — verification uses public key
- [[eoa]] — the account whose address comes from this key pair
- [[cryptography]] — broader context

## Sources

- [[sources/web3-chapters]] — Chapter: Cryptography
