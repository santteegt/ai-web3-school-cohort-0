---
title: "Reputation (Agent)"
type: concept
tags: [aixweb3-bridge, identity-reputation, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Reputation is a collection of signals formed by an agent's historical performance. It should not be compressed into a single black-box score — users need to understand why an agent is trusted for a specific task type.

## Key Points

- Signals: success rate, response time, dispute rate, refund rate, user ratings, verification passes, stake amount, task-type performance
- Must be broken down by task type: a governance-summary agent may not be reliable for contract testing
- Time decay matters: performance from two years ago may not represent current quality (model, owner, endpoint, tool stack may have changed)
- Reputation must be bound to identity — without stable identity, records cannot accumulate

## Related Concepts

- [[agent-trust-and-reputation]]
- [[review]]
- [[attestation]]
- [[stake]]
- [[slashing]]
- [[validation]]
- [[erc-8004]]
- [[agent-identity]]

## Sources

- [[sources/bridge-chapters]]
