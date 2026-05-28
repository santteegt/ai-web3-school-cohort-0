---
title: "Local-first AI"
type: concept
tags: [aixweb3-bridge, privacy-security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Local-first AI prioritizes processing sensitive data locally, calling cloud models only when necessary and with minimized data. It is a hybrid architecture: local models for filtering, de-identification, and initial risk screening; cloud models receive only necessary summaries; final transactions still confirmed by wallet or smart account.

## Key Points

- Vitalik's vision: as AI moves wallet interfaces from "click and input" to "say the goal and let the bot complete it," local-first becomes critical for user devices to take on data protection and active defense
- Practical approach: local model extracts "3 transactions relevant to this task" → cloud model receives only that summary
- Local-first does not mean completely offline — it means reducing unnecessary data transmission by default
- Important for wallets: if AI accesses wallet, identity, and asset operations, local-first adds a data protection layer

## Related Concepts

- [[ai-sovereignty]]
- [[local-ai]]
- [[model-choice]]
- [[ai-privacy]]
- [[data-boundary]]
- [[minimal-disclosure]]

## Sources

- [[sources/bridge-chapters]]
