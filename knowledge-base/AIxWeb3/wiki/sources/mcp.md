---
title: "MCP"
type: source
tags: [ai-foundations, mcp, tool-use, agent, security]
source_file: "raw/MCP.md"
source_hash: "sha256:253d6a443bf25dd37bd1328ef09d9a73f27aa7f45c7f5731f4c17dc3ca5b4781"
date_ingested: "2026-05-24"
---

## Summary

This source provides a deep technical treatment of the Model Context Protocol — how it standardizes the connection between models and external tools through a client/server architecture. It introduces the critical design requirements for MCP components: tools need schemas (otherwise parameter guessing breaks calls), permissions must hold outside the protocol (MCP is not a security boundary), and errors must be transmissible. The source emphasizes that permission design is the most underestimated issue when MCP enters real products.

## Key Concepts

- [[mcp]] — standardizes tool discovery, call format, and results between model clients and external servers
- [[mcp-server]] — exposes resources, tools, and prompts; must define permission model and side-effect boundaries per capability
- [[mcp-client]] — connects model to MCP servers; handles capability discovery, tool presentation to model, confirmation flows, and session isolation
- [[tool-schema]] — describes tool name, purpose, parameters, return values, and constraints; vague schemas cause wrong-parameter tool calls
- [[mcp-permission-model]] — permission is the most underestimated MCP issue; must distinguish read/write, session vs. long-term auth, user confirmation needs
- [[tool-calling]] — MCP turns tool calling into a discoverable, reusable, manageable protocol
- [[guardrails]] — MCP does not enforce permissions; real authorization and isolation must be implemented by the system
- [[prompt-injection]] — malicious tool results can propagate injected instructions back to the model via the MCP response

## Notable Points

- "MCP handles tool discovery and call format. Web3 account system handles final permission and execution boundaries." — MCP is not a wallet-security solution.
- "Tools need schemas: otherwise tool calls become natural-language parameter guessing."
- Different tool calls have different risk levels — permission must distinguish: read-only vs. write, current-session vs. long-term authorization, user confirmation requirements, external side effects, and revocability.
