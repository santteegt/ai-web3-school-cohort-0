---
title: "Inference"
type: source
tags: [ai-foundations, llm, inference]
source_file: "raw/Inference.md"
source_hash: "sha256:8fe7fc9a47d487a9767f1fba353688f4bfd17405f700d17f374142d8d52113d7"
date_ingested: "2026-05-25"
---

## Summary

This source covers the inference layer — the part of the AI stack that delivers model responses in production under real constraints of latency, cost, privacy, and quality. It establishes that inference is a combined tradeoff across multiple dimensions, and that the choice between API models and local models has architectural implications beyond simple cost. Key components covered include quantization, model serving, and the observability requirements unique to AI × Web3 deployments where on-chain actions require auditable inference records.

## Key Concepts

- [[inference]] — the production layer delivering model outputs under latency, cost, and quality constraints
- [[maas]] — API-based model access (MaaS); handles most inference cases but still requires engineering discipline
- [[local-model]] — running model weights locally for privacy, cost control, or offline use
- [[quantization]] — reducing model weight precision to lower VRAM and latency at the cost of output quality
- [[model-serving]] — infrastructure for production model inference: queuing, batching, streaming, monitoring
- [[ai-agent-tracing]] — inference in AI × Web3 must leave auditable records of model, inputs, outputs, and tool triggers

## Notable Points

- "Quality has a cost: stronger models usually mean higher cost, longer latency, or more complex deployment."
- "Services should be replaceable: clear model-call encapsulation makes fallback, rollout, and evaluation possible."
- In AI × Web3, inference must leave auditable records: which model was used, where inputs came from, what the output was, whether tools were triggered, and how failures were handled
