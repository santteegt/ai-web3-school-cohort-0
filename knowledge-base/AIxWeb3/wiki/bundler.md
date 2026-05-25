---
title: "Bundler"
type: concept
tags: [web3-foundations, account-abstraction]
source_count: 1
date_updated: "2026-05-25"
---

# Bundler

## Definition

In the ERC-4337 account abstraction system, a bundler is an off-chain service that collects UserOperations from the alternative mempool, validates them, and submits them as a single on-chain transaction to the EntryPoint contract. Bundlers play the same role that miners/validators play for regular transactions, but for the ERC-4337 user operation flow.

## Key Points

- **Alt mempool**: UserOperations are submitted to a separate peer-to-peer mempool, not the standard transaction mempool
- **Simulation**: bundlers simulate UserOperations before inclusion to ensure they pass validation and do not revert
- **Gas fee**: bundlers pay L1 gas upfront and are reimbursed by the paymaster or the smart account
- **MEV risk**: bundlers can reorder UserOperations for profit, similar to transaction MEV
- **Bundler-as-a-service**: providers like Pimlico, Alchemy, Biconomy, StackUp offer hosted bundler APIs
- **Decentralization**: the bundler network is designed to be permissionless; any node can be a bundler

## Related Concepts

- [[erc-4337]] — the standard that defines the bundler role
- [[smart-account]] — the account type whose operations bundlers process
- [[paymaster]] — co-participant: pays gas that bundler spends
- [[web3-transaction]] — bundler submits the actual L1 transaction
- [[gas]] — bundler manages gas for UserOperations

## Sources

- [[sources/web3-chapters]] — Chapter: Account Abstraction
