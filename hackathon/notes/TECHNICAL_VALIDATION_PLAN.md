# GuildOS — Technical Validation Plan (Week 4 / Pre-Submission)

> Deadline: **2026-06-13 12:00 UTC+8 (04:00 UTC)**
> Network: **Base Sepolia testnet**
> This plan covers every integration point that must be validated before submitting to Casual Hackathon.

---

## How to use this file

Work through sections in order. Each check has a **Status** column — update it as you go:
`[ ]` pending · `[x]` passed · `[!]` blocked / fallback triggered

---

## 1. Agent Wallet — Cobo CAW

Validates that agent wallets can send transactions on Base Sepolia with enforced spending scope.

| # | Check | Evidence | Status |
|---|---|---|---|
| 1.1 | Cobo CAW wallet initialized for Orchestrator Agent | Wallet address printed; Base Sepolia balance > 0 | `[ ]` |
| 1.2 | Cobo CAW wallet initialized for Specialist Agent | Wallet address printed; Base Sepolia balance > 0 | `[ ]` |
| 1.3 | Pact-scoped API key restricts Orchestrator to AgentFightClub contract address only | Attempt an out-of-scope call → must fail; screenshot | `[ ]` |
| 1.4 | Pact-scoped API key restricts Specialist to ERC-8004 contract address only | Same rejection test | `[ ]` |
| 1.5 | `eth_sendTransaction` via CAW succeeds for a no-op testnet call | Tx hash returned; visible on Basescan | `[ ]` |

**Fallback if CAW unavailable:** Use local signer (private key in env) for all testnet calls. Note the fallback in demo notes.

---

## 2. AgentFightClub (Moloch v3) — Guild Lifecycle

Validates the full guild treasury and governance flow via AgentFightClub Skill API or direct DAOhaus SDK.

| # | Check | Evidence | Status |
|---|---|---|---|
| 2.1 | `launch()` — Guild contract deployed on Base Sepolia with mandate string | Contract address + Basescan tx hash | `[ ]` |
| 2.2 | `commit()` — Treasury funded (≥ 0.001 ETH for testnet demo) | Tx hash; treasury balance readable via `eth_getBalance` | `[ ]` |
| 2.3 | `propose()` — Specialist Agent membership proposal recorded on-chain | Proposal ID returned; Basescan event log shows `ProposalSubmitted` | `[ ]` |
| 2.4 | `vote()` — Human founder vote approves the proposal | Tx hash; Basescan shows `VoteSubmitted`; proposal state → `Passed` | `[ ]` |
| 2.5 | `settle()` — Payment released from treasury to Specialist wallet after acceptance | Tx hash; Specialist wallet balance increases by expected amount; Basescan confirms | `[ ]` |
| 2.6 | Guild context store (JSON) written and readable after each phase transition | File `guild_context.json` updated; fields: guild_address, mandate, treasury, member_list, task_state | `[ ]` |

**Fallback if AgentFightClub API is down:** Deploy Moloch v3 DAO directly via DAOhaus SDK; same call signatures; no ClawBank dependency.

---

## 3. ERC-8004 Registry — Agent Identity and Reputation

Validates that both agent profiles are readable and that the Specialist's delivery record is written post-acceptance.

| # | Check | Evidence | Status |
|---|---|---|---|
| 3.1 | Orchestrator Agent ERC-8004 profile readable via 8004scan API | JSON response with: `name`, `capabilities[]`, `a2a_endpoint`, `delivery_count` | `[ ]` |
| 3.2 | Specialist Agent ERC-8004 profile readable; **before-state** captured | Snapshot saved to `./logs/erc8004_specialist_before.json` | `[ ]` |
| 3.3 | `recordDelivery()` call succeeds after `settle()` | Tx hash; Basescan shows `DeliveryRecorded` event | `[ ]` |
| 3.4 | Specialist ERC-8004 profile **after-state** shows +1 delivery record | Six fields present: task_type, deliverable_hash, acceptance_timestamp, payment_wei, guild_address, a2a_task_id | `[ ]` |
| 3.5 | Before/after delta is demo-ready (printable side-by-side) | Script or CLI command that outputs both states for live demo | `[ ]` |

**Fallback if 8004scan API is slow/down:** Serve from cached profile JSON files at startup; note in demo.

---

## 4. A2A Protocol — Cross-Agent Communication

Validates A2A SDK v1.0.0 message exchange across both agent harnesses.

| # | Check | Evidence | Status |
|---|---|---|---|
| 4.1 | Orchestrator Agent Card published at reachable URL (or local port) | `GET /.well-known/agent.json` returns valid A2A agent card | `[ ]` |
| 4.2 | Specialist Agent Card published; includes capability claims matching the demo task | Same check on Specialist endpoint | `[ ]` |
| 4.3 | A2A `task/invite` sent from Orchestrator → Specialist | Message logged; Specialist receives and parses correctly | `[ ]` |
| 4.4 | A2A `task/quote` received from Specialist → Orchestrator (scope, cost, timeline) | Quote fields: `scope`, `estimated_cost_wei`, `deadline_iso`; logged | `[ ]` |
| 4.5 | A2A `task/send` (full task delegation) sent Orchestrator → Specialist | Full payload logged: task description, input data, acceptance criteria, deadline, budget | `[ ]` |
| 4.6 | A2A `task/delivered` received Specialist → Orchestrator (deliverable ref + SHA-256 hash) | Hash matches the file committed on-chain (check 5.2) | `[ ]` |
| 4.7 | A2A `task/accepted` sent Orchestrator → Specialist after human acceptance | Message logged; Specialist receives confirmation | `[ ]` |
| 4.8 | Full A2A message log exported | File `./logs/a2a_trace_<date>.json` with all seven message events | `[ ]` |

---

## 5. On-Chain Deliverable Hash Commitment

Validates that the deliverable is hashed and committed to Base Sepolia before human review.

| # | Check | Evidence | Status |
|---|---|---|---|
| 5.1 | Deliverable file produced by GLM-5.1 (code or analysis output) | File present in repo; non-zero size | `[ ]` |
| 5.2 | SHA-256 hash computed over deliverable file | Hash string printed; matches what Specialist sends in `task/delivered` | `[ ]` |
| 5.3 | Hash committed to guild contract on Base Sepolia via `eth_sendTransaction` | **Tx hash saved** — this is a primary demo evidence item; Basescan link clickable | `[ ]` |
| 5.4 | Contract storage confirms hash is readable post-commit | `eth_call` to read stored hash returns matching value | `[ ]` |

---

## 6. GLM-5.1 Specialist Agent — Task Execution

Validates that the Specialist Agent completes a real task using GLM-5.1 long-horizon planning.

| # | Check | Evidence | Status |
|---|---|---|---|
| 6.1 | GLM-5.1 API key configured and reachable | Test call returns non-error response | `[ ]` |
| 6.2 | Specialist Agent decomposes task into a multi-step plan | Plan logged with ≥ 3 steps before execution begins | `[ ]` |
| 6.3 | Specialist Agent completes all plan steps and produces structured output | Output file written; format matches acceptance criteria from A2A task message | `[ ]` |
| 6.4 | Agent execution trace logged (each step: plan → tool call → result → next step) | Trace file `./logs/glm_trace_<date>.json`; readable for demo | `[ ]` |
| 6.5 | Orchestrator automated pre-check passes on deliverable | Pre-check report: hash present ✅, format valid ✅, size > 0 ✅ | `[ ]` |

---

## 7. Orchestrator Agent — MCP Tool Manifest

Validates that the Orchestrator's tools are registered and callable as an MCP server.

| # | Check | Evidence | Status |
|---|---|---|---|
| 7.1 | MCP server starts without error | Server log shows all tools registered: `guild_launch`, `talent_query`, `task_invite`, `task_delegate`, `deliverable_review`, `settle`, `reputation_write` | `[ ]` |
| 7.2 | `guild_launch` tool callable and returns guild contract address | Tool call log; contract address matches check 2.1 | `[ ]` |
| 7.3 | `talent_query` tool returns ERC-8004 shortlist (hardcoded for MVP) | Returns Specialist profile JSON | `[ ]` |
| 7.4 | `task_delegate` tool sends A2A `task/send` and logs message ID | Message ID present in A2A trace (check 4.5) | `[ ]` |
| 7.5 | `deliverable_review` tool runs pre-check and returns report | Report fields: hash_match, format_valid, size_check, evaluator_verdict | `[ ]` |
| 7.6 | `settle` tool calls AgentFightClub `settle()` and returns settlement tx hash | Tx hash matches check 2.5 | `[ ]` |
| 7.7 | `reputation_write` tool calls `ERC-8004.recordDelivery()` and returns tx hash | Tx hash matches check 3.3 | `[ ]` |

---

## 8. Human Gates — CLI Interaction

Validates that each human confirmation gate stops execution and waits for explicit input.

| # | Gate | Check | Status |
|---|---|---|---|
| 8.1 | Gate 0 | Orchestrator presents ERC-8004 shortlist and halts; execution resumes only after `y` input | `[ ]` |
| 8.2 | Gate 0.5 | Specialist quote displayed; CLI prompt `Accept quote? [y/N]`; execution halts | `[ ]` |
| 8.3 | Gate 1 | AgentFightClub `vote` called only after human approves membership; rejection path tested | `[ ]` |
| 8.4 | Gate 2 | Deliverable + pre-check report presented; `settle()` called only after human accepts | `[ ]` |
| 8.5 | Dispute stub | Gate 2 rejection sets `task_state: DISPUTED` in `guild_context.json`; no settlement tx fired | `[ ]` |

---

## 9. End-to-End Demo Run

A complete smoke test of the full minimum loop, run twice before submission.

| # | Check | Evidence | Status |
|---|---|---|---|
| 9.1 | Run 1: Full loop completes without error (fresh guild, fresh agents) | Terminal output from start to settlement tx | `[ ]` |
| 9.2 | Run 2: Repeat with a different task input; same outcome | Confirms repeatability | `[ ]` |
| 9.3 | Two primary Basescan tx hashes confirmed clickable | (1) Deliverable hash commit · (2) AgentFightClub settlement — both resolve on Basescan | `[ ]` |
| 9.4 | Before/after ERC-8004 Specialist profile delta visible side-by-side | Screenshot or terminal diff captured for demo slide | `[ ]` |
| 9.5 | A2A trace log exported and readable | File present; all 7 message events visible | `[ ]` |
| 9.6 | GLM-5.1 execution trace exported and readable | File present; plan steps + tool calls visible | `[ ]` |

---

## 10. Submission Evidence Checklist

Artifacts to assemble for the Casual Hackathon submission form.

| # | Artifact | Location | Status |
|---|---|---|---|
| 10.1 | GitHub repo with README (problem, architecture, run instructions, SDK used) | `github.com/santteegt/ai-web3-school-cohort-0` | `[ ]` |
| 10.2 | Demo video (3–5 min) showing full minimum loop | Link (Loom / YouTube) | `[ ]` |
| 10.3 | Deliverable hash commit — Basescan tx link | Saved in `submissions/tx_hashes.md` | `[ ]` |
| 10.4 | AgentFightClub settlement — Basescan tx link | Saved in `submissions/tx_hashes.md` | `[ ]` |
| 10.5 | Specialist Agent wallet address | Saved in `submissions/tx_hashes.md` | `[ ]` |
| 10.6 | ERC-8004 Specialist profile before/after screenshots | `./logs/erc8004_*.json` + screenshots | `[ ]` |
| 10.7 | A2A message trace log | `./logs/a2a_trace_<date>.json` | `[ ]` |
| 10.8 | Cobo CAW key code/config (Cobo track requirement) | Anonymized config snippet in README | `[ ]` |
| 10.9 | GLM-5.1 long-horizon task run log (Z.AI track evidence) | `./logs/glm_trace_<date>.json` | `[ ]` |
| 10.10 | Team info: name, role, wallet address, contact | In submission form | `[ ]` |

---

## 11. Fallback Readiness

Quick-reference for each integration risk and its pre-staged fallback.

| Integration | Risk | Fallback | Pre-staged? |
|---|---|---|---|
| AgentFightClub Skill API | Alpha; may be unavailable | DAOhaus SDK direct deploy | `[ ]` |
| Cobo CAW | Node indexing lag | Local private-key signer | `[ ]` |
| ERC-8004 / 8004scan API | Downtime or latency | Cached profile JSON served locally | `[ ]` |
| Base Sepolia RPC | Congestion | Alchemy RPC + backup Infura endpoint | `[ ]` |
| GLM-5.1 API | Rate limit or timeout | Pre-recorded output for demo task | `[ ]` |
| Live demo tx timing | Slow finality during presentation | Pre-staged tx hashes on screen; point Basescan at them | `[ ]` |

---

*Created: 2026-06-07 | Agent: Sensei (Claude via Cowork) | Based on: hackathon/PROJECT_PROPOSAL.md v1.2*
