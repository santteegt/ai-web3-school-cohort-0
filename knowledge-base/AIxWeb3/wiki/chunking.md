---
title: "Chunking"
type: concept
tags: [ai-foundations, rag]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Chunking is the process of splitting long documents into smaller, retrievable pieces for use in a RAG system. Each chunk becomes a retrievable unit that can be independently matched against a query.

## Key Points

- **Too small chunks** → semantic breaks — a single concept spans multiple chunks, retrieval misses context
- **Too large chunks** → noisy results and higher token costs — irrelevant content fills the retrieved window
- Technical documentation requires especially careful chunking — code examples, API signatures, and parameter descriptions should stay together
- A steadier approach is to **split by document structure** (headings, sections, paragraphs) rather than fixed character counts
- **Each chunk should preserve metadata**: source URL, heading path, update time, and version — this enables metadata filtering during retrieval
- Chunk metadata is what separates a reliable RAG system from a "demo that retrieves some paragraphs"

## Related Concepts

- [[retrieval-augmented-generation]] — chunking is step 1 of the RAG pipeline
- [[vector-database]] — chunks with their embeddings and metadata are stored here
- [[retriever]] — retrieval quality depends heavily on chunk quality
- [[knowledge-base]] — the source documents being chunked

## Sources

- [[sources/rag]] — chunking strategies and metadata requirements
