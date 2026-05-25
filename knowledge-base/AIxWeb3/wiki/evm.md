---
title: "EVM (Ethereum Virtual Machine)"
type: concept
tags: [web3-foundations, smart-contracts, network]
source_count: 2
date_updated: "2026-05-25"
---

# EVM (Ethereum Virtual Machine)

## Definition

The Ethereum Virtual Machine (EVM) is the sandboxed runtime environment that executes smart contract bytecode across all Ethereum nodes. It is deterministic — identical input always produces identical output — enabling trustless distributed computation. EVM compatibility has become the de facto standard: most L2s and many L1s run the same EVM bytecode.

## Key Points

- **Stack-based**: 256-bit word size; operations manipulate a stack, memory, and persistent storage
- **Deterministic**: every node that executes a transaction produces the same state transition
- **Isolated sandbox**: contracts cannot access the internet or system resources; only on-chain state
- **Gas accounting**: each opcode costs a specific amount of gas; execution halts if gas is exhausted
- **EVM-compatible chains**: Polygon, Arbitrum, Optimism, BSC, Avalanche C-Chain all run EVM — deploy once, run on many
- **Precompiles**: built-in contracts for expensive operations (elliptic curve math, hashing) at reduced gas cost
- **Storage layout**: each contract has its own 2^256-slot key-value store; layout must be understood for upgrades

## Related Concepts

- [[smart-contract]] — the code the EVM executes
- [[solidity]] — compiled to EVM bytecode
- [[gas]] — the EVM accounting unit for computation
- [[web3-transaction]] — the input that triggers EVM execution
- [[layer-2]] — many L2s are EVM-compatible
- [[rollup]] — executes transactions off-chain in an EVM and posts results to L1
- [[erc-4337]] — UserOperations are validated and executed inside the EVM

## Sources

- [[sources/web3-chapters]] — Chapter: Smart Contract, Network
- [[sources/web3-fundamentals-introduction]] — Module B: on-chain execution
