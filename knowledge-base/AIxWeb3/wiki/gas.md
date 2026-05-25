---
title: "Gas"
type: concept
tags: [web3-foundations, network, wallet]
source_count: 2
date_updated: "2026-05-25"
---

# Gas

## Definition

Gas is the unit measuring the computational work required to execute an operation on the EVM. Every transaction specifies a gas limit and pays a fee in ETH (denominated in gwei). Gas prevents spam, allocates scarce block space, and compensates validators. On L2 networks, gas costs are dramatically lower due to batching and cheaper DA (data availability).

## Key Points

- **EIP-1559 model**: total fee = `baseFee` (burned by protocol) + `priorityFee` (tip to validator); `maxFeePerGas` caps what you're willing to pay
- **Gas limit**: the maximum gas the sender allows the transaction to consume; set too low → reverts (but fee still partly consumed)
- **Gas price ≠ total cost**: `cost = gasUsed × effectiveGasPrice`; complex contract calls use more gas than simple ETH transfers
- **Out-of-gas reverts**: state changes are rolled back, but gas spent is not refunded
- **L1 vs L2 costs**: L1 Ethereum (~$1–50 per tx in peaks); L2 rollups (cents to fractions of a cent)
- **Paymaster**: via ERC-4337, a paymaster contract can sponsor gas on behalf of a user or AI agent

## Related Concepts

- [[web3-transaction]] — transactions pay gas
- [[evm]] — the runtime that consumes gas per operation
- [[layer-2]] — dramatically reduces gas costs
- [[rollup]] — L2 mechanism that amortizes L1 gas across many transactions
- [[paymaster]] — contract that can pay gas on others' behalf
- [[erc-4337]] — enables gasless UX via paymasters
- [[defi]] — gas costs critically affect DeFi profitability

## Sources

- [[sources/web3-chapters]] — Chapter: Wallet, Network
- [[sources/web3-fundamentals-introduction]] — Module B: gas and execution costs
