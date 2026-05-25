---
title: "Consensus"
type: concept
tags: [web3-foundations, network]
source_count: 1
date_updated: "2026-05-25"
---

# Consensus

## Definition

Consensus is the mechanism by which distributed blockchain nodes agree on the canonical state of the chain — which transactions happened, in which order, and what the current state is. Without consensus, each node could have a different view of "what happened," making trustless coordination impossible.

## Key Points

- **Proof of Work (PoW)**: nodes race to solve a cryptographic puzzle; winner adds the next block; energy-intensive; Ethereum abandoned this in 2022 ("The Merge")
- **Proof of Stake (PoS)**: validators stake ETH as collateral; randomly selected to propose blocks; slashed for misbehavior; energy-efficient
- **Finality**: PoS provides economic finality — reversing a finalized block requires burning at least 1/3 of staked ETH
- **Byzantine Fault Tolerance**: consensus protocols tolerate up to a threshold of malicious nodes
- **L2 consensus**: L2 rollups typically have a sequencer (centralized or decentralized) for ordering; post validity proofs to L1 for ultimate security
- **Consensus ≠ agreement among users**: consensus is a technical protocol; governance is a separate social process

## Related Concepts

- [[proof-of-stake]] — Ethereum's current consensus mechanism
- [[block]] — the output of consensus
- [[blockchain-network]] — the network that consensus secures
- [[rollup]] — inherits L1 consensus security for L2 transactions
- [[layer-2]] — extends L1 consensus guarantees

## Sources

- [[sources/web3-chapters]] — Chapter: Network
