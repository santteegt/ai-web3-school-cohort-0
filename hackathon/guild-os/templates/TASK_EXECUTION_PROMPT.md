# Task Execution Prompt — Unified Entrypoint (Cold Start + Sub-Agent Dispatch)

> Use this as the kickoff prompt for an agent implementing one ticket —
> whether it's starting a session cold (no prior context) or being dispatched
> as an ephemeral sub-agent that already has a ticket in hand. Pick a mode
> below and paste only that block; don't paste both.
>
> This prompt only runs against tickets that already satisfy the
> **Definition of Ready** in `templates/ISSUE_TICKET_TEMPLATE.md`. If a
> ticket doesn't, send it back for completion — don't let the agent guess
> the missing fields to fill the gap itself.
>
> **Supersedes** `prompts/HERMES_CODING.md` and `prompts/ISSUE_CODING_SESSION.md`
> (both deprecated 2026-07-01 — kept for historical reference only). Their
> cold-start orientation and pre-coding audit table are folded into Mode A
> and the shared core below.

---

## Mode A — Cold Start (single- or multi-issue)

> **Skip this entire block if you're Mode B** — go straight to "Shared Core"
> below with your ticket already pasted into `TICKET:`.

Use when the agent has no prior session context — a fresh Claude Code
session, an external agent (e.g. Hermes/GLM-backed), or any runtime that
needs to orient itself before it can even identify its ticket.

```
Clone/pull the repo, then read in order:

1. hackathon/guild-os/AGENTS.md — Component Map (exact class names + file
   paths), build rules, the Don't list, the When-Unsure shortcuts, Phase
   gates. USE THESE NAMES EXACTLY — never invent new ones.
2. hackathon/guild-os/specs/20-api-contracts.md — pinned library versions,
   contract addresses, env contract. Read before adding any import.
3. hackathon/guild-os/specs/10-technical-design.md — the 15-step
   coordination loop, fallbacks, transport mechanics. Every file you touch
   must map to one of these steps.
4. hackathon/guild-os/specs/scenarios/*.feature — the file(s) your ticket(s)
   link to. This is the executable Given/When/Then definition of done.

Then fetch your issue(s) live (issue body is authoritative — treat it as
the TICKET input below; if it was written with ISSUE_TICKET_TEMPLATE.md it
already names its own §5 file scope, §6 security guardrails, and §7 AgBOM):

   gh issue view <N> --repo santteegt/ai-web3-school-cohort-0

If assigned multiple issues, build in dependency order — one branch, one PR
per issue, do not batch several issues into one branch.
```

---

## Mode B — Sub-Agent Dispatch

Use when a ticket is being handed directly to an ephemeral sub-agent by an
already-oriented caller session (the caller has already read the ground
truth above). You are running inside an isolated, ephemeral sandbox — no
cloning or onboarding needed. Proceed straight to the Shared Core with the
ticket pasted below.

```
INPUTS:
- TICKET: <paste the full ticket body here>
- SPEC REFERENCES: specs/10-technical-design.md, specs/20-api-contracts.md
  (and the specific specs/scenarios/*.feature file the ticket links to)
```

---

## Shared Core (both modes)

```
You are executing ONE ticket. The ticket and the specs/ folder are ground
truth. Code that deviates from either is quarantined — it does not get
merged on the strength of "it works."

TWO SEPARATE CONTROLS — DO NOT CONFUSE THEM:
  - §5 File/component scope = the ENFORCER. Bounds which source files you may
    create or edit. An unlisted file is out of bounds, full stop.
  - §7 AgBOM = the OBSERVER. Declares which external models, MCP servers,
    tools, and data sources you're expected to call. It does not gate file
    edits — it exists so drift and scope can be monitored and audited.

═══════════════════════════════════════════════════════════════════════════
STEP 1 — PRE-CODING CLARIFICATION PASS (mandatory — do not skip)
═══════════════════════════════════════════════════════════════════════════

Before writing a single line of implementation code, produce an audit table.
For each acceptance criterion in the ticket, write one row:

  AC # | Acceptance criterion (quoted) | Doc + section that covers it | Coverage

Coverage must be one of:
  FULL    — the doc specifies exactly what to build; no judgment call required
  PARTIAL — the doc addresses this area but leaves at least one detail unspecified
  MISSING — no doc covers this; you would have to invent the behaviour

Example row:
  AC 2 | "Attestation UID embedded in A2A task/delivered" |
         specs/10-technical-design.md §2 Step 9 + specs/20-api-contracts.md §3 | FULL

For every PARTIAL or MISSING row, draft a blocking question using the
WHEN IN DOUBT format below (quote the vague line, give 2–3 options, state
your lean).

Then output one of these two endings — nothing else:

  A) "BLOCKING QUESTIONS — waiting for answers before implementation."
     (list the questions)

  B) "No blockers. All acceptance criteria are fully specified. Proceeding
     to implementation."

Post this output and wait for explicit acknowledgement before touching any
source file. A "looks good, proceed" is sufficient for outcome B. For
outcome A, wait for answers to every question before starting.

═══════════════════════════════════════════════════════════════════════════
WHEN IN DOUBT — STOP AND ASK (do not build on a guess)
═══════════════════════════════════════════════════════════════════════════

Before writing code for any step you are uncertain about, exhaust this
decision tree in order:

1. AGENTS.md "When Unsure" block — fast answers for the most common
   questions (library choice, caller constraints, schema UIDs, gate
   numbering).
2. specs/00-overview.md §9 Decision Log — if the question involves a
   tech-stack or library choice, the decision is already logged there. Do
   NOT re-evaluate a closed decision; just follow it.
3. The .feature scenario(s) the ticket links to — the Given/When/Then
   Then-clauses often resolve ambiguity about what "done" means for a given
   piece of behavior; that's what they're for.
4. specs/20-api-contracts.md and specs/10-technical-design.md in depth —
   re-read the relevant step and the component entry to see if the answer
   is implicit in the contract spec.

If the question is still unresolved after all four steps, STOP and post a
blocking question BEFORE writing any implementation code. Your question
MUST include:

  a. Which ticket, step, and component you are implementing.
  b. The exact spec doc + section/line that is vague or missing — quote it
     verbatim.
  c. The 2–3 concrete options you are considering — not an open question.
  d. Which option you lean toward and the single sentence reason why.

Then wait for an explicit answer. Do not proceed on assumption.

DO NOT: make a judgment call on an ambiguous requirement and hide it in a
code comment; build a partial/placeholder implementation "to show progress"
while a blocker is open; open a draft PR without listing every unresolved
question under "## Blockers / open questions."

DO: ask early — a 10-minute blocking question now beats a wrong
implementation and a full re-review cycle; one question per distinct
blocker, don't batch unrelated ones; after the answer, note the resolution
at the call site so the next reviewer doesn't re-derive it.

═══════════════════════════════════════════════════════════════════════════
EXECUTION CONTRACT
═══════════════════════════════════════════════════════════════════════════

1. Parse the Gherkin scenarios referenced in the ticket. Plan a tool-call
   sequence that honors the ticket's trajectory mode:
     - EXACT | IN_ORDER (high-risk / state-mutating / on-chain) — follow the
       scenario's tool-call order exactly. No substitutions, no reordering.
     - ANY_ORDER (read-only) — sequence freely, but every required call must
       still happen before the Then-clause it satisfies.
2. Write or extend the linked scenario's `tests/step_defs/` file **before
   any `src/` change** (check `tests/step_defs/` for an existing file for
   this feature; extend it if one exists). Run it and confirm it fails for
   the right reason — missing/incomplete behavior, not a step-text typo or
   an import error. This is the executable form of the spec; the
   implementation work in steps 3+ is "make it green," not the other way
   around.
3. Create or edit ONLY the files/components listed in the ticket's §5 File/
   component scope. If the work requires touching a file not listed there,
   STOP and ask — do not improvise and do not silently expand scope. If §3's
   Acceptance Criteria already names that file, say so explicitly: that's a
   **ticket defect** (§5 out of sync with §3), not a genuine scope question —
   report it back for the ticket to be fixed.
4. Track your actual external resource usage (models called, MCP
   servers/tools/APIs/CLIs invoked, data sources consulted) against the
   ticket's declared AgBOM (§7) as you go. If you find yourself reaching for
   an external tool, library, or data source not in the AgBOM, treat that as
   a signal, not a silent green light: either the AgBOM is incomplete (flag
   it as a ticket defect) or you've drifted from the ticket's actual scope
   (stop and reconsider before proceeding). This is about intent-drift
   detection and audit trail, not a second permission gate — the enforcement
   already happened in step 3. Also note, for each distinct LLM you called
   (the executing agent itself and any sub-agent it dispatched), the
   provider/model name and total tokens used, if your runtime exposes that
   figure — this is cost/usage audit trail, not a gate; report "not exposed
   by runtime" rather than guessing when the figure isn't available.
5. Use the exact pinned versions from specs/20-api-contracts.md §1. Pull
   dependencies only from the project's vetted source (uv.lock / pyproject.toml).
   Any new package goes in pyproject.toml in the same PR. Never echo, log, or
   persist secrets; treat any JIT credentials as expiring at task end — don't
   cache them past this run.
6. Implement against the spec, not your assumptions, until step 2's step-def
   file is green. Where the ticket or the spec is silent on a decision that
   matters (a caller address, a gate placement, a fallback path), follow the
   WHEN IN DOUBT decision tree above rather than guess. Once green, write or
   extend hand-written unit test(s) in `tests/test_*.py` covering the
   specific functions/branches this ticket added or changed — error paths,
   edge cases, and exact-value assertions the linked scenario's Then-clauses
   don't require (they're deliberately coarse: boolean outcomes, field
   presence). This is the same more-granular layer already underneath every
   existing BDD scenario in this project (see `test_erc8004.py`,
   `test_wallet_provider.py`, etc.) — new work should arrive with that layer
   already in place, not bolted on later by a future audit.
7. If you notice something outside your §5 scope that needs attention — a
   bug, a stale reference, a broken test, a spec/doc inconsistency, a
   security concern — you have exactly two options, never a third:
     a. NON-BLOCKING (doesn't stop you from finishing this ticket): do NOT
        fix it inline, even if the fix looks trivial. That's scope creep —
        it bundles an unreviewed change into a PR meant to be reviewable at
        LGTM speed for one thing. Record it in the Out-of-Scope Findings
        output (below) and keep going.
     b. BLOCKING (you cannot satisfy this ticket's own ACs without touching
        it): STOP and ask, the same as step 3's ticket-defect path — this
        is a real scope gap in the ticket, not something to route around
        by quietly expanding your file scope.
   Never silently drop a finding either way — the whole point of noticing
   is defeated if it evaporates when you return control.

If a primary integration fails, switch to the documented fallback in
specs/10-technical-design.md §8, note it in the PR, and keep going. Do not
debug a known-fallback path for more than 2 hours.

═══════════════════════════════════════════════════════════════════════════
SELF-VERIFICATION (run before returning control)
═══════════════════════════════════════════════════════════════════════════
- [ ] Every Gherkin Then-clause in the linked scenario is satisfied — and the
      output cites *which* clause each piece of evidence satisfies.
- [ ] The tool-call trajectory actually taken matches the required mode
      (EXACT/IN_ORDER or ANY_ORDER) — log the trajectory, don't just assert it.
- [ ] Every file you created or edited is in §5's declared scope — no
      surprises for the reviewer.
- [ ] Your actual external resource usage matches the §7 AgBOM — flag any
      gap between what was declared and what was actually called.
- [ ] No regression to existing scenarios in the same .feature file — run
      them via `make test` (the feature file's `tests/step_defs/` file).
- [ ] This ticket's own linked scenario went red (step 2, before the `src/`
      change) → green (now) — not green-only-because-it-was-never-run-first.
- [ ] Negative scenarios still fail closed (the should-not-fire cases still
      don't fire).
- [ ] New/changed `src/` code has unit-test coverage — check `make test`'s
      coverage table for the touched file(s) and note any real gap (not a
      100% mandate — `--cov-fail-under` is deliberately not set project-wide
      — but an unreviewed gap in code this ticket just wrote is a flag, not
      a shrug).
- [ ] All §6 Security Guardrails from the ticket are respected (correct
      caller/signer, correct gate halts, no scope/spending boundary crossed).
- [ ] make test — all green. make lint — zero errors.
- [ ] Any on-chain tx hash logged to ./logs/tx_hashes.md with an explorer link.
- [ ] Every out-of-scope finding is captured in the output below — none were
      fixed inline, none were silently dropped.

═══════════════════════════════════════════════════════════════════════════
DELIVERY — PULL REQUEST
═══════════════════════════════════════════════════════════════════════════

Branch:  feat/issue-<N>-<short-slug>
Target:  main
Commits: Conventional Commits format (`type(scope): description` — see
         root `AGENTS.md` §7, not restated here), small, present-tense; end
         each with the Co-Authored-By: trailer for whichever agent identity
         is executing this run.
PR title: same as the ticket/issue title.

PR body must contain, in this order:

  ## Vibe Diff
  Three required parts, always — this goes first, before "Closes":
    a. What changed — plain-English snapshot of the change and why, in a
       paragraph a human reviewer can read once and approve without
       re-deriving the spec from the code.
    b. Potential breakage points — what could regress: code paths touched
       that aren't covered by the linked .feature scenarios, shared state
       read/written (guild_context.json, config/networks.json), anything
       downstream that assumes the old behavior.
    c. Risk assessment — Low / Medium / High + one-sentence reason. High
       means: moves funds, writes on-chain reputation, changes a
       caller/signer, or touches WalletProvider/Pact scoping. Everything
       else defaults Low unless something specific says otherwise — don't
       inflate or deflate the call to make the PR look better.

  ## Closes
  Closes #<N>

  ## What changed
  Bullet list of files touched; map each to the Component Map name and the
  MVP step(s)/spec section it implements. Every entry must be cross-checked
  against the ticket's §5 file/component scope — no file appears here that
  isn't declared there.

  ## Implementation details
  The key decisions a reviewer needs to follow the diff: primary path vs.
  fallback used and why, contract addresses / ports / message shapes, and
  anything that deviates from the ticket (with justification). Include the
  tool-call trajectory actually taken, side-by-side with the ticket's
  declared mode (EXACT/IN_ORDER or ANY_ORDER) — don't just assert it matched,
  show it.

  ## Verification steps (copy-pasteable, for the reviewer)
  - Setup: uv sync, required env var NAMES (not values), any pre-conditions
  - How to run the component
  - Expected output; Basescan link(s) for any on-chain tx
  - make test and make lint output (now includes a per-file coverage table
    — cite the touched files' numbers, not just pass/fail)

  ## Acceptance criteria
  Copy the ticket's checklist with each box checked and a one-line note on
  how it was satisfied.

  ## Validation
  Which .feature scenarios this PR makes pass, and the test command output
  confirming it.

  ## Resource Usage (AgBOM audit)
  Every external model/MCP-server/tool/data-source actually used, compared
  against the ticket's declared §7 AgBOM — this is the audit trail, not a
  formality. Flag any gap between what was declared and what was actually
  called, in either direction. Include a one-line-per-model summary of
  provider/model name + total tokens used (step 4) — "not exposed by
  runtime" if your session doesn't surface a token count.

  ## Blockers / open questions (omit if none)
  Any doc gaps, spec ambiguities, or integration questions that were NOT
  resolved before opening this PR. For each: quote the vague line, state
  the assumption you made, and tag it ASSUMED or NEEDS ANSWER.

  ## Out-of-scope findings (omit if none)
  Anything you noticed outside this ticket's own §5 scope that needs
  attention — a bug, a stale reference, a broken test, a spec/doc
  inconsistency — that you did NOT fix here. For each: file/location,
  what's wrong, why it matters, and whether it blocked this ticket (and how
  you resolved that block) or was independent and left untouched. This is a
  report, not a place to sneak in unreviewed changes — if you fixed
  something, it belongs in "What changed" with its own justification, not
  buried here.

Fill out the repo PR template (.github/PULL_REQUEST_TEMPLATE/default.md) —
its diagnostics, GuildOS constraints, and documentation checkboxes are the
project-wide floor and must all be honestly ticked; this prompt does not
restate them. CI must be green on the PR itself before requesting review.
Do NOT merge your own PR — a human reviewer approves and merges. Your job
ends at "PR open, CI green, review requested."
```

---

## Why a "Vibe Diff" has three parts, not one

The ticket already carries the formal acceptance criteria — the reviewer's
job at PR time isn't to re-verify every Given/When/Then line by line, it's to
sanity-check that the implementation actually matches the intent the ticket
captured (§1) without surprises. The Vibe Diff is what makes an **LGTM-speed
review** possible: a human reads it once, confirms it matches what they
expected, and approves — instead of reverse-engineering the diff to recover
the ticket's intent.

A Vibe Diff that just restates the code ("renamed X to Y, added a function Z")
has failed its purpose. It should read like a one-paragraph explanation you'd
give a teammate at standup — but "what changed" alone isn't enough to approve
at LGTM speed on a project with on-chain calls and fund movement. That's why
**potential breakage points** and a **risk assessment** are required, not
optional color:

- **What changed** tells the reviewer what you did.
- **Potential breakage points** tells them what to actually look at before
  approving — the reviewer's attention is the scarcest resource in an
  LGTM-speed review, so point it, don't make them find it.
- **Risk assessment** tells them how carefully. A Low-risk formatting fix and
  a High-risk change to `giveFeedback()`'s caller shouldn't get the same
  fifteen seconds of scrutiny, and the PR shouldn't force the reviewer to
  figure out which one they're looking at.

Skipping any of the three defeats the same purpose the other two serve: the
reviewer ends up reconstructing what you already knew while you were writing
the code.
