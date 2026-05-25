---
title: "Proof of Stake (PoS)"
type: concept
tags: [web3-foundations, network, consensus]
source_count: 1
date_updated: "2026-05-25"
---

# Proof of Stake (PoS)

## Definition

Proof of Stake is Ethereum's consensus mechanism (adopted at "The Merge" in September 2022). Validators lock up (stake) 32 ETH as collateral to participate in block proposal and attestation. Validators are pseudorandomly selected to propose blocks; the committee of attestors votes to finalize them. Misbehavior is punished by "slashing" — forcibly removing a portion of the staked ETH.

## Key Points

- **Validator**: requires 32 ETH stake; runs consensus + execution clients; earns staking rewards (~3–5% APY)
- **Slots and epochs**: one validator proposes per 12-second slot; 32 slots per epoch; finality after ~2 epochs
- **Slashing**: deliberate misbehavior (double voting, surround voting) → portion of stake is burned
- **Economic security**: attacking the chain requires staking and risking a majority of the ~$80B+ staked ETH
- **Vs Proof of Work**: PoS uses ~99.95% less energy than PoW; selection is by stake rather than computation
- **Liquid staking**: protocols like Lido, Rocket Pool let users stake < 32 ETH and receive liquid tokens (stETH, rETH)
- **Decentralization concern**: stake concentration risks; liquid staking dominance is a governance concern

## Related Concepts

- [[consensus]] — PoS is the consensus mechanism
- [[block]] — PoS validators produce and attest blocks
- [[blockchain-network]] — Ethereum's mainnet uses PoS
- [[layer-2]] — L2 sequencers may have their own staking/consensus
- [[defi]] — liquid staking is a major DeFi vertical

## Sources

- [[sources/web3-chapters]] — Chapter: Network
