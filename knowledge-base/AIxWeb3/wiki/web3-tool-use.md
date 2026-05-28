---
title: "Web3 Tool Use"
type: concept
tags: [aixweb3-bridge, agent, web3-foundations]
source_count: 2
date_updated: "2026-05-28"
---

## Definition

Web3 Tool Use is the process of turning RPC, contract reads, transaction generation, wallet confirmation, block explorers, and DeFi operations into tools callable by agents. What is truly difficult is not "being able to call" but permissions, parameters, simulation, and logs. Core principle: models can choose tools, but tools must use deterministic boundaries to limit the model.

## Key Points

- Read-write separation: reading on-chain state and sending transactions must be different tools with different permissions
- Structured parameters: chain ID, contract address, method, args, value, and slippage cannot be buried in natural language
- Logs cannot be omitted: every tool call must record inputs, outputs, time, source, and errors
- Web3 tools are higher-stakes than typical API tools — irreversible and with financial consequences

## Sub-Concepts

- [[rpc-tool]] — chain state queries, gas estimation, broadcast (read-only vs. write separation critical)
- [[contract-read]] — view/pure functions, balances, allowances; low-risk but can mislead
- [[contract-write]] — state-changing calls; requires simulation + policy + confirmation + receipt tracking
- [[wallet-tool]] — most sensitive boundary; sign/send/authorize must be separate actions
- [[explorer-tool]] — verifiable evidence: transaction success, source code, events, token transfers
- [[defi-tool]] — swap/lending/positions with protocol whitelist, slippage limits, simulation required
- [[tool-permission]] — layered rules: auto-allowed → session-key → manual → prohibited
- [[tool-log]] — full audit record per tool call: goal, inputs, output, error, chain ID, confirmer

## Related Concepts

- [[tool-calling]] — the base mechanism; Web3 tool use is a domain application
- [[mcp]] — the protocol for exposing Web3 tools to agents
- [[chain-aware-context]] — Web3 tool calls populate chain-aware context
- [[agent-wallet]] — the wallet is the tool that signs and submits transactions
- [[guardrails]] — especially important for irreversible Web3 tool calls
- [[verification-chain]] — simulation and human check are mandatory before Web3 execution

## Sources

- [[sources/aixweb3-school]] — Web3 tool use as AI × Web3 Bridge topic
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
