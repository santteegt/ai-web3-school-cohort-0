---
title: "Chain-aware Context"
type: concept
tags: [aixweb3-bridge, context, web3-foundations]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Chain-aware context is the practice of incorporating live on-chain state — wallet balances, contract storage, recent transactions, governance votes, oracle prices — into an agent's context so that its reasoning is grounded in current blockchain reality rather than stale or fabricated data.

## Key Points

- On-chain state is the "fact layer" of agent context in Web3 settings — it should be fetched fresh at query time, not cached long-term
- Chain-aware context requires [[retrieval-augmented-generation]] applied to blockchain data: RPC queries, indexer lookups, and event log retrieval
- Key challenge: on-chain data is voluminous and constantly changing — [[context-engineering]] decisions (what to fetch, when to refresh, what to summarize) are critical
- Any agent action based on chain-aware context (e.g. "user has enough USDC for this transaction") must be re-verified at execution time, not just at context-building time
- Connects to [[web3-tool-use]]: agents retrieve chain state via RPC calls, indexer APIs, and oracle feeds

## Related Concepts

- [[context-engineering]] — chain-aware context is a specialized form of context engineering
- [[retrieval-augmented-generation]] — on-chain data is retrieved and injected as evidence
- [[five-layer-agent-context]] — on-chain state populates the fact layer
- [[web3-tool-use]] — the tools used to fetch on-chain data
- [[agent-wallet]] — wallet balance and permission state is a critical chain-aware context element
- [[information-governance]] — on-chain data has high trust but must be timestamped

## Sources

- [[sources/aixweb3-school]] — chain-aware context as AI × Web3 Bridge topic
