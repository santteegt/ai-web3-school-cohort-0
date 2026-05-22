---
title: "Knowledge Base (AI)"
type: concept
tags: [ai-foundations, context, rag]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

A knowledge base is an external repository that a system retrieves from to supply the model with current, verifiable information beyond its training data. It addresses model knowledge staleness but does not automatically guarantee correctness — the quality of the knowledge base depends on how well sources, versions, and deprecation status are maintained.

## Key Points

- A knowledge base must record for each document: source URL, last update time, applicable protocol version, applicable runtime environment, whether it's from an official source or third party, and whether human review is needed
- Good at solving **model knowledge staleness** (training cutoff) — especially important in fast-moving domains like Web3 protocols
- Does **not automatically guarantee correctness** — stale or unofficial content in the knowledge base will be retrieved and presented as authoritative
- In AI × Web3 contexts, a knowledge base entry for a DeFi protocol must track: applicable chain, contract version, whether the protocol has been audited, and deprecation status
- The LLM Wiki pattern (this vault) is itself a knowledge base maintained by an LLM

## Related Concepts

- [[retrieval-augmented-generation]] — RAG retrieves from the knowledge base to populate model context
- [[context-engineering]] — decides what knowledge base content to retrieve and when
- [[citations]] — knowledge base entries become citable sources in RAG answers
- [[information-governance]] — knowledge base maintenance is an information governance problem
- [[vector-database]] — common storage layer for knowledge base retrieval
- [[five-layer-agent-context]] — knowledge layer is the fourth layer in agent context

## Sources

- [[sources/context]] — knowledge base definition, maintenance requirements
- [[sources/rag]] — RAG's relationship to knowledge base; freshness and version requirements
