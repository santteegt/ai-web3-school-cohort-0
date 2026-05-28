---
title: "Agent Trust & Reputation"
type: concept
tags: [aixweb3-bridge, identity-reputation, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Agent Trust & Reputation solves how users and other agents judge whether an agent is reliable, whether its history is authentic, and whether there is a cost for failure when it claims to complete a task. Trust is not a single score but a set of traceable, comparable, and interpretable evidence.

## Key Points

- Credibility comes from verifiable behavior, not self-declaration
- Reputation must be bound to identity — without stable identity, records cannot accumulate
- Evaluations must be bound to tasks — generic five-star ratings are less useful than specific task records
- Penalties must be real — commitments without cost are easily abused
- Reputation by task type: an agent good at summarizing governance proposals is not necessarily good at contract tests
- Time decay matters — good performance two years ago may not represent current service quality after model/owner changes

## Sub-Concepts

- [[reputation]] — collection of historical performance signals (success rate, dispute rate, task type breakdown)
- [[review]] — task-bound feedback with deliverable hash and evaluator identity
- [[attestation]] — verifiable claim with issuer, subject, claim, evidence, expiration, revocation
- [[stake]] — economic guarantee; viewed alongside validation and task history
- [[slashing]] — collateral confiscation for verifiable defaults (timeout, forged signatures, contradictory results)
- [[validation]] — capability or task result verification recorded with test data and validator
- [[erc-8004]] — draft standard for agent identity, reputation, and verification registry

## Position in AI × Web3

Agent Trust & Reputation connects [[agent-identity]], [[settlement-and-escrow]], and [[machine-payment]]. Without a trust layer, agents cannot safely delegate to each other; without reputation, users cannot judge which agent is worth paying.

## Related Concepts

- [[agent-identity]]
- [[settlement-and-escrow]]
- [[machine-payment]]
- [[identity-reputation-capability]]
- [[erc-8004]]
- [[attestation]]
- [[ai-oracle]]

## Sources

- [[sources/bridge-chapters]]
