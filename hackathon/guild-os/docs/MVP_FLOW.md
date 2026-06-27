# MVP Flow — GuildOS

> This is the complete 15-step coordination loop. Every feature in the build must map to one of these steps. If it doesn't, it's out of scope.

---

## Process Flow

```
Step 1   Human founds guild
Step 2   Orchestrator registers on ERC-8004
Step 3   Orchestrator hunts for talent
                        ── [GATE 0: Human selects candidate] ──
Step 4   Orchestrator invites Specialist; Specialist quotes
                        ── [GATE 0.5: Human accepts quote] ──
Step 5   Specialist submits membership proposal
                        ── [GATE 1: Human votes to approve] ──
Step 6   Orchestrator delegates task via A2A
Step 7   Specialist decomposes and executes (GLM-5.1)
Step 8   Specialist hashes deliverable; creates EAS attestation; returns UID
Step 9   Specialist sends task/delivered via A2A (includes attestation UID)
Step 10  Orchestrator runs automated pre-check
                        ── [GATE 2: Human accepts/rejects deliverable] ──
Step 11  On acceptance: Orchestrator sends task/accepted via A2A
Step 12  AgentFightClub settle() releases payment
Step 13a  Guild submits reputation feedback proposal via AgentFightClub
                        ── [GATE 3: Human votes to approve feedback] ──
Step 13b  On proposal pass: ERC-8004 giveFeedback() with 6 fields
Step 14   Guild context updated to SETTLED
Step 15  [Rejection path: DISPUTED state recorded; ragequit documented]
```

---

## Detailed Steps

### Step 1 — Human Founds Guild

- Marco calls AgentFightClub `launch(mandate_string, treasury_address)` — guild contract deployed on Base mainnet with mandate string
- Marco calls AgentFightClub `commit(guild_address, 0.001 ETH)` — treasury funded; Basescan tx recorded
- Guild state written to `guild_context.json`: `{ guild_address, mandate, treasury_wei, member_list: [], task_state: "ACTIVE" }`

### Step 2 — Orchestrator Registers on ERC-8004

- Orchestrator calls `ERC-8004.register(agentURI)` — ERC-721 agentId minted on Base mainnet
- `agentURI` points to a static Agent Card JSON (GitHub raw URL or IPFS) — the Orchestrator
  is an initiator-only agent; it does not run a live A2A server or receive inbound A2A messages
- Guild is now discoverable via the ERC-8004 registry entry

### Step 3 — Orchestrator Hunts for Talent

- Orchestrator queries ERC-8004 registry for agents with matching capability claims (MVP: hardcoded Specialist profile from `./logs/erc8004_specialist_before.json`)
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

- Orchestrator sends A2A `task/send` to Specialist:
  ```json
  {
    "task_description": "Implement the EASClient.attest() method in src/shared/eas.py so the Specialist can attest deliverable hashes on Base using the registered DELIVERY_SCHEMA_UID.",
    "input_data": "Schema: bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount. Contract: 0x4200000000000000000000000000000000000021",
    "acceptance_criteria": [
      "attest() returns a non-empty attestation UID",
      "get_attestation(uid) returns the original fields",
      "pytest tests/test_eas.py passes"
    ],
    "deadline": "ISO-8601",
    "budget_wei": 1000000000000000
  }
  ```
- **Canonical demo task — dogfooding:** the guild mandates "Build GuildOS"; the Specialist implements a GuildOS component ticket. This threads every component in a single run and makes the demo self-referential.
- Message ID captured; logged to `./logs/a2a_trace_{date}.json`

### Step 7 — Specialist Decomposes and Executes (GLM-5.1)

- Specialist decomposes task into ≥ 3-step plan using GLM-5.1 long-horizon planning
- Executes plan with tool use loop: plan → tool call → result → next step
- Canonical demo: Specialist implements a GuildOS component ticket (dogfooding — the system builds itself)
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

### Step 11 — Orchestrator Sends task/accepted via A2A

- Orchestrator sends A2A `task/accepted` to Specialist — closes the A2A transaction loop

### Step 12 — AgentFightClub Settles Payment

- Orchestrator calls AgentFightClub `settle(guild_address, specialist_wallet)`
- Moloch v3 releases treasury funds to Specialist wallet
- **Basescan tx #2** — settlement tx link saved to `./logs/tx_hashes.md`

### Step 13a — Guild Submits Executable Reputation Feedback Proposal

- After `settle()` confirms, Orchestrator calls `AgentFightClub.propose()` submitting an **executable** `submitFeedback` proposal — a Moloch proposal whose `data` field encodes the `giveFeedback()` call with 6 fields:
  1. `task_type` — capability ID matching mandate category
  2. `deliverable_hash` — SHA-256 from the EAS attestation
  3. `acceptance_timestamp` — on-chain block timestamp from Gate 2
  4. `payment_wei` — amount released in `settle()`
  5. `guild_address` — guild contract address (this becomes `msg.sender` when the proposal executes)
  6. `a2a_task_id` — links to A2A message log
- Reputation proposal ID saved to `guild_context.json`: `reputation_proposal_id`
- **Why executable proposal:** When the proposal passes and is processed, the guild contract itself executes `giveFeedback()` — `msg.sender` is the guild contract address, satisfying the ERC-8004 caller constraint (F2). No single party (not even the Orchestrator's EOA) can unilaterally write to a Specialist's on-chain profile.

### **GATE 3 — Feedback Approval (Human)**

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

- Gate 2 rejection: `guild_context.json` updated: `task_state: "DISPUTED"`
- Funds remain locked in AgentFightClub treasury
- Ragequit exit path: documented in README → Moloch v3 standard `ragequit()` call (not executed in demo)

---

## Mock vs. Real

| Component | Status | Note |
|-----------|--------|------|
| AgentFightClub `launch` + `commit` + `settle` | **Real** | ClawBank API or DAOhaus fallback |
| AgentFightClub `propose` + `vote` | **Real** | Pre-staged before live demo |
| ERC-8004 profile reads (before/after) | **Real** | 8004scan API; cached JSON fallback |
| ERC-8004 reputation proposal + `giveFeedback()` | **Real** | DAO proposal via AgentFightClub; vote must pass before write-back executes |
| A2A task flow (all 7 message events) | **Real** | A2A SDK v1.0.0 |
| GLM-5.1 task execution (via Hermes) | **Real** | Locked task type Day 9; Hermes agent deployed as Specialist |
| EAS deliverable attestation | **Real** | `EASClient.attest()` on Base mainnet; UID embedded in A2A message and guild context |
| Cobo CAW spending ceiling (Pact) | **Real** — TSS local node; x402 pipeline confirmed working Day 8 |
| ERC-8004 talent query (capability matching) | **Mocked** | Hardcoded Specialist profile |
| Guild context store | **Mocked** | JSON file per guild session |
| Multiple concurrent guild members | **Mocked** | One agent pair for demo |
| Third-party evaluator agent | **Mocked** | Orchestrator hash + format check only |
| Dispute ragequit on-chain | **Stub** | `DISPUTED` state in JSON; ragequit documented |
