---
title: "Agent Reflection"
type: concept
tags: [ai-foundations, agent]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

Agent reflection is a process where an agent reviews its own intermediate results — failure reasons, logs, tool outputs — and uses that review to correct the next step. It is a quality-improvement mechanism, not a safety mechanism.

## Key Points

- Reflection improves the quality of complex tasks by enabling self-correction within a task
- **"Self-checking can improve quality; deterministic checking is what can carry risk."** — reflection is not a substitute for code-enforced guardrails
- Reflection can only assist in diagnosis; it cannot be the final safety judgment because the model checking its own output is still subject to the same hallucination and reasoning-drift failures
- Useful reflection inputs: tool call failures, schema validation errors, partial results, intermediate state values that don't match expectations
- In multi-agent systems, reflection within one agent does not substitute for verification of handoff results — the receiving agent cannot trust that the sending agent reflected correctly

## Related Concepts

- [[ai-agent]] — reflection is an agent capability
- [[guardrails]] — code-enforced validation is separate from and more reliable than model-level reflection
- [[agent-planning]] — reflection can trigger plan revision
- [[state-management]] — reflection reads from agent state (logs, tool returns, error records)
- [[ai-agent-tracing]] — reflection decisions should be logged in traces for auditability
- [[hallucination]] — models can hallucinate during reflection (confidently misdiagnose a failure reason)

## Sources

- [[sources/agent]] — reflection definition and its relationship to deterministic safety checks
