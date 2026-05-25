---
title: "Eval Harness"
type: concept
tags: [ai-foundations, evaluation]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

An eval harness is the repeatable framework that runs AI system evaluations — feeding input samples to the system, collecting outputs, applying graders, and recording results. Its core value is repeatability: without a harness, it is impossible to reliably compare prompts, models, or retrieval strategies across runs.

## Key Points

- The value of a harness is **repeatability** — without it, comparisons between system versions are subjective and unreliable
- Minimal harness components: (1) input samples, (2) expected outputs or grading rules, (3) system version under test, (4) model and parameter configuration, (5) run logs, (6) result report
- A harness is not the same as a benchmark — benchmarks measure model capability; a harness measures whether your specific system on your specific tasks works for your users
- The harness should be version-controlled and run as part of CI/CD — not run manually before major releases only
- In AI × Web3: the harness should include test cases covering transaction explanations, tool-call parameter bounds, risk-warning completeness, and prompt injection resistance

## Related Concepts

- [[evaluation]] — harness is the execution layer of the eval pipeline
- [[golden-set]] — the sample set the harness runs against
- [[regression-testing]] — the harness runs regression cases before every release
- [[llm-as-judge]] — grading method the harness can invoke for open-ended outputs
- [[observability]] — runtime data that feeds new samples into the harness
- [[dspy]] — DSPy's compilation pipeline is an automated form of harness execution

## Sources

- [[sources/evaluation]] — harness definition: components, repeatability value, relation to graders
