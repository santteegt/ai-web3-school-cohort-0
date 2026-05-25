---
title: "Local Model"
type: concept
tags: [ai-foundations, llm, inference]
source_count: 1
date_updated: "2026-05-25"
---

## Definition

A local model is a language model deployed on infrastructure you control — running model weights directly on your hardware rather than through an API. This approach trades infrastructure burden for control over privacy, cost, customization, and offline availability.

## Key Points

- Fits scenarios with: high privacy requirements (user data cannot leave your infrastructure), cost sensitivity at high volume, offline operation requirements, or deep customization needs (fine-tuning, quantization, custom serving)
- Local deployment variables that affect output quality: model weights (which model family and size), VRAM (limits context window and batch size), context window, concurrency, quantization method, and inference framework (llama.cpp, vLLM, Ollama, etc.)
- Local inference does not automatically mean cheaper — hardware costs, engineering time, and operational burden must be factored in against API pricing
- Common misconception: a local model gives you "control" without specifying what control is needed for. Privacy control, cost control, version control, and output control are different — a local model helps with some and not others
- In AI × Web3: local models are attractive when user wallet data, transaction history, or private key information must not leave the user's device — but model capability tradeoffs must be validated against the quality standards required for on-chain actions

## Related Concepts

- [[inference]] — local model is one of two primary inference deployment modes
- [[maas]] — the API-based alternative to local model deployment
- [[quantization]] — the primary technique for making large models run on smaller local hardware
- [[model-serving]] — the serving infrastructure required for production local inference
- [[lora]] — fine-tuning technique commonly applied to open-source models in local deployments
- [[peft]] — parameter-efficient fine-tuning; relevant for teams adapting open-source local models

## Sources

- [[sources/inference]] — local model use cases, deployment variables, and quality considerations
