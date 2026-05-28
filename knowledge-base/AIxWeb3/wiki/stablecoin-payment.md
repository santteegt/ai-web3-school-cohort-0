---
title: "Stablecoin Payment"
type: concept
tags: [aixweb3-bridge, payment-commerce, defi]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Stablecoins are suitable for machine payments because their prices are relatively stable, settlement is fast, they are programmable, and they are easily verified by contracts and services. However, agents cannot just see "0.1" — they must know the exact token, chain, and decimal precision.

## Key Points

- Distinction required: pricing currency vs. settlement currency (service quotes in USD, pays in USDC via Paymaster)
- Evaluation checklist: liquidity on target chain, recipient accepts that token, failure consumes gas, advance approval required
- Approval is a high-risk action and cannot be mixed with ordinary payments
- USDC/USDT differ in decimal handling, chain availability, and acceptance by service providers

## Related Concepts

- [[machine-payment]]
- [[payment-intent]]
- [[budget]]
- [[stablecoin]]
- [[erc20-token]]
- [[paymaster]]
- [[x402]]

## Sources

- [[sources/bridge-chapters]]
