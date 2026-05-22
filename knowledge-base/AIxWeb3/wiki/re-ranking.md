---
title: "Re-ranking"
type: concept
tags: [ai-foundations, rag]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Re-ranking is a post-retrieval step in a RAG pipeline that reorders candidate documents returned by the retriever, promoting the most relevant, trusted, and complete content to the top before passing the final context to the model.

## Key Points

- Re-ranking moves beyond simple vector similarity — it scores candidates on multiple dimensions: relevance, source trustworthiness, content completeness, recency
- Adds **latency and cost** — whether to use re-ranking depends on the scenario (complex technical Q&A warrants it; simple lookups may not)
- A re-ranker can be a cross-encoder model (slow but accurate), a rule-based system (fast, predictable), or a hybrid
- Without re-ranking, a retriever may return 10 candidates and the model sees an arbitrary mix; with re-ranking, the top-3 it gets are genuinely the best
- In AI × Web3 use cases, re-ranking on recency and official-source flags is especially important — outdated or unofficial documentation causes dangerous downstream decisions

## Related Concepts

- [[retrieval-augmented-generation]] — re-ranking is the optional step between retrieval and context injection
- [[retriever]] — re-ranking operates on what the retriever returns
- [[vector-database]] — re-ranking filters and reorders the vector database results
- [[citations]] — re-ranking helps ensure cited sources are the highest-quality available

## Sources

- [[sources/rag]] — re-ranking role and cost tradeoff
