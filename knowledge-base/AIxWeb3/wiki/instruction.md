---
title: "Instruction (Prompt Design)"
type: concept
tags: [ai-foundations, prompt]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

An instruction is the task rule given to a model that specifies its role, what it should accomplish, what it is prohibited from doing, how to handle uncertain information, and what form the output should take. Instructions are one of the four control layers and the primary vehicle for expressing developer intent to the model.

## Key Points

- A well-formed instruction answers five questions: what is your role / what should you complete / what are you prohibited from doing / how to handle uncertain information / what form should the output take
- Instructions must specifically distinguish between **"explanation"** (model describes something) and **"execution"** (model triggers an action)
- Instructions are placed in the system or developer message — the highest-trust layer — and must not be mixed with user input or retrieved content
- Instructions are **soft constraints** — they shape behavior probabilistically, not deterministically. Code and verification systems enforce hard constraints
- The four-segment practical structure for writing instructions: Task Goal → Available Inputs → Prohibited Behaviors → Output Format

## Related Concepts

- [[prompt-design]] — instructions are the core component of a prompt
- [[four-segment-prompt]] — the practical structure for writing instructions
- [[five-layer-agent-context]] — instructions live in the instruction layer (highest trust)
- [[structured-output]] — instructions should specify the output schema
- [[prompt-injection]] — attacks that attempt to override instructions via injected user content

## Sources

- [[sources/prompt]] — instruction definition and four-segment structure
