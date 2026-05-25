---
title: "Oracle Risk"
type: concept
tags: [web3-foundations, oracle, security]
source_count: 1
date_updated: "2026-05-25"
---

# Oracle Risk

## Definition

Oracle risk refers to the vulnerabilities and attack vectors arising from a smart contract's dependence on off-chain data. Since oracle data is externally sourced, it can be manipulated, delayed, or wrong — and any downstream contract that acts on incorrect data inherits that error. Oracle attacks are among the most lucrative in DeFi history.

## Key Points

- **Price manipulation**: an attacker exploits low-liquidity TWAP oracles via flash loans → temporarily distort pool price → trigger liquidations or drain protocols at artificial prices
- **Stale price**: oracle stops updating (network congestion, node failure); contracts use outdated prices → incorrect liquidations
- **Centralization**: single-node or single-provider oracles are single points of failure and censorship
- **Front-running**: knowing an oracle update before it lands on-chain allows profitable trades (MEV)
- **AI Oracle risk**: if an AI model's output is published on-chain as an oracle, manipulating the model's input or the publication mechanism corrupts all downstream contracts
- **Mitigation**: use decentralized oracle networks (Chainlink DON), TWAP over sufficient windows, validate freshness timestamps, multi-oracle aggregation

## Related Concepts

- [[oracle]] — the system being attacked
- [[price-feed]] — the primary attack surface
- [[ai-oracle]] — extends oracle risk to AI outputs
- [[defi-lending]] — most impacted by oracle attacks
- [[web3-security]] — oracle attacks are a major security category
- [[verifiable-ai]] — on-chain AI output verification helps mitigate AI oracle risk

## Sources

- [[sources/web3-chapters]] — Chapter: Oracle
