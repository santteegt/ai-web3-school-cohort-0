---
title: "DeFi Lending"
type: concept
tags: [web3-foundations, defi]
source_count: 1
date_updated: "2026-05-25"
---

# DeFi Lending

## Definition

DeFi lending protocols enable permissionless borrowing and lending of crypto assets, governed entirely by smart contracts. Lenders deposit assets to earn yield; borrowers put up collateral and take out loans. All positions are over-collateralized (collateral > loan value) to account for price volatility. Major protocols: Aave, Compound.

## Key Points

- **Over-collateralization**: borrowers must deposit more value than they borrow (e.g., 150% collateral ratio) — no credit scoring required
- **Liquidation**: if collateral value falls below a threshold (health factor < 1), anyone can liquidate the position — repay the debt and claim the collateral at a discount
- **Interest rates**: algorithmically set based on pool utilization; higher utilization → higher borrowing rate → incentivizes more deposits
- **aTokens / cTokens**: interest-bearing receipt tokens; depositing USDC to Aave gives you aUSDC that appreciates in value
- **Flash loans**: borrow any amount without collateral if repaid in the same transaction; used for arbitrage, liquidations, and exploits
- **Oracle dependency**: prices used for collateral valuation come from oracles; oracle manipulation = liquidation cascade risk
- **AI × Web3**: agents can monitor positions, rebalance collateral, and execute liquidations autonomously

## Related Concepts

- [[defi]] — lending is a core DeFi vertical
- [[erc20-token]] — the assets borrowed and lent
- [[oracle]] — price feeds for collateral valuation
- [[oracle-risk]] — manipulation risk for lending protocols
- [[liquidity]] — pool liquidity determines rates and availability
- [[smart-contract]] — lending protocols are entirely contract-governed
- [[web3-security]] — smart contract bugs (e.g., Compound comptroller bug) can drain pools

## Sources

- [[sources/web3-chapters]] — Chapter: DeFi
