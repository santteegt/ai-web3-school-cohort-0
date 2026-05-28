---
title: "Slashing"
type: concept
tags: [aixweb3-bridge, identity-reputation, web3-foundations]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Slashing is the confiscation of collateral when an agent defaults, cheats, or submits false results. Slashing design is difficult — incorrectly slashing legitimate service providers hurts the ecosystem, while weak slashing fails to constrain malicious behavior.

## Key Points

- Must define before implementing: default evidence requirements, challenge window, arbitrators, false-positive handling, appeal mechanism
- More suitable for automatic slashing: clearly verifiable defaults — failure to deliver on time, forged signatures, contradictory results, violation of on-chain-checkable policies
- Less suitable for automatic slashing: subjective tasks like "is the report quality sufficient" — enter dispute first
- Incorrect slashing is itself a governance risk

## Related Concepts

- [[agent-trust-and-reputation]]
- [[stake]]
- [[dispute]]
- [[validation]]
- [[reputation]]
- [[erc-8004]]

## Sources

- [[sources/bridge-chapters]]
