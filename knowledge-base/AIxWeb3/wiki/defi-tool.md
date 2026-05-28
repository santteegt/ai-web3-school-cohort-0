---
title: "DeFi Tool"
type: concept
tags: [web3-foundations, aixweb3-bridge, tool-use, defi]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

DeFi Tools encapsulate capabilities like swap, lending, authorization, position query, and liquidation risk for agents. They directly affect assets and require the strictest tool design constraints of any Web3 tool category.

## Key Points

- Required constraints: protocol whitelist, maximum transaction amount, maximum slippage, price source, simulation, allowance check, manual confirmation or session key policy
- Do not give an agent a general tool to "help me call any DeFi protocol"
- Categorized as Advanced difficulty — directly affects user assets
- Even approval is a high-risk action and cannot be mixed with ordinary payments

## Related Concepts

- [[web3-tool-use]]
- [[contract-write]]
- [[defi]]
- [[simulation]]
- [[guard]]
- [[policy]]
- [[tool-permission]]
- [[stablecoin-payment]]

## Sources

- [[sources/bridge-chapters]]
