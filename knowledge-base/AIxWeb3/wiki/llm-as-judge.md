---
title: "LLM-as-Judge"
type: concept
tags: [ai-foundations, evaluation]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

LLM-as-judge is the practice of using a language model to grade another model's outputs — particularly for open-ended tasks like summarization quality, completeness, format adherence, and citation accuracy where rule-based scoring is insufficient.

## Key Points

- Useful when: evaluating summary quality, completeness, format following, source citation — output quality that is hard to capture with exact-match or rule-based scoring
- **Judge models also have bias**: they may miss issues, favor verbose answers, be influenced by output style, or agree with confident-sounding wrong answers
- A steadier approach: (1) use rule scoring for fields that can be judged automatically, (2) use LLM judge for open-ended quality, (3) keep human spot checks for high-risk samples, (4) regularly calibrate consistency between judge and human scoring
- The judge model should be separate from the model under evaluation — using the same model to judge itself compounds any systematic biases
- Calibration is ongoing — as the system evolves, grader and human scores can drift apart, producing misleading eval results

## Related Concepts

- [[evaluation]] — LLM-as-judge is one grading method in the eval pipeline
- [[eval-harness]] — the harness invokes the judge model and records its scores
- [[golden-set]] — the judge grades golden set entries that have open-ended expected outputs
- [[hallucination]] — LLM judges can miss hallucinations in outputs, especially when they are fluent and confident
- [[structured-output]] — for factual fields (e.g. verdict, score, flag), structured output from the judge is more reliable than free-text grading

## Sources

- [[sources/evaluation]] — LLM-as-judge use cases, biases, and calibration requirements
