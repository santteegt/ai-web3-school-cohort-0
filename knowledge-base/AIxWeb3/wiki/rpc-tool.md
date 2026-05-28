---
title: "RPC Tool"
type: concept
tags: [web3-foundations, aixweb3-bridge, tool-use]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

RPC Tools read chain state, query blocks, estimate gas, get logs, or broadcast transactions. Read-only RPC capabilities can be opened widely; writing capabilities must be split out into separate tools with different permissions.

## Key Points

- Tool returns should include: chain ID, RPC provider, block number, method, result, and error
- Read-only and write capabilities must be different tools — never mixed into an "all-purpose RPC" tool
- Return fields allow the agent's answer to state which block's data it is based on
- Read-only RPC is beginner-level risk; broadcast is advanced-level with full policy checks required

## Related Concepts

- [[web3-tool-use]]
- [[contract-read]]
- [[contract-write]]
- [[rpc]]
- [[on-chain-data]]
- [[tool-permission]]
- [[tool-log]]

## Sources

- [[sources/bridge-chapters]]
