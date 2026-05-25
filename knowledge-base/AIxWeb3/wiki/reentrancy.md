---
title: "Reentrancy"
type: concept
tags: [web3-foundations, security, smart-contracts]
source_count: 1
date_updated: "2026-05-25"
---

# Reentrancy

## Definition

Reentrancy is a smart contract vulnerability where an external contract call returns control to the caller before the calling contract has updated its internal state. The attacker's contract re-enters the vulnerable function in the callback, exploiting the stale state. The DAO hack (2016, $60M ETH) is the most famous reentrancy exploit.

## Key Points

- **The pattern**: `withdraw()` sends ETH before updating balance → attacker's fallback re-calls `withdraw()` → balance never decrements → drains contract
- **Checks-Effects-Interactions**: the canonical defense pattern — check conditions, update state (effects), then make external calls (interactions); never call external contracts before updating state
- **Cross-function reentrancy**: attacker re-enters a different function that reads the stale state, not necessarily the same one
- **Read-only reentrancy**: attacker re-enters a view function that's used as an oracle by another contract — corrupts price reads
- **`ReentrancyGuard`**: OpenZeppelin's `nonReentrant` modifier — sets a lock flag before execution, reverts if re-entered
- **Pull-over-push**: instead of pushing ETH to users, let them pull it; eliminates the external call during state-changing operations

## Related Concepts

- [[web3-security]] — reentrancy is the most studied vulnerability
- [[smart-contract]] — the vulnerable artifact
- [[openzeppelin]] — provides `ReentrancyGuard`
- [[access-control]] — unrelated but often paired as defense layers
- [[solidity]] — patterns in Solidity code cause or prevent reentrancy

## Sources

- [[sources/web3-chapters]] — Chapter: Security
