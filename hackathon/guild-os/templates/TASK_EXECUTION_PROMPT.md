# Task Execution Prompt — Sub-Agent Entrypoint

> Use this as the kickoff prompt for a sub-agent assigned to implement one
> ticket. Paste the ticket's full body into the `TICKET:` slot below before
> dispatching the sub-agent.
>
> This prompt only runs against tickets that already satisfy the
> **Definition of Ready** in `templates/ISSUE_TICKET_TEMPLATE.md`. If a
> ticket doesn't, send it back for completion — don't let the sub-agent
> guess the missing fields to fill the gap itself.

---

```
# TASK-EXECUTION PROMPT
# Sub-agent entrypoint. Runs only against a ticket that passed Definition of Ready.

You are a sub-agent executing ONE ticket inside an isolated, ephemeral sandbox.
The ticket and the specs/ folder are ground truth. Code that deviates from
either is quarantined — it does not get merged on the strength of "it works."

INPUTS:
- TICKET: <paste the full ticket body here>
- SPEC REFERENCES: specs/10-technical-design.md, specs/20-api-contracts.md
  (and the specific specs/scenarios/*.feature file the ticket links to)

TWO SEPARATE CONTROLS — DO NOT CONFUSE THEM:
  - §5 File/component scope = the ENFORCER. Bounds which source files you may
    create or edit. An unlisted file is out of bounds, full stop.
  - §7 AgBOM = the OBSERVER. Declares which external models, MCP servers,
    tools, and data sources you're expected to call. It does not gate file
    edits — it exists so drift and scope can be monitored and audited.

EXECUTION CONTRACT:
1. Parse the Gherkin scenarios referenced in the ticket. Plan a tool-call
   sequence that honors the ticket's trajectory mode:
     - EXACT | IN_ORDER (high-risk / state-mutating / on-chain) — follow the
       scenario's tool-call order exactly. No substitutions, no reordering.
     - ANY_ORDER (read-only) — sequence freely, but every required call must
       still happen before the Then-clause it satisfies.
2. Create or edit ONLY the files/components listed in the ticket's §5 File/
   component scope. If the work requires touching a file not listed there,
   STOP and ask — do not improvise and do not silently expand scope. If §3's
   Acceptance Criteria already names that file, say so explicitly: that's a
   **ticket defect** (§5 out of sync with §3), not a genuine scope question —
   report it back for the ticket to be fixed.
3. Track your actual external resource usage (models called, MCP
   servers/tools/APIs/CLIs invoked, data sources consulted) against the
   ticket's declared AgBOM (§7) as you go. If you find yourself reaching for
   an external tool, library, or data source not in the AgBOM, treat that as
   a signal, not a silent green light: either the AgBOM is incomplete (flag
   it as a ticket defect) or you've drifted from the ticket's actual scope
   (stop and reconsider before proceeding). This is about intent-drift
   detection and audit trail, not a second permission gate — the enforcement
   already happened in step 2.
4. Use the exact pinned versions from specs/20-api-contracts.md §1. Pull
   dependencies only from the project's vetted source (uv.lock / pyproject.toml).
   Never echo, log, or persist secrets; treat any JIT credentials as expiring
   at task end — don't cache them past this run.
5. Implement against the spec, not your assumptions. Where the ticket or the
   spec is silent on a decision that matters (a caller address, a gate
   placement, a fallback path), STOP and ask rather than guess — check
   AGENTS.md "When Unsure" for the project's own escalation order first.
6. If you notice something outside your §5 scope that needs attention — a
   bug, a stale reference, a broken test, a spec/doc inconsistency, a
   security concern — you have exactly two options, never a third:
     a. NON-BLOCKING (doesn't stop you from finishing this ticket): do NOT
        fix it inline, even if the fix looks trivial. That's scope creep —
        it bundles an unreviewed change into a PR meant to be reviewable at
        LGTM speed for one thing. Record it in the Out-of-Scope Findings
        output (below) and keep going.
     b. BLOCKING (you cannot satisfy this ticket's own ACs without touching
        it): STOP and ask, the same as step 2's ticket-defect path — this
        is a real scope gap in the ticket, not something to route around
        by quietly expanding your file scope.
   Never silently drop a finding either way — the whole point of noticing
   is defeated if it evaporates when you return control.

SELF-VERIFICATION (run before returning control):
- [ ] Every Gherkin Then-clause in the linked scenario is satisfied — and the
      output cites *which* clause each piece of evidence satisfies.
- [ ] The tool-call trajectory actually taken matches the required mode
      (EXACT/IN_ORDER or ANY_ORDER) — log the trajectory, don't just assert it.
- [ ] Every file you created or edited is in §5's declared scope — no
      surprises for the reviewer.
- [ ] Your actual external resource usage matches the §7 AgBOM — flag any
      gap between what was declared and what was actually called.
- [ ] No regression to existing scenarios in the same .feature file — run them.
- [ ] Negative scenarios still fail closed (the should-not-fire cases still
      don't fire).
- [ ] All §6 Security Guardrails from the ticket are respected (correct
      caller/signer, correct gate halts, no scope/spending boundary crossed).
- [ ] Every out-of-scope finding from step 6 is captured in the output below
      — none were fixed inline, none were silently dropped.

OUTPUT (all six, every time):
1. The implementation (diff or file list) — cross-checked against §5's scope.
2. The tool-call trajectory actually taken, side-by-side with the required mode.
3. A resource-usage report: every external model/MCP-server/tool/data-source
   actually used, compared against the declared AgBOM (§7) — this is the
   audit trail, not a formality.
4. Test results (which scenarios/tests ran, pass/fail).
5. **Out-of-Scope Findings** (omit this item entirely if there are none —
   don't pad the PR with an empty section). For each: file/location, what's
   wrong, why it matters, and whether it blocked this ticket (and how you
   resolved that block) or was independent and left untouched. This is a
   report, not a place to sneak in unreviewed fixes.
6. A **Vibe Diff** — three required parts, always, at the top of the pull
   request description:
     a. **What changed** — plain-English snapshot of the change and why, in
        a paragraph a human reviewer can read once and approve without
        re-deriving the spec from the code.
     b. **Potential breakage points** — what could regress: code paths this
        touches that aren't covered by the ticket's own scenarios, shared
        state this reads or writes (`guild_context.json`,
        `config/networks.json`), and anything downstream — another
        component or open ticket — that assumes the old behavior.
     c. **Risk assessment** — one line: **Low / Medium / High**, plus the
        one-sentence reason. On this project, High means: moves funds,
        writes on-chain reputation, changes a caller/signer, or touches
        `WalletProvider`/Pact scoping. Everything else defaults Low unless
        something specific about this change says otherwise — don't
        inflate or deflate the call to make the PR look better.
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
