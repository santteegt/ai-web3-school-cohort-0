---
title: "Revocation"
type: concept
tags: [aixweb3-bridge, wallet-permission, security]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Revocation is the withdrawal of permissions from an agent — the ability to reclaim access at any time, by user action or automatically by the system. All automated permissions should have a closing entry point visible to the user.

## Key Points

- Revocation must be user-visible: show what permissions the agent currently has and provide a turn-off mechanism
- Automatic revocation triggers: session key expires, limit consumed, multiple transaction failures, anomalous target address detected, agent behavior deviates from task, user inactive for long time
- Designing authorization without revocation is incomplete; the most important part of permission design is how to reclaim it
- Revocation should not only happen on active user operations — the system can also tighten permissions automatically

## Related Concepts

- [[agent-wallet]]
- [[session-key]]
- [[policy]]
- [[guard]]
- [[cobo-pact]]
- [[user-control]]
- [[alert]]
- [[smart-account]]

## Sources

- [[sources/bridge-chapters]]
