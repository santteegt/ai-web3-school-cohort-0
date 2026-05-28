---
title: "Contract Write"
type: concept
tags: [web3-foundations, aixweb3-bridge, tool-use]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Contract Write changes on-chain state and must undergo stricter simulation, permission, and confirmation than reads. Agents should not directly possess "arbitrary contract writing" capabilities — writing tools should be restricted to whitelisted contracts, whitelisted methods, and amount policies.

## Key Points

- Required pre-write checks: chain ID, contract address, ABI method+args, value estimation, gas estimation, simulation results, policy checks, user/smart-account authorization
- After execution: transaction hash and receipt tracking required
- Best practice: restrict to whitelisted contracts, whitelisted methods, and amount policies
- Categorized as Advanced difficulty — highest risk Web3 tool

## Related Concepts

- [[web3-tool-use]]
- [[contract-read]]
- [[wallet-tool]]
- [[simulation]]
- [[guard]]
- [[policy]]
- [[tool-permission]]
- [[agent-wallet]]

## Sources

- [[sources/bridge-chapters]]
