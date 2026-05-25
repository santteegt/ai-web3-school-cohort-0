---
title: "Fine Tuning"
type: source
tags: [ai-foundations, llm, fine-tuning]
source_file: "raw/Fine Tuning.md"
source_hash: "sha256:d48cef814321b9ab9cc3de25f9737713e22a49b6e63ac3037f5840b4f47439b7"
date_ingested: "2026-05-25"
---

## Summary

This source frames fine-tuning as a targeted tool for making a model more consistent on a class of tasks — not a first resort, and not a replacement for good prompting, retrieval, or schema design. It introduces the core fine-tuning methods (SFT, LoRA, PEFT) and dataset requirements. The source emphasizes that fine-tuning requires established evals before starting, clean data, and a clearly scoped objective — and explicitly warns that fine-tuning cannot provide factual correctness, permission safety, or safe tool calling on its own.

## Key Concepts

- [[fine-tuning]] — adapting a pre-trained model to a specific task or style using training data
- [[supervised-fine-tuning]] — SFT: input/expected-output pair training for fixed-format tasks
- [[lora]] — Low Rank Adaptation: parameter-efficient fine-tuning by training smaller adapter matrices
- [[peft]] — Parameter-Efficient Fine-Tuning: class of methods adapting models with minimal parameter changes
- [[overfitting]] — model memorizes training data and fails to generalize to new inputs
- [[evaluation]] — evals must exist before fine-tuning to know if the tuned model actually improved
- [[hallucination]] — fine-tuning improves style/format consistency but does not fix hallucination

## Notable Points

- "Fix data before fixing the model: bad data trains bad habits more stably."
- "Have evals before fine-tuning: otherwise you do not know whether the tuned model improved or only became smoother on a few samples."
- Fine-tuning cannot directly turn the model into a trusted execution layer in AI × Web3 — it can improve format consistency for transaction explanations, governance summaries, risk labels, and tool-call style, but permission safety and reliability must be enforced in code
