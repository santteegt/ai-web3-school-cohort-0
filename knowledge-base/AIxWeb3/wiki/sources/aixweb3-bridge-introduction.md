---
title: "AIxWeb3 Bridge - Introduction"
type: source
tags: [aixweb3-bridge, payment-commerce, identity-reputation, wallet-permission, privacy-security, governance-coordination, dev-tooling]
source_file: "raw/AIxWeb3 Bridge - Introduction.md"
source_hash: "sha256:7113300e90e3c5153406418a0c8fa4862b8ca4a7da7d9a72954f428e9e7c9389"
date_ingested: "2026-05-28"
---

## Summary

This source defines the six cross-domain landscape areas of the AI × Web3 School's Module C (Bridge Layer), providing a structured map of problems that arise at the intersection of AI agents and Web3 mechanisms. Each direction is framed not by technology names but by the actual problem it solves: what needs to happen when machines buy services, agents need verifiable identity, wallets require permission boundaries, private data must stay private, or governance processes need AI assistance. The source also introduces task-level authorization via Cobo CAW's Pact model and references key protocols including x402, ERC-8004, ERC-8183, MPP, MCP, A2A, ERC-4337, and ERC-7702.

## Key Concepts

- [[payment-and-commerce]] — quoting, budgeting, escrow, delivery verification, dispute handling
- [[identity-reputation-capability]] — agent discovery, capability claims, trust, interoperability
- [[wallet-permission-safe-execution]] — authorization scope, revocation, human confirmation
- [[privacy-security-sovereignty]] — prompt injection, tool abuse, sensitive data, user sovereignty
- [[dev-tooling-agent-workflow]] — AI-assisted Web3 builder workflows
- [[governance-coordination-public-goods]] — DAO summaries, action items, contribution records
- [[cobo-pact]] — task-level authorization: budget + scope + time window per task
- [[erc-7702]] — standard EOAs gaining temporary smart-account capabilities
- [[mcp]] — tool context and agent-tool interfaces
- [[a2a-protocol]] — agent-to-agent collaboration protocol
- [[erc-4337]] — account abstraction foundation
- [[x402]] — open payment entry points for machine payments
- [[mpp]] — Machine Payments Protocol
- [[erc-8004]] — agent trust and job/escrow protocol directions

## Notable Points

- "Payment is only one segment of the flow; commerce also includes service discovery, price negotiation, task execution, result acceptance, dispute handling, and settlement."
- "Authorization is not a one-time action; it is a combination of budget, scope, time, operation type, and failure handling."
- "Security design must answer: what can the agent see, what can it call, how much can it spend, on whose behalf can it make decisions, and who is responsible when something goes wrong?"
- Task-level authorization (Cobo CAW Pact) generates a temporary authorization per concrete task rather than granting a long-term permission — the agent can only execute within task-defined boundaries, and the permission expires when the task ends.
