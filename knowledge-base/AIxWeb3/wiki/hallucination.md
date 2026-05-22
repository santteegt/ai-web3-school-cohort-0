---
title: "Hallucination"
type: concept
tags: [ai-foundations, llm, rag]
source_count: 3
date_updated: "2026-05-22"
---

## Definition

Hallucination is the phenomenon where a language model generates factually incorrect, fabricated, or unsupported output with high confidence, presenting invented information as if it were real. It is a structural consequence of how LLMs work — they predict plausible token sequences, not factually verified ones.

## Key Points

- Models **fabricate information with full confidence** — the model's tone gives no signal about accuracy
- Hallucination is especially dangerous with: references (invented URLs, paper titles), code (plausible but broken logic), facts (invented statistics, events), and on-chain data (fabricated addresses, transaction results)
- **Do not handle hallucination only by writing better prompts** — connect output to external verification: source citations, schema validation, rule checks, human confirmation, and audit logs
- RAG does not eliminate hallucination — "RAG without citation and freshness only moves hallucination from inside the model into the retrieval system"
- In longer contexts, **reasoning drift** can occur: the logical chain quietly breaks down over many steps and conclusions diverge from original premises
- In agents, hallucination manifests as **tool misuse** (wrong tool called, wrong parameters) and **execution overreach** (acting beyond authorized scope)

## Related Concepts

- [[large-language-model]] — hallucination is structural to LLM generation
- [[retrieval-augmented-generation]] — reduces hallucination but doesn't eliminate it if citations are missing
- [[citations]] — the user-facing mechanism for verifying RAG-sourced claims
- [[guardrails]] — system-level defense against hallucinated actions
- [[structured-output]] — reduces hallucination impact by binding output to schemas
- [[prompt-injection]] — can trigger intentional hallucination-like behavior via adversarial inputs
- [[verification-chain]] — the full defensive chain: prompt → context → model → code → guard → human

## Sources

- [[sources/llms]] — hallucination as a fundamental LLM property; external verification approach
- [[sources/rag]] — RAG's false promise without citations
- [[sources/ai-fundamentals-introduction]] — hallucination in agent contexts (tool misuse, execution overreach)
