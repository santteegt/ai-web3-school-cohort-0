---
title: "Inference"
type: concept
tags: [ai-foundations, llm, inference]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Inference is the production layer of an AI system — the process of delivering model outputs to users under real constraints of latency, cost, context, quality, privacy, and operational complexity. Inference connects upstream components (models, prompts, RAG, agents) to downstream interfaces (queues, caches, monitoring, UX).

## Key Points

- "Inference is a combined choice across latency, cost, context, stability, quality, privacy, operational complexity, and deployment boundaries" — no single dimension can be optimized in isolation
- The inference layer determines how model capability is consumed by the product; a great model with a poorly designed inference layer produces a poor product
- Three key principles: (1) **Quality has a cost** — stronger models mean higher cost, longer latency, or more complex deployment; (2) **Deployment changes boundaries** — API models reduce infrastructure burden, local models give more control; (3) **Services should be replaceable** — clear model-call encapsulation makes fallback, rollout, and evaluation possible
- The two primary deployment modes: [[maas]] (API models) and [[local-model]] (self-hosted weights)
- Production inference engineering problems that don't disappear with API models: rate limits, timeouts, retries, log redaction, billing control, version changes, output regression
- In AI × Web3: the inference service must leave auditable records — which model, what inputs, what output, which tools triggered, how failures were handled

## Related Concepts

- [[maas]] — API-based inference; the primary mode for most production AI products
- [[local-model]] — self-hosted inference for privacy, cost, or customization
- [[quantization]] — technique for making inference cheaper on smaller hardware
- [[model-serving]] — infrastructure layer for production inference at scale
- [[ai-agent-tracing]] — inference records are part of the agent audit trail
- [[context-window]] — inference latency and cost scale with context window size
- [[large-language-model]] — inference is the consumption layer for LLM capabilities
- [[observability]] — inference logs are the raw material for observability

## Sources

- [[sources/inference]] — inference definition, tradeoffs, deployment modes, and AI × Web3 audit requirements
