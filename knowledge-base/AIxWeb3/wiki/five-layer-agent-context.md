---
title: "Five-Layer Agent Context"
type: concept
tags: [ai-foundations, context, agent]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

The five-layer agent context model is a structured framework for organizing the information a reliable agent context must contain. Each layer has a distinct source, trust level, and refresh rate — mixing them causes security and reliability failures.

## Key Points

The five layers, from highest to lowest trust:

1. **Instruction layer** — system rules, tool-use rules, prohibitions (set by the developer; highest trust)
2. **Task layer** — user goal and current session parameters (set per session)
3. **Fact layer** — on-chain state, tool results, simulation outputs (verifiable, current, from external systems)
4. **Knowledge layer** — documents, standards, forums, historical cases (from [[knowledge-base]]; requires freshness tracking)
5. **Memory layer** — user preferences and project configuration (from [[agent-memory]]; requires revocability)

- **The clearer the layers, the easier permission control, Prompt Injection defense, and auditing become**
- Common failure: content from the knowledge or memory layer being mistaken for instruction-layer authority
- Fact layer content (tool results, on-chain state) must be treated as current, not cached

## Related Concepts

- [[context-engineering]] — the practice of correctly populating all five layers
- [[context-window]] — the budget that all five layers must fit within
- [[agent-memory]] — the fifth layer; requires revocability
- [[knowledge-base]] — the fourth layer; requires freshness tracking
- [[prompt-injection]] — exploits failures in layer separation (untrusted content treated as instructions)
- [[information-governance]] — the framework for managing layers correctly
- [[ai-agent]] — agents that use this layered context model

## Sources

- [[sources/context]] — five-layer model definition and layer descriptions
