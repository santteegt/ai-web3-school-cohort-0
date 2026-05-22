---
title: "MaaS (Model-as-a-Service)"
type: concept
tags: [ai-foundations, llm]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Model-as-a-Service (MaaS) is the API-based access model for large language models where developers call top-tier models via an API key on a per-token billing basis — without needing to run or manage GPU infrastructure.

## Key Points

- Core parameters for any MaaS call: `model`, `messages`, `temperature`, `max_tokens`
- Lowers the barrier to AI development dramatically: no GPU, no ops, pay only for what you use
- Major MaaS providers: OpenAI, Anthropic, Google (Gemini), Z.ai (GLM) — most use OpenAI-compatible APIs
- `temperature` controls output randomness: 0 = deterministic (useful for structured tasks), 1 = diverse (useful for creative tasks)
- Per-token billing means prompt engineering has direct cost implications — concise, effective prompts save money

## Related Concepts

- [[large-language-model]] — the models accessed via MaaS
- [[tokens]] — MaaS billing unit; token count determines cost
- [[structured-output]] — a key pattern for MaaS application development
- [[tool-calling]] — MaaS APIs expose tool/function calling as a first-class feature

## Sources

- [[sources/ai-fundamentals-introduction]] — MaaS definition and core parameters
