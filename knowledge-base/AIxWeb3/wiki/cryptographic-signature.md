---
title: "Cryptographic Signature"
type: concept
tags: [web3-foundations, cryptography, wallet]
source_count: 2
date_updated: "2026-05-25"
---

# Cryptographic Signature

## Definition

A cryptographic signature is a mathematical proof that a specific private key authorized a specific message or transaction, without revealing the key itself. In Web3, every transaction is signed before broadcast. Signing is distinct from logging in — it authorizes a specific on-chain action.

## Key Points

- **Authorization, not authentication**: a signature says "I authorize this specific action," not just "I am who I say I am"
- **Three wallet action types**:
  1. **Connect** — read address only; no signing, no state change
  2. **Sign** — authorize a message; no on-chain state change, but may have off-chain effects (permit, typed data)
  3. **Send** — broadcast a signed transaction; causes on-chain state change and costs gas
- **EIP-712 typed data signing**: structured signing for readable, phishing-resistant approval prompts
- **Not the same as a transfer**: signing an approval (ERC-20 `permit`) is not the same as sending tokens — but abused approvals can be exploited
- **AI agents must get human confirmation**: any agent action involving a signature must pause for user approval

## Related Concepts

- [[private-key]] — the secret used to produce the signature
- [[public-key]] — used by verifiers to confirm the signature
- [[web3-transaction]] — every transaction is a signed message
- [[eoa]] — the account type that signs with private keys
- [[smart-account]] — can validate signatures with custom logic
- [[gas]] — send-type signatures trigger gas costs
- [[web3-security]] — signature phishing is a major attack vector
- [[agent-wallet]] — AI agents need human-confirmed signatures

## Sources

- [[sources/web3-chapters]] — Chapter: Cryptography, Wallet
- [[sources/web3-fundamentals-introduction]] — Module B: signature ≠ login
