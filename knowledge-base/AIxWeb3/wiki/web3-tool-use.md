---
title: "Web3 Tool Use"
type: concept
tags: [aixweb3-bridge, agent, web3-foundations]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Web3 tool use is the pattern of connecting AI agents to blockchain infrastructure — RPC nodes, wallet signers, smart contract interfaces, and indexers — via [[tool-calling]], enabling agents to read chain state and submit transactions.

## Key Points

- RPC calls, contract calls, wallet signing, and indexer queries all become agent tools exposed via [[mcp]] or direct function calling
- Web3 tools are higher-stakes than typical API tools: a tool call to a smart contract may be irreversible and have financial consequences
- Every Web3 tool call that modifies state requires: parameter verification, [[guardrails]], simulation before signing, and explicit human confirmation for high-value actions
- Tool results (RPC responses, transaction receipts) populate the [[five-layer-agent-context]] fact layer — they must be fresh, not cached
- RAG over protocol documentation combined with Web3 tool use enables powerful agent capabilities (e.g. "find the best yield for 100 USDC and execute the deposit")

## Related Concepts

- [[tool-calling]] — the base mechanism; Web3 tool use is a domain application
- [[mcp]] — the protocol for exposing Web3 tools to agents
- [[chain-aware-context]] — Web3 tool calls populate chain-aware context
- [[agent-wallet]] — the wallet is the tool that signs and submits transactions
- [[guardrails]] — especially important for irreversible Web3 tool calls
- [[verification-chain]] — simulation and human check are mandatory before Web3 execution

## Sources

- [[sources/aixweb3-school]] — Web3 tool use as AI × Web3 Bridge topic
