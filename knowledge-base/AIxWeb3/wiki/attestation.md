---
title: "Attestation"
type: concept
tags: [aixweb3-bridge, identity-reputation, verifiable-ai]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

An Attestation is a verifiable claim made by an entity about an agent, task, or result. The value depends on whether the issuer is trustworthy, whether the claim is specific, and whether it is revocable.

## Key Points

- Required fields: issuer, subject, claim, evidence, expiration, and revocation mechanism
- Attestations without expiration and revocation mechanisms can continue to mislead users after conditions change
- Can prove: "this agent passed a capability test," "this output came from a specific TEE environment," "a user confirmed task completion"
- Serves as foundational data for reputation rather than direct user-facing claims — systems aggregate multiple attestations but must allow users to view original evidence
- An attestation does not equal a correct result — it proves "who gave this result under what conditions"

## Related Concepts

- [[agent-trust-and-reputation]]
- [[reputation]]
- [[review]]
- [[did-vc]]
- [[tee]]
- [[proof-of-inference]]
- [[ai-oracle]]

## Sources

- [[sources/bridge-chapters]]
