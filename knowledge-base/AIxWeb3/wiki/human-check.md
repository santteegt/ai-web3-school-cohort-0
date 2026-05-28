---
title: "Human Check"
type: concept
tags: [aixweb3-bridge, wallet-permission, workflow]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Human Check is the user confirmation layer at key risk points in agent workflows. It is not about confirming every step, but about letting users understand and decide at points where asset changes, permission changes, or irreversible actions occur.

## Key Points

- Layered: low-risk reversible (auto-execute) → medium-risk (simulate first, then confirm) → high-risk irreversible (show impact, require confirmation) → policy violation (reject directly, don't ask)
- The real thing to confirm is not "do you want to sign" but: what will this action change, where is the risk, and why is confirmation needed now
- Users should see plain-language impact, not just hex calldata and a "Confirm" button
- High-risk actions include: signing, transfers, approvals, deployment, upgrades, governance voting, key handling

## Related Concepts

- [[human-in-the-loop]]
- [[agent-workflow]]
- [[agent-wallet]]
- [[simulation]]
- [[guard]]
- [[policy]]
- [[session-key]]

## Sources

- [[sources/bridge-chapters]]
