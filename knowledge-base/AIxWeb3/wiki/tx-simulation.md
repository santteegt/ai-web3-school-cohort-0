---
title: "Transaction Simulation"
type: concept
tags: [web3-foundations, security, dev-tooling]
source_count: 1
date_updated: "2026-05-25"
---

# Transaction Simulation

## Definition

Transaction simulation is the process of executing a transaction in a sandbox environment (without on-chain state changes) to preview its outcome — gas cost, return values, state changes, emitted events, and potential reverts. Simulation is used to validate transactions before broadcasting, catch bugs before deployment, and provide users with transparent pre-execution previews.

## Key Points

- **Local simulation**: Hardhat Network and Anvil (Foundry) provide local EVM that executes transactions instantly without mining
- **Mainnet fork**: fork a real chain at a specific block → simulate against real mainnet state; catches integration bugs that local tests miss
- **Tenderly**: cloud-based transaction simulation and debugger; supports mainnet fork, gas profiling, and step-by-step EVM trace
- **User-facing simulation**: wallets (Metamask, Rabby) show simulated balance changes and token approvals before the user signs — reduces phishing risk
- **Pre-flight checks**: AI agents should simulate a transaction before signing and submitting it → detect unexpected state changes that signal malicious intent
- **Gas estimation**: `eth_estimateGas` simulates the transaction to estimate gas cost; unreliable for complex contracts under high load

## Related Concepts

- [[web3-security]] — simulation as a pre-execution defense
- [[web3-transaction]] — what is being simulated
- [[hardhat]] — provides local simulation via Hardhat Network
- [[foundry]] — Forge tests and Anvil for simulation
- [[contract-audit]] — simulation is a pre-audit tool
- [[agent-wallet]] — AI agents should simulate before signing
- [[on-chain-monitoring]] — post-execution complement to pre-execution simulation

## Sources

- [[sources/web3-chapters]] — Chapter: Security
