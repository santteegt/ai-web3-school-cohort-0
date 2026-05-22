---
title: "MCP (Model Context Protocol)"
type: concept
tags: [ai-foundations, agent]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

The Model Context Protocol (MCP) is a unified connectivity protocol that standardizes how LLMs connect to external tools, data sources, and services — enabling any MCP-compatible model to discover and use any MCP-compatible tool without custom integration code per tool.

## Key Points

- MCP addresses the "N × M integration problem" — before MCP, each model needed custom adapters for each tool; MCP defines a single standard interface
- Enables **tool auto-discovery**: agents can dynamically enumerate available tools and their schemas without hardcoded tool lists
- MCP servers expose resources (data), tools (functions), and prompts (templates) through a standardized interface
- In the AI × Web3 context, MCP enables agents to connect to RPC nodes, blockchain indexers, wallet interfaces, and DeFi protocols through a consistent protocol
- MCP is the fourth control layer's infrastructure — tool calling uses MCP to discover and invoke tools

## Related Concepts

- [[tool-calling]] — MCP is the protocol underlying tool calling
- [[ai-agent]] — MCP is listed as a core agent component
- [[web3-tool-use]] — AI × Web3 use case: connecting agents to blockchain tools via MCP
- [[four-control-layers]] — MCP implements the tool calling layer

## Sources

- [[sources/ai-fundamentals-introduction]] — MCP as unified connectivity protocol and core agent component
