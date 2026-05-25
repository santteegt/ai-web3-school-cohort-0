---
title: "Learning Agents"
type: concept
tags: [ai-foundations, agent, frameworks]
source_count: 2
date_updated: "2026-05-25"
---

## Definition

A learning agent is a system that improves from feedback, logs, evaluation results, or user corrections over time — not necessarily by retraining the model, but by updating prompts, adjusting retrievers, adding rules, or improving evaluation test sets through a structured evaluation loop.

## Key Points

- Learning does not require model retraining — prompt updates, retriever tuning, and rule additions are all forms of learning
- **"Learning ability should enter the evaluation loop first, then the production system"** — direct online behavior change from feedback introduces data pollution, unauthorized learning, and unexplained behavior changes
- The safe learning process: (1) record failure cases → (2) label causes manually or with rules → (3) add to eval/regression sets → (4) modify prompts/retrieval/tools/model config → (5) release only after tests pass
- The most common production mistake: turning online user feedback directly into behavior changes without going through the evaluation loop
- In AI × Web3: unauthorized learning from on-chain transaction feedback could silently change an agent's risk tolerance or permission assumptions — all learning must be explicit and auditable

## Related Concepts

- [[ai-frameworks-overview]] — learning agents are a framework-level capability
- [[agent-reflection]] — reflection is a session-level self-correction; learning agents update persistent system components
- [[ai-agent-tracing]] — traces and logs are the raw material for learning
- [[guardrails]] — learning systems must not bypass guardrails during the feedback incorporation process
- [[knowledge-base]] — retriever tuning updates the knowledge base; this is a form of learning
- [[evaluation]] — the structured eval pipeline is the gate all learning must pass through before production
- [[regression-testing]] — regression tests are the final check before a learning update is released
- [[golden-set]] — growing the golden set with observed failures is a core learning activity

## Sources

- [[sources/frameworks]] — learning agents definition and safe learning process
- [[sources/evaluation]] — evaluation loop as the safe path for agent improvement; regression and observability
