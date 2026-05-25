---
title: "Access Control"
type: concept
tags: [web3-foundations, security, smart-contracts]
source_count: 1
date_updated: "2026-05-25"
---

# Access Control

## Definition

Access control in smart contracts refers to the mechanisms that restrict which addresses can call sensitive functions (admin functions, fund transfers, contract upgrades). Without proper access control, anyone can call privileged functions — a critical vulnerability. OpenZeppelin's `Ownable` and `AccessControl` are the standard implementations.

## Key Points

- **`Ownable`**: single owner pattern; `onlyOwner` modifier protects admin functions; simple but centralized — one key = full control
- **`AccessControl`**: role-based; define roles (MINTER_ROLE, ADMIN_ROLE, UPGRADER_ROLE) and grant them independently; multiple signers per role; more flexible and decentralized
- **Admin key compromise**: if the owner/admin private key is leaked, all protected functions are accessible to the attacker — upgrades, fund drains, parameter changes
- **Multisig for admin**: use a Safe multisig as the contract owner → requires M-of-N signers for any admin action; standard practice for production contracts
- **Timelock**: admin actions go through a time-delay queue; gives users time to exit if they disagree with upcoming changes
- **Missing access control**: one of the most common audit findings; functions that should be admin-only but lack modifiers
- **Function visibility**: `private` and `internal` don't appear in the ABI; `external` and `public` are callable by anyone unless protected

## Related Concepts

- [[web3-security]] — access control failures are a major vulnerability class
- [[smart-contract]] — where access control patterns are implemented
- [[openzeppelin]] — provides `Ownable` and `AccessControl`
- [[contract-upgrade]] — upgrade authority requires strict access control
- [[reentrancy]] — often paired with access control as defense layers
- [[smart-account]] — smart accounts can enforce multi-signature access control
- [[agent-wallet]] — access control on agent-controlled contracts

## Sources

- [[sources/web3-chapters]] — Chapter: Security
