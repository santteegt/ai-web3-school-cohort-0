---
title: "Web3 Transaction"
type: concept
tags: [web3-foundations, wallet, network]
source_count: 2
date_updated: "2026-05-25"
---

# Web3 Transaction

## Definition

A Web3 transaction is a signed data package that instructs the network to change on-chain state. It is created by a sender, signed with a private key, broadcast to nodes, picked up by a validator, executed by the EVM, and finalized in a block. Every state-changing action — ETH transfers, contract calls, contract deployments — is a transaction.

## Key Points

- **Fields**: `nonce` (ordering), `to` (recipient/contract address or empty for deploy), `value` (ETH amount), `data` (calldata for contract functions), `gasLimit`, `maxFeePerGas`, `maxPriorityFeePerGas`, `v/r/s` (signature)
- **"How a Call Happens" 8-step flow**: user signs tx → broadcasts to mempool → validator picks up → EVM executes bytecode → state updates → event emitted → receipt returned → finalized in block
- **Transactions can fail**: if gas limit is too low or contract reverts — state is not changed but gas is still consumed
- **Not reversible**: once finalized, a transaction cannot be undone (only overridden by a new tx)
- **EIP-1559 gas model**: base fee (burned) + priority fee (validator tip); more predictable pricing
- **Distinct from signing a message**: signing a message does not broadcast a transaction and costs no gas

## Related Concepts

- [[cryptographic-signature]] — every transaction must be signed
- [[gas]] — execution cost paid per transaction
- [[eoa]] — the account that signs and sends
- [[evm]] — executes the transaction's calldata
- [[block]] — where finalized transactions are stored
- [[smart-contract]] — the target of most non-ETH-transfer transactions
- [[contract-event]] — emitted by contracts during transaction execution
- [[block-explorer]] — where you inspect transaction status and receipts

## Sources

- [[sources/web3-chapters]] — Chapter: Wallet, Smart Contract
- [[sources/web3-fundamentals-introduction]] — Module B: transactions and gas
