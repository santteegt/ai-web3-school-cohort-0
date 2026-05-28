---
title: "Agent Identity"
type: concept
tags: [aixweb3-bridge, web3-foundations, agent]
source_count: 2
date_updated: "2026-05-28"
---

## Definition

Agent Identity is not about giving an agent a name — it is about allowing users, services, and other agents to verify who it is, who controls it, what capabilities it provides, where the service entry point is, and whether historical records can be traced. Core principle: agent identity must be bound to control, capability declarations, and service entry points — not just a display name.

## Key Points

- Identity answers "who are you," capability answers "what can you do," reputation answers "why should others trust you"
- Identity is a prerequisite for payment, trust, and agentic commerce: before paying an agent, users must know who the recipient is
- Authorization must be explicit and session-scoped — remembered identity cannot grant persistent unrestricted permissions
- Identity itself does not equal trust — it is just the first layer

## Sub-Concepts

- [[agent-profile]] — public specification: name, capabilities, endpoint, price, owner, version (machine-readable)
- [[capability]] — concrete task + input/output/risk level declarations bound to schemas and limits
- [[service-endpoint]] — HTTPS/A2A/MCP entry point with owner-signed update history
- [[registry]] — on-chain/off-chain discovery and continuity anchor for agent IDs
- [[did-vc]] — decentralized identifiers + verifiable credentials for cross-platform claims
- [[a2a-protocol]] — agent discovery, task negotiation, result exchange
- [[ownership]] — who can update profile/endpoint/payment address; accountability layer

## Related Concepts

- [[agent-wallet]] — the wallet is the primary on-chain identity anchor
- [[agent-workflow]] — identity is verified at workflow authorization points
- [[guardrails]] — identity-based access control is a form of guardrail
- [[ai-agent-tracing]] — traces are attributed to a specific agent identity
- [[verifiable-ai]] — agent identity enables verifiable attribution of AI actions
- [[agent-trust-and-reputation]] — identity is the prerequisite for accumulating reputation
- [[identity-reputation-capability]] — the broader direction

## Sources

- [[sources/aixweb3-school]] — agent identity as AI × Web3 Bridge topic
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
