---
title: "Vector Database"
type: concept
tags: [ai-foundations, rag]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

A vector database stores document embeddings alongside metadata and retrieves related chunks by measuring similarity between the query embedding and stored embeddings. It is the storage and retrieval backbone of most RAG systems.

## Key Points

- **Vector similarity does not mean the answer is correct** — high cosine similarity can return outdated, irrelevant, or incorrect documents
- "Filter first, then rank" — metadata filters (source, version, chain, update time, trust level, deprecation status) should narrow the candidate set before similarity scoring
- A proper vector database entry stores: vector embedding, source URL, document version, chain/network, update time, trust level, and deprecation flag — not just the vector
- Without metadata, a vector database is a semantic search engine but not a reliable knowledge system
- Common vector databases: Pinecone, Weaviate, Qdrant, Chroma, pgvector

## Related Concepts

- [[embeddings]] — the vectors stored in a vector database
- [[retrieval-augmented-generation]] — vector databases are the storage layer in RAG
- [[chunking]] — chunks with metadata are what the vector database stores
- [[retriever]] — queries the vector database as part of retrieval
- [[re-ranking]] — post-retrieval step that further filters vector database results
- [[knowledge-base]] — a vector database is one implementation of a knowledge base storage layer

## Sources

- [[sources/rag]] — vector database role, metadata requirements, filter-then-rank approach
