---
title: "Externally Owned Account (EOA)"
type: concept
tags: [web3-foundations, wallet, accounts]
source_count: 2
date_updated: "2026-05-25"
---

# Externally Owned Account (EOA)

## Definition

An Externally Owned Account (EOA) is a blockchain account controlled entirely by a private key. It has no on-chain code — it can send transactions and hold assets, but cannot execute arbitrary logic. The term "externally owned" contrasts with contract accounts, which are controlled by their deployed code.

## Key Points

- **Private key = full control**: anyone with the private key can do anything the account can do
- **Address derived from key pair**: the public key is hashed to get the 20-byte address
- **No code**: EOAs cannot have conditional logic, multi-approval requirements, or recovery mechanisms built in
- **Transaction initiator**: all on-chain transactions must originate from an EOA (or a bundler acting on behalf of a UserOperation in ERC-4337)
- **Contrast with smart accounts**: ERC-4337 smart accounts are contract accounts that add programmable authorization on top
- **Wallet apps manage EOAs**: MetaMask, Rainbow, etc. are interfaces to your EOA's private key / seed phrase

## Related Concepts

- [[private-key]] — the controller of an EOA
- [[mnemonic]] — the seed phrase that generates EOA keys
- [[cryptographic-signature]] — how EOAs authorize actions
- [[smart-account]] — the programmable alternative to EOAs
- [[erc-4337]] — enables smart accounts without removing EOAs from the stack
- [[web3-transaction]] — EOAs initiate all transactions
- [[agent-wallet]] — AI agents should not use bare EOAs; prefer smart accounts

## Sources

- [[sources/web3-chapters]] — Chapter: Wallet
- [[sources/web3-fundamentals-introduction]] — Module B: accounts and wallets
