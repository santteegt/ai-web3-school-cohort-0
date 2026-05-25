---
title: "DSPy"
type: concept
tags: [ai-foundations, frameworks]
source_count: 1
date_updated: "2026-05-24"
---

## Definition

DSPy is a framework that treats prompt and LLM pipelines as optimizable programs — defining inputs, outputs, modules, and evaluation metrics, then using automated optimizers to improve prompt strategies rather than hand-tuning by feel.

## Key Points

- "DSPy does not tune prompts only by feel; it brings tasks, data, and metrics into the system"
- Workflow: define inputs → define outputs → define modules → define metrics → run optimizers → better prompts/strategies automatically
- Best suited for: classification, extraction, Q&A, re-ranking, and complex reasoning chains — tasks where a clear dataset and evaluation metric exist
- DSPy shifts the unit of work from "write a better prompt" to "define a better metric and let the optimizer find the prompt"
- Less suitable for: open-ended generative tasks without a clear quality metric; exploratory prototyping

## Related Concepts

- [[ai-frameworks-overview]] — DSPy is the prompt-optimization-oriented framework in the ecosystem
- [[few-shot-prompting]] — DSPy can optimize few-shot examples as part of the pipeline
- [[structured-output]] — DSPy modules define clear input/output schemas
- [[prompt-design]] — DSPy automates the iterative part of prompt design

## Sources

- [[sources/frameworks]] — DSPy definition, use cases, and optimizer approach
