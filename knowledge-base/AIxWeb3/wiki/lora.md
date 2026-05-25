---
title: "LoRA (Low-Rank Adaptation)"
type: concept
tags: [ai-foundations, llm, fine-tuning]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

LoRA (Low-Rank Adaptation) is a parameter-efficient fine-tuning method that trains small adapter matrices rather than updating all model weights — dramatically reducing VRAM requirements and training cost while achieving comparable task adaptation to full fine-tuning.

## Key Points

- Instead of updating all model parameters, LoRA adds low-rank decomposition matrices to specific weight layers — only these adapters are trained
- Reduces training cost and VRAM requirements significantly compared to full fine-tuning
- Commonly used for fine-tuning open-source models (LLaMA, Mistral, Qwen, etc.) on consumer or mid-range hardware
- **LoRA reduces experiment cost, but it is not magic** — task definition, data quality, and evaluation still determine the final result
- LoRA is a subset of [[peft]] (Parameter-Efficient Fine-Tuning)
- Multiple LoRA adapters can be trained for different tasks and swapped onto the same base model at inference time — enabling efficient multi-task deployment

## Related Concepts

- [[peft]] — LoRA is the most widely-used PEFT method
- [[fine-tuning]] — LoRA implements fine-tuning efficiently
- [[supervised-fine-tuning]] — LoRA is the common implementation path for SFT on open-source models
- [[overfitting]] — LoRA reduces but does not eliminate overfitting risk; data quality and epoch count still matter
- [[local-model]] — LoRA is especially relevant for teams running open-source models locally
- [[inference]] — LoRA adapters add minimal latency at inference time compared to full fine-tuned models

## Sources

- [[sources/fine-tuning]] — LoRA definition, use cases, and practical limitations
