---
title: "AA Wallet (Account Abstraction Wallet)"
type: concept
tags: [web3-foundations, aixweb3-bridge, account-abstraction, wallet-permission]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An AA Wallet is a wallet design based on Account Abstraction that gives accounts flexible rules beyond "one private key controls one account." The focus is not on changing the wallet interface but on giving the account itself programmable logic: signatures, permissions, gas payments, recovery, multi-sig, limits, and session keys.

## Key Points

- Traditional EOA: one private key = one account; AA Wallet: account can express rules
- Key rules for agents: who can operate, what can be operated, when it expires, what to do if boundaries are exceeded
- The value for agents is not that "the wallet is more advanced" but that the account can finally express checkable rules
- Foundation for [[smart-account]], [[session-key]], and [[policy]]

## Related Concepts

- [[smart-account]]
- [[erc-4337]]
- [[erc-7702]]
- [[session-key]]
- [[agent-wallet]]
- [[paymaster]]
- [[bundler]]

## Sources

- [[sources/bridge-chapters]]
