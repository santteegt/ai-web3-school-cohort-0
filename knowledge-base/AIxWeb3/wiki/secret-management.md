---
title: "Secret Management"
type: concept
tags: [aixweb3-bridge, privacy-security, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Secret Management handles private keys, API keys, session tokens, JWTs, wallet credentials, and encryption keys in agent systems. These secrets should never enter prompts, model outputs, regular logs, or analytics.

## Key Points

- When agents call services: use secrets via controlled tools, not let the model read them directly
- Rotation and revocation: can an API key be quickly replaced if leaked? Are session tokens short-lived? Are production keys isolated from test keys?
- In Web3: mnemonics and private keys should never appear in any agent prompt — even if users paste them voluntarily
- Extends to all credential types, not just private keys

## Related Concepts

- [[ai-privacy]]
- [[key-safety]]
- [[data-boundary]]
- [[permission-isolation]]
- [[session-key]]
- [[audit-log]]

## Sources

- [[sources/bridge-chapters]]
