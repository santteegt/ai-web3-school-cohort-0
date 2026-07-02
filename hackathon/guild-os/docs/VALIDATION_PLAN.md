# Validation Plan — GuildOS

> ⚠️ **PARTIALLY DEPRECATED 2026-06-30.** Sections 1–10 (per-integration
> definition-of-done) are superseded by the executable Given/When/Then
> assertions in [`specs/scenarios/*.feature`](../specs/scenarios/) — do not
> edit those sections here, update the relevant `.feature` file instead.
> **Section 11 (Hackathon Submission Requirements) is NOT deprecated** — it's
> an operational checklist tied to the external platform, not spec content,
> and remains directly authoritative. Issue
> [#17](https://github.com/santteegt/ai-web3-school-cohort-0/issues/17)
> still points here for it.

> Work through sections in order. Update Status: `[ ]` pending · `[x]` passed · `[!]` blocked / fallback triggered

---

## 1. Agent Wallets (Cobo CAW / Basic Signer) — Day 9 ✅ VALIDATED

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 1.1 | Orchestrator CAW wallet initialized on Base mainnet | Address printed; ETH balance > 0 (fund manually — no faucet on mainnet) | `[x]` |
| 1.2 | Specialist CAW wallet initialized on Base mainnet | Same | `[x]` |
| 1.3 | CAW Pact allowlists the DAO `propose`/`vote`/`process` calls and caps tribute | Pact config set; non-allowlisted call + over-cap tribute both refused at signature level | `[x]` |
| 1.4 | Allowlisted DAO call via CAW succeeds on Base mainnet | Tx hash returned; visible on https://basescan.org | `[x]` |
| 1.5 | Wallet layer is provider-agnostic (`WalletProvider`) | Same scoping holds when `WALLET_PROVIDER` swapped (CAW → ZeroDev/Turnkey) | `[ ]` |

Fallback: swap `WALLET_PROVIDER` to another scoped provider if CAW TSS node fails mid-build. **No EOA fallback** — agents never sign from a raw private key; halt until a scoped provider is restored.

---

## 2. AgentFightClub (Moloch v3) — Days 8–11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 2.1 | `launch()` — guild summoned on Base with name, governance settings, initial members+shares/loot | dao address + treasury address + Basescan tx hash | `[ ]` |
| 2.2 | `commit()` — treasury funded with tribute (≥ 0.001 ETH) | Tx hash; treasury balance readable | `[ ]` |
| 2.3 | `propose()` — Specialist membership proposal on-chain | Proposal ID; Basescan `ProposalSubmitted` event | `[x]` |
| 2.4 | `vote()` — Human founder approves | Tx hash; proposal state → `Passed` | `[x]` |
| 2.5 | `payment_propose()` — payment proposal raised after Gate 2 | `payment_proposal_id`+url saved to `guild_context.json`; carried in `task/accepted` | `[ ]` |
| 2.6 | `settle()` — process the passed payment proposal; funds released to Specialist | **Basescan tx #2**; Specialist balance increases | `[ ]` |
| 2.7 | `guild_context.json` updated after each phase | File readable; all fields present | `[ ]` |

Fallback: DAOhaus SDK direct Moloch v3 deploy if ClawBank API fails on Day 8.

---

## 3. ERC-8004 Registry — Days 9 and 11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 3.1 | Orchestrator ERC-8004 profile readable | JSON: `name`, `capabilities[]`, `a2a_endpoint`, `delivery_count` | `[ ]` |
| 3.2 | Specialist ERC-8004 **before-state** captured | Saved to `./logs/erc8004_specialist_before.json` | `[ ]` |
| 3.3 | Specialist triggers feedback via A2A `feedback/request`; Orchestrator submits `submitFeedback` proposal via `AgentFightClub.propose()` | Proposal ID returned; `reputation_proposal_id` saved to `guild_context.json` | `[ ]` |
| 3.4 | Human votes to approve reputation proposal (Gate 4) | Tx hash; `AgentFightClub.vote(reputation_proposal_id, approve=True)` confirmed | `[ ]` |
| 3.5 | `giveFeedback()` call succeeds after proposal passes | Tx hash; **Basescan tx #3** `DeliveryRecorded` event; saved to `submissions/tx_hashes.md` | `[ ]` |
| 3.6 | Specialist profile **after-state** shows +1 delivery | 6 fields present: task_type, hash, timestamp, wei, guild, a2a_id | `[ ]` |
| 3.7 | Before/after delta printable side-by-side for demo | CLI command or script outputs both states | `[ ]` |

Fallback: serve cached profile JSON if 8004scan API is down.

---

## 4. A2A Protocol — Day 9 (validated), Day 10 (full flow)

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 4.1 | Orchestrator `agentURI` resolves to valid A2A Agent Card JSON | `curl <agentURI>` returns card with `name`, `url`, `capabilities` | `[ ]` |
| 4.2 | Specialist Agent Card at `localhost:10001/.well-known/agent.json` | Same | `[ ]` |
| 4.3 | `task/invite` sent; Specialist receives and parses | Logged in A2A trace | `[x]` |
| 4.4 | `task/quote` received from Specialist | Fields: `scope`, `estimated_cost_wei`, `deadline_iso` | `[x]` |
| 4.5 | `task/send` delivered with full payload | Logged; message ID captured | `[x]` |
| 4.6 | `task/delivered` received with hash matching on-chain commit | Hash cross-check passes | `[x]` |
| 4.7 | `task/accepted` sent after human acceptance, carrying `payment_proposal_id` + url | Specialist receives confirmation with payment proposal reference | `[x]` |
| 4.8 | `feedback/request` sent by Specialist after settlement | Orchestrator receives; triggers reputation stage | `[ ]` |
| 4.9 | Full A2A trace log exported | `./logs/a2a_trace_{date}.json` with all message events (incl. `feedback/request`) | `[x]` |

Fallback: text-body JSON if `Message.metadata` extension fields are rejected.

---

## 5. EAS Deliverable Attestation — Day 10

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 5.1 | GLM-5.1 deliverable file produced | File in repo; non-zero size | `[ ]` |
| 5.2 | SHA-256 hash computed | Hash matches `deliverable_hash` in `task/delivered` message | `[ ]` |
| 5.3 | EAS attestation created via `EASClient.attest()` | Attestation UID returned (non-zero); tx visible on Basescan | `[ ]` |
| 5.4 | Attestation readable via SDK or easscan GraphQL | `eas.getAttestation(uid)` or `base.easscan.org/graphql` returns matching data | `[ ]` |
| 5.5 | Attestation UID embedded in A2A `task/delivered` message | Logged in `a2a_trace_{date}.json`; field `attestation_uid` present | `[ ]` |
| 5.6 | easscan attestation link navigable | **easscan attestation #1** — `https://base.easscan.org/attestation/{uid}` saved to `./logs/tx_hashes.md` | `[ ]` |

Prerequisite: `DELIVERY_SCHEMA_UID` registered once against SchemaRegistry `0x4200000000000000000000000000000000000020` on Base mainnet before Step 8.

---

## 6. GLM-5.1 Specialist Execution — Day 8 (task type lock), Day 10 (full run)

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 6.1 | GLM-5.1 API key configured and reachable | Test call returns response | `[ ]` |
| 6.2 | Demo task type locked | Decision noted in `docs/TECH_STACK.md` Decision Log; Hermes agent deployed Day 9 | `[x]` |
| 6.3 | Specialist reads the GitHub issue, then decomposes into ≥ 3-step plan within technical_constraints/AgBOM | Issue loaded; plan logged before execution | `[ ]` |
| 6.4 | All plan steps complete; structured output produced; hash per `deliverable_format` | Output written; BDD acceptance_criteria pass; hash (zip SHA-256 or commit) ready to attest | `[ ]` |
| 6.5 | Execution trace logged | `./logs/glm_trace_{date}.json` readable | `[ ]` |
| 6.6 | Orchestrator pre-check passes | Report: hash ✅ · format ✅ · size ✅ | `[ ]` |

Fallback: deterministic prompt "Write a Python function that computes SHA-256 of a given input and returns the hex digest" if all 3 task types fail on Day 8.

---

## 7. Orchestrator MCP Tools — Day 9–10

| # | Tool | Check | Status |
|---|------|-------|--------|
| 7.1 | `guild_launch` | Returns dao + treasury address matching check 2.1 | `[x]` stub |
| 7.2 | `talent_query` | Returns Specialist profile JSON (hardcoded) | `[x]` |
| 7.3 | `task_invite` | Sends A2A `task/invite`; message ID logged | `[x]` |
| 7.4 | `task_delegate` | Sends A2A `task/send` (full work order); message ID in trace (4.5) | `[x]` |
| 7.5 | `deliverable_review` | Returns `{hash_match, format_valid, size_check, evaluator_verdict}` | `[x]` |
| 7.6 | `payment_propose` | Returns `payment_proposal_id`+url; saved to `guild_context.json` (check 2.5) | `[ ]` |
| 7.7 | `settle` | Processes the passed payment proposal; returns settlement tx hash matching check 2.6 | `[ ]` stub |
| 7.8 | `reputation_propose` | Returns reputation proposal ID; saved to `guild_context.json` (check 3.3) | `[ ]` |
| 7.9 | `reputation_write` | Returns `DeliveryRecorded` tx hash after Gate 4 vote passes (check 3.5) | `[ ]` |

---

## 8. Human Gates — Day 10–11

| # | Gate | Check | Status |
|---|------|-------|--------|
| 8.1 | Gate 0 | ERC-8004 shortlist displayed; CLI halts; resumes only on `y` | `[ ]` |
| 8.2 | Gate 0.5 | Quote displayed; `Accept quote? [y/N]` halts execution | `[ ]` |
| 8.3 | Gate 1 | membership `vote` called only after human approves; rejection tested | `[x]` |
| 8.4 | Gate 2 | payment proposal raised only after human accepts deliverable | `[ ]` |
| 8.5 | Gate 3 | `settle()` processes the payment proposal only after human votes+processes it | `[ ]` |
| 8.6 | Gate 4 | `giveFeedback()` called only after human approves reputation proposal vote | `[ ]` |
| 8.7 | Dispute stub | Gate 2 (deliverable) or Gate 3 (payment) rejection → `task_state: DISPUTED` in JSON; no settlement tx | `[ ]` |

---

## 9. End-to-End Smoke Test — Day 11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 9.1 | Run 1: Full loop from fresh guild to settlement | Terminal output start → settlement tx | `[ ]` |
| 9.2 | Run 2: Different task input; same outcome | Confirms repeatability | `[ ]` |
| 9.3 | Both Basescan tx hashes clickable | (1) Hash commit · (2) Settlement — both resolve | `[ ]` |
| 9.4 | ERC-8004 before/after delta visible | Screenshot or terminal diff captured | `[ ]` |
| 9.5 | A2A trace exported with all message events (incl. `feedback/request`) | File present | `[ ]` |
| 9.6 | GLM-5.1 trace exported with plan + tool calls | File present | `[ ]` |

---

## 10. Submission Artifacts — Day 12

| # | Artifact | Location | Status |
|---|----------|----------|--------|
| 10.1 | README with problem, architecture, run instructions, SDK used | `README.md` | `[ ]` |
| 10.2 | Basescan tx #1 (hash commit) link in README | `submissions/tx_hashes.md` | `[ ]` |
| 10.3 | Basescan tx #2 (settlement) link in README | `submissions/tx_hashes.md` | `[ ]` |
| 10.4 | ERC-8004 before/after screenshots | `./logs/` | `[ ]` |
| 10.5 | CAW Pact config (live proof) | README §SDK Used | `[ ]` |
| 10.6 | GLM-5.1 trace log | `./logs/glm_trace_*.json` | `[ ]` |
| 10.7 | A2A trace log | `./logs/a2a_trace_*.json` | `[ ]` |
| 10.8 | Demo video (3–5 min) | Loom / YouTube link | `[ ]` |
| 10.9 | Team info (name, wallet, contact) | Submission form | `[ ]` |

---

## 11. Hackathon Submission Requirements (Casual Hackathon)

> Official requirements from the platform. Every item below must be satisfied before submitting the form on Day 13.

### 11.1 Project Identity

| # | Requirement | Where | Status |
|---|-------------|-------|--------|
| 11.1.1 | Project name: **GuildOS** | README title + submission form | `[ ]` |
| 11.1.2 | One-line introduction: *"A programmable studio where founding and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss."* | README subtitle + submission form | `[ ]` |

### 11.2 GitHub README — Required Sections

All sections must be present and complete in `README.md` before Day 13:

| # | Section | Notes | Status |
|---|---------|-------|--------|
| 11.2.1 | **Project background** — problem, why it matters, why AI + Web3 are both required | `docs/PROBLEM.md` is the source; summarise in README | `[ ]` |
| 11.2.2 | **Installation / run instructions** — prerequisites, `pip install`, env vars, two-terminal setup | Already drafted; verify against final working build | `[ ]` |
| 11.2.3 | **Core features** — guild formation, A2A task delegation, GLM-5.1 execution, hash commitment, settlement, ERC-8004 reputation | Add a Features section to README | `[ ]` |
| 11.2.4 | **Technical architecture** — swimlane or Mermaid diagram showing the 9-step flow; component map | Embed Mermaid or ASCII diagram from `docs/MVP_FLOW.md` | `[ ]` |
| 11.2.5 | **APIs / SDKs / AI tools used** — A2A SDK, GLM-5.1, Cobo CAW, AgentFightClub, ERC-8004, Alchemy, ZeroDev (design exhibit) | Expand existing SDK table in README | `[ ]` |
| 11.2.6 | **Third-party disclosures** — explicitly list all third-party APIs, SDKs, open-source code, and AI tools used | Add a dedicated "Third-Party Disclosures" section | `[ ]` |

### 11.3 Demo

| # | Requirement | Notes | Status |
|---|-------------|-------|--------|
| 11.3.1 | Demo link or demo video | Loom / YouTube; 3–5 min recommended | `[ ]` |
| 11.3.2 | Clear walkthrough of the core flow | Must show: mandate → A2A flow → GLM-5.1 output → hash on Basescan → settlement → ERC-8004 delta | `[ ]` |

### 11.4 Project Documentation / Proposal

| # | Requirement | Where | Status |
|---|-------------|-------|--------|
| 11.4.1 | **Problem** | `docs/PROBLEM.md` → link from README or embed | `[ ]` |
| 11.4.2 | **Solution** | README §Minimum Demo Loop or dedicated section | `[ ]` |
| 11.4.3 | **Target users** | `docs/PROBLEM.md §Target Users` → include in submission | `[ ]` |
| 11.4.4 | **Technical implementation** | `docs/TECH_STACK.md` + `docs/MVP_FLOW.md` → summarise in README or proposal doc | `[ ]` |
| 11.4.5 | **Current completion** | Add a "Completion Status" section to README with Mock vs. Real table from `docs/MVP_FLOW.md` | `[ ]` |
| 11.4.6 | **Follow-up plan** | Add "Post-Hackathon Roadmap" section — semantic ERC-8004 matching, Mem0 memory, multi-guild, web UI | `[ ]` |

### 11.5 On-Chain / Testnet Evidence

| # | Evidence | Location | Status |
|---|----------|----------|--------|
| 11.5.1 | Guild contract address | `submissions/tx_hashes.md` + README | `[ ]` |
| 11.5.2 | Basescan tx #1 — deliverable hash commit | `submissions/tx_hashes.md` + README (clickable) | `[ ]` |
| 11.5.3 | Basescan tx #2 — AgentFightClub settlement | `submissions/tx_hashes.md` + README (clickable) | `[ ]` |
| 11.5.4 | Orchestrator Agent wallet address (CAW) | `submissions/tx_hashes.md` | `[ ]` |
| 11.5.5 | Specialist Agent wallet address (CAW) | `submissions/tx_hashes.md` | `[ ]` |
| 11.5.6 | ERC-8004 agentId for both agents | `submissions/tx_hashes.md` + README | `[ ]` |
| 11.5.7 | ERC-8004 `DeliveryRecorded` event tx | `submissions/tx_hashes.md` | `[ ]` |
| 11.5.8 | Screenshots of Basescan pages for each tx | `./logs/screenshots/` | `[ ]` |

### 11.6 Compliance and Security Boundaries

Must be documented in README or a dedicated section:

| # | Requirement | Notes | Status |
|---|-------------|-------|--------|
| 11.6.1 | **Permission boundaries** — which actions are automated vs. human-gated | Document the 6 human gates (Gate 0, 0.5, 1, 2, 3, 4); reference `docs/MVP_FLOW.md §Automation Boundaries` | `[ ]` |
| 11.6.2 | **Failure handling** — what happens when a component fails | Reference `docs/RISKS.md` fallback table; summarise in README | `[ ]` |
| 11.6.3 | **Human intervention points** — when and why a human must approve | List all 6 gates with the action each gate blocks | `[ ]` |
| 11.6.4 | **Spending limits** — agent wallets do not have unconstrained fund access | Treasury is DAO-held; CAW Pact allowlists the DAO `propose`/`vote`/`process` calls and caps tribute; no EOA fallback | `[ ]` |

### 11.7 Hackathon Contribution Scope

| # | Requirement | Notes | Status |
|---|-------------|-------|--------|
| 11.7.1 | Clearly explain what is new work done during the hackathon | Add "What Was Built During the Hackathon" section — GuildOS is a new project; all code written Jun 8–12 | `[ ]` |
| 11.7.2 | Distinguish pre-existing components vs. hackathon-built integration | Pre-existing: AgentFightClub, ERC-8004, A2A SDK, GLM-5.1, ZeroDev. New: GuildOS coordination layer, MCP tools, A2A handlers, CLI gates, guild context store | `[ ]` |

### 11.8 Runnability

| # | Requirement | Notes | Status |
|---|-------------|-------|--------|
| 11.8.1 | Project is runnable from the README instructions | Do a clean-clone test before Day 13: fresh venv, follow README exactly | `[ ]` |
| 11.8.2 | Not a static presentation or mockup | Confirmed by smoke test × 2 (Section 9) and demo video (11.3) | `[ ]` |

### 11.9 Track Selection

| # | Requirement | Notes | Status |
|---|-------------|-------|--------|
| 11.9.1 | Primary track declared: **Cobo \| Agentic Economy × Cobo Agentic Wallet** | Strongest advantage — full economic loop: CAW wallets, treasury, settlement | `[ ]` |
| 11.9.2 | Secondary track eligibility documented: **Z.AI \| Web3 × Long-Horizon Task** | GLM-5.1 via Hermes; long-horizon trace log as evidence | `[ ]` |
| 11.9.3 | Track alignment section in README or proposal | `docs/TRACK.md` is the source — summarise in README or link directly | `[ ]` |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-30 | **§1** wallet checks reframed to DAO-call allowlist + tribute cap + provider-agnostic swap; no-EOA fallback. **§2** added `payment_propose` (2.5) and redefined `settle` as processing the passed payment proposal (2.6). **§3** reputation now Specialist-triggered (`feedback/request`); gate renumbered to **Gate 4**. **§4** added `feedback/request` check; `task/accepted` carries payment proposal id+url. **§6** adds issue-reading + format-conditional hash. **§7** added `payment_propose`; `settle`/`reputation_write` updated. **§8** gates renumbered to 0,0.5,1,2,3,4 with dispute reachable at Gate 2 or 3. **§11.6** documents 6 gates and DAO-held treasury scoping. Mirrors `specs/` design feedback. |
