# Validation Plan — GuildOS

> Work through sections in order. Update Status: `[ ]` pending · `[x]` passed · `[!]` blocked / fallback triggered

---

## 1. Agent Wallets (ZeroDev / Basic Signer) — Day 9

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 1.1 | Orchestrator wallet initialized on Base Sepolia | Address printed; ETH balance > 0 (faucet) | `[ ]` |
| 1.2 | Specialist wallet initialized on Base Sepolia | Same | `[ ]` |
| 1.3 | ZeroDev session key restricts Orchestrator to AgentFightClub contract only | Out-of-scope call rejected → screenshot | `[ ]` |
| 1.4 | `eth_sendTransaction` via wallet succeeds for a no-op testnet call | Tx hash returned; visible on Basescan | `[ ]` |

Fallback: basic signing (private key in env) if ZeroDev bridge > 3h. Document session key policy as code exhibit.

---

## 2. AgentFightClub (Moloch v3) — Days 8–11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 2.1 | `launch()` — guild deployed on Base Sepolia with mandate string | Contract address + Basescan tx hash | `[ ]` |
| 2.2 | `commit()` — treasury funded (≥ 0.001 ETH) | Tx hash; treasury balance readable | `[ ]` |
| 2.3 | `propose()` — Specialist membership proposal on-chain | Proposal ID; Basescan `ProposalSubmitted` event | `[ ]` |
| 2.4 | `vote()` — Human founder approves | Tx hash; proposal state → `Passed` | `[ ]` |
| 2.5 | `settle()` — payment released to Specialist wallet | **Basescan tx #2**; Specialist balance increases | `[ ]` |
| 2.6 | `guild_context.json` updated after each phase | File readable; all fields present | `[ ]` |

Fallback: DAOhaus SDK direct Moloch v3 deploy if ClawBank API fails on Day 8.

---

## 3. ERC-8004 Registry — Days 9 and 11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 3.1 | Orchestrator ERC-8004 profile readable | JSON: `name`, `capabilities[]`, `a2a_endpoint`, `delivery_count` | `[ ]` |
| 3.2 | Specialist ERC-8004 **before-state** captured | Saved to `hackathon/notes/erc8004_specialist_before.json` | `[ ]` |
| 3.3 | `giveFeedback()` call succeeds after `settle()` | Tx hash; Basescan `DeliveryRecorded` event | `[ ]` |
| 3.4 | Specialist profile **after-state** shows +1 delivery | 6 fields present: task_type, hash, timestamp, wei, guild, a2a_id | `[ ]` |
| 3.5 | Before/after delta printable side-by-side for demo | CLI command or script outputs both states | `[ ]` |

Fallback: serve cached profile JSON if 8004scan API is down.

---

## 4. A2A Protocol — Day 8 (gates), Day 10 (full flow)

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 4.1 | Orchestrator Agent Card at `localhost:10000/.well-known/agent.json` | `curl` returns valid A2A card | `[ ]` |
| 4.2 | Specialist Agent Card at `localhost:10001/.well-known/agent.json` | Same | `[ ]` |
| 4.3 | `task/invite` sent; Specialist receives and parses | Logged in A2A trace | `[ ]` |
| 4.4 | `task/quote` received from Specialist | Fields: `scope`, `estimated_cost_wei`, `deadline_iso` | `[ ]` |
| 4.5 | `task/send` delivered with full payload | Logged; message ID captured | `[ ]` |
| 4.6 | `task/delivered` received with hash matching on-chain commit | Hash cross-check passes | `[ ]` |
| 4.7 | `task/accepted` sent after human acceptance | Specialist receives confirmation | `[ ]` |
| 4.8 | Full A2A trace log exported | `hackathon/notes/a2a_trace_{date}.json` with 7 events | `[ ]` |

Fallback: text-body JSON if `Message.metadata` extension fields are rejected.

---

## 5. On-Chain Deliverable Hash — Day 10

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 5.1 | GLM-5.1 deliverable file produced | File in repo; non-zero size | `[ ]` |
| 5.2 | SHA-256 hash computed | Hash matches what Specialist sends in `task/delivered` | `[ ]` |
| 5.3 | Hash committed to guild contract | **Basescan tx #1** saved to `../../submissions/tx_hashes.md` | `[ ]` |
| 5.4 | Contract storage confirms hash readable | `eth_call` returns matching value | `[ ]` |

---

## 6. GLM-5.1 Specialist Execution — Day 8 (task type lock), Day 10 (full run)

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 6.1 | GLM-5.1 API key configured and reachable | Test call returns response | `[ ]` |
| 6.2 | Demo task type locked | Decision noted in `docs/TECH_STACK.md` Decision Log | `[ ]` |
| 6.3 | Task decomposed into ≥ 3-step plan | Plan logged before execution | `[ ]` |
| 6.4 | All plan steps complete; structured output produced | Output file written; format matches acceptance criteria | `[ ]` |
| 6.5 | Execution trace logged | `hackathon/notes/glm_trace_{date}.json` readable | `[ ]` |
| 6.6 | Orchestrator pre-check passes | Report: hash ✅ · format ✅ · size ✅ | `[ ]` |

Fallback: deterministic prompt "Write a Python function that computes SHA-256 of a given input and returns the hex digest" if all 3 task types fail on Day 8.

---

## 7. Orchestrator MCP Tools — Day 9–10

| # | Tool | Check | Status |
|---|------|-------|--------|
| 7.1 | `guild_launch` | Returns guild contract address matching check 2.1 | `[ ]` |
| 7.2 | `talent_query` | Returns Specialist profile JSON (hardcoded) | `[ ]` |
| 7.3 | `task_invite` | Sends A2A `task/invite`; message ID logged | `[ ]` |
| 7.4 | `task_delegate` | Sends A2A `task/send`; message ID in trace (4.5) | `[ ]` |
| 7.5 | `deliverable_review` | Returns `{hash_match, format_valid, size_check, evaluator_verdict}` | `[ ]` |
| 7.6 | `settle` | Returns settlement tx hash matching check 2.5 | `[ ]` |
| 7.7 | `reputation_write` | Returns `DeliveryRecorded` tx hash matching check 3.3 | `[ ]` |

---

## 8. Human Gates — Day 10–11

| # | Gate | Check | Status |
|---|------|-------|--------|
| 8.1 | Gate 0 | ERC-8004 shortlist displayed; CLI halts; resumes only on `y` | `[ ]` |
| 8.2 | Gate 0.5 | Quote displayed; `Accept quote? [y/N]` halts execution | `[ ]` |
| 8.3 | Gate 1 | `vote` called only after human approves; rejection tested | `[ ]` |
| 8.4 | Gate 2 | `settle()` called only after human accepts deliverable | `[ ]` |
| 8.5 | Dispute stub | Gate 2 rejection → `task_state: DISPUTED` in JSON; no settlement tx | `[ ]` |

---

## 9. End-to-End Smoke Test — Day 11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 9.1 | Run 1: Full loop from fresh guild to settlement | Terminal output start → settlement tx | `[ ]` |
| 9.2 | Run 2: Different task input; same outcome | Confirms repeatability | `[ ]` |
| 9.3 | Both Basescan tx hashes clickable | (1) Hash commit · (2) Settlement — both resolve | `[ ]` |
| 9.4 | ERC-8004 before/after delta visible | Screenshot or terminal diff captured | `[ ]` |
| 9.5 | A2A trace exported with 7 events | File present | `[ ]` |
| 9.6 | GLM-5.1 trace exported with plan + tool calls | File present | `[ ]` |

---

## 10. Submission Artifacts — Day 12

| # | Artifact | Location | Status |
|---|----------|----------|--------|
| 10.1 | README with problem, architecture, run instructions, SDK used | `README.md` | `[ ]` |
| 10.2 | Basescan tx #1 (hash commit) link in README | `submissions/tx_hashes.md` | `[ ]` |
| 10.3 | Basescan tx #2 (settlement) link in README | `submissions/tx_hashes.md` | `[ ]` |
| 10.4 | ERC-8004 before/after screenshots | `hackathon/notes/` | `[ ]` |
| 10.5 | ZeroDev session key config (live or code exhibit) | README §SDK Used | `[ ]` |
| 10.6 | GLM-5.1 trace log | `hackathon/notes/glm_trace_*.json` | `[ ]` |
| 10.7 | A2A trace log | `hackathon/notes/a2a_trace_*.json` | `[ ]` |
| 10.8 | Demo video (3–5 min) | Loom / YouTube link | `[ ]` |
| 10.9 | Team info (name, wallet, contact) | Submission form | `[ ]` |
