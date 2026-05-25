---
title: "Mnemonic (Seed Phrase)"
type: concept
tags: [web3-foundations, wallet, security]
source_count: 2
date_updated: "2026-05-25"
---

# Mnemonic (Seed Phrase)

## Definition

A mnemonic (or seed phrase) is a human-readable sequence of 12 or 24 words (BIP-39 standard) that encodes the master entropy from which all private keys in an HD (Hierarchical Deterministic) wallet are derived. Whoever has the seed phrase has full access to every account the wallet ever generated.

## Key Points

- **BIP-39**: the standard word list and checksum format for encoding entropy as words
- **BIP-32/44 derivation paths**: the seed phrase generates a root key; private keys for specific accounts are derived at paths like `m/44'/60'/0'/0/0` (Ethereum account 0)
- **Generates multiple accounts**: one seed phrase → unlimited private keys; wallets show account 0, 1, 2, …
- **Must never be exposed**: storing in cloud notes, screenshots, or passing to AI tools is a total account compromise
- **Not the same as private key**: the seed phrase is the master; private keys are derived from it
- **Recovery tool**: losing the private key but keeping the seed phrase allows full wallet restoration
- **Social/email recovery vs. mnemonic**: smart accounts (ERC-4337) can replace mnemonic-based recovery with guardian-based or email recovery

## Related Concepts

- [[private-key]] — derived from the mnemonic at a specific path
- [[eoa]] — the account type protected by the mnemonic
- [[smart-account]] — can replace mnemonic dependency with programmable recovery
- [[web3-security]] — seed phrase exposure = total loss
- [[agent-wallet]] — AI agents must never receive seed phrases

## Sources

- [[sources/web3-chapters]] — Chapter: Wallet
- [[sources/web3-fundamentals-introduction]] — Module B: seed phrase security
