---
title: "Key Safety"
type: concept
tags: [aixweb3-bridge, privacy-security, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Key Safety ensures that private keys, API keys, session keys, JWTs, and payment credentials never enter the model context, outputs, regular logs, or analytics. If agents need to execute on-chain, they do so indirectly through wallet tools, smart accounts, session keys, or backend signing services.

## Key Points

- Bottom line: secrets do not enter prompts, model outputs, regular logs, or analytics
- Even temporary session keys must be limited in amount, time, target, and method
- If an agent needs to operate on behalf of a user: use Smart Account policies or session keys instead of EOA private keys in automation runtime
- In Web3: mnemonics and private keys should never appear in any agent prompt — even if a user pastes them voluntarily, the system should recognize and refuse to process them

## Related Concepts

- [[ai-security]]
- [[secret-management]]
- [[permission-isolation]]
- [[session-key]]
- [[agent-wallet]]
- [[sandbox]]
- [[audit-log]]

## Sources

- [[sources/bridge-chapters]]
