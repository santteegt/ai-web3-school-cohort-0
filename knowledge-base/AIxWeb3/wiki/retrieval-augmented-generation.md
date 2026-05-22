---
title: "Retrieval-Augmented Generation (RAG)"
type: concept
tags: [ai-foundations, rag]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Retrieval-Augmented Generation (RAG) is an architecture where a model's response is grounded in external documents retrieved at query time — creating an evidence chain: retrieve, filter, cite, and bound answers to verifiable sources. RAG addresses model knowledge staleness and reduces hallucination, but only when citations and freshness tracking are properly implemented.

## Key Points

- **The core of RAG is not to make answers longer — it is to make answers sourced, versioned, and bounded**
- RAG without citation and freshness tracking only moves hallucination from inside the model into the retrieval system — the danger shifts, not disappears
- A real RAG system makes three explicit judgments: how to chunk documents, what to retrieve for a query, and how to cite or refuse to answer
- **Retrieved results are not facts** — they are candidate evidence; source, time, version, and applicability must still be checked
- **Retrieval failure must allow refusal** — when evidence cannot be found, the system should say "uncertain" instead of letting the model fill the gap
- In AI × Web3 use cases: protocol documentation Q&A, contract interface explanation, governance proposal summaries, audit report retrieval, SDK copilot, transaction interpretation

## Related Concepts

- [[chunking]] — how documents are split into retrievable units
- [[vector-database]] — storage and retrieval layer for RAG
- [[retriever]] — the component that finds candidate documents
- [[re-ranking]] — post-retrieval ordering by relevance and trust
- [[citations]] — the output mechanism that makes RAG answers verifiable
- [[hallucination]] — RAG reduces but doesn't eliminate hallucination without proper citations
- [[knowledge-base]] — the document repository RAG retrieves from
- [[embeddings]] — the representation enabling semantic similarity search in RAG
- [[context-window]] — retrieved documents must fit within context budget
- [[chain-aware-context]] — in AI × Web3, RAG retrieves on-chain state and protocol docs

## Sources

- [[sources/rag]] — RAG definition, components, and AI × Web3 applications
