---
title: "Capability (Agent)"
type: concept
tags: [aixweb3-bridge, identity-reputation, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Capability describes what specific tasks an agent can complete, along with the inputs, outputs, permissions, and risk levels required. Capability declarations should be bound to schemas, prices, limits, test records, and failure conditions.

## Key Points

- "Summarizing governance proposals," "generating Solidity tests," and "executing stablecoin payments" are completely different capabilities — not just "I can do anything"
- Each capability should specify: input types, output format, whether wallet permissions are needed, whether external APIs are called, maximum execution time, failure refund policy
- Risk level marking required: read-only analysis (low), generating transaction drafts (medium), automatically executing transactions (high)
- The more specific the capability declaration, the more useful it is for discovery, routing, and trust

## Related Concepts

- [[agent-identity]]
- [[agent-profile]]
- [[service-endpoint]]
- [[identity-reputation-capability]]
- [[erc-8004]]
- [[a2a-protocol]]

## Sources

- [[sources/bridge-chapters]]
