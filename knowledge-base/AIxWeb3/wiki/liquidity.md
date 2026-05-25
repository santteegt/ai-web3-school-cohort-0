---
title: "Liquidity"
type: concept
tags: [web3-foundations, defi]
source_count: 1
date_updated: "2026-05-25"
---

# Liquidity

## Definition

In DeFi, liquidity refers to the capital deposited into protocols (AMM pools, lending markets) that enables other users to trade, borrow, or perform other financial operations. Liquidity providers (LPs) earn fees in exchange for supplying this capital. Liquidity depth determines slippage: deeper pools = less price impact per trade.

## Key Points

- **Liquidity providers (LPs)**: users who deposit token pairs into AMM pools or assets into lending markets; earn a share of fees
- **Impermanent Loss (IL)**: LPs face IL when the price ratio of their deposited tokens diverges; pure holding may outperform providing liquidity in trending markets
- **TVL (Total Value Locked)**: common DeFi metric measuring total capital locked in a protocol; proxy for protocol health and usage
- **Liquidity mining**: protocols incentivize LPs with governance token rewards; inflated APYs attract capital but also mercenary LPs
- **Concentrated liquidity**: Uniswap v3 allows LPs to concentrate capital in a price range → higher fee capture but higher IL if price exits range
- **Liquidity fragmentation**: same trading pair spread across multiple protocols/chains; reduces depth on any individual venue
- **Bootstrap problem**: new protocols struggle to attract initial liquidity without high incentives

## Related Concepts

- [[amm]] — AMMs depend on LP-supplied liquidity
- [[defi-lending]] — lending markets require depositor liquidity
- [[defi]] — liquidity is the foundational resource
- [[erc20-token]] — LPs deposit token pairs
- [[layer-2]] — L2 liquidity is growing but still fragmented vs L1
- [[oracle]] — TWAP oracles use AMM liquidity pool prices

## Sources

- [[sources/web3-chapters]] — Chapter: DeFi
