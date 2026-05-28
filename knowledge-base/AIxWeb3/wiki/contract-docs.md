---
title: "Contract Docs"
type: concept
tags: [web3-foundations, aixweb3-bridge, context]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Contract Docs help the model understand the design intent, parameter meanings, permission boundaries, and usage patterns of a contract. An ABI only tells you function signatures, not business semantics — documentation, NatSpec, READMEs, and audit reports fill the semantic gaps.

## Key Points

- `execute(bytes calldata data)` could be a normal execution or a high-permission entry point — only docs clarify which
- Documentation can expire: after reading docs, an Agent must still verify with on-chain data (address, version, owner, proxy implementation, events, recent transactions)
- Audit reports and deployment instructions are also part of contract docs
- Docs are auxiliary context; on-chain state is the authoritative fact

## Related Concepts

- [[chain-aware-context]]
- [[on-chain-data]]
- [[abi]]
- [[contract-read]]
- [[malicious-context]]

## Sources

- [[sources/bridge-chapters]]
