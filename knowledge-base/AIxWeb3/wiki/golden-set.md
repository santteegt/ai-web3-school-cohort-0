---
title: "Golden Set"
type: concept
tags: [ai-foundations, evaluation]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

A golden set is a curated collection of high-quality evaluation samples that covers the real tasks the system must handle, key failure modes, and high-risk scenarios. It is the primary input to the eval harness and the ground truth against which system changes are measured.

## Key Points

- 30–100 high-quality samples are often more useful than thousands of low-quality ones
- A golden set should include: (1) common normal questions, (2) boundary questions, (3) questions easy to misjudge, (4) high-risk questions, (5) historical bugs, (6) real user feedback samples
- **Every time you fix an important bug, convert it into a regression sample and add it to the golden set** — this is the compound interest of evaluation
- The golden set is a living artifact: it grows as the system is used, bugs are found, and new edge cases emerge
- A golden set that only contains easy questions gives false confidence — the failure modes that matter are the hard ones
- In AI × Web3: the golden set must include samples covering transaction explanations, ambiguous tool calls, risk warnings, prompt injection attempts, and refusal conditions for uncertain requests

## Related Concepts

- [[evaluation]] — golden set is the sample foundation of any eval pipeline
- [[eval-harness]] — the harness runs against the golden set
- [[regression-testing]] — historical bug samples become regression entries in the golden set
- [[observability]] — real user failures are the source of new golden set entries
- [[llm-as-judge]] — used to grade golden set samples that have open-ended expected outputs

## Sources

- [[sources/evaluation]] — golden set composition, size guidance, and when to add new samples
