---
title: "Web3 Dev Stack"
type: concept
tags: [web3-foundations, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# Web3 Dev Stack

## Definition

The Web3 dev stack is the toolchain for building, testing, and deploying smart contracts and dApp frontends. It ranges from browser-based IDEs for beginners to full-featured Rust-based frameworks for production engineering. The standard progression is: Remix (prototype) → Hardhat/Foundry (engineer) → OpenZeppelin (reuse) → viem/wagmi (frontend integration).

## Key Points

- **Contract development**: Remix IDE (browser), Hardhat (Node.js), Foundry (Rust) — see individual pages
- **Contract libraries**: OpenZeppelin — audited, reusable ERC-20, ERC-721, access control, upgradeable proxies
- **Frontend integration**: viem (low-level TypeScript), wagmi (React hooks over viem)
- **Testing**: Hardhat uses Chai/Mocha; Foundry uses Forge with Solidity tests (faster)
- **Deployment scripting**: Hardhat Ignition, Foundry scripts
- **Local nodes**: Hardhat Network, Anvil (Foundry) — fast local EVM for testing
- **Chain interaction**: Cast (Foundry CLI) for quick on-chain reads and writes from terminal
- **AI coding integration**: vibe coding approaches apply to Solidity; AI agents can help scaffold contracts but human review is critical before deployment

## Related Concepts

- [[remix-ide]] — browser-based entry point
- [[hardhat]] — Node.js dev framework
- [[foundry]] — Rust-based dev framework
- [[openzeppelin]] — standard library
- [[viem-wagmi]] — frontend integration layer
- [[solidity]] — the language used throughout
- [[testnet]] — target for initial deployments
- [[vibe-coding]] — AI-assisted coding applies here

## Sources

- [[sources/web3-chapters]] — Chapter: Dev Stack
