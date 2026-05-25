---
title: "AI × Web3 Agent Architecture"
type: concept
tags: [aixweb3-bridge, agent, web3-foundations]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

The AI × Web3 agent architecture is an 8-step reference pattern for how a relatively stable AI × Web3 agent should operate — from receiving a user goal to recording the final on-chain execution, with explicit checkpoints for policy, simulation, and human confirmation.

## Key Points

The 8-step pattern:
1. **User provides goal and constraints** — scoped, not vague
2. **Agent reads context and generates a plan** — candidate route, not authorization
3. **System splits plan into read-only steps and candidate write steps** — the critical safety gate
4. **Read-only tools run automatically** — RPC queries, balance checks, price lookups
5. **Write tools enter policy checks** — permission validation, spending limit enforcement
6. **Simulation shows on-chain impact** — before any signing, model the transaction outcome
7. **User confirms high-risk actions** — irreversible actions require explicit consent
8. **Wallet/Smart Account executes; logs record each step and final state** — full auditability

- Step 3 (splitting read/write) is the most important architectural decision — most security failures come from skipping or collapsing this step
- Steps 6 and 7 (simulation + human confirmation) are the AI × Web3-specific additions to the general agent verification chain
- Step 8 (logging) closes the audit loop — without it, responsibility attribution is impossible

## Related Concepts

- [[agent-planning]] — step 2 produces the plan that step 3 splits
- [[web3-tool-use]] — steps 4–5 are tool calls
- [[verification-chain]] — this architecture extends the general verification chain for on-chain context
- [[agent-wallet]] — step 7 is the wallet's authorization point
- [[chain-aware-context]] — step 2 reads on-chain context to inform the plan
- [[guardrails]] — policy checks in step 5 are implemented as guardrails
- [[ai-agent-tracing]] — step 8 logging produces the trace

## Sources

- [[sources/agent]] — 8-step AI × Web3 agent architecture
