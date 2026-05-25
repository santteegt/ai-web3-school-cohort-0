---
title: "Smart Contract"
type: concept
tags: [web3-foundations, smart-contracts, evm]
source_count: 2
date_updated: "2026-05-25"
---

# Smart Contract

## Definition

A smart contract is a program deployed on a blockchain that executes deterministically when called. Its state and code are public; execution is replicated by every node. Unlike traditional backends, smart contracts have no concept of a "private" database — all storage is readable on-chain. Once deployed without an upgrade mechanism, the contract logic cannot be changed.

## Key Points

- **Deterministic execution**: all nodes run the same code and produce the same state transition
- **State is public**: every storage slot can be read by anyone; "private" variables are still on-chain
- **Execution is public**: every call and its result is in the transaction record
- **Immutability by default**: without proxy patterns, deployed bytecode cannot be altered
- **Upgrade patterns**: transparent proxy, UUPS, beacon — allow logic replacement while preserving state and address (see [[contract-upgrade]])
- **"How a Call Happens" 8-step flow**: sign tx → mempool → validator → EVM → state change → event → receipt → finalized
- **Different from backend**: no auth middleware, no private DB, no rate limiting — security must be in the contract logic itself
- **Testnets first**: always deploy to testnet before mainnet; mainnet mistakes can cost real funds

## Related Concepts

- [[evm]] — the runtime that executes contract bytecode
- [[solidity]] — primary language for writing contracts
- [[abi]] — interface definition for calling contracts
- [[contract-event]] — contracts emit events to signal state changes
- [[contract-upgrade]] — proxy patterns for mutable logic
- [[web3-security]] — contract vulnerabilities (reentrancy, access control)
- [[openzeppelin]] — reusable, audited contract components
- [[testnet]] — deploy here before mainnet
- [[web3-tool-use]] — AI agents interact with contracts via tool calls

## Sources

- [[sources/web3-chapters]] — Chapter: Smart Contract
- [[sources/web3-fundamentals-introduction]] — Module B: smart contracts vs backend
