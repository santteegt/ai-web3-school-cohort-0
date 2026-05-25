---
title: "Fine-Tuning"
type: concept
tags: [ai-foundations, llm, fine-tuning]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Fine-tuning is the process of continuing to train a pre-trained language model on task-specific data to make it more consistent on a class of tasks — improving format adherence, style, domain terminology, or output structure without training from scratch.

## Key Points

- Fine-tuning is for **consistency on a class of tasks**, not for injecting new factual knowledge into the model
- Fine-tuning is not the first step: before fine-tuning, ask: Is the prompt unclear? Is context missing? Did retrieval fail? Does output format lack a schema? Is the model itself insufficient? Is there an eval proving the problem is stable?
- **Have evals before fine-tuning** — without a baseline eval, you cannot tell whether the tuned model improved or only became smoother on a few samples
- **Fix data before fixing the model** — bad data trains bad habits more stably
- **Do not use fine-tuning to store real-time knowledge** — fine-tuned weights are static; time-sensitive information belongs in RAG
- Fine-tuning does not automatically provide: factual correctness, permission safety, reliable citations, or safe tool calling — these must be enforced in code and system design
- Good use cases for fine-tuning in AI × Web3: transaction-explanation style, governance-summary format, risk-label output, contract-comment style, tool-call response format

## Related Concepts

- [[supervised-fine-tuning]] — the most common fine-tuning method using input/output pairs
- [[lora]] — parameter-efficient fine-tuning approach; reduces training cost
- [[peft]] — broader class of parameter-efficient fine-tuning methods
- [[overfitting]] — core risk in fine-tuning; model memorizes training data
- [[evaluation]] — evals must be established before and after fine-tuning to measure improvement
- [[hallucination]] — fine-tuning improves consistency but does not eliminate hallucination
- [[retrieval-augmented-generation]] — preferred over fine-tuning for injecting time-sensitive knowledge
- [[large-language-model]] — fine-tuning adapts an LLM's behavior without modifying its architecture

## Sources

- [[sources/fine-tuning]] — fine-tuning overview, when to use it, and what it cannot do
