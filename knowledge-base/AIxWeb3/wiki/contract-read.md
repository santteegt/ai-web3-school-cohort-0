---
title: "Contract Read"
type: concept
tags: [web3-foundations, aixweb3-bridge, tool-use]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Contract Read calls contract view/pure functions that do not change on-chain state. It is the most commonly used and relatively low-risk Web3 tool for agents — used to read balances, configuration, allowances, pool status, price parameters, nonces, and pause state.

## Key Points

- Does not change on-chain state; no user confirmation needed
- Can still mislead: wrong network, wrong contract address, ABI mismatch, or lagging RPC data can produce incorrect facts
- Suitable reads: balances, allowance, owner, pool TVL, configuration, whether paused
- Agent answers derived from contract reads should cite the block number and contract address

## Related Concepts

- [[web3-tool-use]]
- [[rpc-tool]]
- [[contract-write]]
- [[abi]]
- [[on-chain-data]]
- [[tool-permission]]

## Sources

- [[sources/bridge-chapters]]
