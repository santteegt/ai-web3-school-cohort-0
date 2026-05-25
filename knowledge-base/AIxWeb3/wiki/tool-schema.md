---
title: "Tool Schema"
type: concept
tags: [ai-foundations, mcp, agent]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

A tool schema is the machine-readable description of a tool — its name, purpose, parameters (types, required fields, defaults), return values, constraints, and side-effect flags — that enables both humans and models to understand when and how to use the tool correctly.

## Key Points

- "If a tool schema is vague, the model will fill gaps with wrong parameters" — schema quality directly determines tool call correctness
- A good tool schema answers: when should this tool be used? what does each parameter mean? which fields are required? does it change external state? what is returned on failure?
- Tool schemas are central to MCP — they are what the MCP server exposes and the MCP client presents to the model
- In AI × Web3, tool schemas for blockchain operations must explicitly flag: whether the call is read-only or a state change, which network/chain it operates on, what wallet permissions are required, and what simulation is available
- Tool schemas should be versioned alongside the tools themselves — a schema change without a version bump causes silent failures in downstream agents

## Related Concepts

- [[mcp]] — tool schemas are a core MCP primitive
- [[mcp-server]] — servers define and expose tool schemas
- [[mcp-client]] — clients read schemas and present them to the model
- [[tool-calling]] — tool calls reference schema-defined names and parameters
- [[structured-output]] — tool schemas are a form of structured output definition
- [[mcp-permission-model]] — the schema's side-effect flag informs permission requirements

## Sources

- [[sources/mcp]] — tool schema definition and design requirements
