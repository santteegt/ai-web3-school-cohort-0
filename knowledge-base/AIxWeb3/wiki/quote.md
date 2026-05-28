---
title: "Quote (Machine Payment)"
type: concept
tags: [aixweb3-bridge, payment-commerce]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Quote is an executable price offer given by a service provider to an agent. A qualified quote contains: service content, price, currency, recipient address, validity period, delivery conditions, refund conditions, and a quote ID.

## Key Points

- Agents must check: within budget, service provider trustworthy, quote not expired
- Validity period is critical: prices, exchange rates, service capacity, and gas all change — expired quotes cannot be reused
- Quotes should be signable or source-verifiable: quotes without signature, ID, and bound recipient address are hard to prove in disputes
- Expired quotes create "user thought 0.1 USDC but price was 1 USDC at execution" problems

## Related Concepts

- [[machine-payment]]
- [[payment-intent]]
- [[budget]]
- [[settlement-and-escrow]]
- [[x402]]
- [[mpp]]

## Sources

- [[sources/bridge-chapters]]
