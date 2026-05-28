---
title: "Escrow"
type: concept
tags: [aixweb3-bridge, payment-commerce, defi]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Escrow locks funds temporarily in a contract or trusted account, waiting for delivery conditions to be met before release. It provides the intermediate layer between payment and delivery: funds are first locked, released after acceptance, and refunded or arbitrated on failure.

## Key Points

- State machine is the key: `Created → Funded → Delivered → Accepted → Released` (or `Refunded` / `Disputed`)
- Each state defines: who can trigger it, what evidence is needed, how to handle timeout
- Escrow without task description, delivery standards, and dispute paths will only trap both parties in the contract
- Suitable for: one-time tasks, API packages, model inference, data delivery, cross-agent delegation

## Related Concepts

- [[settlement-and-escrow]]
- [[receipt]]
- [[delivery-proof]]
- [[acceptance]]
- [[refund]]
- [[dispute]]
- [[evaluator]]
- [[erc-8183]]
- [[payment-intent]]

## Sources

- [[sources/bridge-chapters]]
