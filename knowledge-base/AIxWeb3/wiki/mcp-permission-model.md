---
title: "MCP Permission Model"
type: concept
tags: [ai-foundations, mcp, security]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

The MCP permission model is the set of rules defining which agent or user can call which tools, under what authorization scope, and with what confirmation requirements — the most underestimated issue when MCP enters real products.

## Key Points

- Permission must distinguish at minimum: read-only vs. write, current-session authorization vs. long-term authorization, whether user confirmation is required, whether sensitive information can be accessed, whether external side effects are created, and whether the action is revocable and auditable
- Different tool calls have different risk levels — a blanket "all tools allowed" permission model is never appropriate for production
- "Permissions must also hold outside the protocol" — MCP specifies how tools are called, not who is authorized to call them; real authorization must be implemented at the application layer
- In AI × Web3, MCP permission models must account for: wallet signing authority (session-scoped only), contract interaction allowlists, spending limits per session, and revocation on anomaly detection
- The permission model should be defined before tools are exposed, not added retroactively

## Related Concepts

- [[mcp]] — permission is a core MCP design concern
- [[mcp-server]] — servers define the initial permission boundaries
- [[mcp-client]] — clients enforce user confirmation requirements
- [[tool-schema]] — the schema's side-effect flag informs which permission tier a tool falls in
- [[guardrails]] — application-layer guardrails implement the permission model in code
- [[agent-wallet]] — wallet permissions are the highest-stakes subset of MCP permission models in Web3 contexts

## Sources

- [[sources/mcp]] — permission model definition and risk dimensions
