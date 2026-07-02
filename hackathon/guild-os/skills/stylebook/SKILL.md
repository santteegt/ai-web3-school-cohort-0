---
name: stylebook
description: GuildOS workspace stylebook — judgment-level code conventions (docstrings, error messages, logging, comments) that ruff can't mechanically enforce. Use before writing or reviewing any src/ change — docstring style, error message content, logging format, or comment discipline.
---

# GuildOS Stylebook

> **What this is:** a workspace-specific stylebook for judgment-level
> conventions a linter can't mechanically enforce. It complements, not
> replaces, `ruff` — `ruff` catches syntax and the two conventions below it
> *can* check (import order, logging format); everything else here is
> pattern-matching against the codebase's existing house style, checked by
> a reviewer, not a machine.
>
> **What this is NOT:** a place for naming conventions (classes, functions,
> files, A2A message types) — those are part of the API contract, not house
> style, and live in `specs/20-api-contracts.md` §7. Read both; don't
> duplicate one into the other.

---

## Automated (ruff enforces these — `make lint`)

`pyproject.toml`'s `[tool.ruff.lint]` selects, beyond the defaults:

- **`I` — import sorting.** Order: `from __future__ import annotations` →
  blank line → stdlib (alphabetical) → blank line → local `from src...`
  imports (alphabetical). Run `ruff check --fix` to auto-sort; don't
  hand-order imports.
- **`G` — logging format.** `logger.info("...%s...", value)`, never
  `logger.info(f"...{value}...")`. Lazy `%`-style args mean the string
  isn't built unless the log level is actually emitted — cheap at scale,
  free at hackathon scale, but it's the established pattern, so match it.

If you find yourself wanting a rule ruff could check but doesn't yet, say
so in the ticket's Out-of-Scope Findings — extending `[tool.ruff.lint]` is
its own reviewable change, not something to bundle into an unrelated PR.

## Judgment-level (this file governs, a reviewer checks)

### Module docstrings: why, not what

Every module opens with a docstring in this shape:

```python
"""ComponentName — one-line role.

Then prose that explains constraints, cross-references, and gotchas a
reader would otherwise have to reconstruct from the diff history — not a
restatement of what the functions below obviously do.
"""
```

Good (real example, `src/shared/network_config.py`):

```python
"""NetworkConfig — loads per-network on-chain settings from config/networks.json.

Components must never hardcode a contract address, RPC URL, or explorer link.
Read CHAIN_ID from the environment, then call into this module to resolve
everything network-specific. Secrets (ALCHEMY_API_KEY, private keys) stay in
the environment and are substituted into the RPC URL template here — they are
never written into config/networks.json.
"""
```

This tells a reader the constraint (never hardcode) and the mechanism
(env → this module → config file) — information genuinely lost if you only
read the function signatures below it. A docstring that instead said
"Loads network config from a JSON file" would be restating the module name.

**Cite `specs/`, never `docs/`.** `docs/*.md` is deprecated (see
`AGENTS.md` "Files — Read Before Coding"). A docstring or comment pointing
at `docs/RISKS.md §F2` or `docs/MVP_FLOW.md` is citing a dead source — use
`specs/10-technical-design.md §8 F2` or the equivalent `specs/` section
instead. (Some existing files still carry pre-finalization `docs/`
citations from before 2026-06-30 — fixing one in the course of an
unrelated ticket is fine; don't go hunting for them as scope creep. If you
notice one, it's a valid Out-of-Scope Finding.)

### Error handling: context in the message, narrow exception types

```python
raise RuntimeError("PRIVATE_KEY env var not set — cannot sign transactions")
raise RuntimeError(f"moloch-agent failed (exit {result.returncode}): {stderr}")
```

- `RuntimeError` with an f-string that names *what's missing or what
  failed*, not a bare `raise Exception("error")`. The message is what a
  human sees in a stack trace at 2am — make it answer "what do I check
  first," not just "something broke."
- `NotImplementedError` is reserved for genuine stubs (see
  `src/shared/erc8004.py`) — a marker that a ticket hasn't landed yet, not
  a general-purpose error.
- Never a bare `except:` — catch the specific exception you're handling,
  or let it propagate. Fallback paths (`specs/10-technical-design.md` §8
  F1/F3/F4/etc.) are explicit `try/except` blocks with a comment naming
  which fallback they implement, not a catch-all.

### Logging: module-level logger, structured, not print()

```python
logger = logging.getLogger(__name__)
...
logger.info("Signer address: %s", signer_address)
logger.warning("Sponsor failed (may already be sponsored): %s", e)
```

One `logger = logging.getLogger(__name__)` per module, right after the
imports. No `print()` in `src/` — CLI-facing output (gate prompts, run
summaries) goes through `src/cli/` explicitly, everything else logs.

### Comments: only when the WHY isn't obvious from the code

This project's default is **no comments**. Add one only when it captures
something the code itself can't: a non-obvious constraint, a workaround for
a specific upstream bug, a reason a simpler approach doesn't work. Don't
narrate what the next line does — that's what reading the next line is for.

---

## Why a stylebook instead of just more ruff rules

Some of the above genuinely can't be checked mechanically — "does this
docstring explain the why or just restate the what" and "is this error
message specific enough to be useful" are reviewer judgment calls, not
syntax. `ruff` (`make lint` in CI, required on every PR) is the enforcer for
what's checkable; this skill is the reference for what a reviewer is
checking against everything else. See `.github/PULL_REQUEST_TEMPLATE/default.md`
and `hackathon/guild-os/templates/TASK_EXECUTION_PROMPT.md` — both point here.
