---
title: "Hermes"
type: concept
tags: [ai-foundations, frameworks, agent]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

Hermes is a model and agent ecosystem from Nous Research oriented around reliable tool calling and structured output — rather than a general-purpose orchestration framework. Its value is in the model's native ability to produce the structured output and tool-call format required by agent workflows.

## Key Points

- "Do not look only at benchmark scores. Look at whether it can reliably produce the structured output and tool-call format you need" — Hermes is evaluated on format reliability, not general benchmark performance
- Hermes specializes in function calling and JSON output — tasks where model output reliability directly determines system correctness
- Relevant for AI × Web3 because on-chain tool calls require precise, schema-valid output — a model that occasionally produces malformed tool calls is not production-safe for smart contract interactions
- Hermes models are available via Nous Research and compatible with OpenAI-style function calling format

## Related Concepts

- [[ai-frameworks-overview]] — Hermes is in the agent tooling ecosystem
- [[structured-output]] — Hermes's core competency
- [[tool-calling]] — reliable tool calling is Hermes's primary design goal
- [[mcp]] — Hermes can serve as the model layer in an MCP-connected agent stack
- [[web3-tool-use]] — a model with reliable tool calling is essential for Web3 agent safety

## Sources

- [[sources/frameworks]] — Hermes description and evaluation criterion
