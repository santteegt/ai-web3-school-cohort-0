---
title: "TEE (Trusted Execution Environment)"
type: concept
tags: [aixweb3-bridge, verifiable-ai, privacy-security, frontier]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Trusted Execution Environment (TEE) isolates code and data and proves through attestation that a program ran in a specific, protected environment. It is suitable for scenarios requiring privacy with lower proof costs than ZK — private data scoring, model inference, agent runtime proof.

## Key Points

- Strength: relative engineering availability — runs complex programs, handles private inputs, lower proof cost than ZK
- Weakness: relies on hardware and supply chain trust (not pure cryptographic trust); hardware vulnerabilities, remote attestation services, runtime configurations all become trust assumptions
- Best for: "I cannot disclose input or model details, but I need to prove this program ran in a protected environment"
- TEE + signed logs is a practical hybrid for production proof-of-inference systems

## Related Concepts

- [[verifiable-ai]]
- [[proof-of-inference]]
- [[zk]]
- [[zkml]]
- [[ai-oracle]]
- [[attestation]]
- [[local-ai]]
- [[encrypted-data]]

## Sources

- [[sources/bridge-chapters]]
