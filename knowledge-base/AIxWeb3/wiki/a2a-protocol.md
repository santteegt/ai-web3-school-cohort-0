---
title: "A2A Protocol (Agent-to-Agent)"
type: concept
tags: [aixweb3-bridge, identity-reputation, interoperability, protocol]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A2A (Agent-to-Agent) is a communication layer protocol that handles how agents discover each other, communicate, negotiate tasks, and exchange results. It is the collaboration protocol layer, complementing the identity layer — identity says "who I am talking to," A2A handles "how to collaborate."

## Key Points

- More than just a wallet address: agents need to know what protocols the other supports, how to authenticate, how task status is synchronized, and how results are returned
- In payment scenarios, A2A messages should be associated with Payment Intent, Receipt, and Escrow states — otherwise dialogue and settlement split into irreconcilable systems
- Combined with identity: agents can discover, negotiate, delegate, and return results across platforms
- Different from MCP: A2A is for agent-to-agent; MCP is for agent-to-tool

## Related Concepts

- [[agent-identity]]
- [[mcp]]
- [[payment-intent]]
- [[service-endpoint]]
- [[capability]]
- [[settlement-and-escrow]]
- [[identity-reputation-capability]]

## Sources

- [[sources/bridge-chapters]]
- [[sources/aixweb3-bridge-introduction]]
