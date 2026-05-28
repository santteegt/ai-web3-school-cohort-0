---
title: "Machine Payment"
type: concept
tags: [aixweb3-bridge, web3-foundations, agent]
source_count: 3
date_updated: "2026-05-28"
---

## Definition

Machine Payment discusses how agents, APIs, services, and wallets automatically complete quoting, authorization, payment, receipts, and budget control. The focus is not on "AI spending money" but on making payments between machines limitable, verifiable, and traceable. Core principle: decouple "payment intent" from "actual settlement" and ensure every step has evidence.

## Key Points

- Budget precedes execution — without budget boundaries, there is no safe automatic payment
- Quotes must be comparable: agents need price, currency, validity period, service scope, and refund conditions
- Receipts must be verifiable: after payment, it must be provable to whom it was paid, why, and what was delivered
- The full flow: user authorizes budget → agent gets quote → system checks policy → payment enters escrow or direct settlement → service delivered → receipt as evidence
- Micro-payment patterns require L2s, payment channels, or batch settlement — L1 gas fees make per-call settlement uneconomical

## Sub-Concepts

- [[stablecoin-payment]] — pricing vs. settlement currency, chain/token considerations
- [[budget]] — layered spending limits: global, task, call, provider, emergency stop
- [[quote]] — executable price offer with validity period, refund conditions, and quote ID
- [[payment-intent]] — authorization to pay for a service type, not yet settled
- [[x402]] — HTTP 402 payment flow for per-use API/content payments
- [[mpp]] — Machine Payments Protocol: discovery, quote, auth, settlement, receipt
- [[subscription]] — continuous service payment with cancellation capabilities
- [[micropayment]] — high-frequency small-amount with batch settlement strategies

## Related Concepts

- [[agent-wallet]] — the payment mechanism for machine payments
- [[settlement-and-escrow]] — completing the payment lifecycle after initial transfer
- [[agent-workflow]] — payment is a step in agentic workflows
- [[agent-identity]] — the paying agent must be identifiable for receipt purposes
- [[web3-tool-use]] — payment tool calls sign and submit transactions
- [[payment-and-commerce]] — the broader direction this belongs to

## Sources

- [[sources/aixweb3-school]] — machine payment as AI × Web3 Bridge topic
- [[sources/program-structure]] — testnet payments as Week 3 practice exercise
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
