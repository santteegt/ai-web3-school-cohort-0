---
title: "Foundry"
type: concept
tags: [web3-foundations, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# Foundry

## Definition

Foundry is a Rust-based smart contract development framework for Ethereum. It is dramatically faster than Node.js-based alternatives because it compiles and runs tests natively in Rust. Tests are written in Solidity itself (no JavaScript required). The toolchain includes Forge (testing), Cast (CLI chain interaction), Anvil (local node), and Chisel (REPL).

## Key Points

- **Forge**: test runner; Solidity tests run in milliseconds vs. seconds in Hardhat; fuzzing support built-in
- **Cast**: CLI tool for interacting with deployed contracts — call functions, send transactions, query state
- **Anvil**: fast local EVM node; fork any chain at any block; instant block mining
- **Chisel**: interactive Solidity REPL for quick experimentation
- **Fuzz testing**: generate thousands of random inputs automatically to find edge cases
- **No JavaScript required**: write tests in pure Solidity; closer to the contract mental model
- **Gas snapshots**: track gas costs per test function; detect regressions
- **Preferred by security researchers**: fast fuzzing and native Solidity tests suit audit workflows

## Related Concepts

- [[web3-dev-stack]] — the framework layer
- [[solidity]] — both the source and the test language in Foundry
- [[hardhat]] — Node.js alternative; choose based on team preference
- [[openzeppelin]] — compatible; import via `forge install`
- [[testnet]] — deploy via `forge create` or Foundry scripts

## Sources

- [[sources/web3-chapters]] — Chapter: Dev Stack
