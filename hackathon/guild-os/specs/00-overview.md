# 00 — Overview: Vision & the "Why"

> Provenance: `docs/PROBLEM.md`, `docs/TRACK.md`, `hackathon/PROJECT_PROPOSAL.md`,
> and the Decision Logs from `docs/TECH_STACK.md` + `docs/RISKS.md`.

## TL;DR

GuildOS closes a coordination gap: capable contributors — human and AI — cannot yet form
credible, accountable, ephemeral work structures without a rent-extracting intermediary.
A human founds a guild with a funded treasury; an AI specialist joins by governance vote;
the orchestrator delegates real work over A2A; the specialist executes with GLM-5.1 and
attests the deliverable via EAS; on human acceptance the treasury pays out and the
specialist's on-chain reputation grows. This document is the "why" — read it first so you
can think forward when the later specs leave a detail implicit.

---

## 1. Problem Statement

The coordination infrastructure for AI-augmented knowledge work does not exist yet.
Traditional freelance and agency structures are slow and opaque: finding a specialist
takes weeks, reputation is locked in platforms you do not own, and every project restarts
context from scratch. AI agents can now execute real development work autonomously, but
without structure they hallucinate, overreach, and leave no verifiable trail. Neither side
uses what the other offers: developers treat agents as tools rather than collaborators, and
agents have no economic structure that rewards verified delivery with portable reputation.

The result is a coordination gap no existing platform addresses.

---

## 2. Target Users

- **Primary:** Independent developers and small dev shops (1–4 people) who need
  short-duration specialized expertise — security review, contract audits, frontend, data
  analysis, spec writing — and are tired of platform fees, marketplace rigidity, and
  context-losing chat coordination.
- **Secondary:** AI agent developers who want their agents to participate in economic
  structures, deliver verifiably, and accumulate portable reputation across engagements.
- **Not this hackathon:** Enterprise procurement, non-technical clients, anyone needing a
  polished consumer UI. The demo targets a technically fluent audience who can read a
  Basescan transaction.

---

## 3. North Star Scenario — Dogfooding

> The canonical scenario that all `scenarios/*.feature` example data uses.

GuildOS is demonstrated by **building GuildOS with GuildOS**. The guild's mandate is to
ship GuildOS components; the Specialist is an agentic AI × Web3 engineer (Hermes / GLM-5.1)
that picks up GuildOS tickets and delivers working code. A single run threads every
component end-to-end:

1. The human founder (e.g. Marco) asks the Orchestrator to launch a guild; the Orchestrator
   collects the guild name, mandate *"Build GuildOS components"*, governance settings, the
   initial member list with shares/loot, and the treasury tribute, then summons the DAO and
   returns the dao + treasury addresses.
2. The Orchestrator surfaces a Specialist candidate from ERC-8004; Marco approves the invite (Gate 0).
3. The Specialist quotes scope/cost/deadline for a GuildOS ticket; Marco accepts the quote (Gate 0.5).
4. The Specialist proposes membership; Marco votes it in via AgentFightClub governance (Gate 1).
5. The Orchestrator delegates the ticket over A2A — GitHub issue link, technical constraints,
   Agent Bill of Materials, BDD acceptance tests, and deliverable format.
6. The Specialist reads the issue, decomposes and executes with GLM-5.1, producing a code deliverable.
7. The Specialist hashes the deliverable (zip hash or commit hash) and creates an EAS attestation on Base.
8. The result returns over A2A carrying the attestation UID; the Orchestrator pre-checks it and Marco accepts (Gate 2).
9. The Orchestrator raises a payment proposal; Marco votes and processes it (Gate 3) and the
   DAO treasury releases payment to the Specialist's wallet.
10. The Specialist requests feedback over A2A; the guild submits a `submitFeedback` proposal;
    on the passing vote (Gate 4), `giveFeedback()` writes the delivery record to the
    Specialist's ERC-8004 reputation — on-chain and portable.

This self-referential framing makes the thesis concrete: a guild of agents that can build
the very coordination substrate they run on.

> ASSUMPTION: the original `PROBLEM.md`/proposal narrative used a one-off "audit an ERC-20
> staking contract" story. The dogfooding mandate supersedes it as the canonical demo per
> the spec decision; the audit framing is retained only as an illustrative alternative.

---

## 4. Why Web3 Is Necessary

| Without Web3 | With Web3 (GuildOS) |
|--------------|---------------------|
| Reputation is a database row on a platform | Portable on-chain record (ERC-8004) — readable by any future guild or employer |
| Payment depends on the platform releasing funds | Contract-enforced treasury (Moloch v3) — payment releases only on acceptance, not on trust |
| Mandate/deliverable is an editable doc | EAS attestation — cryptographically signed by the Specialist, timestamped, queryable on easscan |

Web3 makes these properties enforceable at the protocol level, not the platform level.

## 5. Why AI Is Necessary

| Without AI | With AI (GuildOS) |
|------------|-------------------|
| Sourcing specialists takes weeks | Orchestrator queries ERC-8004 and returns a shortlist in seconds |
| Execution needs human availability | Specialist executes autonomously via GLM-5.1 long-horizon planning |
| Context lost between projects | A2A log + on-chain delivery record creates a verifiable work trail |

## 6. Intersection Test

| Machine execution | Economic exchange | Permission control | Verifiable records |
|-------------------|-------------------|--------------------|--------------------|
| GLM-5.1 executes tasks autonomously | DAO-held treasury; payment on a passing vote | Provider-agnostic scoped wallets (DAO-call allowlist); 6 human gates; AgentFightClub governance | EAS delivery attestation; ERC-8004 reputation; settlement tx |

All four dimensions present — GuildOS is a genuine AI × Web3 intersection problem, not a
DAO-for-humans nor a platform-locked agent tool.

---

## 7. Track Alignment

### Cobo | Agentic Economy × Cobo Agentic Wallet (primary)

GuildOS's core story is economic coordination at machine speed: a shared treasury funds a
mandate, a specialist agent is paid for verified work via a DAO payment proposal, and capital
moves programmatically on a passing vote — not on trust. The treasury is **DAO-held**, so no
agent wallet ever custodies funds. Agents act through a **provider-agnostic wallet layer**
(Cobo CAW by default, swappable to ZeroDev / Turnkey) whose **Pact** scopes exactly the DAO
governance calls — `propose`, `vote`, `process` on the guild contract — and caps the one
fund-moving agent call, `tribute`. There is no EOA fallback. Maps directly to the track's
"agent-to-agent work protocols" and "A2A Economy" directions.

**Key demo evidence:** CAW Pact config shown live (TSS node running); the Pact allowlists the
DAO governance calls and caps tribute; the payment is processed through a DAO proposal at
Gate 3; CAW wallet address + anonymized Pact config in README.

### Z.AI | Web3 × Long-Horizon Task (secondary)

The Specialist (Hermes agent) uses **GLM-5.1** to decompose a ticket into a ≥3-step plan,
execute a ReAct tool-use loop, and produce a structured deliverable. Web3 proof: the
deliverable's SHA-256 hash is EAS-attested on Base mainnet, UID embedded in the A2A
`task/delivered` message, queryable on `base.easscan.org`.

**Key demo evidence:** `glm_trace_*.json` showing multi-step execution; non-trivial code
output; EAS attestation of the GLM-5.1 output hash.

---

## 8. Success Criteria (Evaluation Scorecard)

| Question | GuildOS answer |
|----------|----------------|
| Would this exist without AI? | Yes, but as a DAO for humans. AI adds first-class agent membership, long-horizon execution, A2A capability matching. |
| Would this exist without Web3? | Yes, but reputation/payment/mandate would be platform-controlled. Web3 gives portable reputation, enforced treasury, tamper-proof records. |
| Who initiates / executes / pays / accepts / arbitrates? | Initiates: Human. Executes: Specialist. Pays: Guild treasury. Accepts: Human. Arbitrates: AgentFightClub governance + human vote. Chain complete. |
| Automated vs. human? | Automated: delegation, execution, EAS attestation, proposal drafting, on-chain processing. Human gates (6): candidate selection, quote acceptance, membership vote, deliverable acceptance, payment-proposal vote, feedback vote. |
| How is the result verified, and is verification cheaper than coordination? | EAS attestation of the hash before acceptance; UID cross-referenced in A2A + ERC-8004. One easscan read + hash compare — far cheaper than human coordination. |
| Which layer? | Primary application layer (guild formation/operation); secondary protocol layer (coordination primitives). |
| Most likely failure mode? | Immature interfaces (ERC-8004 draft, AFC alpha, A2A new). Mitigation: one integration risk/day, fallbacks pre-defined (see `10-technical-design.md`). |

**Definition of "judges know it's complete":** two clickable on-chain proofs — (1) the EAS
attestation of the deliverable hash on `base.easscan.org`, and (2) the AgentFightClub
settlement tx on Basescan — plus the Specialist's ERC-8004 reputation delta (before: 0
deliveries of this task type → after: 1 verified delivery with UID + timestamp).

---

## 9. Why-Appendix — Decision Log (think-forward background)

Carried forward so an agent reading the spec understands *why* the locked choices were made
and does not re-litigate them.

| Date | Decision | Outcome |
|------|----------|---------|
| 2026-06-06 | Agent wallet provider | First moved CAW → ZeroDev Kernel v3.3 (CAW repo empty, x402/signing broken) |
| 2026-06-06 | Testnet | Base Sepolia chosen initially (ZeroDev + ERC-8004 deployed there) |
| 2026-06-07 | Orchestrator harness | Claude Code MCP server — demo two heterogeneous stacks over A2A |
| 2026-06-07 | A2A SDK | v1.0.0 line (stable, Linux Foundation), not 0.3 |
| 2026-06-08 | Agent wallet provider | **CAW restored** (TSS node restart fixed signing; x402 working) — ZeroDev demoted to design exhibit |
| 2026-06-08 | Network | **Base mainnet (8453)** — AFC has no Base Sepolia contracts/subgraph |
| 2026-06-09 | AgentFightClub | Full flow confirmed: launch → commit → propose → vote → settle |
| 2026-06-09 | GLM-5.1 / Hermes | Specialist stack locked; long-horizon prompt locked |
| 2026-06-11 | Deliverable commitment | **EAS attestation replaces raw `eth_sendTransaction`** — signed by Specialist, stable UID cross-referencing A2A ↔ ERC-8004, easscan-queryable, same gas |
| 2026-06-17 | Reputation write | Routed through an **executable `submitFeedback` DAO proposal** — passing vote triggers `giveFeedback()` with the guild contract as caller |

> ASSUMPTION: the proposal/TECH_STACK Decision Logs predate the EAS and DAO-feedback
> decisions; the two final rows reflect the current target design and supersede any earlier
> "Base Sepolia" / "raw hash commit" / "orchestrator calls giveFeedback directly" wording.
