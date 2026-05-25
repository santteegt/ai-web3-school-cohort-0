---
title: "MCP Server"
type: concept
tags: [ai-foundations, mcp]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

An MCP server is the component that exposes capabilities to AI clients — resources (data to read), tools (functions to call), and prompts (templates to use). It is responsible for defining what it makes available and under what permission conditions.

## Key Points

- An MCP server must define its permission model before exposing capabilities — not as an afterthought
- Server design checklist for each capability: which resources are exposed? which tools are read-only vs. side-effectful? are parameter schemas clear? how are errors returned? is user authorization required? where are logs and audits recorded?
- The server exposes the interface; it does not enforce application-layer authorization — "real authorization, audit, and isolation still need to be implemented by the system"
- In AI × Web3: an MCP server exposing wallet tools, contract calls, or RPC endpoints must have especially tight permission boundaries — read-only blockchain queries can be open, but signing operations require explicit session-scoped authorization

## Related Concepts

- [[mcp]] — MCP server is one side of the MCP client-server split
- [[mcp-client]] — the client that connects to and queries MCP servers
- [[tool-schema]] — servers define tool schemas for every exposed tool
- [[mcp-permission-model]] — permission design is the server's most critical responsibility
- [[web3-tool-use]] — Web3 tools are exposed via MCP servers
- [[guardrails]] — application-layer guardrails supplement MCP server boundary definitions

## Sources

- [[sources/mcp]] — MCP server definition and design checklist
