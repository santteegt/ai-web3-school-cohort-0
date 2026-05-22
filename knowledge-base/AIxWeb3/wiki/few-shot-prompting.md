---
title: "Few-Shot Prompting"
type: concept
tags: [ai-foundations, prompt]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Few-shot prompting is a technique where examples of the desired input-output pattern are included in the prompt, guiding the model to imitate the judgment method and output format shown. The model generalizes from these examples to handle new inputs in the same style.

## Key Points

- Few-shot examples help the model understand complex output formats that are hard to specify in text alone
- They also transfer domain-specific judgment: if examples show how to classify edge cases, the model learns that classification boundary
- **Few-shot examples carry maintenance costs** — they are test assets that must be updated together with evaluation sets; stale examples mislead the model
- Few-shot examples can be placed in the system prompt (for consistent behavior) or in user messages (for task-specific demonstration)
- More examples is not always better — too many examples consume [[context-window]] budget; 2–5 high-quality examples typically outperform 20 mediocre ones

## Related Concepts

- [[prompt-design]] — few-shot is one technique within prompt design
- [[instruction]] — examples complement written instructions, especially for format-heavy tasks
- [[structured-output]] — few-shot examples are especially useful for teaching complex output schemas
- [[context-window]] — examples consume token budget; must be weighed against other context needs

## Sources

- [[sources/prompt]] — few-shot definition and maintenance cost warning
