---
title: "Four-Segment Prompt Structure"
type: concept
tags: [ai-foundations, prompt]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

The four-segment prompt structure is a practical template for writing instructions that are unambiguous and executable: Task Goal, Available Inputs, Prohibited Behaviors, and Output Format (including Failure Format).

## Key Points

1. **Task Goal** — the specific outcome expected; answers "what should be accomplished"
2. **Available Inputs** — what data, context, or documents the model has access to; sets information boundaries
3. **Prohibited Behaviors** — explicit list of what the model must not do; reduces unwanted completions
4. **Output Format and Failure Format** — the schema or structure for success responses; and what to return when uncertain or unable to answer (e.g. `{"error": "insufficient evidence"}`)

- The failure format is often omitted but is critical — without it, models fill gaps with hallucinated answers instead of refusing
- This structure maps directly to the [[five-layer-agent-context]] layers: goal → task layer, inputs → fact/knowledge layers, prohibitions → instruction layer
- Few-shot examples can be added as a fifth section when the output format is complex

## Related Concepts

- [[prompt-design]] — the broader discipline this structure belongs to
- [[instruction]] — the full task rule; four-segment is the practical way to write it
- [[structured-output]] — the output format segment should specify the schema
- [[few-shot-prompting]] — examples can augment the output format guidance

## Sources

- [[sources/prompt]] — four-segment structure definition
