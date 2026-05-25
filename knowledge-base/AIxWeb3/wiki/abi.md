---
title: "ABI (Application Binary Interface)"
type: concept
tags: [web3-foundations, smart-contracts, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# ABI (Application Binary Interface)

## Definition

The ABI (Application Binary Interface) is a JSON specification describing a smart contract's public interface: its functions, their parameter types, return types, and emitted events. The ABI is the "contract" between a deployed smart contract and the code that calls it — without it, calldata cannot be encoded or decoded.

## Key Points

- **Produced at compile time**: the Solidity compiler outputs both `bytecode` (deployed) and `abi` (used by callers)
- **Encodes function calls**: the first 4 bytes of calldata = Keccak256(function signature)[0:4] (the "function selector")
- **Decodes return values and events**: libraries like viem, ethers.js, and web3.py use the ABI to parse raw hex responses
- **ABI encoding**: parameters are ABI-encoded per the spec; different types encode differently (uint256, address, bytes, tuples)
- **Required for interaction**: to call a contract function you need both its address and its ABI
- **Block explorers use ABI**: Etherscan shows human-readable function names after contract verification
- **Minimal ABI**: you don't need the full ABI — only the functions you plan to call

## Related Concepts

- [[solidity]] — the source that produces the ABI
- [[smart-contract]] — the deployed artifact the ABI describes
- [[evm]] — the bytecode is what the EVM runs; ABI is for external callers
- [[viem-wagmi]] — use ABI to call contracts from frontends/scripts
- [[block-explorer]] — uses verified ABI for readable display
- [[contract-event]] — events are also defined in the ABI
- [[web3-tool-use]] — AI agents use ABIs to call contracts via tools

## Sources

- [[sources/web3-chapters]] — Chapter: Smart Contract
