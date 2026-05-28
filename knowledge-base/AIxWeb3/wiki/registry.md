---
title: "Registry (Agent)"
type: concept
tags: [aixweb3-bridge, identity-reputation, web3-foundations]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Registry is used to register, discover, and update agent identities. On-chain registries provide publicly searchable identity anchors: agent ID, owner, profile URI, service endpoint, and update records. Off-chain registries are more flexible but have more centralized trust boundaries.

## Key Points

- Value: discovery and continuity — users find the same agent ID, owner, and profile through a registry without relying on social media links
- On-chain registry can prove "who registered this identity" but cannot prove "this agent is safe or useful" — capabilities and reputation need subsequent verification
- Update records themselves are a trust signal (frequent undisclosed changes reduce trust)
- Registries need Sybil resistance to prevent fake identity farming

## Related Concepts

- [[agent-identity]]
- [[agent-profile]]
- [[service-endpoint]]
- [[erc-8004]]
- [[did-vc]]
- [[ownership]]
- [[reputation]]

## Sources

- [[sources/bridge-chapters]]
