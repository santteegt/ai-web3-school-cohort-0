---
title: "ERC-20 Token"
type: concept
tags: [web3-foundations, defi, smart-contracts]
source_count: 1
date_updated: "2026-05-25"
---

# ERC-20 Token

## Definition

ERC-20 is the Ethereum token standard defining a common interface for fungible tokens. Any contract implementing ERC-20's functions (`transfer`, `transferFrom`, `approve`, `allowance`, `balanceOf`, `totalSupply`) can be recognized and handled uniformly by wallets, DEXes, and other contracts — enabling composability.

## Key Points

- **Fungible**: all tokens of a contract are identical and interchangeable (vs ERC-721 NFTs)
- **`transfer(to, amount)`**: move tokens from caller's balance to `to`
- **`approve(spender, amount)`**: allow `spender` to withdraw up to `amount` from caller's balance
- **`transferFrom(from, to, amount)`**: pull tokens from `from` if approved; used by DEXes, lending protocols
- **ERC-20 `permit`**: EIP-2612 extension enabling gasless approval via signature (used in DeFi composable flows)
- **Approval risk**: unlimited approvals are dangerous; any bug in the approved contract can drain your balance
- **OpenZeppelin ERC-20**: the reference implementation; includes `_mint`, `_burn`, and optional hooks
- **Token economics**: supply, distribution, and governance rights vary by project

## Related Concepts

- [[defi]] — ERC-20 is the foundational asset in all DeFi
- [[amm]] — trades ERC-20 pairs in liquidity pools
- [[defi-lending]] — borrows/lends ERC-20 tokens against collateral
- [[openzeppelin]] — provides the reference ERC-20 implementation
- [[smart-contract]] — ERC-20 is a contract
- [[cryptographic-signature]] — ERC-2612 permit uses signature-based approvals
- [[paymaster]] — paymasters can accept ERC-20 gas payment

## Sources

- [[sources/web3-chapters]] — Chapter: DeFi
