# CLAUDE.md — GuildOS

You are building **GuildOS**, a Python multi-service application that coordinates AI agents through the A2A protocol, on-chain treasury (AgentFightClub / Moloch v3), and verifiable reputation (ERC-8004) on **Base mainnet (chain_id 8453)**. This is a **7-day hackathon build** ending June 13. Scope is locked — every file in `docs/` defines the boundaries.

## Files — Read Before Coding

| File | Read When |
|------|-----------|
| `docs/PROBLEM.md` | Before any new feature — understand what we're solving |
| `docs/TECH_STACK.md` | Before adding imports or calling external services |
| `docs/MVP_FLOW.md` | Before any change to agent coordination logic |
| `docs/RISKS.md` | Before touching AgentFightClub, ERC-8004, or ZeroDev — fallbacks are already decided |
| `docs/VALIDATION_PLAN.md` | Definition of done per integration |
| `config/networks.json` | Before touching any contract address, RPC URL, or explorer link — these are network-specific, not env vars |
| `guild_context.json` | Current guild state (mock store — one JSON file per session) |

## Component Map — Use These Names, Never Invent New Ones

| Component | Location | What It Does |
|-----------|----------|--------------|
| `OrchestratorServer` | `src/orchestrator/server.py` | MCP server entry point; registers all tools |
| `OrchestratorTools` | `src/orchestrator/tools.py` | 9 tools: `guild_launch`, `talent_query`, `task_invite`, `task_delegate`, `deliverable_review`, `payment_propose`, `settle`, `reputation_propose`, `reputation_write` |
| `SpecialistAgent` | `src/specialist/agent.py` | Python A2A server; runs GLM-5.1 long-horizon tasks; responds to task messages; sends `feedback/request` after settlement |
| `A2AClient` | `src/shared/a2a.py` | Sends/receives A2A messages (invite, quote, send, delivered, accepted, feedback/request) |
| `EASClient` | `src/shared/eas.py` | `attest()` and `get_attestation()` — Specialist creates EAS delivery attestation; UID embedded in A2A `task/delivered` |
| `ERC8004` | `src/shared/erc8004.py` | `register()` and `giveFeedback()` — caller constraint: NOT the agent's own wallet (guild contract via proposal execution) |
| `AgentFightClub` | `src/shared/agentfightclub.py` | `launch`, `commit`, `propose`, `vote`, `settle` — ClawBank API or DAOhaus SDK fallback |
| `WalletProvider` | `src/shared/wallet.py` | Provider-agnostic signing + Pact scoping (CAW default; ZeroDev/Turnkey swappable); scopes DAO calls + caps tribute; no EOA fallback |
| `NetworkConfig` | `src/shared/network_config.py` | Loads `config/networks.json` for the active `CHAIN_ID`; the only path to a contract address, RPC URL, or explorer link |
| `GuildContext` | `src/shared/guild_context.py` | Read/write `guild_context.json`; the mock guild state store |
| `HumanGates` | `src/cli/gates.py` | Gate 0, 0.5, 1, 2, 3, 4 — CLI `y/N` prompts; always halt execution and wait |

## Spec-Driven Development — Issue Templates

GuildOS issues are not free-text tickets — they're the last link in a chain
that starts with human intent and ends in code an agent can execute without
guessing:

```
Human Intent → BDD/Gherkin scenarios (specs/scenarios/*.feature)
            → feature spec (specs/10-technical-design.md, specs/20-api-contracts.md)
            → a fully specified ticket
```

**Why this matters:** a ticket is the only barrier standing between an agent
and a hallucinated implementation. Given a blueprint, an agent executes.
Given a vibe, it guesses — and on a project with on-chain calls, caller
constraints, and DAO-governed money movement, a guess is never a free
mistake. A complete ticket always carries: acceptance criteria, technical
constraints (including the tool-call trajectory mode), interface
definitions, security guardrails, and an AgBOM (Agent Bill of Materials).

Two templates govern this — read both before creating or picking up an issue:

| Template | Use it when | Location |
|----------|-------------|----------|
| Issue Ticket Template | Creating a new GitHub issue | `templates/ISSUE_TICKET_TEMPLATE.md` |
| Task-Execution Prompt | Dispatching an agent to implement an existing ticket | `templates/TASK_EXECUTION_PROMPT.md` |

### Creating an issue

1. Confirm the behavior is already captured as a Given/When/Then scenario in
   `specs/scenarios/*.feature`. **If it isn't, don't write the ticket yet** —
   work with the user to draft the scenario first (positive case + at least
   one negative/should-not-fire case), get their sign-off, and add it to the
   right feature file — or a new one, following `specs/README.md`'s naming
   convention — before continuing.
2. Copy `templates/ISSUE_TICKET_TEMPLATE.md` into the new issue body and fill
   in every section, linking to the spec instead of restating it wherever
   possible.
3. Walk the **Definition of Ready** checklist at the bottom of the template.
   If any box is unchecked, the ticket is not ready to assign — finish it.
   An unchecked box is exactly the kind of gap an agent will fill with a guess.
4. Writing the BDD scenario *with* the user up front, rather than inferring
   it from a vague request, is what later lets the user review the resulting
   pull request at LGTM speed — the scenario already states what "done"
   looks like, so they're confirming, not re-deriving it from the diff.

### Working on an issue

Before touching any source file for a specific issue, read
`templates/TASK_EXECUTION_PROMPT.md` and follow it as the execution contract
for that ticket — not just as background reading. In particular:

- Treat the ticket and `specs/` as ground truth, over any inference from the
  current state of `src/`. Where existing source code disagrees with the
  spec, the spec wins (see the layered control model in `specs/README.md`).
- Honor the ticket's tool-call trajectory mode exactly — `EXACT | IN_ORDER`
  for high-risk or state-mutating calls (anything on-chain, anything that
  moves funds or writes reputation), `ANY_ORDER` for read-only calls.
- Stay inside the ticket's AgBOM. A tool, model, or data source not listed
  there is not authorized for this ticket — stop and ask rather than expand
  scope silently.
- Before returning, run the self-verification checklist in the prompt and
  produce a **Vibe Diff**: a short, plain-English summary of what changed and
  why, placed at the top of the pull request description. This is what makes
  the LGTM-speed review in the previous section possible — without it, the
  reviewer has to reconstruct intent from the diff instead of confirming it.

## Before Building

1. Read `docs/TECH_STACK.md` — versions and library choices are locked
2. Read `docs/RISKS.md` Decision Log — fallbacks are already decided; don't re-evaluate
3. Check the Component Map above — use existing module names and class names exactly
4. Confirm which sprint Day (8–13) the task belongs to; match that Day's P0 gate

## While Building

- All A2A messages must be logged to `./logs/a2a_trace_{date}.json`
- All GLM-5.1 calls must log plan + tool calls + output to `./logs/glm_trace_{date}.json`
- Every human gate (0, 0.5, 1, 2, 3, 4) must halt execution and wait for explicit `y` — never skip or auto-proceed
- All on-chain calls must log the tx hash and print the Base mainnet Basescan URL (https://basescan.org/tx/...)
- Guild state transitions must update `guild_context.json` immediately after the on-chain event

## After Building

- Run `make test` — all tests must pass
- Run `make lint` — no lint errors
- Log any new on-chain tx hashes to `./logs/tx_hashes.md`
- Add new error patterns to `docs/VALIDATION_PLAN.md` under the relevant section

## When Unsure

- **Which library for Base mainnet calls?** → `web3.py` with Alchemy RPC; see `docs/TECH_STACK.md`
- **AgentFightClub API or DAOhaus SDK?** → Check `docs/RISKS.md` § Decision Log; ClawBank API confirmed working Day 9
- **Which wallet calls `giveFeedback()`?** → The **guild contract** (`msg.sender`) — via the executable proposal mechanism. Neither the Orchestrator's EOA nor the Specialist's wallet is ever the direct caller (see `docs/RISKS.md §F2`).
- **How does payment get released?** → Treasury is DAO-held. After Gate 2, call `payment_propose` (AFC `payment` proposal with deliverable details + specialist address); send `task/accepted` carrying the `payment_proposal_id`+url; **Gate 3** halts for the human to vote+process; `settle(guild_address, payment_proposal_id)` then processes the passed proposal. No agent wallet moves treasury funds.
- **Does `reputation_write` need a DAO proposal first?** → Yes — full sequence: Specialist sends `feedback/request`; (1) `reputation_propose` submits an executable `submitFeedback` Moloch proposal encoding the `giveFeedback()` call; (2) **Gate 4** halts for human vote; (3) on passing vote, `AgentFightClub.process(proposal_id)` executes the proposal — `msg.sender = guild contract`. Never call `giveFeedback()` directly from an EOA.
- **Which wallet provider / how is signing scoped?** → Use the `WalletProvider` abstraction (`src/shared/wallet.py`); CAW is the default, ZeroDev/Turnkey swappable via `WALLET_PROVIDER`. The Pact allowlists the DAO `propose`/`vote`/`process` calls and caps tribute. **Never** fall back to raw EOA signing — halt instead.
- **Need a contract address, RPC URL, or explorer link?** → Never read it from `os.environ` or hardcode it. Call `src/shared/network_config.py` (`get_contract_address`, `get_rpc_url`, `get_explorer_tx_url`, `get_easscan_attestation_url`, `get_delivery_schema_uid`) — it resolves the value from `config/networks.json` for the active `CHAIN_ID`. Only `CHAIN_ID` itself and secrets (`ALCHEMY_API_KEY`, private keys) live in `.env`.
- **EAS schema not found on `attest()`?** → Check `network_config.get_delivery_schema_uid()`; register the schema and write the UID into `config/networks.json` (not `.env`) if missing (see `docs/RISKS.md §F7`)
- **New A2A message type needed?** → Check `src/shared/a2a.py` for the established pattern; don't invent new types without updating `docs/MVP_FLOW.md`
- **Is this feature in scope?** → Check `docs/MVP_FLOW.md`; if not in the 15 steps, it's out of scope

## Don't

- Run any transaction on Ethereum mainnet — never Ethereum mainnet under any circumstance
- Hardcode chain_id — always read from `CHAIN_ID` env var (8453 = Base canonical/evidence; 84532 = Base Sepolia isolated testing only)
- Use Base Sepolia for submission evidence — Basescan tx #1/2/3 must be on Base (8453)
- Hardcode a contract address, RPC URL, or explorer link, or read one from `os.environ` directly — always go through `src/shared/network_config.py`; the values live in `config/networks.json`, not `.env`
- Hardcode private keys, API keys, or seed phrases in source files
- Fall back to raw EOA signing for agents — sign only through the scoped `WalletProvider`; halt if no scoped provider is available
- Move treasury funds outside a DAO proposal — treasury is DAO-held; payment flows only through the Gate-3 payment proposal
- Skip human gate prompts — every gate must halt and wait; use `src/cli/gates.py`
- Add Python packages without updating `requirements.txt`
- Call `giveFeedback()` from the Specialist Agent's wallet — it will revert (F2)
- Build UI components — two terminal windows are the demo surface
- Query the live ERC-8004 registry for talent matching — hardcoded Specialist profile is MVP
- Implement ragequit on-chain — document the path only
- Add features not in the 15-step MVP flow

## Sprint — Day Gates

| Day | Date | Theme | P0 Gate |
|-----|------|-------|---------|
| 8 | Jun 8 | Validation | `launch` live · A2A test green · GLM-5.1 task locked |
| 9 | Jun 9 | Wallets + Identity | Both wallets on-chain · ERC-8004 agentIds · Guild funded |
| 10 | Jun 10 | A2A + Execution | Hash on Base mainnet · Basescan tx #1 saved |
| 11 | Jun 11 | Settlement + Reputation + E2E | payment proposal passed (Gate 3) · `settle()` tx · reputation proposal passed (Gate 4) · ERC-8004 delta · Smoke test passes |
| 12 | Jun 12 | Demo Prep | README, demo script, all artifacts — repo clean |
| 13 | Jun 13 | Submission | Submitted before 12:00 UTC+8 (04:00 UTC) |

## Customizing This File

Add new components to the Component Map when they are created. Update Don't rules when a fallback is triggered. Add Day-specific guidance before each morning session starts.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-30 | Component Map: tools 8→9 (added `payment_propose`), added `WalletProvider`, A2A messages now include `feedback/request`, gates 0,0.5,1,2 → 0,0.5,1,2,3,4. When-Unsure: added payment-proposal (Gate 3) and wallet-provider entries; reputation → Gate 4. Don't: no agent EOA fallback, treasury is DAO-held. Sprint Day 11 reflects payment (Gate 3) + reputation (Gate 4). Mirrors `specs/` + `docs/` design feedback. |
| 2026-06-30 | Added **Spec-Driven Development — Issue Templates** section (between Component Map and Before Building): the Human Intent → BDD/Gherkin → spec → ticket chain, plus "Creating an issue" and "Working on an issue" workflows. Added `templates/ISSUE_TICKET_TEMPLATE.md` and `templates/TASK_EXECUTION_PROMPT.md`. |
| 2026-06-30 | **Network config extracted to `config/networks.json`.** New `NetworkConfig` component (`src/shared/network_config.py`); `erc8004.py`/`agentfightclub.py` refactored to use it instead of hardcoded addresses/`RPC_URL` (also fixes a prior bug where `erc8004.py` hardcoded "Base Sepolia" against every other doc's "Base mainnet"). `ERC8004_CONTRACT`, `REPUTATION_CONTRACT`, `EAS_CONTRACT`, `EAS_SCHEMA_REGISTRY`, `DELIVERY_SCHEMA_UID` removed from `.env`/`.env.example` — only `CHAIN_ID` (selector) and secrets remain there. Added Component Map row, When-Unsure entry, Don't rule, and a "Files — Read Before Coding" row. |
