---
title: "Evaluator"
type: concept
tags: [aixweb3-bridge, payment-commerce, evaluation]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Evaluator is a role or system that judges whether delivery is qualified. Evaluators themselves need to be evaluated — an evaluator with a high error rate turns escrow into random judgment.

## Key Points

- Types: scripts, test suites, models, human reviewers, multiple validators, or on-chain contracts
- AI evaluators are suitable for preliminary judgment; high-value tasks need re-reviewable evidence and challenge mechanisms
- System should record evaluator versions, inputs, outputs, error rates, and historical dispute results
- Recommended combination for code/data/report tasks: scripts check format → test suites check functionality → AI checks semantics → humans handle disputes
- Do not press all responsibility onto one model

## Related Concepts

- [[settlement-and-escrow]]
- [[acceptance]]
- [[dispute]]
- [[ai-oracle]]
- [[validation]]
- [[evaluation]]
- [[erc-8183]]

## Sources

- [[sources/bridge-chapters]]
