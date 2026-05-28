---
title: "Refund"
type: concept
tags: [aixweb3-bridge, payment-commerce]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Refund returns funds when delivery fails, times out, or is cancelled. Refund rules must be written before the task starts — who can trigger it, after how long, whether a partial fee is deducted, and whether the service provider can appeal.

## Key Points

- Common refund triggers: service provider timeout, delivery format error, acceptance failure, task cancellation, quote expiration, service provider endpoint unavailable
- Partial delivery scenarios require partial refund rules (e.g., data scraped but analysis failed → proportional payment)
- Without partial refund rules, both parties easily enter a dispute
- Refund is part of the protocol, not a temporary kindness after failure

## Related Concepts

- [[settlement-and-escrow]]
- [[escrow]]
- [[dispute]]
- [[receipt]]
- [[payment-intent]]
- [[acceptance]]

## Sources

- [[sources/bridge-chapters]]
