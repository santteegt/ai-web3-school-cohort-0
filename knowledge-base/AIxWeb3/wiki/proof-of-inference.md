---
title: "Proof of Inference"
type: concept
tags: [aixweb3-bridge, verifiable-ai, frontier]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Proof of Inference attempts to prove that an output definitely came from a specific model and input. Implementation paths include TEE attestation, ZK proof, signed logs, replayable inference, or trusted service proofs — each with different cost, privacy, verifiability, and engineering tradeoffs.

## Key Points

- What is being proven matters: input unchanged, model version, execution environment, output not tampered with, or entire calculation correct — these are different goals
- Full inference proof for large LLMs is currently very costly — real systems use compromises: TEE for environment, signed logs for I/O, ZK for critical post-processing, challenges for disputes
- "Strongest proof" not always best: signed logs may suffice for "this service returned this result"; TEE better for "came from specific binary + model"; ZK for minimal third-party trust
- Product documentation must clarify the exact object of proof

## Related Concepts

- [[verifiable-ai]]
- [[ai-oracle]]
- [[tee]]
- [[zk]]
- [[zkml]]
- [[attestation]]
- [[verifiable-compute]]
- [[audit-trail]]

## Sources

- [[sources/bridge-chapters]]
