---
title: "On-chain Data"
type: concept
tags: [web3-foundations, aixweb3-bridge, context]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

On-chain Data is data that can be directly verified on the chain: balances, transactions, logs, contract states, and block information. For an Agent reading on-chain data, a complete record must include chain ID, block number, contract address, method, return value, and read time.

## Key Points

- Common sources: RPCs, block explorers, indexers, and protocol APIs
- Without chain ID, block number, contract address, and read time, a model can confuse data from different chains, times, and contracts
- On-chain state is time-sensitive — balance, authorization, and position change with blocks
- Context must distinguish between facts and interpretations: tools return facts, models interpret

## Related Concepts

- [[chain-aware-context]]
- [[rpc-tool]]
- [[explorer-context]]
- [[indexing-context]]
- [[transaction-history]]
- [[contract-read]]

## Sources

- [[sources/bridge-chapters]]
