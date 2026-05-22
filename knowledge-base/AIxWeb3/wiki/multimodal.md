---
title: "Multimodal"
type: concept
tags: [ai-foundations, llm]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Multimodal refers to the ability of a model to process and reason over multiple types of input — text, images, audio, video, and screenshots — rather than text alone.

## Key Points

- Multimodal inputs expand what can enter a model's context: UI screenshots, charts, contract ABIs in image form, video recordings of transactions
- **Multimodal input also needs boundaries via structured key judgments and trusted sources** — images and audio can carry adversarial content just as text can
- In AI × Web3, multimodal models can interpret transaction UIs, on-chain visualizations, and wallet interface screenshots directly
- Even with multimodal capability, key decisions must still come from structured, trusted data sources — not from the model's visual interpretation alone

## Related Concepts

- [[large-language-model]] — the base architecture extended by multimodal capability
- [[context-window]] — multimodal inputs (images, audio) consume significant context budget
- [[information-governance]] — applies equally to non-text inputs
- [[hallucination]] — multimodal models can hallucinate about visual content too

## Sources

- [[sources/llms]] — multimodal as LLM capability; governance requirements
