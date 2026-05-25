---
title: "Evaluation"
type: source
tags: [ai-foundations, evaluation, agent]
source_file: "raw/Evaluation.md"
source_hash: "sha256:882f72b3021d8a34fb056456d5dbb146093146a0cd7c555f092351e700935292"
date_ingested: "2026-05-25"
---

## Summary

This source establishes evaluation as the disciplined, repeatable practice of measuring whether AI system changes actually improve reliability — not just subjectively feel better. It introduces the core components of an eval pipeline: harness, golden set, LLM-as-judge, regression testing, and observability. The central claim is that AI behavior that cannot be measured repeatedly cannot be improved reliably. In AI × Web3 contexts, eval is especially critical because errors can affect assets, permissions, governance, and on-chain execution.

## Key Concepts

- [[evaluation]] — the overall practice of measuring AI system reliability through explicit samples, metrics, and grading
- [[eval-harness]] — the repeatable framework that feeds samples, calls the system, runs graders, and records results
- [[golden-set]] — curated sample set covering real tasks, boundary cases, high-risk questions, and historical bugs
- [[llm-as-judge]] — using an LLM to grade open-ended outputs; useful but requires calibration against human scoring
- [[regression-testing]] — converting known bugs into test cases that rerun before every release
- [[observability]] — recording real-user behavior at runtime to feed back into the golden set and eval pipeline
- [[learning-agents]] — evaluation loop is the safe path by which agents improve without direct online behavior change

## Notable Points

- "AI behavior that cannot be measured repeatedly cannot be improved reliably."
- Test tasks first, not only models — users care whether the whole chain completes the task, not benchmark scores
- In AI × Web3, eval should specifically cover: transaction explanation accuracy, risk-warning completeness, tool-call parameter bounds, prompt injection identification, citation traceability, and human-check triggers for high-risk actions
