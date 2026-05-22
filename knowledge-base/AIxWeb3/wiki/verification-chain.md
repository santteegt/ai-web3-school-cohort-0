---
title: "Verification Chain"
type: concept
tags: [ai-foundations, prompt, security]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

The verification chain is a multi-layer system design pattern where each step in the pipeline adds a check before an action is taken. A prompt alone is insufficient security; the complete chain distributes responsibility across prompt, context, model output, code validation, simulation, and human review.

## Key Points

The six-step chain:
1. **Prompt** — defines task and output format (soft constraint)
2. **Context** — provides trusted data and explicit source boundaries
3. **Model** — generates explanation or candidate action
4. **Code** — verifies schema and business rules (hard constraint)
5. **Guard / Simulation** — checks on-chain impact before execution
6. **Human check** — confirms high-risk or irreversible actions

- "A prompt alone should not bear the burden of security" — each layer catches failure modes that earlier layers miss
- High-risk actions (database writes, payments, contract calls, signing) require all six layers — skipping any layer creates exploitable gaps
- In AI × Web3, the guard/simulation step is especially important: simulating a transaction before signing prevents irreversible losses
- The chain is not sequential in practice — some layers run in parallel (e.g. schema validation + human confirmation prompt happen simultaneously)

## Related Concepts

- [[prompt-design]] — layer 1 of the chain
- [[context-engineering]] — layer 2 of the chain
- [[structured-output]] — enables layer 4 (code validation requires structured output to parse)
- [[guardrails]] — the guard layer (step 5)
- [[hallucination]] — the verification chain is the primary defense against hallucination-driven actions
- [[prompt-injection]] — the chain limits injection damage even when the prompt layer is bypassed

## Sources

- [[sources/prompt]] — six-step verification chain definition
- [[sources/ai-fundamentals-introduction]] — validation as mandatory for AI output in agent contexts
