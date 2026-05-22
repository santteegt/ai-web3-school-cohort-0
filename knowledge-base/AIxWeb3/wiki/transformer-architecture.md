---
title: "Transformer Architecture"
type: concept
tags: [ai-foundations, llm]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

The Transformer is the neural network architecture underlying modern LLMs, introduced in the 2017 paper "Attention Is All You Need." Its core innovation is the **attention mechanism**, which allows the model to attend to any position in the input while generating output, learning relationships between words, code, facts, and context regardless of distance.

## Key Points

- Attention enables the model to dynamically weight how relevant each input token is when generating each output token
- Transformers give models **strong pattern-composition ability** — they can find and combine patterns across long inputs
- Transformers do **not** give models final authority over facts — they compose patterns, not ground truth
- The model can produce wrong summaries when context is missing or similar patterns from training mislead it
- "Attention Is All You Need" (Vaswani et al., 2017) is the canonical reference for technical background

## Related Concepts

- [[large-language-model]] — transformers are the architectural foundation of LLMs
- [[tokens]] — transformers operate on token sequences
- [[embeddings]] — tokens are converted to embeddings before attention operations
- [[context-window]] — the maximum sequence length a transformer can attend to
- [[hallucination]] — a failure mode enabled by pattern-composition without ground-truth verification

## Sources

- [[sources/llms]] — transformer pattern-composition ability and its limits
