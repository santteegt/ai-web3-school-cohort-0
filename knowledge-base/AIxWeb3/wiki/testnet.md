---
title: "Testnet"
type: concept
tags: [web3-foundations, network, dev-tooling]
source_count: 2
date_updated: "2026-05-25"
---

# Testnet

## Definition

A testnet is a blockchain network that uses valueless test tokens instead of real cryptocurrency. Testnets replicate the behavior of mainnet but allow developers, students, and users to experiment, deploy contracts, and test transactions without financial risk. All AI × Web3 learning and experiments should be completed on testnets first.

## Key Points

- **Sepolia**: current primary Ethereum testnet; recommended for smart contract development and testing; faucets available (Google, Alchemy, Chainlink)
- **Holesky**: testnet focused on staking and validator operations; much higher ETH supply than Sepolia
- **Faucets**: web services that give free test ETH to any address; rate-limited to prevent abuse
- **Test token ≠ real value**: test ETH cannot be bridged to mainnet or exchanged for real value
- **Same EVM behavior**: contract behavior, gas mechanics, and tooling work identically on testnet and mainnet
- **Deploy → test → mainnet**: the recommended deployment progression; testnets catch bugs cheaply
- **Testnet explorers**: Sepolia Etherscan (`sepolia.etherscan.io`) mirrors mainnet Etherscan

## Related Concepts

- [[blockchain-network]] — testnet is a type of network
- [[smart-contract]] — deploy here before mainnet
- [[gas]] — gas mechanics identical to mainnet (but tokens are free)
- [[block-explorer]] — each testnet has its own explorer
- [[web3-dev-stack]] — Hardhat/Foundry/Remix all support testnet deployment
- [[layer-2]] — L2 testnets: Arbitrum Sepolia, Base Sepolia, etc.

## Sources

- [[sources/web3-chapters]] — Chapter: Network
- [[sources/web3-fundamentals-introduction]] — Module B: testnets vs mainnet
