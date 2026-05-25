---
title: "Overfitting"
type: concept
tags: [ai-foundations, llm, fine-tuning, evaluation]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Overfitting occurs when a model learns training data too specifically — memorizing patterns and outputs rather than generalizing from them — resulting in high performance on training examples but degraded performance on new, real-world inputs.

## Key Points

- Common causes in fine-tuning: validation and training sets are too similar; training runs for too many epochs; training dataset is too small or too homogeneous
- Warning sign: "the model looks good on your prepared examples, but falls apart when real users ask questions"
- Overfitting is especially dangerous when training data is biased toward common or easy cases — the model performs well on benchmarks while failing on the long tail of real user behavior
- Detection requires a held-out test set that is truly separate from training data — a validation loss that matches training loss is not sufficient if both sets were drawn from the same narrow distribution
- In AI × Web3: a fine-tuned model that overfits to clean, well-formatted transaction examples will fail on real user inputs that use ambiguous phrasing, unusual token names, or edge-case amounts

## Related Concepts

- [[fine-tuning]] — overfitting is the primary failure mode in fine-tuning
- [[supervised-fine-tuning]] — SFT on small datasets is especially prone to overfitting
- [[evaluation]] — eval on a held-out test set is the primary overfitting detection mechanism
- [[golden-set]] — a diverse golden set covering boundary cases is what reveals overfitting in practice
- [[hallucination]] — overfitted models can hallucinate convincingly in-distribution while being unreliable out-of-distribution

## Sources

- [[sources/fine-tuning]] — overfitting causes, warning signs, and detection requirements
