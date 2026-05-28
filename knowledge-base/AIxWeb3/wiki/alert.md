---
title: "Alert (Agent Security)"
type: concept
tags: [aixweb3-bridge, privacy-security, observability]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Alert detects anomalies in agent behavior and triggers timely interruption of automation. Alerts must be connected to response actions — detecting anomalies without responses has limited security value.

## Key Points

- Monitorable signals: abnormal tool call frequency, rapid budget consumption, non-whitelisted addresses, consecutive failed transactions, session key boundary violation attempts, large approvals, prompt injection hits
- Response actions: pause agent, revoke session keys, freeze escrows, notify user, enter human review
- Avoid over-disturbing users: low-risk anomalies enter background queue; only high-risk asset actions trigger immediate interruption
- Alerts that detect problems but don't respond are not security mechanisms — they're just logging

## Related Concepts

- [[ai-security]]
- [[audit-log]]
- [[revocation]]
- [[tool-abuse]]
- [[observability]]
- [[human-check]]

## Sources

- [[sources/bridge-chapters]]
