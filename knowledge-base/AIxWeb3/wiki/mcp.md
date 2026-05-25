---
title: "MCP (Model Context Protocol)"
type: concept
tags: [ai-foundations, agent, mcp]
source_count: 2
date_updated: "2026-05-24"
---

## Definition

The Model Context Protocol (MCP) is a unified connectivity protocol that standardizes how LLMs connect to external tools, data sources, and services — enabling any MCP-compatible model to discover and use any MCP-compatible tool without custom integration code per tool-model pair.

## Key Points

- MCP addresses the "N × M integration problem" — before MCP, each model needed custom adapters for each tool; MCP defines a single standard interface
- Enables **tool auto-discovery**: agents can dynamically enumerate available tools and their schemas without hardcoded tool lists
- Architecture: **[[mcp-client]]** connects the model to **[[mcp-server]]s** that expose resources, tools, and prompts
- **Tools need schemas** ([[tool-schema]]) — otherwise tool calls become natural-language parameter guessing
- **Permissions must hold outside the protocol** — MCP specifies how tools are called, not who is authorized; real authorization, audit, and isolation must be implemented by the application layer
- **Errors must be transmissible** — returned clearly instead of leaving the model to guess at failure
- **[[mcp-permission-model]]** is the most underestimated issue when MCP enters real products — different tools have different risk levels and require different authorization scopes
- In AI × Web3: MCP serves as the interface layer for agents connecting to on-chain tools; the Web3 account system handles final permission and execution boundaries — MCP is not a wallet-security solution

## Related Concepts

- [[mcp-server]] — exposes capabilities; must define permission model and side-effect boundaries
- [[mcp-client]] — connects model to servers; handles capability discovery, confirmation flows, session isolation
- [[tool-schema]] — the machine-readable description every MCP tool must have
- [[mcp-permission-model]] — permission design per tool risk level
- [[tool-calling]] — MCP is the protocol underlying tool calling
- [[ai-agent]] — MCP is listed as a core agent component
- [[web3-tool-use]] — AI × Web3 use case: connecting agents to blockchain tools via MCP
- [[four-control-layers]] — MCP implements the tool calling layer
- [[guardrails]] — MCP does not enforce permissions; application guardrails must supplement it

## Sources

- [[sources/ai-fundamentals-introduction]] — MCP as unified connectivity protocol and core agent component
- [[sources/mcp]] — MCP architecture, client/server split, tool schemas, and permission model
