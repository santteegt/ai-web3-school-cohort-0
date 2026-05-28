---
title: "Data Boundary"
type: concept
tags: [aixweb3-bridge, privacy-security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Data Boundary defines how data flows between user devices, application backends, model services, on-chain, and third-party tools. For every data field, ask: Is it necessary? Can it be de-identified? Can it be processed locally? Will it enter logs? Will it be sent to third-party models?

## Key Points

- Data boundaries should be drawn as data flow diagrams, not just long privacy policy texts
- Per-tool boundaries: data seen by browser tools, wallet tools, model tools, and indexing tools should not be shared by default
- Must account for: where user input is stored, where wallet addresses flow, who the model service provider is, how long logs are kept
- Core question: is each data item necessary for this specific task?

## Related Concepts

- [[ai-privacy]]
- [[minimal-disclosure]]
- [[local-ai]]
- [[permission-isolation]]
- [[user-consent]]
- [[private-memory]]
- [[secret-management]]

## Sources

- [[sources/bridge-chapters]]
