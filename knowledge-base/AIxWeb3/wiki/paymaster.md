---
title: "Paymaster"
type: concept
tags: [web3-foundations, account-abstraction]
source_count: 1
date_updated: "2026-05-25"
---

# Paymaster

## Definition

A Paymaster is a smart contract in the ERC-4337 account abstraction system that sponsors gas fees on behalf of users or AI agents. It allows smart accounts to send transactions without holding ETH for gas — the paymaster covers the cost, optionally charging the user in ERC-20 tokens, loyalty points, or nothing at all.

## Key Points

- **Gas sponsorship**: the paymaster deposits ETH into the EntryPoint; this deposit covers gas for sponsored UserOperations
- **ERC-20 gas payments**: paymasters can accept ERC-20 token payment from users and convert it to ETH internally
- **Subsidy model**: dApps can subsidize gas for users as a UX improvement
- **Allowlist / rate limits**: paymasters can restrict which accounts or contracts they sponsor
- **Paymaster-as-a-service**: Pimlico, Biconomy, Alchemy provide paymaster APIs — no need to deploy your own
- **AI agent use**: a protocol can provide a paymaster so agents operate without maintaining ETH balances; agents request permission-scoped actions and gas is covered automatically
- **Staking requirement**: paymasters must stake ETH in the EntryPoint to prevent abuse

## Related Concepts

- [[erc-4337]] — the standard that defines the paymaster
- [[bundler]] — bundler submits; paymaster reimburses
- [[smart-account]] — the account whose gas is sponsored
- [[gas]] — what the paymaster covers
- [[machine-payment]] — paymaster is one mechanism enabling agent micro-payments
- [[erc20-token]] — paymaster can accept ERC-20 gas payment

## Sources

- [[sources/web3-chapters]] — Chapter: Account Abstraction
