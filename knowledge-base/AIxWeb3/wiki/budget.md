---
title: "Budget (Agent Payment)"
type: concept
tags: [aixweb3-bridge, payment-commerce, wallet-permission]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Budget is the maximum spending scope authorized by the user to the agent. It should not just exist in chat but must enter wallet policies, session keys, or backend ledgers. Without budget boundaries, there is no safe automatic payment.

## Key Points

- Layered budget design: global budget → task budget → single call limit → service provider limit → emergency stop conditions
- Setting only total budget without frequency or service-provider scope allows draining the budget through repeated abnormal calls
- Budget must answer: does this payment belong to the current task, is it within the authorized service scope, does it exceed frequency or amount limits?
- Budget precedes execution — no payment authority without defined limits

## Related Concepts

- [[machine-payment]]
- [[payment-intent]]
- [[policy]]
- [[session-key]]
- [[quote]]
- [[stablecoin-payment]]
- [[cobo-pact]]

## Sources

- [[sources/bridge-chapters]]
