---
title: "Contract Upgrade"
type: concept
tags: [web3-foundations, smart-contracts, security]
source_count: 1
date_updated: "2026-05-25"
---

# Contract Upgrade

## Definition

Contract upgrade refers to patterns that allow replacing the logic of a deployed smart contract while preserving its address, state, and stored data. Since EVM bytecode is immutable once deployed, upgradeability requires a proxy architecture: a stable proxy contract delegates calls to a separate logic (implementation) contract that can be replaced.

## Key Points

- **Why needed**: bugs in immutable contracts can lock or drain funds; upgrade patterns allow patching without migration
- **Transparent proxy**: admin can change implementation; users cannot call admin functions; separated access
- **UUPS (Universal Upgradeable Proxy Standard)**: upgrade logic lives in the implementation; more gas-efficient
- **Beacon proxy**: many proxies share one beacon pointing to the implementation; update beacon = update all
- **Storage collision risk**: implementation contracts must not overwrite proxy storage slots; use EIP-1967 slots
- **OpenZeppelin Upgrades plugin**: tooling to safely deploy and upgrade proxies
- **Tradeoff**: upgradeability requires trust in the admin/owner; truly immutable contracts are more trustless

## Related Concepts

- [[smart-contract]] — the base artifact being upgraded
- [[solidity]] — proxy and implementation contracts written in Solidity
- [[openzeppelin]] — provides OpenZeppelin Upgrades library and UUPS base contracts
- [[evm]] — proxy relies on `delegatecall` opcode
- [[web3-security]] — admin key compromise = full contract takeover
- [[access-control]] — upgrade authority must be tightly controlled

## Sources

- [[sources/web3-chapters]] — Chapter: Smart Contract
