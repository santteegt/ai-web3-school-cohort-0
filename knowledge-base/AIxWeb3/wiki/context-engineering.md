---
title: "Context Engineering"
type: concept
tags: [ai-foundations, context]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Context engineering is the discipline of designing how information enters a model — deciding what sources to include, how to order and label them, how to isolate untrusted content, and what must be re-queried every time. Its goal is to ensure the model works at the right information layer.

## Key Points

- Context engineering decisions: choose data sources, order/trim/label sources, isolate untrusted content, decide which information must be re-queried every time
- A stable tool-using agent context should include: current task state, tool return values, relevant logs/evidence, trusted data sources, external check results, the user's original intent, system prohibitions, and output schema
- The failure modes of bad context engineering: treating an untrusted webpage as a system instruction, using stale docs as current rules, treating a user wish as fact, leaking previous task state into the next task
- **Context must be refreshable**: prices, permissions, versions, and task progress cannot be cached long-term as if still current
- Context is an **information governance** problem — every piece of input must be labeled by source, freshness, permission level, and trust level

## Related Concepts

- [[context-window]] — the budget that context engineering must fit within
- [[five-layer-agent-context]] — the five-layer model that context engineering must populate correctly
- [[information-governance]] — the broader framing: source, freshness, permission, trust labeling
- [[agent-memory]] — one layer of context that requires special governance (revocability)
- [[knowledge-base]] — the external repository that context engineering retrieves from
- [[prompt-injection]] — the attack that exploits poor context zone separation
- [[retrieval-augmented-generation]] — a technique for dynamically populating context with relevant knowledge

## Sources

- [[sources/context]] — full definition and components of context engineering
