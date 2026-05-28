---
title: "Agent Profile"
type: concept
tags: [aixweb3-bridge, identity-reputation, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Agent Profile is the public specification document of an agent — machine-readable and human-readable. It contains: name, description, service scope, price, interface, wallet address, capability list, model/tool descriptions, privacy policy, owner, and version.

## Key Points

- A profile is not marketing copy — it must contain machine-parseable fields (endpoints, capabilities, schemas, auth, payment, terms, versions)
- Update history is a trust signal: if an agent changes model, backend, payment address, or adds high-risk capabilities, it should not happen silently
- Humans need: what this agent does, who operates it, how it charges
- Machines need: endpoints, capability schemas, authentication method, payment terms, version info

## Related Concepts

- [[agent-identity]]
- [[capability]]
- [[service-endpoint]]
- [[ownership]]
- [[registry]]
- [[a2a-protocol]]
- [[did-vc]]

## Sources

- [[sources/bridge-chapters]]
