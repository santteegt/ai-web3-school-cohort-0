---
title: "Large Language Model (LLM)"
type: concept
tags: [ai-foundations, llm]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

A Large Language Model is a neural network trained on vast text corpora that generates outputs by predicting the most likely next token sequence given an input. LLMs excel at language understanding, code generation, and reasoning — but are fundamentally unreliable for deterministic factual recall, computation, and maintaining state across sessions.

## Key Points

- LLMs generate outputs that are **probabilistically reasonable, not facts that are trustworthy by default**
- They are best treated as a **reasoning layer**, not a truth source or permission judge
- Key facts must come from databases, APIs, logs, and documentation — not from the model
- LLM output should be **turned into checkable objects**: schemas, parameters, citations, or logs — not left as natural language
- Four capabilities LLMs have: language understanding, code generation, reasoning, summarization
- Four things LLMs cannot replace: accurate factual recall, deterministic computation, state persistence, permission authority
- In AI × Web3: LLMs sit in the **understanding and generation layer** — they turn user goals into plans and explain on-chain data in human language; the closer they get to the execution layer, the more output must be turned into verifiable objects

## Related Concepts

- [[tokens]] — the unit LLMs operate on
- [[transformer-architecture]] — the architectural pattern that enables LLMs
- [[hallucination]] — the failure mode of generating confident falsehoods
- [[embeddings]] — the representation layer beneath generation
- [[context-window]] — the working memory that bounds what an LLM can see
- [[tool-calling]] — how LLMs act on the world rather than just generate text
- [[structured-output]] — how to make LLM output verifiable and machine-processable
- [[ai-agent]] — systems where LLMs plan and execute autonomously

## Sources

- [[sources/llms]] — core technical mental model
- [[sources/ai-fundamentals-introduction]] — control layers and agent components
