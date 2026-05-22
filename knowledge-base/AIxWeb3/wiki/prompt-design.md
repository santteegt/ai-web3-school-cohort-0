---
title: "Prompt Design"
type: concept
tags: [ai-foundations, prompt]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Prompt design is the practice of crafting the interface between a user (or developer) and a language model — an executable communication protocol that specifies task goals, input boundaries, output formats, failure handling, and security rules. A well-designed prompt turns a vague task into a work instruction the model can execute stably.

## Key Points

- A prompt is a **communication protocol**, not a security mechanism — real boundaries are enforced by code, permissions, and verification
- "A good prompt is not about making the model more confident, but about letting the model stop at the right time"
- **Instruction layers must be clear**: system rules, developer rules, user goals, and retrieved content must not be mixed
- **Output formats must be machine-verifiable**: critical results should use JSON schemas, function parameters, or explicit fields
- **High-risk actions cannot rely solely on prompt interception**: payments, database writes, signing require code-layer verification

**The four-segment prompt structure:**
1. **Task Goal** — what you want the model to accomplish
2. **Available Inputs** — what data/context is provided
3. **Prohibited Behaviors** — what the model must not do or say
4. **Output Format and Failure Format** — expected output shape; what to return when uncertain

## Related Concepts

- [[instruction]] — the specific segment defining role, goal, prohibitions, and output format
- [[four-segment-prompt]] — the four-part structure: goal, inputs, prohibitions, format
- [[few-shot-prompting]] — augmenting prompts with examples to guide model behavior
- [[structured-output]] — machine-verifiable output; the goal of output format design
- [[prompt-injection]] — the attack vector enabled by poor prompt design
- [[verification-chain]] — the full system that prompt design is part of (not the sole defense)
- [[context-engineering]] — prompt sits within the broader context engineering discipline

## Sources

- [[sources/prompt]] — full prompt design principles and four-segment structure
