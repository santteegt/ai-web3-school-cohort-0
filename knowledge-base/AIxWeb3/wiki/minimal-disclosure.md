---
title: "Minimal Disclosure"
type: concept
tags: [aixweb3-bridge, privacy-security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Minimal Disclosure is about exposing only the minimum information necessary to complete a task. It's both a technical principle and a product design principle — send only necessary fields, use ZK proofs, use one-time addresses, isolate identities by application, use summaries instead of original text.

## Key Points

- "Sufficient balance to pay 10 USDC" doesn't require exposing all holdings
- "User has permission" doesn't require revealing real identity
- "Transaction risks summary" doesn't require uploading full wallet history
- Most common implementation in AI products: "summary instead of raw data" — extract 3 relevant transactions, not the full history
- Principle applies at every data flow point: what the model sees, what tools receive, what logs store

## Related Concepts

- [[ai-privacy]]
- [[data-boundary]]
- [[local-ai]]
- [[zk]]
- [[user-consent]]
- [[ai-sovereignty]]

## Sources

- [[sources/bridge-chapters]]
