# Ethereum Attestation Service (EAS) — Fit Analysis for GuildOS

> **Purpose:** Determine whether EAS fits GuildOS's reputation and deliverable verification needs, and whether it can improve on (or replace) the raw deliverable hash commitment in Step 8.
> **Created:** 2026-06-06
> **Sources verified:** EAS contracts README, EAS SDK README (GitHub), base.easscan.org/graphql (live check), PROTOTYPING_RESOURCES.md Section 7, PROJECT_PROPOSAL.md Sections 5–9

---

## TL;DR

EAS fits GuildOS **better than the proposal currently uses it** — but in a different role than described. The proposal scopes EAS as a late-priority read query (Day 4+) for third-party attestation enrichment. The analysis reveals a more valuable integration: **EAS should replace the raw deliverable hash `eth_sendTransaction` (Step 8)** with an EAS attestation, giving GuildOS a cryptographically signed, immediately queryable, chainable proof of delivery at the same gas cost. EAS should NOT replace ERC-8004 — it can't do agent identity or capability claiming, and the demo's primary proof point (ERC-8004 profile delta) requires 8004scan. EAS is one of the lowest-risk components in the stack: 100% test coverage, MIT license, deployed at a predictable address on Base Sepolia, live GraphQL API confirmed.

---

## Feature Coverage Matrix

| GuildOS Feature | EAS Operation / Field | Status | Notes |
|---|---|---|---|
| ERC-8004 profile read (identity, capabilities, endpoint) | ❌ Not in scope | ❌ Not supported | EAS is attestation-only; no identity schema. Use ERC-8004 + 8004scan for this. |
| Deliverable hash commitment on-chain (Step 8) | `eas.attest({schema, data: {recipient, data: encodedHash, ...}})` | ✅ Supported | **Better than raw tx**: signed by Specialist, queryable via easscan GraphQL, chainable via `refUID`. |
| Reputation write-back after acceptance (Step 12) | `eas.attest()` from guild contract or human, with `refUID` pointing to Step 8 attestation | ⚠️ Partial | EAS can write the acceptance record, but the ERC-8004 write-back (profile delta) is a separate and required operation. These are complementary, not alternatives. |
| Third-party trust signal read (Step 5 — human membership gate) | GraphQL query to `base.easscan.org/graphql` by recipient address | ✅ Supported | Query any attestations about the Specialist Agent. Enriches the trust display alongside ERC-8004 profile data. |
| Revocation of a delivery claim if dispute arises | `eas.revoke({schema, data: {uid}})` | ✅ Supported | Attester can revoke their own attestation; revocation timestamp is stored on-chain. |
| Chaining attestations (delivery → acceptance) | `refUID` field on `attest()` | ✅ Supported | The human acceptance attestation can reference the Specialist's delivery attestation UID, creating a traceable proof chain. |
| Off-chain attestation (store outside chain, timestamp on-chain) | `offchain.signOffchainAttestation()` + `eas.timestamp()` | ✅ Supported | Useful for storing verbose A2A message logs off-chain with an on-chain anchor. |
| Private / selective disclosure | `PrivateData` class — Merkle tree proof | ✅ Supported | Not needed for MVP, but relevant post-hackathon if delivery metadata is sensitive. |
| Delegated attestation (agent signs, relayer pays gas) | `eas.attestByDelegation()` | ✅ Supported | Useful if the Specialist Agent's wallet has no gas — orchestrator or relayer can pay. |
| ERC-8004 capability schema read | ❌ Not in scope | ❌ Not supported | No EAS schema covers agent capabilities. ERC-8004 is required. |
| Multi-attestation (batch) | `eas.multiAttest([...])` | ✅ Supported | Could batch the delivery hash + schema registration in one tx if needed. |

---

## Gaps and Alternatives

### Gap 1: Agent Identity and Capability Claiming

**GuildOS needs:** An on-chain agent profile with name, capabilities list, A2A endpoint, and delivery history — the "who is this agent" layer that feeds the human membership gate (Step 5).

**EAS provides:** Attestations about subjects — claims made by issuers. EAS has no built-in concept of an agent profile, capability schema, or A2A endpoint field.

**Delta:** Fundamental scope mismatch. EAS cannot fill this role.

**Alternative:** ERC-8004 is the correct tool. No replacement needed — EAS and ERC-8004 serve different layers and should coexist in GuildOS.

---

### Gap 2: ERC-8004 Reputation Write-Back (Step 12 Profile Delta)

**GuildOS needs:** After acceptance, the Specialist's ERC-8004 profile gains a new delivery record (task type, deliverable hash, acceptance timestamp, payment amount, guild address). This is the "before/after" demo proof point that judges will see.

**EAS provides:** EAS can write a GuildOS delivery attestation (attester = guild contract, recipient = Specialist Agent address, schema = custom delivery record). However, this does NOT update the ERC-8004 profile directly — it creates a separate attestation readable via easscan.

**Delta:** EAS write ≠ ERC-8004 profile update. Both can coexist: EAS as a second proof trail, ERC-8004 as the primary profile delta. For the hackathon, ERC-8004 write-back is required for the demo proof point. EAS write is optional enrichment.

**Alternative:** No change needed to ERC-8004 path. Consider adding an EAS attestation alongside as an additional Basescan-visible proof at no significant cost.

---

### Gap 3: Access Control on Who Can Attest About an Agent

**GuildOS needs:** Only the guild contract (or authorized parties) should be able to write reputation records about the Specialist Agent. Self-attestation should not count as verified reputation.

**EAS provides:** By default, ANY address can attest about ANY recipient. There is no enforced "only the guild contract can write about this agent" constraint in the base EAS contract.

**Delta:** Without a resolver contract, a malicious actor could attest fake deliveries about any agent. This is a real trust problem for reputation display.

**Mitigation:** Deploy a `SchemaResolver` that enforces `attester == guildContractAddress` before accepting attestations. This is a thin contract (1 function, extends `SchemaResolver.sol`). Buildable in under 2 hours. For the hackathon, acceptable to skip the resolver and attest from the known guild contract address only — the demo uses controlled addresses, not an open registry.

**Alternative for production:** Add a Merkle-proof-based allowlist resolver that accepts attestations only from registered guild contracts.

---

### Gap 4: GraphQL Query Structure (Open Question)

**GuildOS needs:** Query attestations by recipient (agent address) from easscan on Base Sepolia.

**EAS provides:** `https://base.easscan.org/graphql` is live (confirmed 200 OK). Typical query:

```graphql
{
  attestations(
    where: { recipient: { equals: "0xAGENT_ADDRESS" } }
    orderBy: [{ time: desc }]
    take: 10
  ) {
    id
    schema
    attester
    time
    revocationTime
    data
    decodedDataJson
  }
}
```

**Open question:** Whether Base Sepolia attestations are indexed at `base.easscan.org` or a separate testnet explorer URL. Need to verify on Day 1.

---

## The Underutilized Integration: EAS as Deliverable Hash Commitment

The proposal currently plans Step 8 as "one `eth_sendTransaction` to the guild contract" — a raw event emission. This works, but EAS provides a strictly better alternative at the same cost:

**Current plan:** Specialist calls `guild.commitDeliverable(deliverableHash)` → emits event → Basescan shows the tx.

**With EAS:** Specialist calls `eas.attest({schema: DELIVERY_SCHEMA_UID, data: {recipient: guildAddress, data: encodedHash}})` → emits `Attested` event → easscan shows the attestation with: attester (Specialist), recipient (guild), hash, timestamp, revocable flag.

**Why EAS is better for this:**
1. **Signed proof**: The attestation is signed by the Specialist's key (not just a tx from any wallet). It cryptographically proves the Specialist made this claim.
2. **Queryable by UID**: The attestation UID is a stable identifier that can be included in the A2A result message, the ERC-8004 delivery record, and the human review display — creating a traceable thread across all GuildOS layers.
3. **`refUID` chaining**: The human acceptance attestation (if added) references the delivery attestation UID → auditable causal chain: delivery → acceptance → settlement.
4. **easscan explorer**: Judges can navigate directly to `base.easscan.org/attestation/{uid}` and see all fields decoded — no ABI parsing needed. More demo-friendly than a raw Basescan event log.
5. **Same gas cost**: One `attest()` call costs roughly the same as one `eth_sendTransaction` to a guild contract.

**Schema design for delivery commitment:**

```solidity
// Register once before the hackathon:
string schema = "bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount";
// Revocable: false (delivery is permanent unless disputed)
// Resolver: address(0) for MVP, custom resolver post-hackathon
```

---

## Stability Assessment

| Dimension | Assessment |
|---|---|
| Contract maturity | **Production-ready.** 100% statement/branch/function/line test coverage (350 statements, 172 branches). MIT license. Deployed on Ethereum mainnet since 2022. |
| Base deployment | **Stable.** EAS at `0x4200000000000000000000000000000000000021` on both Base mainnet (v1.0.1) and Base Sepolia (v1.2.0). This is a predictable OP-stack address — unchanged across OP-compatible chains. |
| SDK | TypeScript/JavaScript. 136 stars, 453 commits, 5 open issues. Active maintenance. `npm install @ethereum-attestation-service/eas-sdk`. No alpha warnings. |
| easscan GraphQL | `base.easscan.org/graphql` confirmed live (200 OK). Standard GraphQL endpoint — no auth required for read queries. Pagination via `take`/`skip`. |
| Schema registration | Permanent: once registered, a schema UID is immutable. No version drift risk once deployed. |
| Known issues | None found. No CVEs in public disclosure. |
| Hackathon risk level | **LOW.** Lowest-risk component in the GuildOS stack. Contracts are audited and in production; SDK is stable; explorer is live. |

---

## Recommended Integration Path

**Phase 1 (Hackathon MVP — Days 1–2):**

Register the GuildOS delivery schema on Base Sepolia once:
```
bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount
```
Use this schema UID in all deliverable hash commits (Step 8). The attestation UID goes into: the A2A result message, the ERC-8004 delivery record `refUID`, and the demo UI "verify on easscan" link.

**Phase 2 (Hackathon MVP — Day 4+):**

Query `base.easscan.org/graphql` for any existing attestations about the Specialist Agent to enrich the Step 5 trust display. Show attester count, most recent attestation time, and whether any attestations have been revoked.

**Phase 3 (Post-hackathon):**

Add an acceptance attestation from the guild contract (via `attestByDelegation`) referencing the Specialist's delivery attestation UID via `refUID`. Deploy a resolver contract that rejects attestations from non-guild-contract addresses.

**What NOT to do:** Do not attempt to replace ERC-8004 with EAS. They serve different layers. ERC-8004 is the agent identity and capability standard. EAS is the open attestation transport. Use both.

---

## Day 1 Test Checklist

These 5 operations carry the most integration risk and must be validated before building the rest of the stack:

1. **Schema registration on Base Sepolia** — Register `bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount` on `0x4200000000000000000000000000000000000020`. Capture the schema UID. Verify it's queryable via `schemaRegistry.getSchema({uid})`. Fail here = nothing else works.

2. **Attest a delivery hash on Base Sepolia** — Call `eas.attest()` from the Specialist Agent's wallet using the schema UID. Confirm the returned attestation UID is non-zero and the tx appears on Basescan.

3. **Read the attestation back via SDK** — Call `eas.getAttestation(uid)` and verify all fields match what was submitted. Confirm `decodedDataJson` decodes correctly.

4. **Query via easscan GraphQL (Base Sepolia)** — Confirm the attestation is indexed and queryable by recipient address. Determine whether Base Sepolia uses `base.easscan.org` or a separate testnet URL. If a separate URL exists, update the demo UI config.

5. **`refUID` chain** — Create a second attestation referencing the first via `refUID`. Verify both attestations are linked and navigable on easscan. This validates the delivery → acceptance chain before building the full flow.

---

## Minimum Integration Sketch

### Step 8: Deliverable Hash Commitment (replaces raw `eth_sendTransaction`)

```typescript
import { EAS, SchemaEncoder, NO_EXPIRATION } from '@ethereum-attestation-service/eas-sdk';
import { ethers } from 'ethers';

// Base Sepolia addresses
const EAS_CONTRACT = '0x4200000000000000000000000000000000000021';
const DELIVERY_SCHEMA_UID = '0x<register once before hackathon>';

// Specialist Agent's signer
const specialistSigner = new ethers.Wallet(process.env.SPECIALIST_PRIVATE_KEY, provider);
const eas = new EAS(EAS_CONTRACT);
eas.connect(specialistSigner);

// Encode the deliverable data
const schemaEncoder = new SchemaEncoder(
  'bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount'
);
const encodedData = schemaEncoder.encodeData([
  { name: 'deliverableHash', value: deliverableHash, type: 'bytes32' },    // SHA-256 of the actual deliverable
  { name: 'taskType', value: 'audit', type: 'string' },                    // e.g. 'audit', 'code', 'analysis'
  { name: 'guildContract', value: guildContractAddress, type: 'address' },
  { name: 'paymentAmount', value: paymentAmountWei, type: 'uint256' }
]);

// Submit the attestation (Step 8)
const tx = await eas.attest({
  schema: DELIVERY_SCHEMA_UID,
  data: {
    recipient: guildContractAddress,   // Guild contract is the "receiver" of this delivery claim
    expirationTime: NO_EXPIRATION,
    revocable: false,                  // Delivery is permanent
    data: encodedData
  }
});
const deliveryAttestationUID = await tx.wait();
// deliveryAttestationUID goes into: A2A result message, ERC-8004 delivery record, demo UI
```

### Reading existing attestations for trust display (Step 5 enrichment)

```typescript
// Query easscan GraphQL for attestations about the Specialist Agent
const agentAddress = '0xSPECIALIST_AGENT_ADDRESS';

const query = `{
  attestations(
    where: {
      recipient: { equals: "${agentAddress}" }
      revocationTime: { equals: 0 }  // non-revoked only
    }
    orderBy: [{ time: desc }]
    take: 20
  ) {
    id
    schema
    attester
    time
    decodedDataJson
  }
}`;

const response = await fetch('https://base.easscan.org/graphql', {  // or base-sepolia equivalent
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query })
});

const { data } = await response.json();
const attestations = data.attestations;
// Filter for GuildOS delivery schema and display alongside ERC-8004 profile
```

### Schema registration (one-time, before hackathon Day 1)

```typescript
import { SchemaRegistry } from '@ethereum-attestation-service/eas-sdk';

const SCHEMA_REGISTRY = '0x4200000000000000000000000000000000000020'; // Base Sepolia
const schemaRegistry = new SchemaRegistry(SCHEMA_REGISTRY);
schemaRegistry.connect(deployerSigner);

const tx = await schemaRegistry.register({
  schema: 'bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount',
  resolverAddress: '0x0000000000000000000000000000000000000000', // No resolver for MVP
  revocable: false
});
await tx.wait();
// Log and hardcode the returned schema UID
```

---

## Ecosystem Alternatives (if EAS is unsuitable)

For completeness — though EAS has no significant gaps for GuildOS's scoped use:

| Alternative | Pros | Cons |
|---|---|---|
| **Sign Protocol** | More access control hooks, same attestation model | Less mature, smaller ecosystem, not pre-deployed on Base |
| **Verax** | Multi-module attestation design, richer queries | Deployed on Linea, not Base; would require cross-chain bridge |
| **Raw guild contract event** | Simplest, no external dependency | No explorer support, attester not cryptographically proven, no UID |
| **ERC-8183 escrow event** | Purpose-built for task/payment lifecycle | Draft standard, no live implementation confirmed on Base |

EAS wins on all dimensions relevant to GuildOS: Base deployment, stable SDK, easscan explorer, attestation UID as stable cross-reference, production maturity.

---

*Research date: 2026-06-06 | Agent: Sensei (Claude via Cowork)*
*Sources: ethereum-attestation-service/EAS-contracts README · ethereum-attestation-service/eas-sdk README · base.easscan.org/graphql (live) · hackathon/PROJECT_PROPOSAL.md · hackathon/PROTOTYPING_RESOURCES.md Section 7*
