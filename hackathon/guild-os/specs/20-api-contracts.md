# 20 — API Contracts: Pinned Versions, Addresses & Interfaces

> Provenance: `docs/TECH_STACK.md`, `uv.lock` (exact versions), `docs/MVP_FLOW.md`
> (message field defs), project `CLAUDE.md` (component map).

## TL;DR

Every dependency is pinned to the exact version resolved in `uv.lock` — no stale-training
defaults, no bare `>=`. Every on-chain address and the canonical chain are fixed here.
A2A messages and MCP tools have explicit input/output shapes. Deep/nested payloads use
YAML; flat ones use Markdown tables.

---

## 1. Pinned Dependencies

Exact versions from `uv.lock`. Pin these — do not let an agent default to training-data versions.

| Package | Version | Role |
|---------|---------|------|
| python | `>=3.11` | Runtime (uv-managed) |
| `a2a-sdk[http-server]` | `1.1.0` | A2A protocol — task delegation + result return |
| `web3` | `7.16.0` | Base mainnet RPC, tx submission, event reads, EAS/ERC-8004 ABI calls |
| `mcp` | `1.27.2` | Orchestrator MCP server |
| `eth-account` | `0.13.7` | EOA signing |
| `httpx` | `0.28.1` | HTTP client (8004scan, ClawBank API) |
| `pydantic` | `2.13.4` | Data validation / message models |
| `fastapi` | `0.136.3` | A2A route mounting (Specialist server) |
| `uvicorn` | `0.49.0` | ASGI server (Specialist) |
| `click` | `8.4.1` | CLI / human gates |
| `python-dotenv` | `1.2.2` | `.env` loading |
| `pytest` | `9.0.3` | Tests |
| `pytest-asyncio` | `1.4.0` | Async test support (`asyncio_mode = strict`) |
| `ruff` | `0.15.16` | Lint |

> Source of truth is `uv.lock`. If a version here drifts from the lock file, the lock file
> wins — update this table, never the reverse.

---

## 2. Network & On-Chain Addresses

| Item | Value |
|------|-------|
| Canonical network | **Base mainnet — `CHAIN_ID=8453`** (only valid submission-evidence network) |
| Isolated-test network | Base Sepolia — `CHAIN_ID=84532` (components that support it only; never for evidence) |
| Block explorer | `https://basescan.org/tx/...` (Sepolia: `https://sepolia.basescan.org/tx/...`) |
| EAS explorer | `https://base.easscan.org/attestation/{uid}` |
| RPC | Alchemy (Base) — `ALCHEMY_API_KEY` |
| ERC-8004 IdentityRegistry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| ERC-8004 ReputationRegistry | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| EAS contract | `0x4200000000000000000000000000000000000021` |
| EAS SchemaRegistry | `0x4200000000000000000000000000000000000020` |
| `DELIVERY_SCHEMA_UID` | Registered once before Step 8; pinned in `.env` |

### EAS delivery schema

```
bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount
```
Resolver: `0x0000000000000000000000000000000000000000` (none for MVP) · Revocable: `false`.

---

## 3. A2A Message Contracts

Six message types. `A2AClient` (`src/shared/a2a.py`) sends/receives; every message is
logged to `hackathon/notes/a2a_trace_{date}.json`.

| Message | Direction | Fields |
|---------|-----------|--------|
| `task/invite` | Orchestrator → Specialist | `task_spec: object` |
| `task/quote` | Specialist → Orchestrator | `scope: string`, `estimated_cost_wei: int`, `deadline_iso: string` |
| `task/send` | Orchestrator → Specialist | `task: object` (see below) |
| `task/delivered` | Specialist → Orchestrator | `deliverable_reference: string`, `deliverable_hash: string`, `attestation_uid: string`, `attestation_url: string` |
| `task/accepted` | Orchestrator → Specialist | `task_id: string`, `payment_proposal_id: string`, `payment_proposal_url: string` |
| `feedback/request` | Specialist → Orchestrator | `task_id: string`, `deliverable_hash: string` — Specialist asks the guild to record reputation for completed work |

> The `task/delivered` message carries **`attestation_uid` + `attestation_url`** — **never**
> an `on_chain_tx` field. EAS is the deliverable-commitment mechanism in the target design.
> `task/accepted` carries the **payment proposal** id+url (raised before it is sent); the
> Specialist later triggers reputation with **`feedback/request`**.

### `task/send` payload (nests > 3 levels → YAML)

```yaml
task:
  task_id: string
  task_description: string         # e.g. "Implement the EAS attestation module (EASClient)"
  github_issue_url: string         # the ticket the Specialist reads and works from
  input_data: string              # ticket body / spec excerpt / repo ref
  technical_constraints:           # the box the work must stay in
    repo_branch: string           # working branch
    library_versions: [string]    # pinned versions the deliverable must use
    env_vars: [string]            # required environment variable names (values via .env)
  agbom:                          # Agent Bill of Materials — what the agent may use
    tools: [string]
    mcp_servers: [string]
    data_sources: [string]
  acceptance_criteria: [string]    # list of BDD tests that must pass
  deliverable_format: string      # "zip+hash" | "github_commit"
  deadline: string               # ISO-8601
  budget_wei: string             # numeric string (wei)
```

---

## 4. MCP Tool Contracts (Orchestrator)

Async tools registered by `OrchestratorTools` (`src/orchestrator/tools.py`).

| Tool | Input | Output |
|------|-------|--------|
| `guild_launch` | `guild_name: string`, `mandate: string`, `governance_settings: object`, `member_list: [{address, shares, loot}]`, `tribute_wei: string` | `{ guild_address, treasury_address, launch_tx, commit_tx }` |
| `talent_query` | `task_type: string` | `[{ name, agent_id, capabilities[], a2a_endpoint, delivery_count, rating }]` |
| `task_invite` | `specialist_endpoint: string`, `task_spec: object` | `message_id: string` |
| `task_delegate` | `specialist_endpoint: string`, `full_task: object` | `message_id: string` |
| `deliverable_review` | `deliverable_reference: string`, `deliverable_hash: string` | `{ hash_match, format_valid, size_check, evaluator_verdict }` |
| `payment_propose` | `guild_address: string`, `specialist_wallet: string`, `amount_wei: string`, `delivery_record: object` | `{ payment_proposal_id, payment_proposal_url }` |
| `settle` | `guild_address: string`, `payment_proposal_id: string` | `settlement_tx: string` (process after Gate 3 passes) |
| `reputation_propose` | `delivery_record: object` (6 fields, below) | `{ reputation_proposal_id }` |
| `reputation_write` | `reputation_proposal_id: string` | `reputation_tx: string` (after Gate 4 passes) |

### Delivery record — the 6 ERC-8004 feedback fields

```yaml
delivery_record:
  task_type: string             # capability ID matching the mandate category
  deliverable_hash: string      # "sha256:<hex>" — same hash that was EAS-attested
  acceptance_timestamp: int     # on-chain block timestamp at Gate 2
  payment_wei: int              # amount released in settle()
  guild_address: string         # guild contract — cross-guild traceability
  a2a_task_id: string           # links to the A2A message log
```

---

## 5. Component Interfaces

### `EASClient` — `src/shared/eas.py`
- `attest(deliverable_hash, task_type, guild_contract, payment_amount) -> { uid, url, tx_hash }`
  — Specialist-signed attestation against `DELIVERY_SCHEMA_UID`.
- `get_attestation(uid) -> { deliverableHash, taskType, guildContract, paymentAmount }`.

### `ERC8004` — `src/shared/erc8004.py`
- `register(agent_uri, signer_private_key) -> tx_hash` — mints the agentId.
- `give_feedback(caller, <6 fields>) -> tx_hash` — emits `DeliveryRecorded`.
  **Caller MUST be the guild contract or Marco's EOA — never the Specialist wallet (F2).**

### `AgentFightClub` — `src/shared/agentfightclub.py`
- `launch(guild_name, mandate, governance_settings, member_list) -> { guild_address, treasury_address, tx_hash }`
- `commit(guild_address, amount_wei) -> tx_hash` — tribute (value-capped by the Pact)
- `propose(guild_address, payload) -> proposal_id` — membership, payment, or executable feedback
- `vote(guild_address, proposal_id, approve=True) -> tx_hash` — sponsor + vote + process
- `settle(guild_address, payment_proposal_id) -> tx_hash` — process the passed payment proposal

### `WalletProvider` — `src/shared/wallet.py`
- Provider-agnostic signing + Pact-scoping interface; **no raw-EOA fallback**.
- `sign(tx) -> signed_tx` — refuses any call outside the Pact allowlist or above the tribute cap.
- Allowlist scopes the DAO contract's `propose` / `vote` / `process` functions; the tribute
  call carries the only value cap.
- Default implementation: Cobo CAW (TSS). Swappable to ZeroDev / Turnkey with the same
  allowlist + cap semantics (selected by `WALLET_PROVIDER`).

### `SpecialistAgent` handlers — `src/specialist/agent.py`
- `handle_task_invite(message) -> task/quote`
- `handle_task_send(message) -> task/delivered` (reads the GitHub issue, executes GLM-5.1, attests, returns UID)
- `request_feedback(task_id, deliverable_hash) -> feedback/request` (triggers the reputation stage after settlement)

---

## 6. Environment Contract

| Variable | Purpose | Default |
|----------|---------|---------|
| `CHAIN_ID` | Active network (8453 canonical / 84532 isolated test) | `8453` |
| `ALCHEMY_API_KEY` | Base RPC | — (required) |
| `GLM_API_KEY` | Z.AI GLM-5.1 | — (required) |
| `ORCHESTRATOR_PRIVATE_KEY` | Orchestrator EOA signing | — (required) |
| `SPECIALIST_PRIVATE_KEY` | Specialist EOA signing | — (required) |
| `ORCHESTRATOR_WALLET_ADDRESS` | Treasury / launch caller | — (required) |
| `SPECIALIST_WALLET_ADDRESS` | Settlement target | — (required) |
| `AGENTFIGHTCLUB_API_KEY` | ClawBank API (skip → DAOhaus fallback) | optional |
| `WALLET_PROVIDER` | Scoped signing provider for `WalletProvider` (`caw` \| `zerodev` \| `turnkey`) | `caw` |
| `ERC8004_CONTRACT` | IdentityRegistry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| `REPUTATION_CONTRACT` | ReputationRegistry | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| `EAS_CONTRACT` | EAS | `0x4200000000000000000000000000000000000021` |
| `EAS_SCHEMA_REGISTRY` | EAS SchemaRegistry | `0x4200000000000000000000000000000000000020` |
| `DELIVERY_SCHEMA_UID` | Registered delivery schema | — (required from Step 8) |
| `ORCHESTRATOR_A2A_PORT` | Orchestrator A2A port | `10000` |
| `SPECIALIST_A2A_PORT` | Specialist A2A port | `10001` |

---

## 7. Appendix — Naming Conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Classes | PascalCase | `OrchestratorServer`, `ERC8004`, `GuildContext` |
| Functions | snake_case | `guild_launch()`, `send_invite()` |
| Constants | SCREAMING_SNAKE | `ERC8004_CONTRACT`, `DELIVERY_SCHEMA_UID` |
| A2A message types | `noun/verb` | `task/invite`, `task/delivered` |
| Files | snake_case | `agentfightclub.py`, `guild_context.json` |
| Git branches | `feat/`, `fix/`, `chore/` | `feat/eas-attestation` |
