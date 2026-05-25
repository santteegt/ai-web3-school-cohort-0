---
title: "Regression Testing (AI)"
type: concept
tags: [ai-foundations, evaluation]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Regression testing in AI systems is the practice of converting known bugs and failure cases into test inputs that are re-run automatically before every change — ensuring that previously fixed problems do not silently return when prompts, models, or retrieval are updated.

## Key Points

- A practical regression workflow: (1) user reports an error → (2) reproduce and record the input → (3) label the expected output or refusal condition → (4) add to regression set → (5) run before every release
- Regression tests are the compound interest of AI reliability — each fixed bug becomes permanent protection against that failure mode
- Without regression tests, every prompt change or model update risks silently breaking previously working cases while only improving the cases you tested manually
- Regression tests should be run in the [[eval-harness]] as part of CI/CD — not manually before major releases only
- In AI × Web3: regression cases should include known tool-call failures, parameter bound violations, risk warnings that were missed, and on-chain action approvals that were incorrectly triggered or suppressed

## Related Concepts

- [[evaluation]] — regression testing is a core part of the eval lifecycle
- [[eval-harness]] — runs regression cases before every change
- [[golden-set]] — historical bug samples are stored in the golden set as regression entries
- [[observability]] — online failures are the source material for new regression cases
- [[learning-agents]] — regression tests are the gate that safe learning must pass before reaching production

## Sources

- [[sources/evaluation]] — regression testing workflow and its role in AI reliability
