---
title: "Hardhat"
type: concept
tags: [web3-foundations, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# Hardhat

## Definition

Hardhat is a Node.js-based development environment for Ethereum smart contracts. It provides a task runner, a local EVM node (Hardhat Network), Solidity compilation, testing with Chai/Mocha, and deployment scripting. It is the most widely used production-grade smart contract dev framework in the JavaScript/TypeScript ecosystem.

## Key Points

- **Hardhat Network**: local EVM with instant mining, `console.log` in Solidity, stack traces on reverts
- **Tasks**: `npx hardhat compile`, `npx hardhat test`, `npx hardhat run scripts/deploy.ts`
- **TypeScript native**: first-class TypeScript support with `hardhat-toolbox`
- **Plugin ecosystem**: `hardhat-ethers`, `hardhat-viem`, `hardhat-ignition` (deployment), `hardhat-verify`
- **Hardhat Ignition**: declarative deployment module system replacing raw scripts
- **Forking**: fork mainnet or any chain at a specific block for realistic integration tests
- **Contract verification**: `hardhat-verify` submits source to Etherscan automatically after deployment
- **OpenZeppelin integration**: OpenZeppelin Upgrades plugin integrates directly with Hardhat

## Related Concepts

- [[web3-dev-stack]] — the framework layer
- [[solidity]] — compiled and tested via Hardhat
- [[foundry]] — Rust-based alternative (faster tests)
- [[openzeppelin]] — commonly used alongside Hardhat
- [[testnet]] — deployment target after local testing
- [[viem-wagmi]] — alternative to ethers.js for on-chain interaction

## Sources

- [[sources/web3-chapters]] — Chapter: Dev Stack
