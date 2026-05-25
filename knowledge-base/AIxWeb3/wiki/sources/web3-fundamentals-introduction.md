---
title: "Web3 Fundamentals - Introduction"
type: source
tags: [web3-foundations, wallets, accounts, signatures, smart-contracts, account-abstraction]
source_file: "raw/Web3 Fundamentals - Introduction.md"
source_hash: "sha256:6588efb9157c56f8fae82d1640d1056dc4127dd2c2f14921feca664a6cb1f30b"
date_ingested: "2026-05-25"
---

# Web3 Fundamentals - Introduction

## Summary

Module B of the AI × Web3 School program covers the foundational concepts for operating within Web3: accounts, wallets, private keys, signatures, gas, smart contracts, and layer 2 networks. The module emphasizes the security responsibilities that come with self-custody and explains how on-chain execution differs from traditional backend logic. It also covers account abstraction (ERC-4337, smart accounts, multisig, Safe) as key infrastructure for AI × Web3 builders who need delegated permissions and human confirmation gates.

## Key Concepts

- [[eoa]] — Externally Owned Accounts, addresses derived from private keys
- [[mnemonic]] — Seed phrases: the master secret behind a wallet; must never be exposed
- [[private-key]] — The actual signing key; distinct from address (public), distinct from seed phrase
- [[cryptographic-signature]] — Authorizes a specific action on-chain; not equivalent to a login click
- [[web3-transaction]] — Signed instructions submitted to the network; requires gas
- [[gas]] — Execution cost on-chain; transactions can fail and require confirmation time
- [[layer-2]] — L2 networks reduce execution costs vs L1
- [[smart-contract]] — Public, immutable (usually) backend logic; state and execution are public
- [[testnet]] — Safe environment for learning and experiments before using mainnet
- [[block-explorer]] — Tool for understanding on-chain behavior (transaction receipts, state)
- [[erc-4337]] — Account abstraction standard enabling smart accounts, bundlers, paymasters
- [[smart-account]] — Contract-based account with programmable authorization logic
- [[session-key]] — Limited-scope key for AI agents; enables permission-bounded on-chain actions
- [[agent-wallet]] — AI × Web3 bridge: recovery, authorization, and security boundaries for AI agents

## Notable Points

- "A wallet is not an ordinary account; it is the entry point to private keys, security responsibility, and on-chain actions."
- "AI agents should not directly touch private keys / seed phrases, and actions involving signatures, approvals, transfers, or contract writes must keep human confirmation."
- "An address is not the same as anonymity, a signature is not the same as ordinary login, and authorization is not the same as transfer."
- Recommended tools: MetaMask, Remix IDE, Sepolia Faucet, Hardhat/Foundry, OpenZeppelin, Safe, viem/wagmi

## Sources Referenced

- Source: https://web3career.build/en/programs/AI-Web3-School?tab=learning
