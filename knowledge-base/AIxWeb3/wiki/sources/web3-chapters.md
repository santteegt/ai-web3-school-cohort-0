---
title: "Web3 Chapters"
type: source
tags: [web3-foundations, cryptography, wallet, smart-contracts, defi, oracle, security, account-abstraction, indexing, network]
source_file: "raw/Web3 Chapters.md"
source_hash: "sha256:5b653865d1c02350233e3f5e5ba4441d6f60fac9beb25f8d1e5eb281e42a29e7"
date_ingested: "2026-05-25"
---

# Web3 Chapters

## Summary

A comprehensive aggregation of 10 handbook chapters from the AI × Web3 School covering the full Web3 technology stack. The source spans cryptographic primitives, wallet mechanics, smart contract development, blockchain networks, account abstraction, DeFi protocols, oracles, on-chain indexing, dev tooling, and security. Together these chapters form the foundational Web3 knowledge layer that bridges into AI × Web3 applications.

## Key Concepts

### Cryptography
- [[cryptography]] — Foundation of all Web3 security: hashing, asymmetric keys, signatures
- [[hash-function]] — Deterministic, one-way: SHA256 / Keccak256; used in block linking and commitments
- [[public-key]] — Derived from private key; used to generate wallet address
- [[private-key]] — The root secret; whoever holds it controls the account
- [[cryptographic-signature]] — Proves key ownership without revealing the key; signs transactions and messages
- [[merkle-tree]] — Tree of hashes enabling efficient membership proofs (used in blocks, Merkle proofs)

### Wallet
- [[eoa]] — Externally Owned Account; key-pair controlled account with no on-chain code
- [[mnemonic]] — BIP-39 seed phrase; deterministically generates all private keys in an HD wallet
- [[web3-transaction]] — Signed data package: nonce, to, value, data, gas fields; submitted to network
- [[gas]] — Unit of computation cost; paid in ETH (gwei); prevents spam; can fail if limit too low
- [[block-explorer]] — Read-only interface to on-chain state: transactions, contracts, events

### Smart Contract
- [[smart-contract]] — Self-executing code deployed on-chain; state is public, execution is deterministic
- [[solidity]] — Primary EVM smart contract language; compiled to bytecode
- [[evm]] — Ethereum Virtual Machine; sandboxed runtime executing bytecode across all EVM-compatible chains
- [[abi]] — Application Binary Interface; defines how to encode/decode contract calls and events
- [[contract-event]] — Emitted log entries stored in transaction receipts; key data source for indexers
- [[contract-upgrade]] — Proxy patterns (transparent, UUPS) enabling contract logic replacement

### Dev Stack
- [[web3-dev-stack]] — Full toolchain: Remix → Hardhat/Foundry → OpenZeppelin → viem/wagmi
- [[remix-ide]] — Browser-based Solidity IDE; fastest path to deploy and interact with contracts
- [[hardhat]] — Node.js dev environment for compiling, testing, and deploying contracts
- [[foundry]] — Rust-based dev framework; faster tests with Forge, scripting with Cast
- [[openzeppelin]] — Audited contract library: ERC-20, ERC-721, access control, upgradeable proxies
- [[viem-wagmi]] — TypeScript libraries for on-chain reads/writes from frontends and scripts

### Network
- [[blockchain-network]] — Distributed ledger: nodes agree on canonical chain state via consensus
- [[block]] — Batch of transactions; linked by parent hash forming the chain
- [[consensus]] — Agreement mechanism (PoS, PoW) determining canonical chain
- [[proof-of-stake]] — Ethereum's consensus: validators stake ETH, propose/attest blocks
- [[testnet]] — Test network with valueless tokens; safe for development (Sepolia, Holesky)
- [[layer-2]] — Scaling solution: executes transactions off-chain, posts proofs/data to L1
- [[rollup]] — L2 type: batches transactions, submits compressed data + validity proof to L1

### Account Abstraction
- [[erc-4337]] — Standard for smart accounts via UserOperation mempool; no protocol change required
- [[smart-account]] — Contract wallet with programmable logic: social recovery, multisig, session keys
- [[bundler]] — Service that collects UserOperations and submits them on-chain
- [[paymaster]] — Contract that sponsors gas fees on behalf of users or AI agents
- [[session-key]] — Limited-scope, time-bounded key for AI agents; no full private-key exposure

### DeFi
- [[defi]] — Decentralized Finance: permissionless financial protocols on-chain
- [[erc20-token]] — Standard fungible token interface: transfer, approve, allowance
- [[amm]] — Automated Market Maker: liquidity pool-based trading; introduces slippage, MEV, IL
- [[defi-lending]] — Over-collateralized borrowing/lending (Aave, Compound); liquidation risk
- [[stablecoin]] — Price-pegged asset: collateralized (DAI), algorithmic (FRAX), fiat-backed (USDC)
- [[liquidity]] — Capital in pools enabling trades; LPs earn fees, bear impermanent loss

### Oracle
- [[oracle]] — Bridge between off-chain data and on-chain contracts
- [[price-feed]] — Real-time asset price data published on-chain (Chainlink, Pyth)
- [[oracle-risk]] — Manipulation, latency, and centralization risks in price feeds
- [[ai-oracle]] — Emerging pattern: oracles that publish AI model outputs verifiably on-chain

### Indexing
- [[on-chain-indexing]] — Processing blockchain events into queryable databases
- [[subgraph]] — The Graph protocol: GraphQL API over indexed on-chain events
- [[rpc]] — Remote Procedure Call: JSON-RPC interface to query blockchain nodes (Infura, Alchemy)
- [[data-pipeline]] — ETL pipeline from raw chain events to structured analytics

### Security
- [[web3-security]] — Defensive practices for smart contracts and on-chain systems
- [[reentrancy]] — Attack: recursive call drains funds before state update (prevented by checks-effects-interactions)
- [[access-control]] — Role-based permissions on contract functions; critical for admin functions
- [[contract-audit]] — Expert review of contract code before mainnet deployment
- [[tx-simulation]] — Pre-execution simulation to detect reverts and unexpected behavior
- [[on-chain-monitoring]] — Real-time alerting on suspicious transactions and state changes

## Notable Points

- "How a Call Happens" 8-step flow: user signs tx → broadcast → mempool → validator picks up → EVM executes bytecode → state change → event emitted → receipt returned
- Three wallet action types: **connect** (read address, no signing), **sign** (authorize message, no state change), **send** (broadcast transaction, state change + gas cost)
- Account Abstraction enables AI agents to operate with session keys bounded to specific contracts, amounts, and time windows — removing full private key exposure
- MEV (Maximal Extractable Value) affects DeFi transactions through front-running and sandwich attacks
- Oracle risk is especially critical for AI Oracles: if the model output published on-chain can be manipulated, downstream contracts are vulnerable

## Sources Referenced

- Source: https://aiweb3.school/en/handbook/web3/
