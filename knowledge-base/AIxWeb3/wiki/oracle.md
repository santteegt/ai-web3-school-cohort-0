---
title: "Oracle"
type: concept
tags: [web3-foundations, oracle, data]
source_count: 1
date_updated: "2026-05-25"
---

# Oracle

## Definition

An oracle is a system that bridges off-chain data into on-chain smart contracts. Blockchains are deterministic, isolated systems — they cannot natively access external APIs, prices, or real-world events. Oracles solve this by publishing authenticated off-chain data on-chain, allowing contracts to act on real-world information.

## Key Points

- **The oracle problem**: how do you trust that the data published on-chain is accurate? Centralized oracles are single points of failure; decentralized oracle networks (DONs) aggregate many independent data sources
- **Chainlink**: dominant decentralized oracle network; aggregates data from many independent node operators; nodes stake LINK as collateral against misbehavior
- **Pyth Network**: high-frequency price oracle fed by institutional data providers (exchanges, market makers); lower latency than Chainlink
- **Push vs pull**: push oracles update on-chain proactively; pull oracles (Pyth) require users to submit a fresh price with their transaction
- **TWAP oracle**: time-weighted average price derived from AMM pool ratios on-chain; trustless but manipulable in low-liquidity pools
- **Data types**: price feeds, randomness (VRF), cross-chain state, weather, sports results
- **AI Oracle**: emerging pattern — publishing verified AI model outputs on-chain (see [[ai-oracle]])

## Related Concepts

- [[price-feed]] — the most common oracle output
- [[oracle-risk]] — risks inherent in oracle systems
- [[ai-oracle]] — AI × Web3 intersection
- [[defi]] — DeFi protocols critically depend on oracles
- [[defi-lending]] — collateral valuation uses oracle prices
- [[smart-contract]] — contracts consume oracle data

## Sources

- [[sources/web3-chapters]] — Chapter: Oracle
