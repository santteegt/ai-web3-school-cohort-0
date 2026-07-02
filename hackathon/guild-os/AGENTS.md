# CLAUDE.md — GuildOS

You are building **GuildOS**, a Python multi-service application that coordinates AI agents through the A2A protocol, on-chain treasury (AgentFightClub / Moloch v3), and verifiable reputation (ERC-8004) on **Base** (canonical: chain_id 8453). Scope is locked — `specs/` defines the boundaries; it is the **canonical, permanent source of truth** (finalized 2026-06-30). Code is disposable; the spec is not.

## Files — Read Before Coding

| File | Read When |
|------|-----------|
| `specs/00-overview.md` | Before any new feature — understand what we're solving, the North Star scenario, track alignment |
| `specs/20-api-contracts.md` | Before adding imports, calling external services, or touching pinned versions/addresses |
| `specs/10-technical-design.md` | Before any change to agent coordination logic, fallbacks, or component boundaries — includes §12 Transport & Integration Mechanics (what the code actually does at the wire level, not just the contract) |
| `specs/scenarios/*.feature` | Before implementing or changing any behavior — these are the executable definition of done; find the file covering your change before writing code |
| `skills/stylebook/SKILL.md` | Before writing a docstring, error message, log line, or comment — the judgment-level stylebook `ruff` can't check |
| `config/networks.json` | Before touching any contract address, RPC URL, or explorer link — these are network-specific, not env vars |
| `guild_context.json` | Current guild state (mock store — one JSON file per session) |
| `docs/*.md` | **Deprecated, historical only** — kept for provenance; do not treat as current. Exception: `docs/VALIDATION_PLAN.md` §11 (hackathon submission requirements) is still live — see [#17](https://github.com/santteegt/ai-web3-school-cohort-0/issues/17) |

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

**Two distinct controls, don't conflate them:**
- **File/component scope** (§5 of the ticket template) is the **enforcer** —
  it bounds which source files an agent may create or edit, the same role
  an IAM policy or file-tree allowlist plays. An unlisted file is out of
  bounds, full stop.
- **AgBOM** (§7) is the **observer** — a declared inventory of the
  *external* models, MCP servers/tools, and data sources a ticket is
  expected to use. It does not gate file edits. It exists for three
  things: (1) a **dynamic resource inventory** baseline before execution,
  (2) **behavioral monitoring** to catch intent drift if an agent starts
  reaching for external tools/libraries the ticket never declared, and (3)
  **auditability** — a record of why the agent called what it called.

Confusing the two has a real failure mode: a ticket that lists a GuildOS
source file in its AgBOM but not in §5 will make an executing agent stop
on the *wrong* file for the *wrong* reason.

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
- Create or edit only the files listed in the ticket's §5 File/component
  scope — that's the enforced boundary. Track your actual external
  resource usage against the ticket's AgBOM (§7) as a monitoring/audit
  check, not a second file gate; an undeclared external tool or model is a
  drift signal to flag, not grounds to block a file edit §5 already
  authorized.
- Before returning, run the self-verification checklist in the prompt and
  produce a **Vibe Diff** — three required parts (what changed, potential
  breakage points, risk assessment), placed at the top of the pull request
  description. This is what makes the LGTM-speed review in the next section
  possible — without it, the reviewer has to reconstruct intent *and* risk
  from the diff instead of confirming both.

### Reviewing a PR

**LGTM is conditional, not a courtesy.** A reviewer approves a GuildOS PR
only when all of the following hold — not "looks fine, I'll trust CI to
catch anything":

- CI (`pytest` + `ruff`, including the `I`/`G` rules — see
  `skills/stylebook/SKILL.md`) is **green on the PR itself**, not on a
  local run the author reported. If CI is red or hasn't run, the correct
  action is requesting changes or waiting, never approving with "should be
  fine once tests pass."
- The Vibe Diff's three parts are actually present and load-bearing — a
  "what changed" that's just a restated file list, a missing "potential
  breakage points," or a risk assessment that doesn't match what the diff
  actually touches (e.g. "Low" on a change that edits `WalletProvider`) is
  grounds to request changes on the PR description alone, before reading
  the diff.
- Every checkbox in `.github/PULL_REQUEST_TEMPLATE/default.md` is honestly
  ticked, not rubber-stamped — an unchecked or skipped box is a question to
  ask, not a formality to wave through.
- Any Out-of-Scope Finding in the PR is read and triaged (spun into its own
  ticket, or explicitly deferred) — approving the PR isn't the same as
  dismissing what it flagged.

If none of the above raise a concern, LGTM at the confidence the Vibe Diff's
risk assessment warrants — a Low-risk PR doesn't need the same scrutiny as
a High-risk one, but "conditional" means the condition was actually checked,
not skipped because the diff looked reasonable at a glance.

## Before Building

1. Read `specs/20-api-contracts.md` — versions and addresses are locked
2. Read `specs/10-technical-design.md` §8 (fallback requirements) and `specs/00-overview.md` §9 (decision log) — both already decided; don't re-evaluate
3. Check the Component Map above — use existing module names and class names exactly
4. Confirm which Phase (0–4) the issue belongs to; don't start a phase whose blocker phase isn't done — see "Sprint — Phase Gates" below

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
- If you hit a new failure pattern, add it as a fallback to `specs/10-technical-design.md` §8 (a new F-number) or as a new negative scenario in the relevant `specs/scenarios/*.feature` file — the spec is where recurring risks get recorded now, not `docs/VALIDATION_PLAN.md`

## When Unsure

- **Which library for Base calls?** → `web3.py` with Alchemy RPC; see `specs/20-api-contracts.md` §1
- **AgentFightClub API or DAOhaus SDK?** → Check `specs/00-overview.md` §9 Decision Log; ClawBank API confirmed working, but the actual current integration is a CLI subprocess wrapper, not either API — see `specs/10-technical-design.md` §12
- **Which wallet calls `giveFeedback()`?** → The **guild contract** (`msg.sender`) — via the executable proposal mechanism. Neither the Orchestrator's EOA nor the Specialist's wallet is ever the direct caller (see `specs/10-technical-design.md` §8 F2).
- **How does payment get released?** → Treasury is DAO-held. After Gate 2, call `payment_propose` (AFC `payment` proposal with deliverable details + specialist address); send `task/accepted` carrying the `payment_proposal_id`+url; **Gate 3** halts for the human to vote+process; `settle(guild_address, payment_proposal_id)` then processes the passed proposal. No agent wallet moves treasury funds.
- **Does `reputation_write` need a DAO proposal first?** → Yes — full sequence: Specialist sends `feedback/request`; (1) `reputation_propose` submits an executable `submitFeedback` Moloch proposal encoding the `giveFeedback()` call; (2) **Gate 4** halts for human vote; (3) on passing vote, `AgentFightClub.process(proposal_id)` executes the proposal — `msg.sender = guild contract`. Never call `giveFeedback()` directly from an EOA.
- **Which wallet provider / how is signing scoped?** → Use the `WalletProvider` abstraction (`src/shared/wallet.py`); CAW is the default, ZeroDev/Turnkey swappable via `WALLET_PROVIDER`. The Pact allowlists the DAO `propose`/`vote`/`process` calls, the ERC-8004 `register()` call, and caps tribute. **Never** fall back to raw EOA signing — halt instead. See `specs/scenarios/12_scoped_spending.feature`.
- **Need a contract address, RPC URL, or explorer link?** → Never read it from `os.environ` or hardcode it. Call `src/shared/network_config.py` (`get_contract_address`, `get_rpc_url`, `get_explorer_tx_url`, `get_easscan_attestation_url`, `get_delivery_schema_uid`) — it resolves the value from `config/networks.json` for the active `CHAIN_ID`. Only `CHAIN_ID` itself and secrets (`ALCHEMY_API_KEY`, private keys) live in `.env`. See `specs/20-api-contracts.md` §2/§6.
- **EAS schema not found on `attest()`?** → Check `network_config.get_delivery_schema_uid()`; register the schema and write the UID into `config/networks.json` (not `.env`) if missing (see `specs/10-technical-design.md` §8 F7)
- **New A2A message type needed?** → Check `src/shared/a2a.py` for the established pattern; don't invent new types without adding a scenario to the relevant `specs/scenarios/*.feature` file and updating `specs/20-api-contracts.md` §3
- **Is this feature in scope?** → Check `specs/10-technical-design.md` §2 and §10 (Constraints & Guardrails); if it doesn't map to a step in the loop or a scenario file, it's out of scope

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

## Sprint — Phase Gates

> Superseded the "Day 8–13" calendar table below on 2026-06-30 — the
> original hackathon dates had already passed and the team's near-term
> goal shifted to **dogfooding**: get the Specialist doing real GuildOS
> work as early as possible, then keep building the rest of the loop
> (settlement, reputation) in parallel. Phases replace calendar days;
> GitHub milestones mirror them exactly (Phase 0 → Phase 4).

| Phase | Theme | Gate to move on | Milestone |
|-------|-------|------------------|-----------|
| 0 | Wallet Infrastructure | `WalletProvider` (CAW) lands and is validated — nothing on-chain signs before this | [#30](https://github.com/santteegt/ai-web3-school-cohort-0/issues/30) |
| 0.5 | Agent Identity Bootstrap | Specialist registers on ERC-8004 first, Orchestrator second — both signed through `WalletProvider` | [#5](https://github.com/santteegt/ai-web3-school-cohort-0/issues/5) |
| 1 | Coordination MVP | Real `task/send` payload built and consumed — first real dogfood delegation reaches Gate 2 | [#32](https://github.com/santteegt/ai-web3-school-cohort-0/issues/32), [#10](https://github.com/santteegt/ai-web3-school-cohort-0/issues/10) |
| 2 | Evidence & Realism | EAS attestation replaces raw hash commit; guild formation takes real founder parameters | [#28](https://github.com/santteegt/ai-web3-school-cohort-0/issues/28), [#31](https://github.com/santteegt/ai-web3-school-cohort-0/issues/31) |
| 3 | Economic Loop | Payment proposal passed (Gate 3) · `settle()` tx · reputation proposal passed (Gate 4) · ERC-8004 delta | [#4](https://github.com/santteegt/ai-web3-school-cohort-0/issues/4), [#6](https://github.com/santteegt/ai-web3-school-cohort-0/issues/6), [#7](https://github.com/santteegt/ai-web3-school-cohort-0/issues/7) |
| 4 | Demo Readiness | Dispute path · E2E smoke test passes · README, demo script, submission form — repo clean | [#13](https://github.com/santteegt/ai-web3-school-cohort-0/issues/13), [#14](https://github.com/santteegt/ai-web3-school-cohort-0/issues/14), [#15](https://github.com/santteegt/ai-web3-school-cohort-0/issues/15), [#16](https://github.com/santteegt/ai-web3-school-cohort-0/issues/16), [#17](https://github.com/santteegt/ai-web3-school-cohort-0/issues/17) |

**Do not start a phase's issues before its blocker phase is done** — Phase
0 blocks everything (nothing signs on-chain without it); Phase 0.5 depends
on Phase 0; Phase 1 has no on-chain dependency and can be built in parallel
with 0/0.5 up to the point where it needs a registered Specialist to
delegate to. Phases 2–4 have no hard ordering constraint against each
other beyond their own internal ACs.

<details>
<summary>Original Day 8–13 calendar table (superseded, kept for history)</summary>

| Day | Date | Theme | P0 Gate |
|-----|------|-------|---------|
| 8 | Jun 8 | Validation | `launch` live · A2A test green · GLM-5.1 task locked |
| 9 | Jun 9 | Wallets + Identity | Both wallets on-chain · ERC-8004 agentIds · Guild funded |
| 10 | Jun 10 | A2A + Execution | Hash on Base mainnet · Basescan tx #1 saved |
| 11 | Jun 11 | Settlement + Reputation + E2E | payment proposal passed (Gate 3) · `settle()` tx · reputation proposal passed (Gate 4) · ERC-8004 delta · Smoke test passes |
| 12 | Jun 12 | Demo Prep | README, demo script, all artifacts — repo clean |
| 13 | Jun 13 | Submission | Submitted before 12:00 UTC+8 (04:00 UTC) |

</details>

## Customizing This File

Add new components to the Component Map when they are created. Update Don't rules when a fallback is triggered. Add phase-specific guidance when a new phase starts.

---

## Changelog

Moved to [`CHANGELOG.md`](CHANGELOG.md), organized per file/area instead of
as a flat timeline — read it when you need the history behind a specific
file, not as part of regular onboarding.
