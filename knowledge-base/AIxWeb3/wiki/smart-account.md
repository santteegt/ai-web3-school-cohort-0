---
title: "Smart Account"
type: concept
tags: [web3-foundations, account-abstraction, security]
source_count: 2
date_updated: "2026-05-25"
---

# Smart Account

## Definition

A smart account (also called a contract wallet or account abstraction wallet) is a blockchain account implemented as a smart contract rather than a raw key pair. Unlike EOAs, smart accounts can have programmable authorization logic: multisig, social recovery, passkey authentication, session keys, and gas sponsorship — making them far more suitable for AI × Web3 agents than bare EOAs.

## Key Points

- **Programmable validation**: authorization logic defined in `validateUserOp`; can require multiple signers, limit actions to specific contracts, or verify session key permissions
- **Social/email recovery**: replace lost keys via trusted guardians or email verification; no seed phrase required
- **Multisig**: require M-of-N approvals before executing any transaction; Safe (formerly Gnosis Safe) is the leading multisig smart account
- **Session keys**: grant AI agents or dApps a limited-scope key — specific contracts, amount caps, time bounds — without exposing the root account key
- **Passkeys**: authorize via device biometrics (Face ID, Touch ID) instead of seed phrases
- **Gas abstraction**: paymasters can sponsor gas; accounts can pay gas in ERC-20 tokens
- **Safe**: the most widely deployed smart account; can be extended with modules for ERC-4337 compatibility
- **AI × Web3 significance**: smart accounts are the primary trust boundary for AI agents operating on-chain

## Related Concepts

- [[erc-4337]] — the standard enabling smart accounts
- [[eoa]] — the simpler alternative smart accounts improve upon
- [[session-key]] — limited-scope keys for agents
- [[bundler]] — submits UserOperations for smart accounts
- [[paymaster]] — gas sponsor for smart accounts
- [[agent-wallet]] — AI × Web3 bridge: smart accounts as agent accounts
- [[web3-security]] — smart account admin key must be tightly controlled
- [[multi-agent-systems]] — smart accounts can enforce inter-agent authorization

## Sources

- [[sources/web3-chapters]] — Chapter: Account Abstraction
- [[sources/web3-fundamentals-introduction]] — Module B: smart accounts, multisig, Safe
