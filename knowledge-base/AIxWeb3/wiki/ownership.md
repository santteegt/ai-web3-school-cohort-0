---
title: "Ownership (Agent Identity)"
type: concept
tags: [aixweb3-bridge, identity-reputation, web3-foundations]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Ownership determines who can update an agent's profile, payment address, service endpoint, and permissions. It establishes accountability: if something goes wrong, who handles refunds, disputes, and compensation.

## Key Points

- High-value agents should not be controlled by a single hot wallet — use Smart Account, multi-sig, or DAO
- Identity updates, endpoint updates, and payment address changes should all leave verifiable records
- Recommended separation: operator (runs the service) vs. owner (controls identity and key updates)
- If the owner is a DAO or multi-sig, governance and operational processes should be understandable by users

## Related Concepts

- [[agent-identity]]
- [[agent-profile]]
- [[registry]]
- [[smart-account]]
- [[eoa]]
- [[dao]]
- [[did-vc]]

## Sources

- [[sources/bridge-chapters]]
