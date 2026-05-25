---
title: "Quantization"
type: concept
tags: [ai-foundations, llm, inference]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Quantization reduces the numerical precision of model weights — for example from FP16 to INT8 or INT4 — allowing large models to run on smaller hardware with lower VRAM requirements and faster inference, at the cost of some output quality.

## Key Points

- Quantization trades off model size, inference speed, and output quality — it makes running large models on smaller devices possible
- Common precision levels: FP32 → FP16 → INT8 → INT4, each step reducing VRAM requirements roughly by half
- **Quality degradation is real**: quantization may reduce output quality in long reasoning, code generation, multilingual tasks, math, and tool calls — the most complex output types
- "Whether a quantized model is usable or not, it should be tested on your own task samples" — general benchmarks do not predict quality on your specific use case
- Quantization is not binary — some layers can be kept at higher precision (e.g. attention layers) while others are reduced, balancing quality and efficiency
- In AI × Web3: quantized models used for tool calling or transaction analysis must be validated against the same tool-call format and accuracy standards as full-precision models — malformed JSON from a quantized model can cause silent failures or incorrect on-chain actions

## Related Concepts

- [[inference]] — quantization is a technique for reducing inference cost
- [[local-model]] — quantization is most relevant for local model deployments
- [[model-serving]] — quantization affects serving hardware requirements and throughput
- [[evaluation]] — quantized models must be evaluated on task-specific samples before production use
- [[tool-calling]] — tool call format reliability can degrade with aggressive quantization
- [[hallucination]] — quantization can increase hallucination rates, especially at lower precision levels

## Sources

- [[sources/inference]] — quantization definition, precision tradeoffs, and task-specific testing requirement
