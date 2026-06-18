# Product.md — A2A × EAS × ERC-8004 Reputation Loop PoC

> SevenD Level-1 | PoC scope only | Last updated: 2026-06-17

---

## Vision

Prove that three Web3/agent standards can interlink in a single coherent coordination workflow:

- **ERC-8004** — on-chain agent identity (register) and reputation (giveFeedback / getSummary)
- **A2A v1.0** — agent discovery, task delegation, structured delivery
- **EAS** — cryptographic proof-of-work attestation embedded in the A2A delivery artifact

The critical linking element: the EAS attestation UID is embedded inside the A2A delivery artifact so CLIENT can verify DEV's work before approving and before writing reputation.

---

## Backlog

| ID | Item | Status |
|----|------|--------|
| P-001 | Register CLIENT and DEV on ERC-8004 IdentityRegistry | ✅ Done |
| P-002 | A2A task delegation (CLIENT → DEV) + DEV A2A server | ✅ Done |
| P-003 | DEV attests deliverable hash via EAS; embeds UID in A2A artifact | ✅ Done |
| P-004 | CLIENT verifies EAS attestation, sends A2A "accepted" | ✅ Done |
| P-005 | DEV requests review via A2A; CLIENT calls ERC-8004 giveFeedback; getSummary 0→1 | ✅ Done |

---

## Acceptance Criteria (top items)

### P-001 — Register identities
- Both CLIENT and DEV addresses have called `IdentityRegistry.register(agentURI)` on Base Sepolia
- Both tx hashes are logged in RUN_LOG.md with basescan links
- DEV's agentURI encodes the A2A endpoint (`http://localhost:3001`)
- Both agentIds are non-zero; `tokenURI(agentId)` resolves to the registration JSON

### P-003 — EAS attestation embedded in A2A artifact
- Schema is registered on Base Sepolia SchemaRegistry; UID stored in RUN_LOG.md
- `eas.attest()` called by DEV signer; attestation UID embedded in A2A artifact `data.eas_attestation_uid`
- `eas.getAttestation(uid)` returns the attestation with correct `deliverableHash`
- Explorer link: `https://base-sepolia.easscan.org/attestation/view/<uid>` or on-chain fallback

### P-005 — Reputation delta
- Before `giveFeedback`: `getSummary(devAgentId, [clientAddress], 'code', '')` returns `count = 0`
- After `giveFeedback`: same call returns `count = 1`, `summaryValue = 100`
- `giveFeedback` tx hash logged in RUN_LOG.md with basescan link

---

## Design Decisions

### A2A SDK: @a2a-js/sdk (official) — adopted after initial custom implementation

The initial PoC used a hand-rolled Express + JSON-RPC 2.0 server (custom `dev-server.ts`) and raw `fetch` calls on the client side. This was replaced with the official [`@a2a-js/sdk`](https://www.npmjs.com/package/@a2a-js/sdk) (v0.3.x, Apache-2.0, published by Google).

| Criterion | Custom Express + fetch | @a2a-js/sdk (adopted) |
|-----------|----------------------|----------------------|
| Wire protocol correctness | ✅ manual JSON-RPC | ✅ SDK-managed |
| Task state management | ❌ hand-rolled in-memory map | ✅ `InMemoryTaskStore` |
| AgentCard discovery | ❌ manual fetch + parse | ✅ `ClientFactory.createFromUrl()` |
| Streaming / cancellation | ❌ not implemented | ✅ built-in |
| TypeScript types | ❌ local interfaces | ✅ `Task`, `Message`, `AgentCard`, `Part` |
| A2A spec alignment | ⚠️ happy path only | ✅ full spec compliance |

**Server pattern**: `AgentExecutor` interface → `execute(requestContext, eventBus)` → publish `Task`, `TaskArtifactUpdateEvent`, `TaskStatusUpdateEvent`, or a direct `Message`.
**Client pattern**: `ClientFactory.createFromUrl(url)` → auto-resolves agent card → `client.sendMessage(params)` returns `Task | Message`.
**Endpoint**: `/a2a/jsonrpc` (was `/a2a`). Agent card still at `/.well-known/agent-card.json`.

### ERC-8004 scaffold: create-8004-agent (reproduced by hand)

`npx create-8004-agent` is interactive-only (no headless mode). Structure reproduced manually. agent0-sdk rejected (v0.31 alpha; failed install due to missing `@babel/code-frame@^7.29.7`).

### agentURI strategy: `data:` URI (no hosting needed)
DEV's agentURI is a base64-encoded JSON containing the A2A endpoint. No IPFS or external hosting required for the PoC.

### EAS schema reuse: compute deterministic UID, check existence before registering
Schema UID = `keccak256(abi.encodePacked(schema, resolverAddress, revocable))`. If schema exists, reuse — never register twice.

### State persistence: `state.json` (gitignored)
Saves agentIds, schema UID, attestation UID, feedback tx hash between runs to enable idempotent re-runs.
