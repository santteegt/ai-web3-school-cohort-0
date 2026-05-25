---
title: "Stablecoin"
type: concept
tags: [web3-foundations, defi]
source_count: 1
date_updated: "2026-05-25"
---

# Stablecoin

## Definition

A stablecoin is a cryptocurrency designed to maintain a stable value relative to a reference asset (typically the US dollar). Stablecoins are the primary unit of account in DeFi, enabling price-stable lending, trading, and payments without converting to fiat. The three main mechanisms: fiat-backed (USDC, USDT), crypto-collateralized (DAI), and algorithmic (FRAX, formerly UST).

## Key Points

- **Fiat-backed**: reserves held off-chain by a custodian; redeemable 1:1 for USD; subject to counterparty and regulatory risk (USDC, USDT, BUSD)
- **Crypto-collateralized**: over-collateralized by crypto assets locked in a smart contract; decentralized but requires excess collateral (DAI via MakerDAO)
- **Algorithmic**: uses protocol mechanics (seigniorage, bonding curves) to maintain peg; fragile to confidence crises — Terra/LUNA collapse (2022) erased $40B
- **Depeg risk**: stablecoins can lose their peg during market stress; USDC depegged briefly during SVB collapse (2023)
- **DeFi plumbing**: stablecoins are the lubricant of DeFi — used for trading pairs, collateral, yields, and payments
- **CBDC**: Central Bank Digital Currencies are government-issued digital currencies; distinct from decentralized stablecoins

## Related Concepts

- [[defi]] — stablecoins are the unit of account
- [[erc20-token]] — most stablecoins are ERC-20 tokens
- [[oracle]] — price oracles monitor stablecoin peg stability
- [[defi-lending]] — stablecoins are primary borrowed/lent assets
- [[machine-payment]] — AI agent payments in stablecoins are more predictable than in ETH

## Sources

- [[sources/web3-chapters]] — Chapter: DeFi
