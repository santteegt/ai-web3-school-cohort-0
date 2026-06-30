# Issue Ticket Template — Spec-Driven Development

> **Why this exists:** a ticket is a blueprint, not a vibe. Given a blueprint,
> an agent executes; given a vibe, it guesses — and on a project with on-chain
> calls, caller constraints, and DAO-governed money movement, a guess is never
> a free mistake. Every field below closes a specific class of hallucination
> an agent would otherwise have to invent an answer for.
>
> **The chain this ticket sits at the end of:**
> Human Intent → BDD/Gherkin scenarios → feature spec in `specs/` → **this ticket**
>
> A ticket should never be the first place a behavior is described. If the
> behavior isn't already captured as a Given/When/Then scenario in
> `specs/scenarios/*.feature`, write that scenario first (see "Missing BDD
> Scenarios?" at the bottom) — the ticket then *points to* the spec, it
> doesn't reinvent it.

---

Copy everything below this line into the new GitHub issue body.

---

# TICKET: <feature-name>

## 1. Intent (the "why")

**Goal:** ____________________________________________

**Background / rationale** — enough for the agent to think forward instead of
guessing at intent mid-implementation. Link the relevant section of
`specs/00-overview.md` or `specs/10-technical-design.md` if one exists:
______________

## 2. BDD Scenarios (Given / When / Then)

Link to the exact scenario(s) in `specs/scenarios/*.feature` this ticket
implements. **Name the exact harness tools** the agent will call at each
step — not a paraphrase of what should happen.

```gherkin
Scenario: Processing a refund for a duplicate charge
  Given a customer was charged twice for order #4521
  When the "refund-processor" skill is triggered
  And the agent calls "lookup_order" with order_id "4521"
  And the agent calls "check_duplicate_charge" with order_id "4521"
  Then the agent should return a "confirmation_with_refund_id"
  And the output must cite the order ID and acknowledge the duplicate charge.
```

**Negative scenarios are mandatory** — at least one case where the skill or
tool-call path must **NOT** fire. A ticket with only happy-path scenarios is
incomplete: the agent has no signal for what restraint looks like, and will
default to firing whenever the inputs look plausible.

## 3. Acceptance Criteria

Testable, and each one traceable back to a Then-clause above. Don't introduce
a requirement here that isn't already implied by a scenario in §2 — if it
matters, it belongs in the Gherkin first.

- [ ] ______
- [ ] ______

## 4. Technical Constraints

- Pinned library versions / env vars — pull from `specs/20-api-contracts.md`
  §1 (pinned dependencies) and §6 (environment contract); never let the agent
  default to a training-data version: ______
- **Tool-call trajectory mode** — this sets how strictly the agent must follow
  the sequence in §2:
  - `EXACT | IN_ORDER` — high-risk / state-mutating / on-chain calls. The
    agent must call tools in exactly this order with exactly these tools; no
    substitutions, no reordering, no skipped steps.
  - `ANY_ORDER` — read-only / side-effect-free calls. The agent may sequence
    these freely as long as every required call happens before the
    Then-clause it satisfies.
- Structures nested more than 3 levels are expressed as YAML, not inline
  Markdown — matches the authoring protocol in `specs/README.md`.

## 5. Interface Definitions

- Required MCP server connections: ______
- Required A2A message types touched — name them; see
  `specs/20-api-contracts.md` §3: ______
- A2UI declarative format for any interactive artifact — N/A for GuildOS
  today, since the two CLI terminals are the only interactive surface
  (see `CLAUDE.md` Don't: "Build UI components"). Leave blank unless that
  constraint changes: ______

## 6. Security Guardrails

- Human gates this ticket must halt at (name them: Gate 0 / 0.5 / 1 / 2 / 3 / 4)
  and what each gate blocks until approved: ______
- Caller / signer constraints — e.g. "never the Specialist wallet," "guild
  contract only via proposal execution." Cite the relevant `docs/RISKS.md`
  §F-number: ______
- Spending or scope boundaries this ticket must respect — CAW Pact allowlist,
  tribute cap, network. `CHAIN_ID` must never be hardcoded: ______

## 7. AgBOM (Agent Bill of Materials — authorized inventory for THIS ticket)

- **Tools:** ______
- **Models:** ______
- **Data sources:** ______

An agent executing this ticket may use *only* what's listed here. Anything
else requires stopping and asking — see `templates/TASK_EXECUTION_PROMPT.md`.

---

## ── DEFINITION OF READY (all must be true before assigning to an agent) ──

- [ ] **Trigger:** positive AND negative (should-not-fire) cases present in §2.
- [ ] **Execution:** tool calls + expected outputs verified against at least
      one representative input.
- [ ] **Regression:** this change keeps a 100% pass rate on existing
      scenarios in the same feature file.
- [ ] **Token budget:** ticket + linked scenario stay bounded — rule of thumb,
      under ~5,000 tokens — to avoid context rot in the executing agent.
- [ ] **Authorization tier set:** Read-Only / Draft-Only / Action-Allowed —
      and the bar for that tier (§6) is met.

If any box above is unchecked, the ticket is **not ready**. Finish it before
assigning — don't let an agent fill the gap by guessing.

---

## Missing BDD Scenarios?

If no `.feature` file covers this behavior yet, don't skip straight to
writing the ticket. Work with the user to draft the Gherkin scenarios first —
Given/When/Then, plus at least one negative case — get their sign-off, then
add the scenario to the right file under `specs/scenarios/` (or create a new
one, following the naming and numbering convention in `specs/README.md`)
before filling in §2.

Writing the scenario *with* the user up front, rather than inferring it from
the ticket, is what lets them later review the resulting pull request at
LGTM speed: the scenario already states what "done" looks like, so reviewing
the PR is a confirmation, not a re-derivation of the spec from the diff.
