---
title: "Guard (Agent Wallet)"
type: concept
tags: [aixweb3-bridge, wallet-permission, security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Guard is a deterministic pre-execution intercept layer that rejects transactions or tool calls not compliant with policy. It is the last line of defense before an agent's action actually leaves the system — checking with deterministic rules even after the model has made a decision.

## Key Points

- Division of labor: the agent generates candidate actions; the Guard rejects actions that exceed boundaries
- Guard checks: target address in whitelist, method allowed, amount within limit, approval amount not abnormal, simulation results meet expectations, current market state unchanged
- Guards are needed because even correct models can be induced by Prompt Injection, tool errors, or context contamination to generate boundary-crossing transactions
- Guards themselves need auditing and recovery mechanisms (they can fail or be bypassed)

## Related Concepts

- [[agent-wallet]]
- [[policy]]
- [[simulation]]
- [[permission-isolation]]
- [[smart-account]]
- [[ai-security]]
- [[prompt-injection]]

## Sources

- [[sources/bridge-chapters]]
