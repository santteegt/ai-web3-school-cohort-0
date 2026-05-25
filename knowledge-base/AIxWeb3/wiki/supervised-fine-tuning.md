---
title: "Supervised Fine-Tuning (SFT)"
type: concept
tags: [ai-foundations, llm, fine-tuning]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Supervised Fine-Tuning (SFT) is the most common fine-tuning method — it trains a pre-trained model on a dataset of input/expected-output pairs, teaching the model to produce a specific class of outputs for a specific class of inputs.

## Key Points

- SFT is suitable for: fixed-format output, specific tone or style, specific task flows, domain terminology and answer habits, tool-call format/style
- SFT is **very sensitive to data quality** — the model will consistently reproduce whatever patterns are in the training data, good or bad
- A small high-quality dataset (hundreds of well-labeled examples) typically outperforms a large noisy dataset for SFT
- SFT changes how the model responds to your task pattern — it does not expand what the model knows; knowledge comes from pretraining and RAG
- In AI × Web3: SFT can teach a model the exact output format for transaction summaries, risk classification labels, or tool-call JSON structure — making outputs machine-parseable and consistent without additional prompt engineering for format enforcement

## Related Concepts

- [[fine-tuning]] — SFT is the standard fine-tuning approach
- [[lora]] — LoRA is often used to implement SFT efficiently on large models
- [[peft]] — SFT via LoRA or adapters is a PEFT approach
- [[overfitting]] — SFT's primary failure mode on small datasets
- [[evaluation]] — SFT outcomes must be measured with evals before and after training
- [[structured-output]] — SFT can stabilize structured output production for specific schemas

## Sources

- [[sources/fine-tuning]] — SFT definition, suitable tasks, data quality sensitivity
