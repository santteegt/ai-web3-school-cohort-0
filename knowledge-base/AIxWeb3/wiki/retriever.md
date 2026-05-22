---
title: "Retriever"
type: concept
tags: [ai-foundations, rag]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

A retriever is the component in a RAG system that selects candidate material from a knowledge base in response to a user query. Retrievers can use vector similarity, keyword matching, metadata filters, graph traversal, or hybrid combinations.

## Key Points

- Types: **vector** (semantic similarity via embeddings), **keyword** (BM25, TF-IDF), **hybrid** (combine vector + keyword), **graph-based** (traverse knowledge graphs), **metadata-filtered** (filter by version, time, source before ranking)
- **A good retriever cannot look only at semantic similarity** — if a query contains a version, environment, time, address, or specific object, pure vector search will retrieve semantically-similar but version-mismatched or context-wrong results
- Hybrid retrieval combining vector and keyword search generally outperforms either alone
- In Web3 contexts: if a user asks about "USDC on Base as of 2025," the retriever must filter by chain=Base and date≤2025, not just search for "USDC"
- Retriever quality is the most important single factor in RAG system reliability

## Related Concepts

- [[retrieval-augmented-generation]] — retrievers are the core selection mechanism
- [[vector-database]] — most retrievers query a vector database
- [[embeddings]] — vector retrievers compute query embeddings to find similar chunks
- [[re-ranking]] — reorders what the retriever returns
- [[chunking]] — retriever quality depends on how well documents were chunked

## Sources

- [[sources/rag]] — retriever types and the necessity of hybrid approaches
