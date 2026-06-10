# GuildOS — Risk & Assumption Memo

> Author: Sensei (Claude via Cowork) | Date: 2026-06-07 | Last updated: 2026-06-09  
> Deadline: 2026-06-13 12:00 UTC+8 (04:00 UTC)  
> Status: Active build sprint — Day 9 of 13 · All core integrations validated · **Build starts Day 10**

---

## Purpose

This memo surfaces the assumptions the demo depends on, the most likely failure points given what we learned during pre-research, and the concrete fallback plan if components are unavailable on demo day. It is a working document: update it as assumptions are validated or invalidated during the build.

---

## 1. Core Assumptions

These are statements the project treats as true. If any prove false, the build path changes.

### A1 — AgentFightClub API is callable from Python ✅ VALIDATED 2026-06-09

**What we assumed:** The AgentFightClub Skill API (ClawBank) accepts authenticated requests, exposes `launch`, `commit`, `propose`, `vote`, and `settle` as callable endpoints, and returns deterministic results within the demo window.

**Result:** ✅ Full flow test passing as of Day 9. `experiments/agent-fight-club/moloch_agent_test.py` executes the complete sequence: launch → commit → propose → vote → settle. Proposal sponsorship timing issue (identified Day 8) is resolved. Assumption holds.

---

### A2 — ERC-8004 registry is live and writable on Base Sepolia

**What we assume:** The IdentityRegistry (`0x8004A818BFB912233c491871b3d84c89A494BD9e`) and ReputationRegistry (`0x8004B663056A597Dffe9eCcC1965A193B7388713`) are deployed, indexed, and accept `register()` and `giveFeedback()` calls from a non-owner wallet (guild contract or human wallet — required by Sybil protection).

**Evidence for:** Contracts confirmed deployed on Base Sepolia; mainnet live since 2026-01-29; 209 stars, 85 forks.

**Evidence against:** `getSummary()` requires a non-empty `clientAddresses` list — must scan `NewFeedback` events first; 8004scan API availability is unconfirmed.

**Key gotcha:** `giveFeedback()` caller CANNOT be the agent's own wallet. The guild contract or Marco's wallet must be the caller. This affects the settlement→reputation sequence: `settle()` must complete before `giveFeedback()` is called, and the caller must be set up correctly before demo day.

**Validation step:** Day 1 — call `register(agentURI)` for both agents; confirm ERC-721 agentId minted. Cache the response.

---

### A3 — A2A SDK v1.0.0 supports the GuildOS message pattern ✅ VALIDATED 2026-06-09

**What we assumed:** `pip install "a2a-sdk[http-server]"` installs a working server; `SendMessage` delivers structured task messages; `Artifact` with a `DataPart` carries the deliverable hash without schema rejection.

**Result:** ✅ A2A coordination loop validated Day 9. All 5 gates passing (agent card, send, quote, deliver, accept). Metadata extension fields accepted without schema rejection. Assumption holds.

---

### A4 — GLM-5.1 produces usable structured output for the chosen task type ✅ VALIDATED 2026-06-09

**What we assumed:** For at least one of the three pre-selected task types, GLM-5.1 via the Z.AI API produces consistent, structured output that can be hashed and presented as a credible deliverable.

**Result:** ✅ Z.AI track alignment reviewed Day 9. Hermes agent instance deployed as the Specialist Agent. Long-horizon task prompt built and locked for the demo. Assumption holds — Hermes + GLM-5.1 produces structured, hashable output for the selected task type.

---

### A5 — Cobo CAW enforces per-task spending limits ✅ UPDATED 2026-06-08

**Original assumption:** ZeroDev Kernel v3.3 session keys would handle agent wallet scoping (ZeroDev was chosen after CAW appeared broken on 2026-06-06).

**Updated (2026-06-08):** Cobo CAW is restored as the primary wallet. TSS local node restart resolved the signing failure. Full x402 pipeline confirmed working end-to-end. ZeroDev Kernel is demoted to design exhibit / fallback only.

**Current assumption:** CAW Pact API enforces per-task spending ceiling; TSS node remains stable for the build window (June 8–13).

**Evidence for:** x402 + CAW pipeline live-tested and passing on 2026-06-08.

**Evidence against:** CAW TSS node is local — a second failure would require the same restart. No redundancy.

**Validation step:** ✅ Day 1 confirmed. Monitor TSS node stability; restart immediately if signing fails again.

---

### A6 — Base mainnet RPC is stable and finalizes within demo timing ✅ UPDATED 2026-06-08

**Original assumption:** Base Sepolia RPC provides sub-10-second finality for the demo sequence.

**Updated (2026-06-08):** Network is now **Base mainnet (chain_id 8453)**. AFC moloch-agent has no Base Sepolia support — no contracts, no service, no subgraph deployed. All on-chain operations move to Base mainnet.

**Implication:** Real ETH required on Base mainnet for agent wallets and guild treasury. Gas costs are real (not testnet). Pre-fund agent wallets before Day 9 build.

**Evidence for:** Base mainnet is a production L2; Alchemy supports it; Basescan.org is the explorer.

**Evidence against:** Real gas costs add complexity; pre-funding agent wallets requires manual steps before build begins.

**Mitigation baked in:** Pre-stage governance steps (propose + vote) before live demo. Fund wallets Day 9 morning. Budget: ~0.01 ETH total should cover all demo transactions.

---

## 2. Most Likely Failure Points

Ranked by probability × impact, based on pre-research findings.

### F1 — AgentFightClub Skill API is unavailable or broken (HIGH risk)

**Why likely:** Alpha product; no live test performed during pre-research; ClawBank dependency is an extra abstraction layer that may have its own availability SLA.

**Impact:** Blocks on-chain treasury creation, governance, and settlement — the economic core of the demo.

**Fallback:** Deploy Moloch v3 DAO directly via the DAOhaus SDK. Open source, audited, 4 years in production. Same contract logic; ClawBank is a convenience wrapper, not a protocol dependency. Estimated recovery time: 4 hours to deploy + test.

**Trigger:** If `launch` call fails or returns an error on Day 1, switch immediately. Do not debug ClawBank for more than 2 hours.

---

### F2 — ERC-8004 `giveFeedback()` caller constraint breaks the settlement→reputation sequence (HIGH risk)

**Why likely:** The caller-cannot-be-owner rule is a known gotcha from research. The settlement flow assumes the Orchestrator (or guild contract) calls `giveFeedback()` after `settle()`. If the guild contract address isn't set as an authorized caller, the tx reverts silently.

**Impact:** Reputation write-back fails. The before/after ERC-8004 delta — one of the two key judge-facing verification proofs — is missing.

**Fallback:** Route `giveFeedback()` through Marco's (human founder's) EOA wallet directly. Less elegant but functionally equivalent. The on-chain event is identical.

**Trigger:** If the first `giveFeedback()` call reverts, check msg.sender vs. agent owner before assuming any deeper issue.

---

### F3 — GLM-5.1 output is inconsistent or unusable for the demo task (MEDIUM risk)

**Why likely:** Long-horizon execution is not instant; model may time out, produce unstructured output, or fail on the first demo task type tested.

**Impact:** No real task output → no deliverable hash → the "Specialist executes" step of the demo is hollow.

**Fallback:** Switch task type on Day 1 based on test results. If all three candidate types fail, use a deterministic code-generation prompt (e.g., "Write a Python function that computes SHA-256 of a given input and returns the hex digest") where any capable model produces consistent output. The hash of that output is still a valid on-chain commit.

**Trigger:** Three failed GLM-5.1 attempts on Day 1 → lock in the deterministic fallback prompt.

---

### F4 — ZeroDev Python SDK alpha drops session key support mid-build (MEDIUM risk)

**Why likely:** Alpha SDKs break. The Python SDK has no session key policies — only basic signing. If the TypeScript bridge is harder to wire than expected, agent wallets run without spending limits.

**Impact:** The "controllable fund operations" claim for the Cobo track weakens. Settlement still works (smart account can call `settle()`), but the scoping argument loses its strongest evidence.

**Fallback:** For the hackathon MVP, use the Python SDK for basic signing (no session key scoping) and document the TypeScript session key config as the intended production architecture. The design is correct; the demo limitation is implementation time. Present the session key policy config code as a code exhibit alongside the demo.

**Trigger:** If TypeScript bridge takes more than 3 hours on Day 2, fall back and document the design.

---

### F5 — A2A metadata extension fields rejected by strict schema validation (LOW risk)

**Why likely:** A2A v1.0.0 is stable but strict schema validators may reject non-standard keys in `Message.metadata`. Pre-research rated this GREEN but the gap is real.

**Impact:** A2A messages cannot carry budget or deliverable hash fields natively. Cross-agent communication still works, but the structured task handoff loses semantic richness.

**Fallback:** Carry all GuildOS-specific fields in the message `text` body as a JSON string. Parse on the receiving end. Less elegant but zero schema risk.

**Trigger:** If the Day 1 A2A test gate 3 or 4 fails on metadata validation, switch to text-body encoding immediately.

---

### F6 — Base Sepolia congestion causes tx to time out during live demo (LOW risk)

**Why likely:** Testnet congestion is unpredictable; demo timing is fixed.

**Impact:** `settle()` or deliverable hash commit hangs. Judges see a spinner.

**Mitigation (already designed in):** Pre-stage all governance steps before the demo. Only three transactions happen live: deliverable hash commit, `settle()`, and `giveFeedback()`. Have pre-recorded Basescan screenshots as a last resort.

**Trigger:** If any live tx takes more than 30 seconds, show the pre-recorded screenshot and note testnet latency.

---

## 3. Week 4 Fallback Plan

> "Week 4" = the final build days (2026-06-10 through 2026-06-12) plus submission day (2026-06-13).

The fallback plan has two tiers. Tier A preserves the full demo loop with degraded components. Tier B is the minimum viable demo that still passes the judge evaluation criteria.

---

### Tier A — Degraded Components, Full Demo Loop Intact

Apply when one or two components are unavailable but the core loop (fund → delegate → execute → hash → settle → reputation) can still run end-to-end.

| Component unavailable | Substitution |
|---|---|
| AgentFightClub Skill API | Direct Moloch v3 via DAOhaus SDK |
| Cobo CAW | ZeroDev Kernel (already primary path) |
| ERC-8004 8004scan API | Cached JSON profile file; direct contract reads |
| GLM-5.1 for task X | Deterministic fallback prompt (SHA-256 generator) |
| ZeroDev session keys | Basic signing, design documented as code exhibit |

Tier A still produces two clickable Basescan tx hashes and an ERC-8004 reputation delta. All judge evaluation criteria are met.

---

### Tier B — Minimum Viable Demo

Apply only if three or more components fail simultaneously — an unlikely but possible scenario given the alpha/draft status of multiple dependencies.

**What Tier B demonstrates:**

1. **A2A message exchange** — Orchestrator sends a structured task message; Specialist returns a result with a deliverable hash. Both agents log every message. The A2A exchange is provable from logs even without on-chain settlement.

2. **On-chain deliverable hash** — One `eth_sendTransaction` directly from Marco's EOA wallet commits the SHA-256 hash of the Specialist's output to a minimal deployed contract on Base Sepolia. No AgentFightClub, no ERC-8004, no session keys — just a hash on chain with a Basescan tx link.

3. **GLM-5.1 execution log** — The Specialist's full execution trace (prompt → plan → tool calls → output) is shown in the terminal. The output itself is the deliverable.

4. **Design artifact** — The Moloch v3 treasury config, ERC-4337 session key policy, and ERC-8004 reputation schema are presented as code and diagrams. "This is what is deployed; this is what breaks when X is unavailable" is a valid technical narrative for judges who can read a contract.

**What Tier B drops:** Treasury funded via AgentFightClub, formal governance (propose/vote), automated settlement, and the ERC-8004 reputation delta.

**When to invoke Tier B:** If, by the end of Day 11 (2026-06-11 EOD), AgentFightClub and ERC-8004 writes are both failing with no resolution path, switch to Tier B. Do not attempt to build around both simultaneously in the final 48 hours.

---

## 4. Decision Log

Track assumption validation and fallback triggers here as the build progresses.

| Date | Component | Result | Action taken |
|---|---|---|---|
| 2026-06-06 | Cobo CAW | ❌ Non-functional | Replaced with ZeroDev Kernel |
| 2026-06-06 | ERC-8004 | ✅ Deployed, gotchas documented | Use with caller constraint workaround |
| 2026-06-06 | A2A v1.0.0 | ✅ GREEN | Proceed; test Day 9 morning |
| 2026-06-06 | ERC-8183 | ⚠️ Too new, no Base Sepolia deploy | Deferred post-hackathon as planned |
| 2026-06-08 | Cobo CAW | ✅ **Restored** — TSS node restart fixed signing | CAW is primary wallet again; ZeroDev demoted to design exhibit |
| 2026-06-08 | AgentFightClub | ✅ Functional — probe script live | `experiments/agent-fight-club/moloch_agent_test.py` runs; timing issue with proposal sponsorship being fixed Day 9 |
| 2026-06-08 | Network | ⚠️ **Base Sepolia → Base mainnet** | AFC has no Base Sepolia support (no contracts, no subgraph); all on-chain ops move to Base mainnet (chain_id 8453) |
| 2026-06-09 | AgentFightClub | ✅ **Full flow confirmed** | Complete sequence working: launch → commit → propose → vote → settle; timing issue resolved |
| 2026-06-09 | A2A SDK v1.0.0 | ✅ **Coordination loop validated** | All 5 gates passing; metadata fields accepted; no schema issues |
| 2026-06-09 | GLM-5.1 / Hermes | ✅ **Specialist stack locked** | Hermes agent deployed; Z.AI track alignment reviewed; long-horizon task prompt locked |
| — | ZeroDev session keys | Demoted — design exhibit only | CAW restored; ZeroDev no longer on critical path |

---

*Last updated: 2026-06-08 | Agent: Sensei*
