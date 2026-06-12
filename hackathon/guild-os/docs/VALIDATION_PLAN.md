# Validation Plan — GuildOS

> Work through sections in order. Update Status: `[ ]` pending · `[x]` passed · `[!]` blocked / fallback triggered

---

## 1. Agent Wallets (Cobo CAW / Basic Signer) — Day 9 ✅ VALIDATED

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 1.1 | Orchestrator CAW wallet initialized on Base mainnet | Address printed; ETH balance > 0 (fund manually — no faucet on mainnet) | `[x]` |
| 1.2 | Specialist CAW wallet initialized on Base mainnet | Same | `[x]` |
| 1.3 | CAW Pact restricts Orchestrator to AgentFightClub contract only | Pact config set; x402 pipeline confirmed working Day 8 | `[x]` |
| 1.4 | `eth_sendTransaction` via CAW succeeds on Base mainnet | Tx hash returned; visible on https://basescan.org | `[x]` |

Fallback: basic signing (private key in env) if CAW TSS node fails mid-build.

---

## 2. AgentFightClub (Moloch v3) — Days 8–11

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 2.1 | `launch()` — guild deployed on Base mainnet with mandate string | Contract address + Basescan tx hash | `[ ]` |
| 2.2 | `commit()` — treasury funded (≥ 0.001 ETH) | Tx hash; treasury balance readable | `[ ]` |
| 2.3 | `propose()` — Specialist membership proposal on-chain | Proposal ID; Basescan `ProposalSubmitted` event | `[x]` |
| 2.4 | `vote()` — Human founder approves | Tx hash; proposal state → `Passed` | `[x]` |
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

## 4. A2A Protocol — Day 9 (validated), Day 10 (full flow)

| # | Check | Evidence | Status |
|---|-------|----------|--------|
| 4.1 | Orchestrator Agent Card at `localhost:10000/.well-known/agent.json` | `curl` returns valid A2A card | `[ ]` |
| 4.2 | Specialist Agent Card at `localhost:10001/.well-known/agent.json` | Same | `[ ]` |
| 4.3 | `task/invite` sent; Specialist receives and parses | Logged in A2A trace | `[x]` |
| 4.4 | `task/quote` received from Specialist | Fields: `scope`, `estimated_cost_wei`, `deadline_iso` | `[x]` |
| 4.5 | `task/send` delivered with full payload | Logged; message ID captured | `[x]` |
| 4.6 | `task/delivered` received with hash matching on-chain commit | Hash cross-check passes | `[x]` |
| 4.7 | `task/accepted` sent after human acceptance | Specialist receives confirmation | `[x]` |
| 4.8 | Full A2A trace log exported | `hackathon/notes/a2a_trace_{date}.json` with 7 events | `[x]` |

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
| 6.2 | Demo task type locked | Decision noted in `docs/TECH_STACK.md` Decision Log; Hermes agent deployed Day 9 | `[x]` |
| 6.3 | Task decomposed into ≥ 3-step plan | Plan logged before execution | `[ ]` |
| 6.4 | All plan steps complete; structured output produced | Output file written; format matches acceptance criteria | `[ ]` |
| 6.5 | Execution trace logged | `hackathon/notes/glm_trace_{date}.json` readable | `[ ]` |
| 6.6 | Orchestrator pre-check passes | Report: hash ✅ · format ✅ · size ✅ | `[ ]` |

Fallback: deterministic prompt "Write a Python function that computes SHA-256 of a given input and returns the hex digest" if all 3 task types fail on Day 8.

---

## 7. Orchestrator MCP Tools — Day 9–10

| # | Tool | Check | Status |
|---|------|-------|--------|
| 7.1 | `guild_launch` | Returns guild contract address matching check 2.1 | `[x]` stub |
| 7.2 | `talent_query` | Returns Specialist profile JSON (hardcoded) | `[x]` |
| 7.3 | `task_invite` | Sends A2A `task/invite`; message ID logged | `[x]` |
| 7.4 | `task_delegate` | Sends A2A `task/send`; message ID in trace (4.5) | `[x]` |
| 7.5 | `deliverable_review` | Returns `{hash_match, format_valid, size_check, evaluator_verdict}` | `[x]` |
| 7.6 | `settle` | Returns settlement tx hash matching check 2.5 | `[x]` stub |
| 7.7 | `reputation_write` | Returns `DeliveryRecorded` tx hash matching check 3.3 | `[x]` stub |

---

## 8. Human Gates — Day 10–11

| # | Gate | Check | Status |
|---|------|-------|--------|
| 8.1 | Gate 0 | ERC-8004 shortlist displayed; CLI halts; resumes only on `y` | `[ ]` |
| 8.2 | Gate 0.5 | Quote displayed; `Accept quote? [y/N]` halts execution | `[ ]` |
| 8.3 | Gate 1 | `vote` called only after human approves; rejection tested | `[x]` |
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
| 10.5 | CAW Pact config (live proof) | README §SDK Used | `[ ]` |
| 10.6 | GLM-5.1 trace log | `hackathon/notes/glm_trace_*.json` | `[ ]` |
| 10.7 | A2A trace log | `hackathon/notes/a2a_trace_*.json` | `[ ]` |
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
| 11.5.8 | Screenshots of Basescan pages for each tx | `hackathon/notes/screenshots/` | `[ ]` |

### 11.6 Compliance and Security Boundaries

Must be documented in README or a dedicated section:

| # | Requirement | Notes | Status |
|---|-------------|-------|--------|
| 11.6.1 | **Permission boundaries** — which actions are automated vs. human-gated | Document the 4 human gates (Gate 0, 0.5, 1, 2); reference `docs/MVP_FLOW.md §Automation Boundaries` | `[ ]` |
| 11.6.2 | **Failure handling** — what happens when a component fails | Reference `docs/RISKS.md` fallback table; summarise in README | `[ ]` |
| 11.6.3 | **Human intervention points** — when and why a human must approve | List all 4 gates with the action each gate blocks | `[ ]` |
| 11.6.4 | **Spending limits** — agent wallets do not have unconstrained fund access | CAW Pact config; describe per-task ceiling and contract allowlist | `[ ]` |

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
