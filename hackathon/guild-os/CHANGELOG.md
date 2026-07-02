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
