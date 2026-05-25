---
title: "AMM (Automated Market Maker)"
type: concept
tags: [web3-foundations, defi]
source_count: 1
date_updated: "2026-05-25"
---

# AMM (Automated Market Maker)

## Definition

An Automated Market Maker (AMM) is a type of decentralized exchange (DEX) that uses liquidity pools and mathematical pricing formulas instead of traditional order books. Users trade against the pool; the price adjusts automatically based on the ratio of assets in the pool. Uniswap pioneered the `x * y = k` constant-product AMM.

## Key Points

- **Liquidity pool**: a smart contract holding two (or more) ERC-20 tokens; any user can trade against it
- **Constant product formula**: `x * y = k` — as one asset leaves the pool, the other must enter proportionally; price determined by ratio
- **Slippage**: large trades move the price; the difference between expected and executed price; higher for illiquid pools
- **MEV (Maximal Extractable Value)**: validators or searchers front-run or sandwich trades to profit; a structural property of public mempools
- **Impermanent Loss (IL)**: liquidity providers face IL when the price ratio of their deposited tokens changes; they're better off holding if no fees earned
- **Concentrated liquidity**: Uniswap v3 lets LPs focus liquidity in a price range → higher capital efficiency but active management needed
- **Stable swaps**: Curve uses a different formula optimized for stable pairs (USDC/USDT) — minimal slippage near peg

## Related Concepts

- [[defi]] — AMMs are the core trading primitive
- [[erc20-token]] — pools hold ERC-20 pairs
- [[liquidity]] — LPs supply liquidity to pools
- [[oracle]] — AMM prices can be used as on-chain price oracles (TWAP); also vulnerable to price manipulation
- [[gas]] — each swap is a transaction costing gas
- [[layer-2]] — L2 AMMs (Uniswap on Arbitrum) dramatically reduce swap costs

## Sources

- [[sources/web3-chapters]] — Chapter: DeFi
