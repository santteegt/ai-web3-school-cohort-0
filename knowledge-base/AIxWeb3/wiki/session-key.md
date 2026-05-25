---
title: "Session Key"
type: concept
tags: [web3-foundations, account-abstraction, security, aixweb3-bridge]
source_count: 2
date_updated: "2026-05-25"
---

# Session Key

## Definition

A session key is a limited-scope cryptographic key granted to an AI agent, dApp, or service to act on behalf of a smart account, within precisely defined boundaries. Unlike a full private key, a session key can only perform specific actions (e.g., swap on one DEX, spend up to $100 USDC, valid for 24 hours) — and the smart account's validation logic enforces these limits on-chain.

## Key Points

- **Scope constraints**: limited to specific contract addresses, function selectors, max value per transaction, or total spend cap
- **Time bounds**: session key expires after a set period; no manual revocation needed
- **No root key exposure**: the agent never sees the account's main private key; it only signs UserOperations within its permitted scope
- **On-chain enforcement**: the smart account's `validateUserOp` checks session key permissions against the policy stored in contract state
- **Revocation**: owner can revoke a session key at any time by updating the smart account's policy
- **Use case — AI agent**: agent is granted a session key for specific DeFi rebalancing actions; human remains in control via the root account
- **Use case — dApp**: instead of approving a full ERC-20 allowance, a session key scopes what the dApp can do

## Related Concepts

- [[erc-4337]] — the infrastructure enabling session keys
- [[smart-account]] — the account that grants and enforces session key policies
- [[private-key]] — what session keys replace for agent use cases
- [[agent-wallet]] — AI × Web3: session keys are the recommended agent authorization mechanism
- [[web3-security]] — session keys dramatically reduce blast radius of a compromised agent
- [[bundler]] — bundles the session-key-signed UserOperations

## Sources

- [[sources/web3-chapters]] — Chapter: Account Abstraction
- [[sources/web3-fundamentals-introduction]] — Module B: session keys, permission limits
