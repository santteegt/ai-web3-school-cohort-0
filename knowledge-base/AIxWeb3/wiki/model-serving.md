---
title: "Model Serving"
type: concept
tags: [ai-foundations, llm, inference]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

Model serving is the infrastructure layer that delivers language model responses in production — covering model loading, request queuing, batching, GPU utilization, token streaming, logging, monitoring, health checks, and scaling. It is what transforms a model from an offline artifact into a production service.

## Key Points

- A mature inference service must answer: (1) How are failed requests retried or degraded? (2) How are model versions rolled out gradually? (3) How are input/output logs redacted for privacy? (4) Should long requests enter a queue? (5) How are cost, latency, and error rate monitored?
- Request batching is the primary lever for GPU utilization efficiency — serving one request at a time wastes most GPU capacity on large models
- Token streaming (returning tokens as they are generated) is critical for UX in interactive applications — users perceive streaming responses as significantly faster than waiting for the full completion
- Version management in serving is non-trivial — rolling out a new model or prompt version without regressions requires gradual rollout, shadow testing, and clear rollback procedures
- In AI × Web3: serving logs must be treated as audit records — they are the evidence chain linking on-chain actions back to specific model decisions

## Related Concepts

- [[inference]] — serving is the production infrastructure for inference
- [[local-model]] — model serving frameworks (vLLM, Ollama, TGI) are the serving infrastructure for local models
- [[maas]] — API providers handle serving infrastructure; teams using MaaS still own request management, retries, and logging
- [[observability]] — serving metrics (latency, error rate, cost) are the primary inputs to production observability
- [[ai-agent-tracing]] — serving logs contribute to the agent execution audit trail
- [[quantization]] — affects hardware requirements and throughput in the serving layer

## Sources

- [[sources/inference]] — model serving components and production readiness checklist
