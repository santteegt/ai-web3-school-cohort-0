---
title: "LLMs"
type: source
tags: [ai-foundations, llm, tokens, embeddings, transformer, hallucination]
source_file: "raw/LLMs.md"
source_hash: "sha256:f8330999ce2f6be8e018ad93274c3e8b74f076ddabd8de599592c9afb8336a7f"
date_ingested: "2026-05-22"
---

## Summary

This source builds the core mental model for how LLMs work at a technical level: token handling, embeddings, transformer architecture, and hallucination. Its central thesis is that model output is a candidate result, not a fact — and the goal of learning LLMs is to develop one judgment: when to trust and when to verify. It defines the appropriate role for LLMs in system design: a reasoning layer, not a truth source or permission judge.

## Key Concepts

- [[tokens]] — segments produced by the tokenizer; affect context capacity, cost, and completeness
- [[embeddings]] — maps text/code to vectors for semantic similarity; good for retrieval, not correctness
- [[transformer-architecture]] — attention mechanism enabling pattern composition across input positions
- [[hallucination]] — models fabricate plausible-sounding facts; must be handled via external verification
- [[multimodal]] — models processing text, images, audio, video, screenshots
- [[large-language-model]] — probabilistic text generator; reasoning layer, not truth source
- [[structured-output]] — outputs constrained to schemas, parameters, or explicit fields

## Notable Points

- "Treat the model as a reasoning layer, not a truth source" — key facts must come from databases, APIs, logs, and documentation.
- "Turn outputs into checkable objects" — summaries, plans, and action suggestions should land in schemas or logs, not just natural language.
- Transformers give models strong pattern-composition ability but not final authority over facts — they can produce wrong summaries when context is missing.
