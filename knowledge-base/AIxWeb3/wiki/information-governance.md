---
title: "Information Governance"
type: concept
tags: [ai-foundations, context, security]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Information governance in AI systems is the practice of labeling every piece of context by its source, freshness, permission level, and trust level — ensuring the model processes the right information at the right authority level. It is the discipline that prevents context-based failures like treating untrusted web content as system instructions.

## Key Points

- Every input to the model must be classified: who produced it, how fresh it is, what permission level it carries, and how trusted the source is
- **Trusted sources must be explicitly marked** — system state, user input, retrieved documents, and tool results belong in separate zones
- **Context must be refreshable** — state, config, permissions, prices, and task progress cannot be cached long-term as if current
- **Memory must be revocable** — historical context must not become hidden permanent permissions
- Without information governance, models will blend "what the user said," "what a webpage wrote," "what the chain returned," and "what the system requires" — treating all with equal authority
- The five-layer model is the practical implementation of information governance for agents

## Related Concepts

- [[five-layer-agent-context]] — the operational model for information governance in agents
- [[context-engineering]] — the design practice that implements information governance
- [[prompt-injection]] — the attack that exploits information governance failures
- [[agent-memory]] — memory governance: revocability and authorization re-binding
- [[knowledge-base]] — knowledge governance: source, version, deprecation tracking

## Sources

- [[sources/context]] — information governance framing of the context problem
