---
title: "Local AI"
type: concept
tags: [aixweb3-bridge, privacy-security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Local AI places part of the inference on the user's device or in a private environment to reduce the transmission of sensitive data. Suitable for: processing private documents, summarizing wallet history, generating drafts, and sensitive classification.

## Key Points

- Principle: filter and de-identify locally first, then send only necessary summaries to more powerful cloud models
- Example: extract "3 transactions related to this task" from wallet history locally, not upload the entire history
- Local does not mean absolutely safe: local agents can still be attacked by malicious files, plugins, or web pages — sandboxing and permission control still required
- "Local-first" does not mean completely offline; it means reducing unnecessary data transmission by default

## Related Concepts

- [[ai-privacy]]
- [[local-first-ai]]
- [[data-boundary]]
- [[ai-sovereignty]]
- [[minimal-disclosure]]
- [[sandbox]]

## Sources

- [[sources/bridge-chapters]]
