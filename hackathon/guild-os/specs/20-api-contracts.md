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
| `pytest-bdd` | `8.1.0` | Executes `specs/scenarios/*.feature` directly via `tests/step_defs/` — `bdd_features_base_dir` points at `specs/scenarios/`, no copy |
| `ruff` | `0.15.16` | Lint |

> Source of truth is `uv.lock`. If a version here drifts from the lock file, the lock file
> wins — update this table, never the reverse.

---

## 2. Network & On-Chain Addresses

**Source of truth is `config/networks.json`, not `.env`.** Every value below
is network-specific (it differs — or could differ — between Base and Base
Sepolia), so it's keyed by `CHAIN_ID` in that file and resolved through
`src/shared/network_config.py`. No component reads a contract address, RPC
URL, or explorer link from an environment variable directly; only `CHAIN_ID`
itself (the network selector) and secrets (`ALCHEMY_API_KEY`, private keys)
live in `.env` — see §6.

| Item | Value | Resolved via |
|------|-------|---------------|
| Canonical network | **Base — `CHAIN_ID=8453`** (only valid submission-evidence network) | `network_config.is_canonical()` |
| Isolated-test network | Base Sepolia — `CHAIN_ID=84532` (components that support it only; AgentFightClub has no deployment here; never for evidence) | — |
| Block explorer | `https://basescan.org/tx/...` (Sepolia: `https://sepolia.basescan.org/tx/...`) | `network_config.get_explorer_tx_url(tx_hash)` |
| EAS explorer | `https://base.easscan.org/attestation/{uid}` | `network_config.get_easscan_attestation_url(uid)` |
| RPC | `https://base-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}` (Sepolia: `base-sepolia` subdomain); `ALCHEMY_API_KEY` substituted from env at load time | `network_config.get_rpc_url()` |
| ERC-8004 IdentityRegistry | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` (chain `8453`, canonical) | `network_config.get_contract_address("erc8004_identity_registry")` |
| ERC-8004 ReputationRegistry | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` (chain `8453`, canonical) | `network_config.get_contract_address("erc8004_reputation_registry")` |
| EAS contract | `0x4200000000000000000000000000000000000021` (OP-stack predeploy — identical on every OP-stack chain) | `network_config.get_contract_address("eas")` |
| EAS SchemaRegistry | `0x4200000000000000000000000000000000000020` (OP-stack predeploy) | `network_config.get_contract_address("eas_schema_registry")` |
| WETH | `0x4200000000000000000000000000000000000006` (OP-stack predeploy; used by AgentFightClub `commit()`) | `network_config.get_contract_address("weth")` |
| `delivery_schema_uid` | Registered once per network before Step 8; written into `config/networks.json`, not `.env` | `network_config.get_delivery_schema_uid()` |

> **Correction (2026-07-15):** the ERC-8004 addresses above were fixed on
> chain `8453` (canonical) by an earlier commit (`bf69d81`) — the values
> previously listed here (`0x8004A818...`/`0x8004B663...`) were a real,
> deployed-but-not-the-ecosystem-standard registry pair (verified on
> Basescan, but not the address 8004scan.io and most third-party
> tools/explorers index by default — see
> `hackathon/research/ERC8004_RESOURCE_REVIEW.md`). That fix was never
> propagated to this table until now.
>
> **Known drift, not yet fixed:** `config/networks.json`'s `84532` (Base
> Sepolia) block still has the *old* addresses — the original ASSUMPTION
> below ("registry addresses are listed identically for both networks") is
> now literally false in config. Non-blocking (Sepolia is isolated-test
> only, never submission evidence) but worth a follow-up fix.
>
> ASSUMPTION: ERC-8004 registry addresses were originally assumed identical
> on both networks (consistent with a CREATE2 vanity deploy at a fixed
> address per chain) — no longer true for `84532` per the drift noted
> above; the schema already supports per-network divergence.

### EAS delivery schema

```
bytes32 deliverableHash, string taskType, address guildContract, uint256 paymentAmount
```
Resolver: `0x0000000000000000000000000000000000000000` (none for MVP) · Revocable: `false`.

---

## 3. A2A Message Contracts

Six message types. `A2AClient` (`src/shared/a2a.py`) handles **sync** messages
(Orchestrator as A2A client); `SpecialistA2AClient` (`src/specialist/a2a_client.py`)
handles **proactive** messages (Specialist as A2A client). Every message is
logged to `hackathon/notes/a2a_trace_{date}.json`. Messages marked **sync** are
responses within the same `message/send` request-response cycle (Orchestrator is the
A2A client). Messages marked **proactive** are separate `message/send` requests
initiated by the Specialist as A2A client → Orchestrator A2A server (port 10000).

| Message | Direction | Timing | Fields |
|---------|-----------|--------|--------|
| `task/invite` | Orchestrator → Specialist | sync | `task_spec: object` |
| `task/quote` | Specialist → Orchestrator | sync (response) | `scope: string`, `estimated_cost_wei: int`, `deadline_iso: string` |
| `task/send` | Orchestrator → Specialist | sync (non-blocking, `return_immediately: true`) | `task: object` (see below) |
| `task/delivered` | Specialist → Orchestrator | **proactive** (after harness completes) | `deliverable_reference: string`, `deliverable_hash: string`, `attestation_uid: string`, `attestation_url: string` |
| `task/accepted` | Orchestrator → Specialist | sync | `task_id: string`, `payment_proposal_id: string`, `payment_proposal_url: string` |
| `feedback/request` | Specialist → Orchestrator | **proactive** (after settlement) | `task_id: string`, `deliverable_hash: string` — Specialist asks the guild to record reputation for completed work |

> The `task/delivered` message is a **proactive A2A push** — the Specialist sends it as
> a new `message/send` to the Orchestrator's A2A server (port 10000) after the harness
> completes the work, not as a response to the original `task/send`. It carries
> **`attestation_uid` + `attestation_url`** — **never** an `on_chain_tx` field. EAS is the
> deliverable-commitment mechanism in the target design. `task/accepted` is a sync response
> carrying the **payment proposal** id+url (raised before it is sent); the Specialist later
> triggers reputation with a **proactive `feedback/request`** message.

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
  orchestrator_endpoint: string   # URL of the Orchestrator's A2A server (e.g. http://localhost:10000) — where the Specialist sends proactive task/delivered and feedback/request
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

### `NetworkConfig` — `src/shared/network_config.py`
- `get_chain_id() -> str` — reads `CHAIN_ID` from env (default `"8453"`).
- `get_network_config(chain_id=None) -> dict` — full `config/networks.json` block for the network.
- `get_contract_address(name, chain_id=None) -> str` — `name` is one of
  `erc8004_identity_registry`, `erc8004_reputation_registry`, `eas`,
  `eas_schema_registry`, `weth`.
- `get_rpc_url(chain_id=None) -> str` — builds the RPC URL, injecting `ALCHEMY_API_KEY`.
- `get_explorer_tx_url(tx_hash, chain_id=None) -> str`,
  `get_easscan_attestation_url(uid, chain_id=None) -> str`.
- `get_delivery_schema_uid(chain_id=None) -> str | None`.
- `is_canonical(chain_id=None) -> bool` — true only for Base.
- **Every other component reads network-specific values through this
  module — never from `os.environ` directly and never hardcoded.**

### `EASClient` — `src/shared/eas.py`
- `attest(deliverable_hash, task_type, guild_contract, payment_amount) -> { uid, url, tx_hash }`
  — Specialist-signed attestation against `network_config.get_delivery_schema_uid()`.
- `get_attestation(uid) -> { deliverableHash, taskType, guildContract, paymentAmount }`.

### `ERC8004` — `src/shared/erc8004.py`

Registration metadata is stored fully on-chain as a base64-encoded
`data:application/json;base64,...` URI (RFC 2397) — no IPFS pin or HTTPS
host needs to stay alive for the registration to remain resolvable.
Capabilities/skills live on the relevant `services[]` entry, never as a
top-level field, per [erc-8004/best-practices](https://github.com/erc-8004/best-practices)
and [best-practices.8004scan.io](https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html):

```jsonc
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "...", "description": "...",
  "services": [
    {"name": "A2A", "endpoint": "...", "version": "0.3.0", "a2aSkills": ["..."]},
    {"name": "OASF", "endpoint": "", "version": "0.8", "skills": ["..."], "domains": ["..."]}
  ],
  "active": true,                      // optional, defaults true
  "image": "...",                      // optional
  "x402Support": false,                // optional
  "registrations": [{"agentId": 1, "agentRegistry": "eip155:8453:0x..."}],  // optional; see register_agent()
  "supportedTrust": ["reputation"]     // optional
}
```

- `build_a2a_service(endpoint, version="0.3.0", a2a_skills=None) -> dict`,
  `build_mcp_service(endpoint, version="2025-06-18", tools=None,
  prompts=None, resources=None, capabilities=None) -> dict`,
  `build_oasf_service(skills=None, domains=None, endpoint="", version="0.8")
  -> dict` — convenience `services[]` entry builders (optional to use —
  `services` accepts any well-formed dict).
- `build_registration_uri(name, description, services, image=None,
  x402_support=None, active=True, registrations=None, supported_trust=None)
  -> str` — only `name`/`description`/`services` required; returns the
  base64 `data:` URI above.
- `build_registrations_entry(agent_id) -> dict` — `{"agentId":
  agent_id, "agentRegistry": "eip155:{chain_id}:{identity_registry_address}"}`
  (CAIP-10-style).
- `register(agent_uri, wallet_address) -> {"agent_id", "tx_hash",
  "agent_uri", "minted": bool}` — mints the agentId on
  `network_config.get_contract_address("erc8004_identity_registry")`
  through `WalletProvider` (no private key ever passed or read). Idempotent:
  if `wallet_address` already owns an agentId (`balanceOf() > 0`), no
  transaction is broadcast — the cached (`logs/erc8004_registrations.json`)
  or on-chain-recovered (`Registered` event scan) registration is returned
  instead, with `minted=False`.
- `update_registration_uri(agent_id, new_uri) -> tx_hash` — calls
  `setAgentURI(agentId, newURI)` through `WalletProvider`; the update path
  for any registration content change, never a second `register()`.
- `register_agent(name, description, services, wallet_address, image=None,
  x402_support=None, active=True, registrations=None, supported_trust=None)
  -> {"agent_id", "agent_uri" (final), "register_tx_hash",
  "update_tx_hash": str | None, "minted": bool}` — **the recommended entry
  point.** Composes the above: `build_registration_uri()` → `register()` →
  if `minted`, immediately backfills the `registrations[]` self-reference
  via `build_registrations_entry()` + `update_registration_uri()`, since
  `agentId` can't be known until `register()` succeeds. **Every fresh
  registration is therefore two on-chain transactions** (`Registered`, then
  `URIUpdated`) — the idempotent no-op path stays a single balance check,
  no transaction either way.
- `read_profile(agent_id) -> {"agent_id", "name", "capabilities",
  "domains", "delivery_count", "a2a_endpoint", "agent_uri"}` — decodes
  `tokenURI(agent_id)` (the `data:` URI locally, or an `https://`/`ipfs://`
  fallback for forward-compatibility, tolerating unresolvable URIs rather
  than raising); `capabilities`/`domains` are scanned across `services[]`
  (`a2aSkills` from A2A, `capabilities` from MCP, `skills`/`domains` from
  OASF — merged, deduplicated); `delivery_count` via
  `getSummary(agentId, [], "", "")` (correct by construction for a
  before-state/freshly-registered agent — full `clientAddresses`
  aggregation is deferred, see `hackathon/research/ERC8004_ERC8183_ANALYSIS.md` Gap 2).
- `give_feedback(caller, <6 fields>) -> tx_hash` — **still a stub**
  (issues #6/#7). Emits `DeliveryRecorded` on
  `network_config.get_contract_address("erc8004_reputation_registry")`.
  **Caller MUST be the guild contract (via DAO proposal execution) — never an
  agent EOA, never the Specialist wallet (F2).**

### `AgentFightClub` — `src/shared/agentfightclub.py`
- `launch(guild_name, mandate, governance_settings, member_list) -> { guild_address, treasury_address, tx_hash }`
- `commit(guild_address, amount_wei) -> tx_hash` — tribute (value-capped by the Pact)
- `propose(guild_address, payload) -> proposal_id` — membership, payment, or executable feedback
- `vote(guild_address, proposal_id, approve=True) -> tx_hash` — sponsor + vote + process
- `settle(guild_address, payment_proposal_id) -> tx_hash` — process the passed payment proposal

### `WalletProvider` — `src/shared/wallet.py`
- Provider-agnostic signing + Pact-scoping interface; **no raw-EOA fallback**.
- `sign(tx) -> signed_tx` — refuses any call outside the Pact allowlist or above the tribute cap.
- Allowlist scopes the DAO contract's `propose` / `vote` / `process` functions and the
  ERC-8004 IdentityRegistry's `register` / `setAgentURI` functions (both uncapped — neither
  moves funds out of the agent wallet); the tribute call carries the only value cap.
- Default implementation: Cobo CAW (TSS). Swappable to ZeroDev / Turnkey with the same
  allowlist + cap semantics (selected by `WALLET_PROVIDER`).

### `GuildToolsServer` — `src/guild/server.py` + `src/guild/tools.py`
- Shared MCP server (stdio) — any guild agent runs its own local instance
  with its own `AGENT_WALLET_*` env; not bound to the Orchestrator (see
  `10-technical-design.md` §12).
- Tool `guildtools_identity_register(name, description, services, image=None,
  x402_support=None, active=True, registrations=None, supported_trust=None)`
  — reads `AGENT_WALLET_ADDRESS` from its own process env, delegates to
  `erc8004.register_agent(...)`. Returns the same shape as
  `register_agent()`.
- Tool `guildtools_identity_read_profile(agent_id)` — delegates to
  `erc8004.read_profile(agent_id)`.
- `src/guild/tools.py::identity_register()` / `identity_read_profile()` take
  `wallet_address` as an explicit parameter and never read env vars
  themselves — `server.py`'s tool handler is the only place
  `AGENT_WALLET_ADDRESS` is read from the environment.

### `SpecialistAgent` handlers — `src/specialist/agent.py`
- `handle_task_invite(message) -> task/quote` — synchronous; returns quote in COMPLETED task
- `handle_task_send(message) -> WORKING` — non-blocking; delegates to the harness work engine and returns WORKING immediately. The harness later produces the deliverable, updates the task store to COMPLETED, and uses `SpecialistA2AClient` to send `task/delivered` proactively
- `request_feedback(task_id, deliverable_hash) -> feedback/request` — called by the harness after settlement to trigger the reputation stage; sends proactively via `SpecialistA2AClient` to the Orchestrator's A2A server

### `SpecialistA2AClient` — `src/specialist/a2a_client.py`
- `send_delivered(orchestrator_endpoint, task_id, deliverable_hash, attestation_uid, attestation_url) -> dict` — proactive `message/send` to the Orchestrator's A2A server after harness work completes
- `send_feedback_request(orchestrator_endpoint, task_id, deliverable_hash) -> dict` — proactive `message/send` after settlement to trigger the reputation proposal (Gate 4)
- Uses `a2a.client.client_factory.ClientFactory` to resolve the Orchestrator's Agent Card and send messages — same transport pattern as `A2AClient`

### `OrchestratorA2AServer` — `src/orchestrator/a2a_server.py`
- A2A HTTP server on `ORCHESTRATOR_A2A_PORT` (default 10000), running alongside the MCP stdio server
- Publishes an Agent Card at `/.well-known/agent-card.json`
- Receives inbound `task/delivered` → triggers deliverable pre-check (Gate 2)
- Receives inbound `feedback/request` → triggers reputation proposal (Gate 4)
- Built with the same `a2a-sdk` server components as the Specialist (`AgentExecutor`, `LegacyRequestHandler`, `InMemoryTaskStore`)

---

## 6. Environment Contract

`.env` holds only the network **selector** (`CHAIN_ID`) and **secrets**.
Every network-specific value (contract addresses, RPC URL, explorer links,
`delivery_schema_uid`) lives in `config/networks.json`, keyed by `CHAIN_ID` —
see §2. A ticket whose "Technical Constraints" section lists a contract
address or RPC URL as an env var is wrong; it should cite
`network_config.get_contract_address(...)` / `get_rpc_url()` instead.

### `.env`

| Variable | Purpose | Default |
|----------|---------|---------|
| `CHAIN_ID` | Active network — the only switch between Base (8453, canonical) and Base Sepolia (84532, isolated test); resolves into `config/networks.json` | `8453` |
| `ALCHEMY_API_KEY` | Secret — substituted into `config/networks.json`'s `rpc_url_template` | — (required) |
| `ORCHESTRATOR_WALLET_ADDRESS` | Treasury / launch caller | — (required) |
| `SPECIALIST_WALLET_ADDRESS` | Settlement target | — (required) |
| `CLAWBANK_API_KEY` | ClawBank API (skip → DAOhaus fallback) | optional |
| `WALLET_PROVIDER` | Scoped signing provider for `WalletProvider` (`caw` \| `zerodev` \| `turnkey`) | `caw` |
| `ORCHESTRATOR_A2A_PORT` | Orchestrator A2A port | `10000` |
| `SPECIALIST_A2A_PORT` | Specialist A2A port | `10001` |
| `AGENT_WALLET_ADDRESS` | The calling agent's own CAW wallet address — **per-process**: each agent's own environment, never a single global value shared across the Orchestrator and Specialist. Read only by `WalletProvider` (signing) and `GuildToolsServer`'s tool handler (ERC-8004 registration's idempotency/cache key) | — (required) |
| `AGENT_WALLET_API_KEY` | CAW API key for the calling agent's wallet (`caw wallet current --show-api-key`) — per-process, same scoping as `AGENT_WALLET_ADDRESS` | — (required) |
| `AGENT_WALLET_WALLET_ID` | CAW wallet ID for the calling agent — per-process, same scoping as `AGENT_WALLET_ADDRESS` | — (required) |

### `config/networks.json` (per `CHAIN_ID`, not an env var)

| Key | Purpose |
|-----|---------|
| `rpc_url_template` | RPC base URL with `{ALCHEMY_API_KEY}` placeholder |
| `explorer_tx_url` | Block-explorer tx URL prefix |
| `easscan_attestation_url` | easscan attestation URL prefix |
| `contracts.erc8004_identity_registry` | IdentityRegistry address |
| `contracts.erc8004_reputation_registry` | ReputationRegistry address |
| `contracts.eas` | EAS contract address |
| `contracts.eas_schema_registry` | EAS SchemaRegistry address |
| `contracts.weth` | WETH predeploy address |
| `delivery_schema_uid` | Registered delivery schema UID for this network |
| `role` | `"canonical"` or `"isolated-test"` |

---

## 7. Appendix — Naming Conventions

| Entity | Pattern | Example |
|--------|---------|---------|
| Classes | PascalCase | `OrchestratorServer`, `ERC8004`, `GuildContext` |
| Functions | snake_case | `guild_launch()`, `send_invite()` |
| Constants | SCREAMING_SNAKE | `CHAIN_ID`, `DEFAULT_CHAIN_ID`, `CONFIG_PATH` |
| A2A message types | `noun/verb` | `task/invite`, `task/delivered` |
| Files | snake_case | `agentfightclub.py`, `guild_context.json` |
| Git branches | `feat/`, `fix/`, `chore/` | `feat/eas-attestation` |
