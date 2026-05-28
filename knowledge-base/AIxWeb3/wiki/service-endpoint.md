---
title: "Service Endpoint"
type: concept
tags: [aixweb3-bridge, identity-reputation, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Service Endpoint is the entry point for external systems to call an agent: HTTPS API, A2A endpoint, MCP server, Webhook, or on-chain registry-pointed service address. Endpoints must handle authentication, rate limiting, versioning, availability, and logging.

## Key Points

- Security of endpoint directly affects identity credibility — hijacked endpoint means users call a malicious service
- Endpoint updates must require an owner signature and maintain a history
- Should describe supported protocols and versions (A2A, MCP, REST, WebSocket differ in interaction)
- Agents need to negotiate capabilities and task formats before using an endpoint

## Related Concepts

- [[agent-identity]]
- [[agent-profile]]
- [[registry]]
- [[a2a-protocol]]
- [[mcp-server]]
- [[ownership]]

## Sources

- [[sources/bridge-chapters]]
