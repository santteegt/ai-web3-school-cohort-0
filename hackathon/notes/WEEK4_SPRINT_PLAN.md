# GuildOS — Week 4 Sprint Plan

> Build window: **2026-06-08 (Mon) → 2026-06-13 12:00 UTC+8 (submission)**  
> Network: **Base mainnet (chain_id 8453)** — AFC has no Base Sepolia support  
> Wallet: **Cobo CAW** (TSS local node restored; x402 pipeline confirmed working 2026-06-08)  
> Team: Solo (Santiago)  
> Deadline: **2026-06-13 12:00 UTC+8 (04:00 UTC)**  
> Reference: [SCOPE_REVIEW.md](SCOPE_REVIEW.md) · [RISK_ASSUMPTION_MEMO.md](RISK_ASSUMPTION_MEMO.md) · [TECHNICAL_VALIDATION_PLAN.md](TECHNICAL_VALIDATION_PLAN.md)
>
> **⚠️ Network change (2026-06-08):** All "Base Sepolia" references in this plan now mean **Base mainnet**. Explorer: https://basescan.org. Real ETH required — pre-fund agent wallets Day 9 morning before build starts.

---

## Week Overview

| Day | Date | Theme | P0 Gate |
|---|---|---|---|
| Day 8 | Mon Jun 8 | **Validation** — confirm all live integrations pass or trigger fallbacks | AgentFightClub `launch` live · A2A test suite green · GLM-5.1 task type locked |
| Day 9 | Tue Jun 9 | **Wallets + Identity** — agent wallets operational, ERC-8004 agents registered, guild funded | Both agent addresses on-chain · Guild funded with mandate |
| Day 10 | Wed Jun 10 | **A2A + Execution** — full A2A flow + GLM-5.1 task + deliverable hash on-chain | `task/delivered` received · Hash committed to Base Sepolia · Basescan tx #1 saved |
| Day 11 | Thu Jun 11 | **Settlement + Reputation + End-to-End** — close the loop | `settle()` tx · ERC-8004 delta visible · Full loop smoke test passes |
| Day 12 | Fri Jun 12 | **Demo Prep + Evidence** — README, submission artifacts, demo script | Repo submission-ready · All Basescan tx hashes saved |
| Day 13 | Sat Jun 13 | **Submission** — demo video + form submit | Submitted before 12:00 UTC+8 |

---

## Day 8 — Monday, June 8 · Validation Day ✅ COMPLETE

**Theme:** Before writing integration code, confirm every live dependency actually works. Make fallback decisions before noon so the rest of the week builds on solid ground.

### Results Summary

| Task | Result | Decision |
|---|---|---|
| **CAW wallet** | ✅ Restored — TSS node restart fixed signing; x402 pipeline end-to-end working | **CAW is primary wallet** — ZeroDev demoted to design exhibit |
| **AgentFightClub** | ✅ Functional — probe script at `experiments/agent-fight-club/moloch_agent_test.py` | ClawBank API live; timing issue with proposal sponsorship → fix Day 9 |
| **Network** | ⚠️ **Base Sepolia → Base mainnet** — AFC has no Base Sepolia support | All on-chain ops move to Base mainnet (chain_id 8453) |
| **A2A + GLM-5.1** | ⏳ Deferred to Day 9 morning | Day 8 scope filled by CAW/AFC validation |

### Day 8 Deliverables — Status

- [x] AgentFightClub decision: ✅ live API (ClawBank) — timing issue fix in progress
- [x] Wallet decision: ✅ Cobo CAW (not ZeroDev)
- [x] Network decision: ✅ Base mainnet
- [ ] A2A test suite → **moved to Day 9 morning**
- [ ] GLM-5.1 task type locked → **moved to Day 9 morning**
- [ ] Repo scaffold → carry to Day 9

---

## Day 9 — Tuesday, June 9 · Wallets + Identity + A2A/GLM ✅ COMPLETE

**Theme:** Integration validation complete. All three core stacks validated. Project build starts Day 10.

### Validation Results

| Integration | Result | Notes |
|---|---|---|
| **AFC full flow** | ✅ Working | launch → commit → propose → vote → settle; timing issue resolved |
| **A2A coordination loop** | ✅ Working | All 5 gates passing; metadata extension fields accepted |
| **GLM-5.1 / Hermes** | ✅ Locked | Hermes agent deployed as Specialist; Z.AI track alignment confirmed; long-horizon task prompt locked |

### Day 9 Deliverables — Status

- [x] AFC full flow: ✅ confirmed working (`experiments/agent-fight-club/moloch_agent_test.py`)
- [x] A2A: ✅ coordination loop working, all 5 gates pass
- [x] GLM-5.1 demo task type: ✅ locked (Hermes agent + long-horizon prompt)
- [ ] ERC-8004 agent registration → **carry to Day 10**
- [ ] Guild launch + fund → **carry to Day 10**
- [ ] Repo scaffold → **carry to Day 10**

### What Carries to Day 10

Day 10 opens with ERC-8004 `register()` for both agents and guild formation before the A2A+execution flow begins. All integration dependencies are now confirmed — no blockers.

---

## Day 10 — Wednesday, June 10 · Setup + A2A + Execution

**Theme:** Start with ERC-8004 agent registration and guild formation (carried from Day 9), then run the full A2A conversation. GLM-5.1/Hermes executes the locked demo task. Deliverable is hashed and committed to chain. End-of-day: Basescan tx #1 (deliverable hash) is in hand.

**Day 10 morning priority (before A2A):** Pre-fund agent wallets · `ERC-8004.register()` for both agents · AFC `launch` + `commit` + `propose` + `vote` (Gate 1) · Save `erc8004_specialist_before.json`

### Morning (4h): A2A flow + GLM-5.1 execution

| Task | Real or Mock | Evidence |
|---|---|---|
| Orchestrator sends A2A `task/invite` to Specialist | **Real** | Logged in A2A trace; Specialist receives and parses |
| Specialist responds with A2A `task/quote` (scope, `estimated_cost_wei`, `deadline_iso`) | **Real** | Quote logged; Orchestrator surfaces to human. **Gate 0.5**: CLI `Accept quote? [y/N]` |
| Orchestrator sends A2A `task/send` (full task: description, input, acceptance criteria, deadline, budget) | **Real** | Full payload logged; message ID captured |
| Specialist decomposes task into ≥3-step plan using GLM-5.1 | **Real** | Plan logged before execution begins |
| GLM-5.1 executes task (multi-step; tool use loop) | **Real** | Output file written; structured and non-empty |
| Execution trace logged | **Real** | Save to `hackathon/notes/glm_trace_<date>.json` |
| Specialist computes SHA-256 of deliverable | **Real** | Hash string printed and confirmed |

### Afternoon (3h): On-chain hash + A2A delivery

| Task | Real or Mock | Evidence |
|---|---|---|
| Specialist sends SHA-256 hash to guild contract via `eth_sendTransaction` (Base Sepolia) | **Real** | **Basescan tx #1** — deliverable hash commit. Save to `submissions/tx_hashes.md` |
| Contract storage read: confirm hash is readable post-commit (`eth_call`) | **Real** | Returned hash matches Specialist's value |
| Specialist sends A2A `task/delivered` to Orchestrator (deliverable reference + hash) | **Real** | Message logged; hash in message matches on-chain hash |
| Orchestrator automated pre-check: hash present ✅ · format valid ✅ · size > 0 ✅ | **Real (minimal)** | Pre-check report printed |
| Orchestrator presents deliverable + pre-check report to human. **Gate 2**: `Accept deliverable? [y/N]` | **Real** | CLI prompt halts; execution waits |
| Export A2A trace log | **Real** | Save `hackathon/notes/a2a_trace_<date>.json` (all 7 message events) |

### Day 10 Deliverables

- [ ] **Basescan tx #1**: deliverable hash commit link — saved to `submissions/tx_hashes.md`
- [ ] `a2a_trace_<date>.json` — all 7 A2A events present
- [ ] `glm_trace_<date>.json` — plan + tool calls + output visible
- [ ] Deliverable file in repo (non-zero, structured output)
- [ ] Pre-check report: all three checks passing

### What is Mocked Today

- Third-party evaluator agent: Orchestrator's pre-check covers hash + format only. Full evaluator is post-hackathon.
- Multiple task iterations: single task, single round-trip. Parallelism is out of scope.

---

## Day 11 — Thursday, June 11 · Settlement + Reputation + End-to-End

**Theme:** Close the loop. Human accepts. Payment released. ERC-8004 reputation written. Full smoke test. End-of-day: Basescan tx #2 (settlement) in hand and the before/after ERC-8004 delta is visible.

### Morning (4h): Settlement + reputation write-back

| Task | Real or Mock | Evidence |
|---|---|---|
| On Gate 2 acceptance: Orchestrator sends A2A `task/accepted` to Specialist | **Real** | Message logged; closes A2A transaction loop |
| Orchestrator calls AgentFightClub `settle(guild_address, specialist_wallet)` | **Real** | **Basescan tx #2** — treasury release. Save to `submissions/tx_hashes.md` |
| Confirm Specialist wallet balance increased by expected amount | **Real** | `eth_getBalance` before/after diff |
| Orchestrator calls `ERC-8004.giveFeedback()` with 6 fields: task_type, deliverable_hash, acceptance_timestamp, payment_wei, guild_address, a2a_task_id | **Real** | Basescan `DeliveryRecorded` event emitted |
| **Caller note**: `giveFeedback()` must be called from Marco's EOA or the guild contract — NOT from the Specialist wallet. Verify caller before submitting. | — | If it reverts → switch to Marco's EOA (F2 fallback) |
| Capture Specialist ERC-8004 **after-state** | **Real** | Save to `hackathon/notes/erc8004_specialist_after.json` |
| Generate before/after delta (side-by-side CLI output or script) | **Real** | Confirm: delivery_count +1, all 6 fields present |
| Update `guild_context.json`: `task_state: SETTLED` | **Real (JSON file)** | — |

### Afternoon (3h): Dispute stub + smoke test

| Task | Real or Mock | Evidence |
|---|---|---|
| Implement dispute stub: Gate 2 rejection path sets `task_state: DISPUTED` in `guild_context.json` | **Stub** — JSON only. No ragequit call executed. | `guild_context.json` shows `DISPUTED` state |
| Document ragequit exit path in README (Moloch v3 ragequit is standard; cite DAOhaus docs) | **Documentation only** | — |
| **Full loop smoke test (Run 1)**: fresh guild, fresh agents, full sequence start to finish | **Real** | Terminal output from mandate → settlement → reputation delta |
| **Full loop smoke test (Run 2)**: different task input | **Real** | Confirms repeatability |
| Confirm two primary Basescan tx hashes clickable: (1) deliverable hash · (2) settlement | **Real** | Both resolve on Basescan |

### Day 11 Deliverables

- [ ] **Basescan tx #2**: AgentFightClub settlement link — saved to `submissions/tx_hashes.md`
- [ ] `erc8004_specialist_after.json` committed to `hackathon/notes/`
- [ ] Before/after delta: delivery_count delta + all 6 fields visible
- [ ] Smoke test Run 1: passes end-to-end
- [ ] Smoke test Run 2: passes (different input)
- [ ] Dispute stub: `DISPUTED` state in JSON confirmed

### What is Mocked Today

- Ragequit execution: documented only, no on-chain call.
- Multiple guild members: architecture supports N; demo confirms 2.
- Semantic capability matching: hardcoded pair throughout.

### Tier B Trigger Point

> If by **EOD Day 11** AgentFightClub AND ERC-8004 writes are both failing with no resolution path, switch to Tier B (A2A + raw hash commit + GLM-5.1 trace as demo surface). Do not attempt to fix both in the final 48 hours. See `RISK_ASSUMPTION_MEMO.md §3` for Tier B scope.

---

## Day 12 — Friday, June 12 · Demo Prep + Evidence Assembly

**Theme:** Nothing new is built. The code is done. Today is about making the work legible to judges and assembling every submission artifact.

### Morning (3h): README + run instructions

| Task | Output |
|---|---|
| Write `README.md`: problem statement, architecture diagram (text or Mermaid), run instructions, API/SDK used | Submission-ready README |
| Add Mermaid swimlane or ASCII architecture diagram (9-step flow from proposal) | Embedded in README |
| Document two primary Basescan tx hashes prominently in README | Clickable links |
| Document ERC-8004 before/after delta in README (or link to JSON files) | Judge-readable |
| Document Cobo CAW / ZeroDev session key config (or fallback design exhibit) | Cobo track requirement |
| Document GLM-5.1 long-horizon run evidence (link to `glm_trace_*.json`) | Z.AI track evidence |

### Afternoon (3h): Demo script + submission evidence

| Task | Output |
|---|---|
| Write demo script (2 pages): what to say at each step, which terminal to show, pre-staged steps checklist | `hackathon/notes/DEMO_SCRIPT.md` |
| Create `submissions/tx_hashes.md`: all Basescan links, agent wallet addresses, ERC-8004 agentIds | Submission artifact |
| Pre-stage the demo: run the membership proposal + vote steps so only the final 3 txs happen live | State saved in `guild_context.json` |
| Fallback evidence assembled: pre-recorded Basescan screenshots for each critical tx | `hackathon/notes/screenshots/` |
| Final git status: `git add . && git commit -m "Week 4 build complete — submission ready" && git push` | Clean repo on GitHub |

### Day 12 Deliverables

- [ ] `README.md` with architecture, run instructions, SDK evidence, tx hashes
- [ ] `hackathon/notes/DEMO_SCRIPT.md`
- [ ] `submissions/tx_hashes.md` complete
- [ ] Pre-staged demo state ready (guild live, proposal passed, ready to delegate)
- [ ] All fallback screenshots saved
- [ ] Repo pushed and clean

### What is Mocked Today

Nothing new is mocked today. The scope is locked.

---

## Day 13 — Saturday, June 13 · Submission (≤ 12:00 UTC+8)

**Theme:** Record, submit, done.

| Task | Deadline |
|---|---|
| Record demo video (3–5 min): show mandate → A2A flow → GLM-5.1 output → hash commit on Basescan → settlement → ERC-8004 delta | Before 10:00 UTC+8 |
| Fill Casual Hackathon submission form: project name, description, GitHub link, demo link, tx hashes, team info | Before 11:30 UTC+8 |
| Santiago reviews and confirms payload before submitting | **Manual submission — Sensei does NOT auto-submit** |
| Post-submission: save confirmation link/ID to `submissions/` | After submit |

**Submission deadline: 2026-06-13 12:00 UTC+8 (04:00 UTC). No late submissions accepted.**

---

## Mock vs. Real — Full Week Summary

| Component | Status for Demo | Fallback |
|---|---|---|
| AgentFightClub `launch` + `commit` | **Real** | DAOhaus SDK direct deploy |
| AgentFightClub `propose` + `vote` + `settle` | **Real** | Same fallback |
| ERC-8004 register + before/after read | **Real** | Cached JSON if 8004scan down |
| ERC-8004 reputation write-back (6 fields) | **Real** | Route via Marco's EOA if guild contract reverts |
| A2A task flow (all 7 message events) | **Real** | Text-body JSON if metadata rejected |
| GLM-5.1 long-horizon task execution | **Real** | Deterministic fallback prompt |
| On-chain deliverable hash commit | **Real** | Always real — one `eth_sendTransaction` |
| Cobo CAW spending limit | **Real** — Pact-scoped per-task ceiling | ZeroDev session key policy as design exhibit only |
| Human gate CLI prompts (Gates 0, 0.5, 1, 2) | **Real** | — |
| Orchestrator automated pre-check | **Real (minimal)** | — |
| ERC-8004 talent query / shortlist | **Mocked** — hardcoded Specialist profile | — |
| Guild context store | **Mocked** — JSON file per session | — |
| Multiple concurrent guild members | **Mocked** — one agent pair | — |
| Third-party evaluator agent | **Mocked** — Orchestrator hash + format check | — |
| Dispute ragequit on-chain call | **Stub** — `DISPUTED` state in JSON only | — |
| Polished web UI | **Cut** — two terminal windows | — |
| Persistent shared memory (Mem0 / LangChain) | **Cut** — JSON file | — |

---

## Daily Scope Creep Checks

Before ending each day, confirm none of these are in progress:

- [ ] Building a second specialist agent path (one pair is the demo)
- [ ] Integrating Mem0 or LangChain memory (JSON is the stub — ship it)
- [ ] Querying the live ERC-8004 registry for real (hardcoded profile is correct)
- [ ] Building any frontend UI (terminal is the demo surface)
- [ ] Implementing ragequit on-chain (document only)
- [ ] Deploying extra contracts beyond what the demo strictly needs (Base mainnet, keep it lean)

---

## If Things Slip: Priority Order

If time pressure forces cuts, drop in this order:

1. **Drop last**: Two Basescan tx hashes (deliverable hash + settlement) — judges must be able to click these.
2. **Drop last**: ERC-8004 reputation delta (before/after) — second key verification proof.
3. **Drop before those**: ZeroDev session keys → fall back to design exhibit.
4. **Drop before those**: A2A quote round-trip (Gate 0.5) → collapse into a single task/send if needed.
5. **Never drop**: GLM-5.1 real execution (Z.AI track requires it); on-chain hash commit; AgentFightClub settle.

---

*Sprint Plan v1.0 · 2026-06-07 · Agent: Sensei (Claude via Cowork)*  
*Sources: PROJECT_PROPOSAL.md v1.2 · SCOPE_REVIEW.md · RISK_ASSUMPTION_MEMO.md · TECHNICAL_VALIDATION_PLAN.md*
