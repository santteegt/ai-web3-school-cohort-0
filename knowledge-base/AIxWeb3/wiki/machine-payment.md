---
title: "Machine Payment"
type: concept
tags: [aixweb3-bridge, web3-foundations, agent]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

Machine payment is the capability of AI agents to autonomously complete micro-payments and service settlements on-chain — paying for compute, APIs, data, or task completion without human intervention for each transaction.

## Key Points

- Enables agent-to-agent commerce: one agent pays another for a service it needs to complete its task
- Requires a scoped [[agent-wallet]] with spending limits — unbounded payment authority for an agent is a critical security risk
- Machine payment is at the core of the **Agentic Commerce** frontier track: agents discover services, negotiate terms, complete payment, and leave on-chain receipts
- On-chain receipts (transaction hashes, event logs) serve as immutable proof of service payment — critical for auditability
- Micro-payment patterns require low-fee chains (L2s) or payment channels — L1 gas fees make per-task micro-payments uneconomical

## Related Concepts

- [[agent-wallet]] — the payment mechanism for machine payments
- [[agent-workflow]] — payment is a step in agentic workflows
- [[agent-identity]] — the paying agent must be identifiable for receipt purposes
- [[web3-tool-use]] — payment tool calls sign and submit transactions
- [[verification-chain]] — payment submissions require simulation and validation

## Sources

- [[sources/aixweb3-school]] — machine payment as AI × Web3 Bridge topic
- [[sources/program-structure]] — testnet payments as Week 3 practice exercise
