# MVP Flow — GuildOS

> This is the complete 15-step coordination loop. Every feature in the build must map to one of these steps. If it doesn't, it's out of scope.

---

## Process Flow

```
Step 1   Human asks Orchestrator to launch a guild (name, mandate, governance, members+shares/loot, tribute)
Step 2   Orchestrator registers its profile on ERC-8004
Step 3   Orchestrator hunts for talent (talent-pool skill)
                        ── [GATE 0: Human selects candidate] ──
Step 4   Orchestrator invites Specialist; Specialist quotes
                        ── [GATE 0.5: Human accepts quote] ──
Step 5   Specialist submits membership proposal
                        ── [GATE 1: Human votes to approve] ──
Step 6   Orchestrator delegates ticket via A2A (issue, constraints, AgBOM, BDD, format)
Step 7   Specialist reads issue, decomposes and executes (GLM-5.1) → hashable deliverable
Step 8   Specialist creates EAS attestation of the deliverable hash; returns UID
Step 9   Specialist sends task/delivered via A2A (includes attestation UID)
Step 10  Orchestrator runs automated pre-check
                        ── [GATE 2: Human accepts/rejects deliverable] ──
Step 11a  Orchestrator raises payment proposal via AgentFightClub (deliverable details, specialist address)
Step 11b  Orchestrator sends task/accepted via A2A (carries payment_proposal_id + url)
                        ── [GATE 3: Human votes + processes payment proposal] ──
Step 12   On pass: settle() processes the payment proposal; DAO treasury releases funds
Step 13a  Specialist requests feedback via A2A; Orchestrator submits executable submitFeedback proposal
                        ── [GATE 4: Human votes to approve feedback] ──
Step 13b  On proposal pass: giveFeedback() executes with the guild contract as msg.sender
Step 14   Guild context updated to SETTLED
Step 15  [Rejection path: DISPUTED at Gate 2 or Gate 3; ragequit documented]
```

---

## Detailed Steps

### Step 1 — Human Founds Guild

- Marco asks the Orchestrator to launch a guild. Using its **guild-launch skill**, the Orchestrator collects:
  - `guild_name` — the club name
  - `mandate` + `governance_settings` (voting period, grace period, quorum)
  - `member_list` — initial members as wallet addresses with their `shares`/`loot` distribution
  - `tribute_wei` — the initial treasury tribute value
- The Orchestrator executes the on-chain launch through its **AgentFightClub skill** (either path — ClawBank API or DAOhaus SDK): `launch` (summon) + `commit` (tribute) on Base
- Returns the **dao address** and **treasury address**; Basescan txs recorded
- Guild state written to `guild_context.json`: `{ guild_name, guild_address, treasury_address, mandate, governance_settings, treasury_wei, member_list, task_state: "ACTIVE" }`

### Step 2 — Orchestrator Registers on ERC-8004

- Orchestrator calls `ERC-8004.register(agentURI)` — ERC-721 agentId minted on Base mainnet
- `agentURI` points to a static Agent Card JSON (GitHub raw URL or IPFS) — the Orchestrator
  is an initiator-only agent; it does not run a live A2A server or receive inbound A2A messages
- Guild is now discoverable via the ERC-8004 registry entry

### Step 3 — Orchestrator Hunts for Talent

- Marco asks the Orchestrator to find talent. Its **talent-pool skill** points to a script that calls `talent_query` to surface specialist candidates via ERC-8004 / A2A cards (MVP: hardcoded list from `./logs/erc8004_specialist_before.json`)
- Returns shortlist to human for review

### **GATE 0 — Candidate Selection (Human)**

- Human reviews the ERC-8004 shortlist; approves the invite
- CLI prompt: `Approve invite to Specialist Agent [y/N]?`
- Execution halts until `y` input

### Step 4 — Orchestrator Invites; Specialist Quotes

- Orchestrator sends A2A `task/invite` to Specialist
- Specialist confirms availability; responds with A2A `task/quote`: `{ scope, estimated_cost_wei, deadline_iso }`
- Orchestrator surfaces the quote to Marco

### **GATE 0.5 — Quote Acceptance (Human, lightweight)**

- Human reviews scope / cost / timeline
- CLI prompt: `Accept quote? [y/N]`
- This gate locks economic terms before the task begins

### Step 5 — Specialist Submits Membership Proposal

- Specialist calls AgentFightClub `propose(specialist_erc8004_id)` — proposal recorded on-chain
- Proposal ID saved to `guild_context.json`

### **GATE 1 — Membership (Human)**

- Human reviews Specialist's on-chain ERC-8004 profile: delivery history, acceptance rate, stake
- Human calls AgentFightClub `vote(proposal_id, approve=True)`
- Proposal state → `Passed`; Specialist is now a guild member
- CLI prompt: `Approve Specialist membership? [y/N]`

### Step 6 — Orchestrator Delegates Task via A2A

- Orchestrator sends A2A `task/send` to Specialist with the **full work order**:
  ```json
  {
    "task_description": "Implement the EASClient.attest() method in src/shared/eas.py so the Specialist can attest deliverable hashes on Base using the registered DELIVERY_SCHEMA_UID.",
    "github_issue_url": "https://github.com/<org>/guild-os/issues/<n>",
    "input_data": "Schema: bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount. Contract: 0x4200000000000000000000000000000000000021",
    "technical_constraints": {
      "repo_branch": "feat/eas-attestation",
      "library_versions": ["web3==7.16.0"],
      "env_vars": ["EAS_CONTRACT", "DELIVERY_SCHEMA_UID"]
    },
    "agbom": {
      "tools": ["read_file", "write_file", "run_tests"],
      "mcp_servers": ["evm-mcp-server", "context7"],
      "data_sources": ["docs/TECH_STACK.md", "specs/20-api-contracts.md"]
    },
    "acceptance_criteria": [
      "BDD: attest() returns a non-empty attestation UID",
      "BDD: get_attestation(uid) returns the original fields",
      "BDD: pytest tests/test_eas.py passes"
    ],
    "deliverable_format": "github_commit",
    "deadline": "ISO-8601",
    "budget_wei": 1000000000000000
  }
  ```
- `technical_constraints` (branch, library versions, env vars), the **Agent Bill of Materials (AgBOM)** (allowed tools, MCP servers, data sources), `acceptance_criteria` as a list of **BDD tests** that must pass, and `deliverable_format` (`zip+hash` or `github_commit`) are all required.
- **Canonical demo task — dogfooding:** the guild mandates "Build GuildOS"; the Specialist implements a GuildOS component ticket. This threads every component in a single run and makes the demo self-referential.
- Message ID captured; logged to `./logs/a2a_trace_{date}.json`

### Step 7 — Specialist Decomposes and Executes (GLM-5.1)

- Specialist **reads the GitHub issue** and loads the ticket prompt instructions before planning
- Decomposes the task into a ≥ 3-step plan using GLM-5.1 long-horizon planning, staying within the declared `technical_constraints` and using only tools in the AgBOM
- Executes plan with tool use loop: plan → tool call → result → next step
- Canonical demo: Specialist implements a GuildOS component ticket (dogfooding — the system builds itself)
- Produces a hashable deliverable per `deliverable_format`: **zip+hash** → SHA-256 of the zip; **github_commit** → the resulting commit hash. Either way the resulting hash is what gets attested in Step 8.
- Full trace logged to `./logs/glm_trace_{date}.json`

### Step 8 — Specialist Hashes Deliverable; Creates EAS Attestation

- Specialist computes SHA-256 of deliverable file
- Creates EAS attestation via `EASClient.attest()` on Base mainnet:
  - Schema: `DELIVERY_SCHEMA_UID` (registered once before demo)
  - Recipient: guild contract address
  - Data: `{deliverableHash, taskType, guildContract, paymentAmount}`
  - Revocable: `false` (delivery is permanent)
- Attestation UID returned (stable, non-zero, immutable on-chain)
- **easscan attestation #1** — `https://base.easscan.org/attestation/{uid}` saved to `./logs/tx_hashes.md`
- UID stored in `guild_context.json`: `attestation_uid`

> **Why EAS over raw `eth_sendTransaction`:** The attestation is cryptographically signed by the Specialist's key (proving the *Specialist* made this delivery claim), carries a stable UID that cross-references the A2A message and ERC-8004 record, and is queryable by judges via easscan without ABI parsing. Same gas cost as a raw tx.

### Step 9 — Specialist Sends task/delivered via A2A

- Specialist sends A2A `task/delivered` to Orchestrator:
  ```json
  {
    "deliverable_reference": "path/to/output",
    "deliverable_hash": "sha256:...",
    "attestation_uid": "0x...",
    "attestation_url": "https://base.easscan.org/attestation/0x..."
  }
  ```

### Step 10 — Orchestrator Runs Automated Pre-Check

- Orchestrator evaluates: hash present ✅ · format valid ✅ · size > 0 ✅
- Produces pre-check report; surfaces to human alongside deliverable

### **GATE 2 — Deliverable Acceptance (Human)**

- Human reviews deliverable + pre-check report against acceptance criteria
- CLI prompt: `Accept deliverable? [y/N]`
- Acceptance → Steps 11–14; Rejection → Step 15

### Step 11a — Orchestrator Raises the Payment Proposal

- The treasury is **DAO-held** — no agent wallet custodies funds, so payment moves only through a governance proposal.
- After Gate 2 acceptance, the Orchestrator calls `payment_propose(guild_address, specialist_wallet, amount_wei, delivery_record)` — an AgentFightClub `payment` proposal carrying the deliverable details and the Specialist's address as the payout target
- Proposal id + url saved to `guild_context.json`: `payment_proposal_id`

### Step 11b — Orchestrator Sends task/accepted via A2A

- Orchestrator sends A2A `task/accepted` to Specialist — closes the A2A transaction loop and **carries `payment_proposal_id` + `payment_proposal_url`** so the Specialist can track the payout

### **GATE 3 — Payment Approval (Human)**

- Human reviews the payment proposal (amount, recipient, deliverable)
- Human calls `AgentFightClub.vote(payment_proposal_id, approve=True)` and processes it
- CLI prompt: `Approve and process payment to Specialist? [y/N]`
- Execution halts until `y` — no funds move without this vote. A voted-down proposal sets `task_state: "DISPUTED"`.

### Step 12 — AgentFightClub Settles Payment

- On a passing Gate-3 vote, `settle(guild_address, payment_proposal_id)` **processes** the payment proposal
- Moloch v3 releases treasury funds to the Specialist wallet
- **Basescan tx #2** — settlement tx link saved to `./logs/tx_hashes.md`; `guild_context.settlement_tx` set

### Step 13a — Specialist Requests Feedback; Guild Submits Executable Reputation Proposal

- The **Specialist triggers** this stage by sending A2A `feedback/request` to the Orchestrator, asking the guild to record reputation for the completed work
- The Orchestrator then calls `AgentFightClub.propose()` submitting an **executable** `submitFeedback` proposal — a Moloch proposal whose `data` field encodes the `giveFeedback()` call with 6 fields:
  1. `task_type` — capability ID matching mandate category
  2. `deliverable_hash` — SHA-256 from the EAS attestation
  3. `acceptance_timestamp` — on-chain block timestamp from Gate 2
  4. `payment_wei` — amount released in `settle()`
  5. `guild_address` — guild contract address (this becomes `msg.sender` when the proposal executes)
  6. `a2a_task_id` — links to A2A message log
- Reputation proposal ID saved to `guild_context.json`: `reputation_proposal_id`
- **Why executable proposal:** When the proposal passes and is processed, the guild contract itself executes `giveFeedback()` — `msg.sender` is the guild contract address, satisfying the ERC-8004 caller constraint (F2). No single party (not even the Orchestrator's EOA) can unilaterally write to a Specialist's on-chain profile.

### **GATE 4 — Feedback Approval (Human)**

- Human reviews the proposed reputation entry before it goes on-chain
- Human calls `AgentFightClub.vote(reputation_proposal_id, approve=True)`
- CLI prompt: `Approve reputation feedback for Specialist? [y/N]`
- Execution halts until `y` — `giveFeedback()` is NOT called without this vote

### Step 13b — ERC-8004 Reputation Write-Back (on proposal pass)

- On passing vote: `AgentFightClub.process(reputation_proposal_id)` executes the proposal
- **The proposal execution calls `giveFeedback()` with `msg.sender = guild contract address`** — the Orchestrator's EOA is NOT the caller
- Emits `DeliveryRecorded` event on Base mainnet
- `reputation_tx` saved to `guild_context.json`; **Basescan tx #3** saved to `./logs/tx_hashes.md`
- **Caller constraint enforced:** guild contract is always the caller — Specialist wallet calling this directly would revert (F2)

### Step 14 — Guild Context Updated

- `guild_context.json` updated: `task_state: "SETTLED"`
- Specialist ERC-8004 after-state captured to `./logs/erc8004_specialist_after.json`

### Step 15 — Rejection / Dispute Path (Stub)

- Dispute reached at **Gate 2** (deliverable rejected) **or Gate 3** (payment proposal voted down): `guild_context.json` updated: `task_state: "DISPUTED"`
- Funds remain locked in the DAO treasury; no payment proposal is processed
- Ragequit exit path: documented in README → Moloch v3 standard `ragequit()` call (not executed in demo)

---

## Mock vs. Real

| Component | Status | Note |
|-----------|--------|------|
| AgentFightClub `launch` + `commit` + `settle` | **Real** | ClawBank API or DAOhaus fallback; `settle` = process the passed payment proposal |
| AgentFightClub `propose` + `vote` (membership + payment + feedback) | **Real** | Membership pre-staged; payment (Gate 3) + feedback (Gate 4) voted live |
| ERC-8004 profile reads (before/after) | **Real** | 8004scan API; cached JSON fallback |
| ERC-8004 reputation proposal + `giveFeedback()` | **Real** | Specialist-triggered via `feedback/request`; DAO proposal vote (Gate 4) must pass before write-back executes |
| A2A task flow (all message events incl. `feedback/request`) | **Real** | A2A SDK v1.0.0 |
| GLM-5.1 task execution (via Hermes) | **Real** | Locked task type Day 9; Hermes agent deployed as Specialist |
| EAS deliverable attestation | **Real** | `EASClient.attest()` on Base mainnet; UID embedded in A2A message and guild context |
| CAW Pact scoping (DAO-call allowlist + tribute cap) | **Real** | TSS local node; `propose`/`vote`/`process` allowlisted; tribute capped; provider-agnostic via `WalletProvider`; no EOA fallback |
| ERC-8004 talent query (capability matching) | **Mocked** | Hardcoded Specialist profile |
| Guild context store | **Mocked** | JSON file per guild session |
| Multiple concurrent guild members | **Mocked** | One agent pair for demo |
| Third-party evaluator agent | **Mocked** | Orchestrator hash + format check only |
| Dispute ragequit on-chain | **Stub** | `DISPUTED` state in JSON; ragequit documented |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-30 | **Settlement is now DAO-governed.** Split Step 11 into 11a (raise payment proposal) + 11b (`task/accepted` carrying `payment_proposal_id`+url); added **GATE 3 (payment vote+process)**; `settle()` redefined to *process the passed payment proposal*. **Reputation feedback renumbered to GATE 4** and is now **Specialist-triggered** via a new `feedback/request` A2A message. Loop now has **6 human gates** (0, 0.5, 1, 2, 3, 4). Mirrors `specs/` design feedback. |
| 2026-06-30 | **Guild formation (Step 1)** now collects guild name, governance settings, member list with shares/loot, and tribute via the Orchestrator's guild-launch + AgentFightClub skills; returns dao + treasury addresses. **Step 3** runs through the talent-pool skill. |
| 2026-06-30 | **Task delegation (Step 6)** payload expanded: `github_issue_url`, `technical_constraints`, `agbom` (Agent Bill of Materials), BDD-test `acceptance_criteria`, `deliverable_format`. **Step 7** now reads the GitHub issue first and produces a hash per format (zip SHA-256 or commit hash). |
| 2026-06-30 | **Dispute path (Step 15)** now reachable at Gate 2 or Gate 3; treasury is DAO-held. Mock-vs-Real table updated for the payment proposal, `feedback/request`, and provider-agnostic CAW Pact scoping (DAO-call allowlist + tribute cap, no EOA fallback). |
