---
title: "MCP Client"
type: concept
tags: [ai-foundations, mcp]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

An MCP client connects the AI model to one or more MCP servers — discovering available capabilities, presenting tool information to the model, translating model-generated call requests into MCP protocol messages, and handling user confirmation flows and session isolation.

## Key Points

- Client responsibilities: discover server capabilities, present tool schemas to the model, convert model output (`{tool, params}`) into MCP protocol calls, handle user confirmation prompts, maintain session isolation, display tool calls to users
- The client is the trust boundary between the model's requests and the server's execution — it should validate that the model's requested tool call matches the schema before forwarding
- Session isolation: the client must prevent tool calls from one session from affecting another (e.g. a multi-user MCP deployment should not leak session context between users)
- Tool call display: showing the user what tool is being called with what parameters — before execution — is a key human-in-the-loop pattern
- The client owns the UX of tool use; the server owns the capability boundary

## Related Concepts

- [[mcp]] — the client is one side of the MCP client-server architecture
- [[mcp-server]] — the server the client connects to
- [[tool-schema]] — the client reads and presents tool schemas to the model
- [[mcp-permission-model]] — the client enforces user confirmation requirements from the permission model
- [[tool-calling]] — MCP clients implement the tool calling execution path
- [[five-layer-agent-context]] — tool results returned via the client populate the fact layer

## Sources

- [[sources/mcp]] — MCP client definition, responsibilities, and session isolation requirement
