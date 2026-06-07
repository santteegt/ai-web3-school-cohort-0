# Risks and Fallbacks — GuildOS

> This document is a working file. Update the Decision Log as assumptions are validated or invalidated during the build.

---

## F1 — AgentFightClub Skill API Unavailable (HIGH)

**Why:** Alpha product; ClawBank dependency is an extra abstraction; no live test during pre-research.

**Impact:** Blocks treasury creation, governance, and settlement.

**Fallback:** Deploy Moloch v3 DAO directly via **DAOhaus SDK** (open source, audited, 4 years production). Same contract logic — `launch`, `commit`, `propose`, `vote`, `settle` map directly. Estimated recovery: 4 hours.

**Trigger:** If `launch` call fails or errors on Day 8, switch immediately. Do not debug ClawBank for more than 2 hours.

---

## F2 — ERC-8004 `giveFeedback()` Caller Constraint (HIGH)

**Why:** `giveFeedback()` caller CANNOT be the agent's own wallet — Sybil protection. The guild contract or Marco's EOA must be the caller.

**Impact:** `settle()` must complete before `giveFeedback()` is called, AND the caller must be set up correctly before demo day. If the Specialist calls it directly, the tx reverts silently.

**Fallback:** Route `giveFeedback()` through Marco's (human founder's) EOA wallet. Functionally equivalent — the on-chain `DeliveryRecorded` event is identical.

**Trigger:** If the first `giveFeedback()` call reverts, check `msg.sender` before assuming any deeper issue. If the issue is the caller, switch to Marco's EOA immediately.

---

## F3 — GLM-5.1 Output Inconsistent for Demo Task (MEDIUM)

**Why:** Long-horizon execution quality for niche technical tasks is unknown. First test may produce unstructured or incomplete output.

**Impact:** No real deliverable → no hash → "Specialist executes" step is hollow.

**Fallback:** Test 3 task types on Day 8 morning. If all fail, use a deterministic fallback: `"Write a Python function that computes SHA-256 of a given input and returns the hex digest."` Any capable model produces consistent, hashable output.

**Trigger:** Three failed GLM-5.1 attempts on Day 8 → lock in the deterministic fallback prompt.

---

## F4 — ZeroDev Session Keys — Python SDK Gap (MEDIUM)

**Why:** ZeroDev Python SDK is alpha with no session key support. TypeScript/Python interop adds a bridge layer with its own complexity.

**Impact:** Agent wallets run without per-task spending limits — the "controllable fund operations" claim for the Cobo track weakens.

**Fallback:** Use basic signing (no session key scoping) for the hackathon. Document the TypeScript session key config as a code exhibit in the README. The design is correct; the demo limitation is implementation time.

**Trigger:** If TypeScript bridge takes more than 3 hours on Day 9, fall back and document the design.

---

## F5 — A2A Metadata Extension Fields Rejected (LOW)

**Why:** A2A v1.0.0 may reject non-standard keys in `Message.metadata`. Pre-research rated GREEN but the gap exists.

**Impact:** Structured task handoff loses `budget_wei` and `deliverable_hash` as native message fields.

**Fallback:** Carry GuildOS-specific fields in the message `text` body as a JSON string. Parse on the receiving end.

**Trigger:** If Day 8 A2A test gate 3 or 4 fails on metadata validation, switch to text-body encoding immediately.

---

## F6 — Base Sepolia Congestion During Live Demo (LOW)

**Mitigation already designed in:** Pre-stage `propose` and `vote` steps before the live demo. Only `settle()`, hash commit, and `giveFeedback()` happen live. Have pre-recorded Basescan screenshots as a last resort.

**Trigger:** If any live tx takes more than 30 seconds, show the pre-recorded screenshot and note testnet latency.

---

## Tier B — Minimum Viable Demo

Apply **only** if three or more components fail simultaneously with no resolution path by EOD Day 11.

| Evidence | Tier B approach |
|----------|-----------------|
| A2A exchange | Orchestrator → Specialist message log (provable from logs without on-chain settlement) |
| On-chain hash | One `eth_sendTransaction` from Marco's EOA to a minimal deployed contract — no AgentFightClub, no ERC-8004 |
| GLM-5.1 evidence | Full execution trace terminal log |
| Design artifacts | Moloch v3 config, ERC-4337 session key policy, ERC-8004 reputation schema shown as code + diagrams |

Tier B **drops:** Treasury via AgentFightClub, formal governance, automated settlement, ERC-8004 reputation delta.

---

## Decision Log

| Date | Component | Result | Action |
|------|-----------|--------|--------|
| 2026-06-06 | Cobo CAW | ❌ Non-functional | Replaced with ZeroDev Kernel v3.3 |
| 2026-06-06 | ERC-8004 | ✅ Deployed; caller constraint documented | Proceed with EOA fallback for `giveFeedback()` |
| 2026-06-06 | A2A v1.0.0 | ✅ GREEN | Test Day 8; use text-body fallback if metadata fails |
| 2026-06-06 | ERC-8183 | ⚠️ No Base Sepolia deploy | Deferred post-hackathon |
| — | AgentFightClub | ⏳ Validate Day 8 | — |
| — | GLM-5.1 task type | ⏳ Validate Day 8 | — |
| — | ZeroDev session keys | ⏳ Validate Day 9 | — |

---

## Scope Creep Signals

If you find yourself doing any of these without an explicit decision, stop:

- Building a second specialist agent path — one pair is the demo
- Integrating Mem0 or LangChain memory — JSON file is the stub; ship it
- Querying the live ERC-8004 registry for real — hardcoded profile is correct
- Building any frontend UI — terminal windows are the demo surface
- Implementing ragequit on-chain — document the path only
- Deploying on mainnet — Base Sepolia tx hashes are credible
- Adding ERC-8183 — AgentFightClub settle is the payment story
