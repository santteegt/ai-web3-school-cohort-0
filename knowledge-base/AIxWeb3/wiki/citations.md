---
title: "Citations (RAG)"
type: concept
tags: [ai-foundations, rag]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

Citations in a RAG system are the explicit links that connect claims in the model's answer back to the specific source documents they were derived from. They are the user's entry point for verifying whether an answer is trustworthy.

## Key Points

- A citation should answer: which document a statement came from, whether the source is official, the document version or update time, which conclusions are model summaries vs. direct quotes, and where evidence is insufficient
- **Citations without freshness context are misleading** — a citation to a 2021 protocol doc for a question about a 2024 upgrade creates false confidence
- "Many RAG demos only reach 'we can retrieve some paragraphs'; they have not reached 'the answer can be verified'"
- **Retrieval failure must trigger refusal, not hallucination** — if no citation can be provided, the system should say "uncertain" rather than fabricate a sourced-sounding answer
- In AI × Web3, on-chain citations (block number, transaction hash, event log) are the gold standard — they are immutable and independently verifiable

## Related Concepts

- [[retrieval-augmented-generation]] — citations are the final output mechanism of RAG
- [[hallucination]] — citations are the user-facing defense against hallucination
- [[knowledge-base]] — citations trace back to knowledge base entries
- [[re-ranking]] — good re-ranking ensures cited sources are the best available
- [[chunking]] — chunks must preserve source metadata so citations are possible

## Sources

- [[sources/rag]] — citations as user verification entry point; what a citation must contain
