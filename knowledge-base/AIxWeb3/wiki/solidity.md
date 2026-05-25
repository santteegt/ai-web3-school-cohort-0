---
title: "Solidity"
type: concept
tags: [web3-foundations, smart-contracts, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# Solidity

## Definition

Solidity is the primary high-level programming language for writing Ethereum smart contracts. It is statically typed, compiled to EVM bytecode, and designed around a contract model. Solidity source code is compiled by `solc` (the Solidity compiler) into bytecode (what gets deployed) and an ABI (what gets used to call the contract).

## Key Points

- **Contract model**: code organized as `contract` declarations with state variables, functions, events, and modifiers
- **Types**: `uint`, `address`, `bytes`, `mapping`, `struct`, `array`; `address payable` for ETH-receiving addresses
- **Visibility**: `public`, `private`, `internal`, `external` — controls who can call a function
- **Modifiers**: reusable access control patterns (e.g., `onlyOwner`)
- **Events**: emitted logs stored in transaction receipts; how frontends and indexers observe state changes
- **Security patterns**: checks-effects-interactions (prevent reentrancy), pull-over-push payments
- **Compiler version pinning**: `pragma solidity ^0.8.0;` — breaking changes between versions require explicit upgrades
- **OpenZeppelin**: library of audited, reusable Solidity contracts (ERC-20, ERC-721, AccessControl)

## Related Concepts

- [[evm]] — the target runtime for compiled Solidity
- [[abi]] — produced alongside bytecode by the compiler
- [[smart-contract]] — the deployment artifact of a Solidity program
- [[openzeppelin]] — the standard library for Solidity development
- [[hardhat]] — development environment for compiling/testing Solidity
- [[foundry]] — alternative fast Rust-based dev environment
- [[remix-ide]] — browser-based Solidity IDE for quick prototyping
- [[web3-security]] — many vulnerabilities originate in Solidity patterns

## Sources

- [[sources/web3-chapters]] — Chapter: Smart Contract, Dev Stack
