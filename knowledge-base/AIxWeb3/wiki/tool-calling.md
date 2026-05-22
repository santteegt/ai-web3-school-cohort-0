---
title: "Tool Calling"
type: concept
tags: [ai-foundations, agent, llm]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

Tool calling is the mechanism by which a language model emits a structured request for a specific function to be executed — transforming the model from a text generator into an actor that can interact with external systems. The model specifies the tool name and parameters; the framework executes the call and returns the result to the model.

## Key Points

- Tool calling is the fourth control layer: **context window → system instructions → prompt → tool calling**
- "Transforms the model from a talker into a doer" — enables agents to read files, query databases, call APIs, execute transactions
- The model emits a structured request (tool name + parameters); execution happens in code, not in the model
- Tool misuse is an agent-specific failure mode: the model invoking the wrong tool or passing incorrect parameters — requires [[ai-agent-tracing]] to detect
- Parameter verification before tool calls is a key [[prompt-injection]] defense — prevents injected content from manipulating what tools are called with what arguments
- In AI × Web3: tool calling connects agents to RPC nodes, wallets, smart contracts, and on-chain data

## Related Concepts

- [[ai-agent]] — agents rely on tool calling to take action
- [[structured-output]] — tool calls are a form of structured output (model emits a structured function call)
- [[mcp]] — the protocol that standardizes how tools are exposed to models
- [[guardrails]] — tool calls must be validated before execution
- [[prompt-injection]] — injected content can manipulate tool call parameters
- [[ai-agent-tracing]] — tool call observability for debugging and auditing
- [[web3-tool-use]] — AI × Web3 application of tool calling (RPC, wallet, contract tools)
- [[four-control-layers]] — tool calling is the fourth control layer

## Sources

- [[sources/ai-fundamentals-introduction]] — tool calling as control layer and agent component
- [[sources/context]] — tool results in the fact layer of agent context
