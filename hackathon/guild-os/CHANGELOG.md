# GuildOS Changelog

> Moved out of `AGENTS.md` on 2026-07-01 to keep the live agent-rules file
> lean — `AGENTS.md` is read at the start of nearly every session (see its
> "Files — Read Before Coding" table and this template's Mode A cold-start
> block), so its own historical record was pure context overhead once it
> grew past a handful of entries. This file is reference-only: read it when
> you need to know *why* something is the way it is, not as onboarding.
>
> Organized **per file/area**, chronological within each section — the
> opposite of a flat timeline, so you can jump straight to the history of
> the one file you're touching instead of scanning entries about files you
> aren't.

---

## `AGENTS.md`

- **2026-06-30** — Component Map: tools 8→9 (added `payment_propose`), added
  `WalletProvider`, A2A messages now include `feedback/request`, gates
  0,0.5,1,2 → 0,0.5,1,2,3,4. When-Unsure: added payment-proposal (Gate 3)
  and wallet-provider entries; reputation → Gate 4. Don't: no agent EOA
  fallback, treasury is DAO-held. Sprint Day 11 reflects payment (Gate 3) +
  reputation (Gate 4).
- **2026-06-30** — Added **Spec-Driven Development — Issue Templates**
  section (Human Intent → BDD/Gherkin → spec → ticket chain), plus
  "Creating an issue" / "Working on an issue" workflows. See
  [templates/](#templatesissue_ticket_templatemd) below.
- **2026-06-30** — Network config extraction added a Component Map row,
  When-Unsure entry, Don't rule, and a "Files — Read Before Coding" row.
  Full change: see [`config/networks.json`](#confignetworksjson--src-sharednetwork_configpy).
- **2026-06-30** — Replaced the stale "Sprint — Day Gates" (Day 8–13,
  already past) with **"Sprint — Phase Gates"** (Phase 0 → 4). See
  [Process — Issues & Milestones](#process--issues--milestones).
- **2026-06-30** — `specs/` finalized as canonical: this file rewired
  top-to-bottom (intro, "Files — Read Before Coding," "Before Building,"
  "When Unsure," error-pattern note in "After Building") to point at
  `specs/` instead of `docs/`. See [`specs/`](#specs).
- **2026-07-01** — New "### Reviewing a PR" section: reviewer-facing
  Conditional LGTM — CI must be green on the PR itself, Vibe Diff's 3 parts
  must be present/load-bearing, PR template checkboxes honestly ticked,
  Out-of-Scope Findings triaged. See
  [`templates/TASK_EXECUTION_PROMPT.md`](#templatestask_execution_promptmd).
- **2026-07-01** — Stylebook references updated (Files table + Reviewing a
  PR) to `skills/stylebook/SKILL.md`. See
  [`skills/stylebook/SKILL.md`](#skillsstylebookskillmd).
- **2026-07-01** — Removed all SevenD/7D-framework artifacts. See
  [Removed artifacts](#removed-artifacts).
- **2026-07-01** — Three execution prompts unified into one. See
  [`templates/TASK_EXECUTION_PROMPT.md`](#templatestask_execution_promptmd)
  and [Deprecated prompts](#deprecated-promptspromptshermes_codingmd-promptsissue_coding_sessionmd).
- **2026-07-02** — SDD section trimmed: "Two distinct controls" and
  "Working on an issue" collapsed to short pointers at
  `templates/TASK_EXECUTION_PROMPT.md`, which now carries the full
  explanation in more detail than this file restated — same
  restate-in-two-places drift risk the prompt-unification entry above
  already fixed once. ~1.9KB removed from a file read at the start of
  nearly every session. See
  [`templates/TASK_EXECUTION_PROMPT.md`](#templatestask_execution_promptmd).

---

## `templates/ISSUE_TICKET_TEMPLATE.md`

- **2026-06-30** — Created, alongside `templates/TASK_EXECUTION_PROMPT.md`,
  as part of the Spec-Driven Development issue-template chain (Human Intent
  → BDD/Gherkin → spec → ticket).
- **2026-07-01** — **AgBOM/AC consistency bug fixed across the backlog.** An
  executing agent correctly stopped on issue #32 because its AgBOM (§7)
  omitted `src/orchestrator/server.py`/`tools.py`, which its own §3/§5
  required editing. Audited every open ticket — same pattern found and
  fixed in #4, #5, #6, #10, #13, #30, #31, #32. §7 now explicitly requires
  every source file an AC/Interface Definition names; a new Definition-of-
  Ready check ("AgBOM completeness") catches this before a ticket is
  assigned.
- **2026-07-01** — **AgBOM model corrected — the above fix conflated two
  different controls.** AgBOM is not a file-edit permission list; it's a
  *dynamic resource inventory* of external models/MCP-servers/tools/data-
  sources, for behavioral monitoring (intent-drift detection) and
  auditability. File/component scope — the actual enforcement boundary —
  belongs in §5 (Interface Definitions), which now carries an explicit
  "File / component scope (the enforcement boundary)" label. Reverted the
  GuildOS source-file paths stuffed into AgBOM across #4, #5, #6, #10, #13,
  #30, #31, #32 the same day; §5 now carries complete file scope for each
  instead (and gained `src/shared/a2a.py` for #32, still missing under
  either model). §5/§7 and the Definition of Ready rewritten accordingly.
- **2026-07-01** — Out-of-Scope Findings cross-reference added to §5,
  pointing at `templates/TASK_EXECUTION_PROMPT.md`'s output section.
- **2026-07-02** — §7's "MCP servers / external tools" example list
  expanded to name the project's actual standard toolset: the
  `evm-mcp-server` MCP server (`@mcpdotdirect/evm-mcp-server`, configured in
  root `.mcp.json` — balance checks, contract reads/writes, tx lookup), the
  `context7` MCP server/skill, the `cobo-agentic-wallet-developer` skill,
  and the `safishamsi/graphify` skill (repo → local queryable knowledge
  graph, for onboarding onto medium/large dependency codebases). Ticket
  authors were previously left to invent generic examples; now the template
  points at the tools actually available in this project.

---

## `templates/TASK_EXECUTION_PROMPT.md`

- **2026-06-30** — Created alongside `templates/ISSUE_TICKET_TEMPLATE.md`.
- **2026-07-01** — Rule 2 rewritten to split file-scope enforcement from
  AgBOM monitoring (see the `ISSUE_TICKET_TEMPLATE.md` AgBOM-model
  correction above); the two controls named explicitly at the top; a
  resource-usage audit report added to the output.
- **2026-07-01** — New rule 6: **Out-of-Scope Findings.** Non-blocking
  findings go in a PR output section; blocking findings (can't satisfy the
  ticket's own ACs without touching the out-of-scope file) escalate as a
  ticket defect instead, same as the rule-2 ticket-defect path.
- **2026-07-01** — **Vibe Diff formalized into 3 required parts** (What
  Changed / Potential Breakage Points / Risk Assessment Low-Medium-High +
  reason) — was previously just "what changed."
- **2026-07-01** — **Unified with `prompts/HERMES_CODING.md` and
  `prompts/ISSUE_CODING_SESSION.md` into the single canonical execution
  prompt.** Both `prompts/` files carried cold-start onboarding and a
  pre-coding AC-coverage audit protocol this file lacked; this file carried
  the corrected AgBOM/file-scope model, trajectory-mode enforcement, and
  Out-of-Scope Findings the other two never got. Rather than keep three
  drifting copies (a log-path inconsistency between `./logs/...` and
  `hackathon/guild-os/output/...` had already crept in), this file gained a
  **Mode A (Cold Start) / Mode B (Sub-Agent Dispatch)** selector: Mode A is
  a short, reference-only onboarding block (read `AGENTS.md` + specs,
  `gh issue view`, skip entirely if dispatched with a ticket in hand); the
  Shared Core carries the pre-coding audit table and When-In-Doubt decision
  tree forward, plus a new DELIVERY section (branch naming, full PR body
  contract, including a `## Resource Usage (AgBOM audit)` PR section and a
  required tool-call-trajectory side-by-side in `## Implementation
  details`). Deliberately did not inline a parallel hard-constraints block
  or port `HERMES_CODING.md`'s budget/model-switching operating rules —
  that content already lives in `AGENTS.md`/the PR template/the ticket's
  own §4/§6. See [Deprecated prompts](#deprecated-promptspromptshermes_codingmd-promptsissue_coding_sessionmd).

---

## `specs/`

- **2026-06-30** — `specs/README.md` finalized as canonical: DRAFT banner
  removed, Finalization Checklist executed. All 6 `docs/*.md` files marked
  deprecated (`VALIDATION_PLAN.md` partially — §11 hackathon submission
  checklist stays live). See the "docs/ → specs/ Migration Map" in
  `specs/README.md` for the full file-by-file mapping.
- **2026-06-30** — Added a Specialist self-registration Gherkin scenario to
  `specs/scenarios/02_talent_discovery.feature` and an
  ERC-8004-`register()` allowlist scenario to
  `specs/scenarios/12_scoped_spending.feature`, as part of reprioritizing
  around dogfooding (see [Process — Issues & Milestones](#process--issues--milestones)).
  Also added a Transport & Integration Mechanics section to
  `specs/10-technical-design.md`.
- **2026-07-01** — `specs/README.md`'s Layered Control Model table updated:
  stylebook reference moved to `skills/stylebook/SKILL.md`; "SevenD"
  dropped from the example-skills list (see
  [Removed artifacts](#removed-artifacts)).

---

## `config/networks.json` / `src/shared/network_config.py`

- **2026-06-30** — **Network config extracted to `config/networks.json`.**
  New `NetworkConfig` component (`src/shared/network_config.py`);
  `erc8004.py`/`agentfightclub.py` refactored to use it instead of
  hardcoded addresses/`RPC_URL` (also fixes a prior bug where `erc8004.py`
  hardcoded "Base Sepolia" against every other doc's "Base mainnet").
  `ERC8004_CONTRACT`, `REPUTATION_CONTRACT`, `EAS_CONTRACT`,
  `EAS_SCHEMA_REGISTRY`, `DELIVERY_SCHEMA_UID` removed from
  `.env`/`.env.example` — only `CHAIN_ID` (selector) and secrets remain
  there.

---

## `.github/PULL_REQUEST_TEMPLATE/default.md`

- **2026-07-01** — Out-of-Scope Findings section added; two stale/inverted
  lines fixed in passing (network constraint checkbox had testnet/mainnet
  backwards; Documentation section pointed at deprecated `docs/*.md`
  instead of `specs/`).
- **2026-07-01** — **Fully modernized.** Replaced the vestigial "Sprint
  Day" field and "7D Checklist → Definition → Design Gate" section (an
  earlier scaffolding approach with separate Definition/Design GitHub
  issues, superseded by the single-ticket SDD workflow) with **"Phase"**
  (0–4) and **"SDD Ticket Compliance"** (Gherkin Then-clauses, trajectory
  mode, §5 file scope, §6 security guardrails, regression, negative
  scenarios). GuildOS Constraints gained the `WalletProvider`-only-signing
  and DAO-proposal-only-payment rules. Added "Resource Usage (AgBOM
  audit)." Moved Vibe Diff to the top of the template.
- **2026-07-01** — Vibe Diff section formalized into 3 required parts
  (matches the `templates/TASK_EXECUTION_PROMPT.md` change).
- **2026-07-01** — Diagnostics checkbox updated to cite
  `skills/stylebook/SKILL.md`.

---

## `skills/stylebook/SKILL.md`

- **2026-07-01** — Created as `SKILLS.md` at the project root: workspace
  stylebook for docstrings, error messages, logging, and comments (what
  `ruff` can't check). `pyproject.toml`'s `[tool.ruff.lint]` gained `I`
  (import-sort) and `G` (logging-format) rules to mechanically enforce the
  two conventions that can be — 13 files auto-fixed, zero behavior change,
  all 106 tests still pass.
- **2026-07-01** — **Relocated to `skills/stylebook/SKILL.md`.** Now a
  proper skill directory with frontmatter (`name`, `description`),
  consistent with the layered control model's `skills/` convention. Also
  fixed a `docs/RISKS.md` citation inside the stylebook's own
  error-handling section — it was violating its own "cite specs/, never
  docs/" rule. References updated in `AGENTS.md`,
  `.github/PULL_REQUEST_TEMPLATE/default.md`, `pyproject.toml`'s
  `[tool.ruff.lint]` comments, `specs/README.md`.

---

## Deprecated prompts (`prompts/HERMES_CODING.md`, `prompts/ISSUE_CODING_SESSION.md`)

- **2026-06-30** — Ground-truth reading lists updated to read `specs/`
  instead of the newly-deprecated `docs/`.
- **2026-07-01** — Out-of-Scope Findings section added to both PR body
  contracts.
- **2026-07-01** — Vibe Diff referenced for the first time (previously
  neither file mentioned it at all).
- **2026-07-01** — **Deprecated.** Both files marked with a banner pointing
  to `templates/TASK_EXECUTION_PROMPT.md` as the sole canonical execution
  prompt; bodies left untouched, kept for historical reference only. See
  the `templates/TASK_EXECUTION_PROMPT.md` entry above for what replaced
  them.

---

## Process — Issues & Milestones

- **2026-06-30** — **Reprioritized around dogfooding.** Replaced the stale
  Day-based sprint calendar with Phase Gates (0 → 4), mirrored by new
  GitHub milestones (old ones closed). Goal: get the Specialist doing real
  work as early as possible, build settlement/reputation in parallel. Issue
  #5 restructured to register the **Specialist first** (it accrues
  reputation) and blocked on #30. Issue #30 (`WalletProvider`) reframed as
  Phase 0 — expanded to also allowlist `ERC-8004.register()`, since
  registration/guild-formation/membership are on-chain coordination too,
  not just fund movement; now blocks every other on-chain-signing ticket.
  New issue #32 files the previously-missing "richer `task/send` payload"
  ticket.

<details>
<summary>Original Day 8–13 calendar table (superseded by Phase Gates 2026-06-30, kept for history)</summary>

| Day | Date | Theme | P0 Gate |
|-----|------|-------|---------|
| 8 | Jun 8 | Validation | `launch` live · A2A test green · GLM-5.1 task locked |
| 9 | Jun 9 | Wallets + Identity | Both wallets on-chain · ERC-8004 agentIds · Guild funded |
| 10 | Jun 10 | A2A + Execution | Hash on Base mainnet · Basescan tx #1 saved |
| 11 | Jun 11 | Settlement + Reputation + E2E | payment proposal passed (Gate 3) · `settle()` tx · reputation proposal passed (Gate 4) · ERC-8004 delta · Smoke test passes |
| 12 | Jun 12 | Demo Prep | README, demo script, all artifacts — repo clean |
| 13 | Jun 13 | Submission | Submitted before 12:00 UTC+8 (04:00 UTC) |

</details>

- **2026-07-02** — Relocated this table out of `AGENTS.md`'s "Sprint —
  Phase Gates" section, where it sat inside a collapsed `<details>` block.
  That collapse only hides content in rendered GitHub UI — an agent reading
  the raw markdown file pays the full token cost regardless, so keeping
  confirmed-obsolete content there provided zero actual context savings.
  Moved here instead, where it's read on demand rather than every session.
- **2026-07-10** — **A2A harness-model canonicalization reconciled across
  the backlog.** Three same-day spec commits made the Orchestrator a full
  bidirectional A2A peer (new `OrchestratorA2AServer`/`SpecialistA2AClient`,
  `.well-known/agent.json` → `agent-card.json`, non-blocking `task/send`,
  new `orchestrator_endpoint` field) and five new issues (#36–#40) were
  filed to build it — but none followed `templates/ISSUE_TICKET_TEMPLATE.md`,
  and their prerequisite BDD scenarios didn't exist yet. Fixed in order:
  (1) added 8 new Given/When/Then scenarios (4 positive + 4 negative) across
  `05_task_delegation.feature`, `06_specialist_execution.feature`,
  `07_deliverable_attestation.feature`, `10_reputation_feedback.feature`,
  with your sign-off, before touching any ticket; (2) rewrote #36–#40 to
  the full template (Intent, BDD references, `EXACT | IN_ORDER` trajectory
  mode, file/component scope, Security Guardrails — including a new
  inbound-trust-boundary guardrail for `OrchestratorA2AServer` — AgBOM,
  Definition of Ready); (3) fixed 4 stale references in #5 (3×
  `agent.json` → `agent-card.json`, 1× `docs/RISKS.md` → `specs/`);
  (4) reconciled #10's file scope off `src/specialist/agent.py` →
  `handle_task_send()` onto the new `src/specialist/work_engine.py` module
  #40 introduces (they were about to both claim the same responsibility in
  different files), updated #28's scope from the now-narrowed
  `src/shared/a2a.py` to `src/specialist/a2a_client.py` (#37) where
  `task/delivered` is actually constructed now, and closed #6's own
  self-flagged gap ("don't let the agent infer the trigger mechanics") by
  linking it to the new scenarios and `Depends on #36, #37`; (5) assigned
  #36–#40 to milestone "Phase 1 — Coordination MVP" and updated the Phase 1
  row above to drop closed #32 and add an explicit **1a (plumbing) → 1b
  (dogfooding)** sub-order — build the transport/coordination cluster
  (#36–#39) end-to-end before wiring in real GLM-5.1 execution (#40, #10),
  per this project's own priority of proving coordination before delegating
  real work.
- **2026-07-10** — **#28 (EAS attestation) fully retrofitted to the ticket
  template**, closing the last of the informal, pre-SDD-template issues
  found during the reconciliation above. Beyond the file-scope fix already
  logged, added: §2 BDD scenario references (all 6 scenarios in
  `07_deliverable_attestation.feature`, including the F7 negative case),
  `EXACT | IN_ORDER` trajectory mode, a proper §5/§7 split, and a security
  guardrail clarifying EAS self-attestation is *not* subject to F2's
  guild-contract-only caller constraint (that's `giveFeedback()`-specific).
  Also caught and fixed: the EAS/SchemaRegistry contract addresses were
  hardcoded inline in the ticket text — corrected to route through
  `network_config.get_contract_address()`, matching every other
  contract-address rule in the project; and `EASClient.attest()`'s call
  site moves from the old `src/specialist/agent.py` to
  `src/specialist/work_engine.py`, the same #40-driven relocation #10
  already got, since the attestation call sits right next to the hash it
  attests.
- **2026-07-10** — **Closed a gap in #39: nothing actually set
  `orchestrator_endpoint`.** The field was referenced across #36–#39 as
  something the Specialist reads and validates, but no ticket had an
  explicit AC to construct it. Traced it to `run_coordination_loop()`'s
  `full_task` dict (`src/cli/runner.py` ~L190–229), which already builds
  every other `task/send` field — added the missing AC to #39, its natural
  owner, since that's the exact function and dict already in its scope.

---

## Casual Hackathon — Event Record

> The AI × Web3 Agentic Builders Hackathon has **concluded**. GuildOS
> (`hackathon/guild-os/`) was the submitted project. This section is the
> historical record of the event — dates, tracks, and submission
> requirements — moved here from root `AGENTS.md` §16 on 2026-07-02 since
> none of it is forward-looking anymore. For the still-useful platform
> CLI/API reference (reusable if Santiago does a future Casual Hackathon
> event), see `setup/CASUAL_HACKATHON.md`.

### Event Reference

| Field | Value |
|---|---|
| Event name | AI × Web3 Agentic Builders Hackathon |
| Platform | https://casualhackathon.com |
| Event page | https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy |
| Event ID | `cmpsjubkg0003p80kxuzrdyjy` |
| Status | **Concluded** |
| Build period | 2026-06-01 — 2026-06-12 |
| Submission deadline | 2026-06-13 12:00 UTC+8 (04:00 UTC) |
| Demo Day | 2026-06-14 |
| Results | 2026-06-17 |
| Prize pool | 7000 USDT total (Cobo: 3500 USDT · Z.AI: 3500 USDT) |

### Tracks

| Track | Slug | Focus |
|---|---|---|
| Cobo \| Agentic Economy × Cobo Agentic Wallet | `cobo-agentic-economy-cobo-agentic-wallet` | Agent-native payments, trustless work agreements, agent resource procurement, autonomous trading, A2A economy |
| Z.AI \| Web3 × Long-Horizon Task | `z-ai-web3-long-horizon-task` | Agentic dev tools, 3D world building, creator economy — all powered by GLM-5.1 for long-horizon autonomous execution |

### Key Submission Requirements (from platform)

1. Project name + one-sentence description
2. GitHub Repo with README (problem, architecture, run instructions, API/SDK used)
3. Demo link or video (3–5 min recommended)
4. On-chain / testnet evidence (contract addresses, tx hashes, agent wallet address, screenshots)
5. Team info (members, roles, wallet addresses, contact)
6. For Cobo track: CAW key code/config, wallet address, proof of funds execution
7. For Z.AI track: GLM-5.1 usage, long-horizon task run log, Web3 proof

### Submission Checklist

Tracked at `hackathon/SUBMISSION_CHECKLIST.md`.

---

## Removed artifacts

- **2026-07-01** — Deleted `.cursor/rules/7d-framework.mdc` and
  `.windsurf/rules/7d-framework.md` — both `alwaysApply`/`always_on` IDE
  rule files from the project's original 7D-framework scaffolding, stale
  duplicates of `AGENTS.md` predating everything built this session, and
  actively wrong on network policy ("Base Sepolia only — never mainnet,"
  the inverse of the locked "Base canonical, Base Sepolia
  isolated-test-only" rule). `AGENTS.md` is the single canonical
  instruction file now.
