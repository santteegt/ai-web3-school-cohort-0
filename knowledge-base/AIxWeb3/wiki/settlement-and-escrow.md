---
title: "Settlement & Escrow"
type: concept
tags: [aixweb3-bridge, payment-commerce, agent, defi]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Settlement & Escrow addresses when money is released, how service is considered complete, how to refund on failure, and how to handle disputes in the agent economy. It turns payment from a single transfer into a complete transaction process by binding task, delivery, acceptance, and payment into a verifiable flow.

## Key Points

- Fund states must be clear: `pending → locked → delivered → accepted/disputed → released/refunded`
- Delivery proof must be preservable: file hashes, API logs, model output signatures, on-chain events, TEE attestations
- Dispute flows must be designed before launch — not after failure
- Good escrow defines business flow (task, acceptance criteria, failure paths) first, then fund flow
- Evaluators should combine automated checks + challenge windows + human review for high-value tasks

## Sub-Concepts

- [[escrow]] — fund locking with state machine until delivery conditions are met
- [[receipt]] — credential recording payer, amount, task ID, acceptance status, transaction hash
- [[delivery-proof]] — file hash, API log, on-chain event, TEE attestation linked to original task
- [[acceptance]] — payer or rule system confirming delivery meets requirements
- [[refund]] — fund return on timeout, format error, delivery failure, or cancellation
- [[dispute]] — challenge flow with cost, evidence format, arbitrator, appeal mechanism
- [[evaluator]] — script/model/human/validator judging delivery qualification
- [[erc-8183]] — draft standard for agent commerce task lifecycle (tasks, states, proof, settlement)

## Position in AI × Web3

Settlement & Escrow is the second half of [[machine-payment]]. Machine Payment solves "how to pay"; Settlement & Escrow solves "how to confirm value exchange is complete after payment." Together they form [[payment-and-commerce]].

## Related Concepts

- [[machine-payment]]
- [[payment-and-commerce]]
- [[agent-trust-and-reputation]]
- [[ai-oracle]]
- [[erc-8004]]
- [[erc-8183]]
- [[payment-intent]]
- [[budget]]

## Sources

- [[sources/bridge-chapters]]
