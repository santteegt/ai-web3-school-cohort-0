---
title: "Inference Network"
type: concept
tags: [aixweb3-bridge, decentralized-ai, frontier]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Inference Network decomposes model inference into a network service: a user or agent sends a request, the network selects a node for execution, results are returned, and billing, auditing, or proof is completed. Nodes do not necessarily belong to the same company.

## Key Points

- System must handle: node discovery, model versions, request routing, rate limiting, failure retries, result verification, and payment settlement
- Key developer questions: which model/node was used, are model versions traceable, can it retry or switch nodes on failure, is user privacy exposed to untrusted nodes, are cost/latency/quality recorded
- For agents initiating on-chain actions from inference results: the network must clarify liability boundaries between output and subsequent execution
- Distributed ≠ trusted by default — verification layer is required

## Related Concepts

- [[decentralized-ai]]
- [[compute-market]]
- [[model-routing]]
- [[quality-benchmark]]
- [[proof-of-inference]]
- [[model-result]]

## Sources

- [[sources/bridge-chapters]]
