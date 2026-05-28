---
title: "AI Oracle"
type: concept
tags: [web3-foundations, oracle, aixweb3-bridge, frontier]
source_count: 2
date_updated: "2026-05-28"
---

## Definition

An AI Oracle is a mechanism that submits model outputs, scores, classifications, or inference results to on-chain systems for use. Its challenge is not just "how to get data on-chain" but how to record inputs, models, versions, proofs, and disputes. Core principle: when AI output affects on-chain assets or permissions, the output itself must have a source, boundary, and dispute mechanism.

## Key Points

- Standard oracles bring external data on-chain; AI oracles bring model judgments: "whether a task is completed," "whether content is non-compliant," "whether an address is high-risk"
- Inputs must be traceable (what the model saw), results must be structured (on-chain systems consume fields, not long text), disputes must be designed upfront (who can challenge, challenge window, review process)
- Layering by risk: low-risk → display labels; medium-risk → human review; high-risk → proofs + challenge periods + multi-party verification
- AI oracle inherits all oracle risks AND adds: model errors, input contamination, prompt injection, data bias, tampered execution environments, non-reviewable outputs

## Sub-Concepts

- [[ai-output]] — structured fields (machine) + human explanation (UI/disputes); never long text for contract decisions
- [[data-feed]] — continuous AI-processed data with version tracking and drift handling
- [[model-result]] — model version + prompt template + input reference + output schema
- [[oracle-risk]] — errors, contamination, prompt injection, economic attacks, versioning issues
- [[proof-of-inference]] — TEE/ZK/signed-log proofs that output came from specific model + input
- [[dispute-challenge]] — optimistic challenge window for objecting to AI oracle outputs

## Related Concepts

- [[oracle]] — AI oracle extends oracle architecture
- [[oracle-risk]] — inherits all standard oracle risks plus AI-specific ones
- [[verifiable-ai]] — on-chain proof of AI computation
- [[smart-contract]] — the consumer of AI oracle outputs
- [[agent-identity]] — AI oracles can attest which agent produced an output
- [[chain-aware-context]] — AI agents read chain state; AI oracles write AI state to chain
- [[settlement-and-escrow]] — AI oracle outputs often trigger escrow state transitions

## Sources

- [[sources/web3-chapters]] — Chapter: Oracle
- [[sources/bridge-chapters]] — detailed chapter with sub-concepts, first principles, and minimal practice
