---
title: "Guardrails"
type: concept
tags: [ai-foundations, agent, security]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Guardrails are input/output validation rules in an agent system that halt execution if a rule is violated — preventing the agent from taking unauthorized, unsafe, or out-of-scope actions regardless of what the model decides.

## Key Points

- "Execution halts if violated" — guardrails are hard stops, not soft hints; they are code-enforced, not prompt-enforced
- Guardrails operate independently of the model: even if the model decides to take a risky action, the guardrail layer vetoes it before execution
- Types: input guardrails (filter or reject malicious inputs), output guardrails (validate action parameters), execution guardrails (check permissions before tool calls)
- Guardrails are part of the [[verification-chain]] — they sit at step 5 (guard/simulation), after the model generates a candidate action
- Human-in-the-loop checkpoints are a form of guardrail for high-stakes or irreversible actions
- In AI × Web3: a guardrail might enforce that an agent can only send up to $100 USDC per transaction, regardless of what instruction the model received

## Related Concepts

- [[ai-agent]] — agents require guardrails as a core safety component
- [[verification-chain]] — guardrails are step 5 (guard/simulation check)
- [[prompt-injection]] — guardrails are the last line of defense if injection bypasses the prompt
- [[agent-handoff]] — control transfers only after guardrails pass
- [[agent-wallet]] — agent wallet permissions are implemented in part via guardrails
- [[structured-output]] — guardrails validate structured output schemas

## Sources

- [[sources/ai-fundamentals-introduction]] — guardrails as core agent component; execution halts on violation
