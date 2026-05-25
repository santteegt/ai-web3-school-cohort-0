---
title: "Private Key"
type: concept
tags: [web3-foundations, cryptography, security]
source_count: 2
date_updated: "2026-05-25"
---

# Private Key

## Definition

A private key is a 256-bit random number that serves as the root secret for a blockchain account. Whoever holds the private key controls the account — can sign transactions, authorize approvals, and transfer funds. It must never be exposed, logged, or passed to any software including AI agents.

## Key Points

- **Root of all authority**: every on-chain action from an account requires a signature from the private key
- **Not recoverable if lost**: no central authority can restore a lost private key
- **Derived from mnemonic**: BIP-32/44 HD wallets derive private keys deterministically from a seed phrase
- **Not the same as address**: the address is public and safe to share; the private key is secret
- **Not the same as seed phrase**: one seed phrase generates many private keys (one per account path)
- **AI agents must not touch it**: session keys and smart accounts provide bounded alternatives (see [[session-key]], [[erc-4337]])

## Related Concepts

- [[mnemonic]] — the seed phrase from which this key is derived
- [[public-key]] — the safe-to-share counterpart
- [[cryptographic-signature]] — the output of applying this key to a message
- [[eoa]] — the account type where private key = full control
- [[session-key]] — limited-scope alternative for AI agent use
- [[smart-account]] — contract wallet that removes need for raw private key exposure
- [[web3-security]] — why protecting this key is the security perimeter
- [[agent-wallet]] — AI × Web3 security principle: agents should not hold private keys

## Sources

- [[sources/web3-chapters]] — Chapter: Cryptography, Wallet
- [[sources/web3-fundamentals-introduction]] — Module B: security boundaries
