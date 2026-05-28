---
title: "Data Feed (AI Oracle)"
type: concept
tags: [aixweb3-bridge, verifiable-ai]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An AI Oracle can manifest as a data feed, continuously providing model-processed data: address risk scores, content moderation labels, transaction intent classifications, market sentiment indices. Unlike price feeds, AI data feeds are more prone to drift.

## Key Points

- AI feeds can drift due to: model upgrades, training data changes, prompt adjustments, input source variations
- Feeds should specify model versions and allow historical queries
- Contracts using feeds for automatic execution must check: stale data, abnormal jumps, and source signatures
- Expired AI scores should not continue affecting liquidations, fund releases, or user bans

## Related Concepts

- [[ai-oracle]]
- [[ai-output]]
- [[model-result]]
- [[oracle-risk]]
- [[oracle]]
- [[price-feed]]

## Sources

- [[sources/bridge-chapters]]
