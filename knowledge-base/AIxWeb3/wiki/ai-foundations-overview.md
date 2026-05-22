---
title: "AI Foundations Overview"
type: topic
tags: [ai-foundations]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

AI Foundations covers the core components needed to understand, build with, and reason about large language model systems — from how models work at a basic level to how agent workflows are structured and evaluated.

## Topics in This Layer

- [[large-language-model]] — what models can do and what they cannot replace
- [[tokens]] — the unit of model processing; affects context, cost, and completeness
- [[embeddings]] — semantic vector representations for search and retrieval
- [[transformer-architecture]] — the architectural foundation of modern LLMs
- [[hallucination]] — the fundamental reliability failure mode
- [[multimodal]] — processing text, images, audio, and video
- [[four-control-layers]] — context window, system instructions, prompt, tool calling
- [[prompt-workflow-agent-boundary]] — three architectures with different failure modes
- [[context-window]] — the model's working memory
- [[context-engineering]] — designing how information enters the model
- [[five-layer-agent-context]] — instruction, task, fact, knowledge, memory layers
- [[information-governance]] — labeling context by source, freshness, permission, trust
- [[agent-memory]] — cross-session persistence; must be revocable
- [[knowledge-base]] — external knowledge repository for retrieval
- [[prompt-design]] — interface design between user and model
- [[instruction]] — task rules for the model
- [[four-segment-prompt]] — Task Goal / Inputs / Prohibitions / Output Format
- [[few-shot-prompting]] — example-based behavior guidance
- [[structured-output]] — schema-constrained model output
- [[prompt-injection]] — adversarial input attack
- [[verification-chain]] — six-layer defense chain
- [[retrieval-augmented-generation]] — sourced, versioned, bounded answers
- [[chunking]] — document splitting for retrieval
- [[vector-database]] — embedding storage and retrieval
- [[retriever]] — candidate selection from knowledge base
- [[re-ranking]] — post-retrieval quality ordering
- [[citations]] — source traceability in answers
- [[ai-agent]] — autonomous planning and execution
- [[tool-calling]] — model-to-world action mechanism
- [[state-management]] — shared state across agent nodes
- [[mcp]] — unified tool connectivity protocol
- [[guardrails]] — hard execution constraints
- [[agent-handoff]] — control transfer between agents
- [[ai-agent-tracing]] — execution chain observability
- [[maas]] — API-based model access
- [[vibe-coding]] — AI-assisted rapid prototyping

## Sources

- [[sources/ai-fundamentals-introduction]]
- [[sources/llms]]
- [[sources/context]]
- [[sources/prompt]]
- [[sources/rag]]
