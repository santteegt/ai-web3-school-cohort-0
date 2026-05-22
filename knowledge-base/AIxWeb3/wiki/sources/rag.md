---
title: "RAG"
type: source
tags: [ai-foundations, rag, chunking, vector-database, retriever, citations]
source_file: "raw/RAG.md"
source_hash: "sha256:05a06e4a829a7a3088db84cf1c75ee753def00c2e3eb93b95689b538b16f6c7a"
date_ingested: "2026-05-22"
---

## Summary

This source defines RAG as an evidence chain — not a tool to make answers longer, but to make them sourced, versioned, and bounded. Its central warning is that RAG without citation and freshness tracking only moves hallucination from inside the model into the retrieval system. A real RAG system makes three judgments: how to chunk documents, what to retrieve, and how to cite or refuse. The source covers all major RAG components — chunking, vector DBs, retrievers, re-ranking, and citations — and maps RAG's role in AI × Web3 contexts.

## Key Concepts

- [[retrieval-augmented-generation]] — evidence chain: retrieve, filter, cite, bound answers to external knowledge
- [[chunking]] — splits long documents into retrievable pieces; preserve source URL, heading path, version per chunk
- [[vector-database]] — stores embeddings + metadata; filter first, then rank; stores version, chain, deprecation status
- [[retriever]] — returns candidate material based on query; hybrid approaches outperform pure vector search
- [[re-ranking]] — reorders candidates by relevance, trust, and completeness; adds latency/cost tradeoff
- [[citations]] — connect answer claims back to source documents; entry point for user verification
- [[hallucination]] — RAG without proper citation/freshness only relocates hallucination to retrieval layer
- [[knowledge-base]] — RAG retrieves from a knowledge base; freshness and version metadata are critical

## Notable Points

- "RAG without citation and freshness only moves hallucination from inside the model into the retrieval system."
- "Vector similarity does not mean the answer is correct" — metadata filters (version, chain, deprecation) must accompany vector search.
- In AI × Web3, RAG results affecting on-chain actions still require simulation, policy check, and human confirmation.
