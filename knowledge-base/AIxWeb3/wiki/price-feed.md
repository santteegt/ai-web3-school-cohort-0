---
title: "Price Feed"
type: concept
tags: [web3-foundations, oracle, defi]
source_count: 1
date_updated: "2026-05-25"
---

# Price Feed

## Definition

A price feed is an oracle service that publishes real-time or regularly updated asset prices on-chain, expressed in USD or other reference currencies. Price feeds are consumed by DeFi protocols for collateral valuation, liquidation triggers, and synthetic asset pricing. Chainlink price feeds are the most widely used.

## Key Points

- **Aggregation**: Chainlink aggregates prices from multiple premium data providers and independent nodes; the median of multiple sources reduces manipulation risk
- **Heartbeat**: feeds update on-chain at fixed intervals (e.g., every hour) and when the price deviates beyond a threshold (e.g., 0.5%)
- **Stale price risk**: if a feed stops updating (node failure, gas spike), contracts may use stale prices → liquidation errors
- **Deviation threshold**: price updates are triggered when the price moves more than X% from the last update; low-volatility assets update less frequently
- **Reference contracts**: each Chainlink feed is a deployed contract at a known address; consumers call `latestRoundData()` to get price, timestamp, and round ID
- **Verify freshness**: contracts should check `updatedAt` timestamp and reject stale prices (older than `heartbeat + buffer`)

## Related Concepts

- [[oracle]] — price feed is the primary oracle type
- [[oracle-risk]] — stale price and manipulation risks
- [[defi-lending]] — collateral valuation uses price feeds
- [[amm]] — AMM-derived TWAP is an alternative on-chain price source
- [[smart-contract]] — feeds are contracts; consuming contracts call them

## Sources

- [[sources/web3-chapters]] — Chapter: Oracle
