## Vibe Diff

<!-- Three required parts — see hackathon/guild-os/templates/TASK_EXECUTION_PROMPT.md -->

**What changed:**
<!-- Plain-English snapshot a reviewer can read once and approve without
     re-deriving the ticket from the diff. -->

**Potential breakage points:**
<!-- Code paths touched that aren't covered by the linked .feature
     scenarios; shared state read/written (guild_context.json,
     config/networks.json); anything downstream that assumes old behavior. -->

**Risk assessment:** Low / Medium / High —
<!-- One sentence why. High = moves funds, writes on-chain reputation,
     changes a caller/signer, or touches WalletProvider/Pact scoping. -->

## What this PR does

<!-- One sentence. -->

Closes #

## Phase

<!-- Phase 0 / 0.5 / 1 / 2 / 3 / 4 — see hackathon/guild-os/AGENTS.md "Sprint — Phase Gates" -->

## SDD Ticket Compliance

<!-- Ticket sections referenced below are from
     hackathon/guild-os/templates/ISSUE_TICKET_TEMPLATE.md -->

- [ ] Every Gherkin Then-clause in the ticket's linked `.feature` scenario(s) is satisfied
- [ ] Tool-call trajectory matches the ticket's declared mode (`EXACT | IN_ORDER` or `ANY_ORDER`)
- [ ] Only files in the ticket's §5 File/component scope were created or edited
- [ ] All §6 Security Guardrails from the ticket are respected (caller/signer, gate halts, spending boundaries)
- [ ] No regression to existing scenarios in the same `.feature` file
- [ ] Negative scenarios still fail closed

### GuildOS Constraints
- [ ] No hardcoded private keys, API keys, or seed phrases
- [ ] Base (chain_id 8453) is the only network used for evidence — Base Sepolia (84532), if used at all, is isolated component testing only
- [ ] All on-chain signing goes through the scoped `WalletProvider` — no raw EOA fallback
- [ ] Treasury funds move only through a DAO proposal (`payment_propose` → Gate 3 → `settle`) — never a direct transfer
- [ ] All A2A messages are logged to `./logs/a2a_trace_{date}.json`
- [ ] All GLM-5.1 calls are logged to `./logs/glm_trace_{date}.json`
- [ ] Human gate prompts (0, 0.5, 1, 2, 3, 4) halt execution and wait for `y/N` — no auto-proceed
- [ ] `giveFeedback()` is called from the guild contract via proposal execution — NOT the Specialist wallet, NOT a raw agent EOA

### Diagnostics
- [ ] `pytest tests/` passes
- [ ] `ruff check src/` clean (includes import-sort `I` and logging-format `G`)
- [ ] Docstrings, error messages, log lines, and comments follow `hackathon/guild-os/skills/stylebook/SKILL.md`
- [ ] On-chain tx hashes saved to `./logs/tx_hashes.md` (if applicable)

### Documentation
- [ ] `specs/` updated if this PR changes a decision, fallback, or contract (see `specs/10-technical-design.md` §8/§9) — `docs/*.md` is deprecated, don't update it instead

## Resource Usage (AgBOM audit)

<!-- Every external model / MCP server / tool / data source actually used,
     compared against the ticket's declared §7 AgBOM. Flag any gap between
     what was declared and what was actually called. -->

## Out-of-Scope Findings

<!-- File/location, what's wrong, why it matters. Delete this section if
     there's nothing to report. Never fix an out-of-scope issue inline —
     report it here so it can be triaged as its own ticket. -->
