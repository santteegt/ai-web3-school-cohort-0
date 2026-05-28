---
title: "Subscription (Machine Payment)"
type: concept
tags: [aixweb3-bridge, payment-commerce]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Subscription is a payment model for continuous services: monthly API packages, continuous monitoring, or long-term agent tasks. Subscriptions require cancellation capabilities even more than one-time payments — users must always be able to stop.

## Key Points

- Required visibility: current authorizations, next deduction time, remaining limits, service scope, cancellation entry
- Avoid "silent renewals" — agent subscriptions must notify users of renewal events and budget impact
- Better integrated with smart account policies: monthly limits, service provider whitelists, deduction time windows, anomaly alerts
- Do not implement subscriptions through infinite allowance — use time-bounded policy instead

## Related Concepts

- [[machine-payment]]
- [[budget]]
- [[payment-intent]]
- [[policy]]
- [[session-key]]
- [[revocation]]

## Sources

- [[sources/bridge-chapters]]
