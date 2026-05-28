---
title: "Payment Intent"
type: concept
tags: [aixweb3-bridge, payment-commerce]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Payment Intent expresses that a user or agent wants to pay for a specific service — but it is not equivalent to having settled. It should be bound to task, amount, recipient, validity period, and acceptable results, providing the authorization context for subsequent payment, escrow, and receipts.

## Key Points

- "User authorizes this type of payment" rather than "a specific transaction has already occurred"
- Required fields: user goal, service provider, maximum amount, currency, chain, expiration time, quote reference, whether automatic retry is allowed, whether human confirmation is required
- Without these fields, agent payment behavior is hard to audit
- Created before actual settlement to provide traceability for the full payment flow

## Related Concepts

- [[machine-payment]]
- [[quote]]
- [[budget]]
- [[settlement-and-escrow]]
- [[receipt]]
- [[a2a-protocol]]

## Sources

- [[sources/bridge-chapters]]
