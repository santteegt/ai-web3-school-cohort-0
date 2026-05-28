---
title: "Policy (Agent Wallet)"
type: concept
tags: [aixweb3-bridge, wallet-permission, security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Policy writes "what the agent can do" into checkable rules that the system can evaluate before execution. Good policies are conditions the system can check, not just descriptions of intent.

## Key Points

- Example policy rules: maximum 10 USDC/day, only whitelisted contracts, only swap operations (no infinite allowance), stop if slippage > 1%, NFT transfers require manual confirmation
- Vague requests like "help me perform low-risk operations" are not suitable for direct translation into on-chain permissions
- The clearer the policy, the more controllable the agent's execution space
- A good policy must allow the system to answer: "Did this operation cross the line?"

## Related Concepts

- [[agent-wallet]]
- [[guard]]
- [[session-key]]
- [[tool-permission]]
- [[human-in-the-loop]]
- [[cobo-pact]]
- [[wallet-permission-safe-execution]]
- [[smart-account]]

## Sources

- [[sources/bridge-chapters]]
