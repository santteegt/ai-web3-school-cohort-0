---
title: "Prompt"
type: source
tags: [ai-foundations, prompt, structured-output, prompt-injection, few-shot]
source_file: "raw/Prompt.md"
source_hash: "sha256:4a9f1103d4657d7989447a38fcbd58e7ea8c0a9d9783553dc5019616d44ce82d"
date_ingested: "2026-05-22"
---

## Summary

This source defines the prompt as the interface design between user and model — an executable communication protocol specifying task goals, input boundaries, output formats, failure handling, and security rules. Its core principle is that prompts are soft constraints, not security boundaries: real security must be enforced by code, permissions, and verification. The source introduces the four-segment prompt structure and explains why high-risk actions require a multi-layer verification chain beyond the prompt alone.

## Key Concepts

- [[prompt-design]] — interface design between user and model; executable communication protocol
- [[instruction]] — task rule given to model: role, goal, prohibitions, uncertainty handling, output format
- [[four-segment-prompt]] — Task Goal / Available Inputs / Prohibited Behaviors / Output Format
- [[few-shot-prompting]] — model imitates judgment and output format from examples; requires maintenance
- [[structured-output]] — results returned in schema-constrained format; critical for downstream code processing
- [[prompt-injection]] — dangerous in agents with internal system access; defense via untrusted content marking
- [[verification-chain]] — prompt → context → model → code validation → guard/simulation → human check

## Notable Points

- "Prompts are soft constraints, not security boundaries" — code, permissions, verification, and auditing bear the real constraints.
- "A good prompt is not about making the model more confident, but about letting the model stop at the right time."
- High-risk actions (database writes, payments, signing) must undergo code-layer verification and human checks — never rely on prompt interception alone.
