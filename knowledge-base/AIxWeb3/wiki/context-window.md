---
title: "Context Window"
type: concept
tags: [ai-foundations, llm, context]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

The context window is the maximum amount of text (measured in tokens) that a model can process in a single request — its "working memory." Everything the model can attend to and reason about must fit within this window.

## Key Points

- A longer context window does **not** imply the model will use every detail perfectly — the model may "see" content but not focus on the right thing
- In real products, the context window should be used **together with retrieval, summarization, and structured data**:
  - Key state → provided directly
  - Long documents → fetched on demand via [[retrieval-augmented-generation]]
  - Low-trust content → isolated and labeled
- The context window is the model's total budget — spending it on irrelevant content crowds out critical information
- Context window size directly affects cost: larger windows use more tokens per request
- The four control layers (system instructions, context, prompt, tool results) all consume context window budget — management is essential in agentic workflows

## Related Concepts

- [[tokens]] — context window is measured in tokens
- [[context-engineering]] — the discipline of deciding what to put in the context window
- [[large-language-model]] — context window is a fundamental LLM parameter
- [[five-layer-agent-context]] — the five layers that compete for context window space
- [[retrieval-augmented-generation]] — a strategy for managing limited context window with external knowledge
- [[agent-memory]] — memories retrieved into context must fit within the window

## Sources

- [[sources/context]] — context window as working memory; limitation with long inputs
- [[sources/ai-fundamentals-introduction]] — context window as first of the four control layers
