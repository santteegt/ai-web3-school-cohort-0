---
title: "Evaluation (AI Systems)"
type: concept
tags: [ai-foundations, evaluation]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Evaluation is the disciplined practice of measuring whether AI system changes actually improve reliability — using explicit samples, metrics, grading methods, and regression tests to determine whether the system got better, not just whether it feels better. Without evaluation, prompt changes, model swaps, and RAG updates can only be judged by subjective trial use.

## Key Points

- "AI behavior that cannot be measured repeatedly cannot be improved reliably."
- Evaluation answers: **did this change make key tasks more reliable? Did it introduce new failure modes?**
- Three common false positives without eval: (1) you change a prompt — some questions improve, others regress; (2) you switch models — average improves, but a critical scenario fails; (3) you add RAG — answers are longer but citations are less accurate
- **Test tasks first, not only models** — users care whether the whole chain completes the task
- **Protect key failure cases first** — high-risk errors, common questions, and edge cases should enter the regression set before anything else
- **Evaluation should stay close to the product** — the further it is from real input, the more it becomes self-comfort rather than signal
- Core components of an eval pipeline: [[eval-harness]] + [[golden-set]] + [[llm-as-judge]] + [[regression-testing]] + [[observability]]
- In AI × Web3, evaluation is especially important because errors affect assets, permissions, governance, and on-chain execution

## Related Concepts

- [[eval-harness]] — the repeatable framework that runs evals
- [[golden-set]] — curated sample set covering real tasks and failure modes
- [[llm-as-judge]] — LLM-based grading for open-ended output quality
- [[regression-testing]] — converting known bugs into tests that rerun before every release
- [[observability]] — online behavioral monitoring that feeds the golden set
- [[learning-agents]] — evaluation loop is the safe path for improving agents without online adaptation
- [[ai-agent-tracing]] — traces feed into observability and the eval golden set
- [[hallucination]] — evaluation is the primary mechanism for detecting and reducing hallucination at the system level
- [[dspy]] — DSPy formalizes the evaluation loop into the framework itself

## Sources

- [[sources/evaluation]] — core eval concepts: harness, golden set, LLM-as-judge, regression, observability
