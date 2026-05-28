---
title: "Chain-aware Context"
type: concept
tags: [aixweb3-bridge, context, web3-foundations]
source_count: 2
date_updated: "2026-05-28"
---

## Definition

Chain-aware Context refers to ensuring that an AI can see the correct chain, address, contract, transaction, event, balance, authorization, and data source before answering or acting — rather than guessing on-chain state from a single user statement. Models cannot judge on-chain facts based on linguistic memory; on-chain facts must be read from tools and indexing layers.

## Key Points

- On-chain state is time-sensitive: balance, authorization, and position change with blocks
- Context must have sources: contract addresses, block numbers, transaction hashes, and explorer links must be traceable
- Context must distinguish between facts and interpretations: tools return facts, models interpret
- Any agent action based on chain-aware context must be re-verified at execution time, not just context-building time
- A complete chain-aware context package includes: user goals, chain ID, user address and balance, relevant contract addresses/ABIs/docs, recent transactions and authorizations, indexing data update time, citations for every key conclusion

## Sub-Concepts

- [[on-chain-data]] — balances, transactions, logs, contract states, block info with chain ID + block number
- [[contract-docs]] — ABI + documentation + NatSpec to fill semantic gaps beyond function signatures
- [[transaction-history]] — past user/contract behavior with hash-level evidence
- [[explorer-context]] — verifiable evidence from block explorers with clickable links
- [[indexing-context]] — product-oriented queryable on-chain events (The Graph, custom indexers)
- [[citations]] — on-chain interpretations must lead back to transaction hashes, block numbers, or explorer links

## Related Concepts

- [[context-engineering]] — chain-aware context is a specialized form of context engineering
- [[retrieval-augmented-generation]] — on-chain data is retrieved and injected as evidence
- [[five-layer-agent-context]] — on-chain state populates the fact layer
- [[web3-tool-use]] — the tools used to fetch on-chain data
- [[agent-wallet]] — wallet balance and permission state is a critical chain-aware context element
- [[information-governance]] — on-chain data has high trust but must be timestamped
- [[malicious-context]] — contract docs and web content can contain attack instructions

## Sources

- [[sources/aixweb3-school]] — chain-aware context as AI × Web3 Bridge topic
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
