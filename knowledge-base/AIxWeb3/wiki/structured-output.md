---
title: "Structured Output"
type: concept
tags: [ai-foundations, prompt, llm]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

Structured output is a technique where the model's response is constrained to a predefined schema — JSON, function parameters, typed fields, or explicit named sections — rather than free-form natural language. This makes model output directly processable by downstream code without parsing or interpretation.

## Key Points

- Critical for application development: **subsequent systems process explicit fields, not prose**
- Structured output is the primary mechanism for turning LLM output into "checkable objects"
- Schema-constrained output reduces hallucination impact — fabricated content still occupies a field, making it detectable and auditable
- In AI × Web3, structured output is essential for anything close to the execution layer: transaction parameters, contract calls, governance votes must be structured, not narrated
- Most major LLM APIs support native structured output (e.g. OpenAI function calling, Anthropic tool use) — prefer these over prompt-based JSON requests, which are less reliable
- Structured output is not infallible — models can still produce invalid JSON or misuse fields; schema validation code must verify the output

## Related Concepts

- [[prompt-design]] — output format specification is the fourth segment of the four-segment prompt
- [[four-segment-prompt]] — the output format segment defines the schema
- [[large-language-model]] — structured output is a key mechanism for making LLM output verifiable
- [[tool-calling]] — tool use is a form of structured output (the model emits a structured function call)
- [[verification-chain]] — code validation of structured output is step 4 of the verification chain
- [[hallucination]] — structured output reduces but doesn't eliminate hallucination

## Sources

- [[sources/prompt]] — structured output definition and role in verification
- [[sources/llms]] — outputs as checkable objects via schemas and logs
