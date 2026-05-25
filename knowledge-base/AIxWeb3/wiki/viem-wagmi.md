---
title: "viem / wagmi"
type: concept
tags: [web3-foundations, dev-tooling, frontend]
source_count: 2
date_updated: "2026-05-25"
---

# viem / wagmi

## Definition

viem is a TypeScript library for low-level Ethereum interactions — reading chain state, encoding/decoding ABI data, sending transactions, and signing messages. wagmi is a React hooks library built on top of viem that provides connectors, wallet management, and query caching for dApp frontends. Together they are the modern replacement for ethers.js / web3.js.

## Key Points

- **viem**: lightweight, tree-shakeable, fully typed; `createPublicClient` (reads), `createWalletClient` (writes/signing)
- **wagmi**: React hooks — `useAccount`, `useBalance`, `useReadContract`, `useWriteContract`, `useWatchContractEvent`
- **Type-safe ABI**: pass ABI as TypeScript `const` to get full type inference on function names and parameter types
- **Multi-chain**: configure any EVM chain with `defineChain`; built-in support for mainnet, Sepolia, Arbitrum, etc.
- **Wallet connectors**: MetaMask, WalletConnect, Coinbase Wallet, Safe — managed by wagmi
- **Script use**: viem works outside React (scripts, agents) for programmatic on-chain interaction
- **Supersedes ethers.js**: better TypeScript ergonomics, smaller bundle, more modular

## Related Concepts

- [[abi]] — viem uses ABI for encoding/decoding
- [[smart-contract]] — viem/wagmi are the primary way frontends call contracts
- [[web3-dev-stack]] — the frontend integration layer
- [[web3-tool-use]] — AI agents can use viem-style calls as tools
- [[eoa]] — wallet clients sign with EOA keys
- [[erc20-token]] — commonly read/written via wagmi hooks

## Sources

- [[sources/web3-chapters]] — Chapter: Dev Stack
- [[sources/web3-fundamentals-introduction]] — Module B: recommended tools
