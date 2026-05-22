---
title: "Agent Wallet"
type: concept
tags: [aixweb3-bridge, web3-foundations, agent]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

An agent wallet is a blockchain wallet (or delegated signing key) granted to an AI agent, scoped with explicit permissions — spending limits, allowed contracts, time windows, and revocation conditions — so the agent can execute on-chain actions within defined boundaries.

## Key Points

- Agents should not hold a primary wallet — instead, they receive **delegated permissions** scoped to specific actions
- Key permission dimensions: spending limit (max value per transaction), contract allowlist (which contracts can be called), time window (valid until when), revocation (can be cancelled at any time)
- Account Abstraction (ERC-4337 / Smart Accounts) enables programmable permission models that are well-suited for agent delegation
- The agent wallet is how [[agent-memory]] about permissions maps to actual on-chain enforcement — remembered permissions must be re-verified at execution time
- Overly broad agent wallets are a primary AI × Web3 security risk: if the agent is compromised or hallucinating, it can cause irreversible financial losses

## Related Concepts

- [[web3-tool-use]] — the agent wallet is the tool that signs transactions
- [[agent-workflow]] — wallet permissions are scoped to specific workflow steps
- [[guardrails]] — guardrails enforce wallet permission limits in code
- [[machine-payment]] — agent wallet is the mechanism for autonomous payments
- [[agent-identity]] — the wallet provides on-chain identity for the agent
- [[verification-chain]] — signing is step 6; must not be reached without all prior checks

## Sources

- [[sources/aixweb3-school]] — agent wallet as AI × Web3 Bridge topic
- [[sources/program-structure]] — agent workflow + wallet confirmation as Week 3 exercise
