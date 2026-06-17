# Risks and Fallbacks — GuildOS

> This document is a working file. Update the Decision Log as assumptions are validated or invalidated during the build.

---

## F1 — AgentFightClub Skill API Unavailable (HIGH) ✅ CLEARED Day 9

**Status:** moloch-agent CLI confirmed working. Full flow tested Day 9: `summon` → `propose` → `vote` → `settle` all passing. `experiments/agent-fight-club/moloch_agent_test.py` is the live probe. This risk is substantially reduced. The `experiments/caw-afc-poc` demonstrates that tx execution can be forwarded to a CAW wallet by building DAO intents via moloch-agent with flags `--build-only --full`

---

## F2 — ERC-8004 `giveFeedback()` Caller Constraint (HIGH)

**Why:** `giveFeedback()` caller CANNOT be the agent's own wallet — Sybil protection. The guild contract (DAO) or Marco's EOA must be the caller.

**Impact:** `settle()` must complete → reputation proposal submitted → DAO vote passed → `giveFeedback()` called. All three preconditions must hold. If the Specialist calls it directly, the tx reverts silently.

**New flow (2026-06-17):** `giveFeedback()` is now gated behind a DAO proposal (`AgentFightClub.propose()` with reputation data payload) and a human vote (Gate 3). The caller of `giveFeedback()` is still the guild contract address or Marco's EOA — this constraint is unchanged.

**Fallback:** Route `giveFeedback()` through Marco's (human founder's) EOA wallet after the DAO vote. If the reputation proposal vote mechanism fails, call `giveFeedback()` directly post-`settle()` using Marco's EOA and note the governance step as a "design exhibit."

**Trigger:** If the reputation proposal vote tx reverts, check that `settle()` confirmed first. If `giveFeedback()` reverts, check `msg.sender` before assuming any deeper issue.

---

## F3 — GLM-5.1 Output Inconsistent for Demo Task (MEDIUM) ✅ CLEARED Day 9

**Status:** Z.AI track alignment reviewed Day 9. Hermes agent deployed as Specialist. Long-horizon task prompt built and locked. This risk is substantially reduced — Hermes + GLM-5.1 produces structured, hashable output for the locked task type.

**Fallback (still available):** If GLM-5.1 fails during build, use the deterministic fallback prompt: `"Write a Python function that computes SHA-256 of a given input and returns the hex digest."` Do not change the locked task type unless GLM-5.1 produces 3 consecutive unusable outputs.

---

## F4 — Agent Wallet Spending Limits (LOW) — ZeroDev replaced by CAW

**Status (updated 2026-06-08):** Cobo CAW restored as primary wallet after TSS local node restart. Full x402 pipeline confirmed working. ZeroDev Kernel v3.3 is **demoted to design exhibit only** — no longer on the critical path.

**Current approach:** CAW Pacts enforce per-task spending ceiling at the signature level — no TypeScript bridge required.

**Remaining risk:** CAW TSS node is local — a second crash requires the same restart. If the node goes down mid-build, restart it immediately; the API itself is stable.

**Fallback:** If CAW becomes permanently unavailable, use basic EOA signing (private key in env) and present ZeroDev session key config as the "intended architecture" code exhibit for Cobo track submission.

---

## F5 — A2A Metadata Extension Fields Rejected (LOW) ✅ CLEARED Day 9

**Status:** A2A coordination loop validated Day 9. All 5 gates passing. Metadata extension fields accepted without schema rejection. This risk is closed.

**Fallback (standby):** If metadata validation fails during real task flow (not the test), carry GuildOS-specific fields in the message `text` body as a JSON string. 15-minute fix — do not block on this.

---

## F6 — Base Mainnet Congestion During Live Demo (LOW)

**Network (updated 2026-06-08):** All on-chain operations run on **Base mainnet (chain_id 8453)** — AFC has no Base Sepolia support. Explorer: https://basescan.org

**Mitigation already designed in:** Pre-stage `propose` and `vote` steps before the live demo. Only `settle()`, EAS attestation, and `giveFeedback()` happen live. Have pre-recorded Basescan + easscan screenshots as a last resort. Pre-fund agent wallets with enough ETH before Day 10 build starts.

**Trigger:** If any live tx takes more than 30 seconds, show the pre-recorded screenshot and note network latency.

---

## F7 — EAS Schema Not Registered Before Demo (LOW)

**Why:** `EASClient.attest()` requires a registered schema UID (`DELIVERY_SCHEMA_UID`). If the schema is not registered on Base mainnet before Step 8, the `attest()` call will fail with a schema revert.

**Mitigation:** Register the GuildOS delivery schema **once** before Day 10 build begins:
```
schema:   "bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount"
resolver: 0x0000000000000000000000000000000000000000  (no resolver for MVP)
revocable: false
```
Hardcode the returned UID in `.env` as `DELIVERY_SCHEMA_UID`. Log the registration tx to `submissions/tx_hashes.md`.

**Fallback:** If `DELIVERY_SCHEMA_UID` is missing at runtime, fall back to raw `eth_sendTransaction` emitting a `DeliverableCommitted(bytes32 hash)` event — sufficient proof of hash commitment, but loses the stable UID and easscan explorer link.

**Trigger:** If `attest()` reverts with a schema-related error, verify `DELIVERY_SCHEMA_UID` in `.env` before debugging further.

---

## Tier B — Minimum Viable Demo

Apply **only** if three or more components fail simultaneously with no resolution path by EOD Day 11.

| Evidence | Tier B approach |
|----------|-----------------|
| A2A exchange | Orchestrator → Specialist message log (provable from logs without on-chain settlement) |
| EAS attestation | One `eth_sendTransaction` from Marco's EOA emitting a `DeliverableCommitted(bytes32 hash)` event — simpler than full EAS but still on-chain proof |
| GLM-5.1 evidence | Full execution trace terminal log |
| Design artifacts | Moloch v3 config, ERC-4337 session key policy, ERC-8004 reputation schema shown as code + diagrams |

Tier B **drops:** Treasury via AgentFightClub, formal governance, automated settlement, ERC-8004 reputation delta.

---

## Decision Log

| Date | Component | Result | Action |
|------|-----------|--------|--------|
| 2026-06-06 | Cobo CAW | ❌ Non-functional | Replaced with ZeroDev Kernel v3.3 |
| 2026-06-06 | ERC-8004 | ✅ Deployed; caller constraint documented | Proceed with EOA fallback for `giveFeedback()` |
| 2026-06-06 | A2A v1.0.0 | ✅ GREEN | Validated Day 9; text-body fallback on standby |
| 2026-06-06 | ERC-8183 | ⚠️ No Base mainnet deploy | Deferred post-hackathon |
| 2026-06-08 | Cobo CAW | ✅ **Restored** — TSS node restart | Primary wallet; ZeroDev demoted to design exhibit |
| 2026-06-08 | Network | ⚠️ **Base Sepolia → Base mainnet** | AFC has no Base Sepolia support; chain_id 8453 |
| 2026-06-09 | AgentFightClub | ✅ Full flow confirmed | launch → commit → propose → vote → settle all working |
| 2026-06-09 | A2A SDK v1.0.0 | ✅ All 5 gates validated | Metadata accepted; coordination loop working |
| 2026-06-09 | GLM-5.1 / Hermes | ✅ Specialist stack locked | Hermes agent deployed; long-horizon prompt locked |
| — | ZeroDev session keys | Demoted — design exhibit only | CAW handles spending limits via Pacts |
| 2026-06-11 | Deliverable hash commitment | ✅ **EAS attestation adopted** | Replaces raw `eth_sendTransaction`; Specialist signs attestation via EASClient; UID embedded in A2A result (see EAS_ANALYSIS.md) |

---

## Scope Creep Signals

If you find yourself doing any of these without an explicit decision, stop:

- Building a second specialist agent path — one pair is the demo
- Integrating Mem0 or LangChain memory — JSON file is the stub; ship it
- Deploying extra contracts beyond what the demo needs — Base mainnet, keep lean
- Adding ERC-8183 — AgentFightClub settle is the payment story
