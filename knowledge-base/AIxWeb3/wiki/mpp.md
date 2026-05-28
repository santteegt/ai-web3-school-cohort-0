---
title: "MPP (Machine Payments Protocol)"
type: concept
tags: [aixweb3-bridge, payment-commerce, protocol]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

MPP (Machine Payments Protocol) focuses on payment negotiation and settlement between machines. It protocolizes the payment process for agent services: service discovery, obtaining quotes, authorizing payments, settlement, and returning receipts — all in machine-readable formats.

## Key Points

- Machine payment requires more than on-chain transfers: quotes, credentials, and error handling are all part of the protocol
- Without a protocol, agents piece together flows from webpages/docs — poor reliability
- Many steps can be completed off-chain; the chain only bears final settlement, collateral, receipt anchoring, or dispute evidence
- MPP is complementary to [[x402]]: x402 handles per-request payment triggers; MPP handles the broader service discovery and settlement lifecycle

## Related Concepts

- [[machine-payment]]
- [[x402]]
- [[payment-intent]]
- [[quote]]
- [[settlement-and-escrow]]
- [[agent-identity]]
- [[erc-8183]]

## Sources

- [[sources/bridge-chapters]]
- [[sources/aixweb3-bridge-introduction]]
