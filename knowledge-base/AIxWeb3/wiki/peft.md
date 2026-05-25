---
title: "PEFT (Parameter-Efficient Fine-Tuning)"
type: concept
tags: [ai-foundations, llm, fine-tuning]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Parameter-Efficient Fine-Tuning (PEFT) is a class of methods for adapting large pre-trained models to specific tasks by modifying a small subset of parameters — rather than updating all weights — making fine-tuning accessible to teams without large GPU clusters.

## Key Points

- PEFT methods include: [[lora]] (most common), prefix tuning, prompt tuning, adapter layers, and IA3
- Suitable scenarios for PEFT: a large model where full fine-tuning is too expensive; a clearly scoped task; a medium-sized dataset; a need to test multiple adapter versions in parallel
- PEFT enables rapid experimentation — multiple task-specific adapters can be trained and compared without retraining the base model
- Hugging Face's `peft` library is the standard implementation for most PEFT methods in open-source workflows
- PEFT does not change the base model weights — the base model remains unchanged and adapters can be activated or deactivated independently

## Related Concepts

- [[lora]] — the most widely-used PEFT method; low-rank adapter matrices
- [[fine-tuning]] — PEFT is an approach to efficient fine-tuning
- [[supervised-fine-tuning]] — PEFT is often the implementation path for SFT at scale
- [[local-model]] — PEFT makes fine-tuning viable for teams running open-source models
- [[evaluation]] — same eval requirements apply to PEFT-trained adapters as to fully fine-tuned models

## Sources

- [[sources/fine-tuning]] — PEFT definition, suitable scenarios, and common methods
