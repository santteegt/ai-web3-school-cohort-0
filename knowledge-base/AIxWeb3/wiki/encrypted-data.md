---
title: "Encrypted Data"
type: concept
tags: [aixweb3-bridge, privacy-security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Encrypted Data can protect privacy during storage and transmission, but encryption alone doesn't automatically solve privacy during model inference — data usually needs to be decrypted or processed in a trusted environment during model inference.

## Key Points

- Encryption must combine with: access control, key management, TEE, and minimized context
- Key holder question changes trust model completely: platform vs. user vs. multi-party sharding vs. hardware
- "Encrypted on server but decrypted for every inference" = storage security only, not inference privacy
- For true inference privacy: combine encryption with TEE or ZK-based schemes

## Related Concepts

- [[ai-privacy]]
- [[tee]]
- [[data-boundary]]
- [[key-safety]]
- [[secret-management]]
- [[local-ai]]

## Sources

- [[sources/bridge-chapters]]
