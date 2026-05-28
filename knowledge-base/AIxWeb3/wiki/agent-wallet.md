---
title: "Agent Wallet"
type: concept
tags: [aixweb3-bridge, web3-foundations, agent]
source_count: 3
date_updated: "2026-05-28"
---

## Definition

An Agent Wallet is not simply "giving an AI a wallet private key." The real problem is: what on-chain actions can the agent perform on behalf of the user, whether these actions have limits on amount, time, object, and risk, and when the user must re-confirm. Agents can only be given verifiable, restricted, and revocable action spaces.

## Key Points

- Agents should not hold a primary wallet — receive delegated permissions scoped to specific actions
- A wallet is not just a signature button but a permission system: expresses time, amount, contracts, methods, assets, recipients, and revocation conditions
- Automation must be bound to revocation capability — users must always see what permissions the agent has, what it has done, and where to turn it off
- Two failure modes: "agent can only suggest, never execute" (useless) vs. "permissions too broad, risks unacceptable" (dangerous)
- Typical safe pipeline: user provides goals → agent reads context → system converts to restricted transactions → guards + simulation check → user confirms → smart account executes → logs record

## Sub-Concepts

- [[aa-wallet]] — account abstraction wallet with programmable rules
- [[smart-account]] — execution boundary with policy, recovery, automation (see also [[erc-4337]])
- [[session-key]] — time/amount/target-limited temporary key for low-risk automation
- [[policy]] — checkable rules defining what the agent can do
- [[guard]] — deterministic pre-execution intercept layer
- [[simulation]] — preview transaction results before signing
- [[revocation]] — user + automatic permission withdrawal
- [[human-check]] — layered confirmation at key risk points
- [[cobo-pact]] — task-level temporary authorization (task intent + budget + scope + time window)

## Related Concepts

- [[web3-tool-use]] — the agent wallet is the tool that signs transactions
- [[agent-workflow]] — wallet permissions are scoped to specific workflow steps
- [[guardrails]] — guardrails enforce wallet permission limits in code
- [[machine-payment]] — agent wallet is the mechanism for autonomous payments
- [[agent-identity]] — the wallet provides on-chain identity for the agent
- [[verification-chain]] — signing is step 6; must not be reached without all prior checks
- [[wallet-permission-safe-execution]] — the broader direction this belongs to

## Sources

- [[sources/aixweb3-school]] — agent wallet as AI × Web3 Bridge topic
- [[sources/program-structure]] — agent workflow + wallet confirmation as Week 3 exercise
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
