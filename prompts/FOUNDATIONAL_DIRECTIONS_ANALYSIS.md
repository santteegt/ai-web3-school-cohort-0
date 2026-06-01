# Prompt — Foundational Directions Analysis

## Goal

Produce a structured analysis of the AI × Web3 foundational directions. For each
direction I should come away understanding its **core problem**, **typical entry
point**, and a **suitable learner profile** with recommended external resources
(prefer resources found in the knowledge base; see Resources below).

## Directions and depth

Produce one document per direction. Depth is determined by the direction's mark:

| Direction | Mark | Document depth |
|---|---|---|
| Identity / Capability | **MAIN** | Deep dive |
| Governance / Coordination | **SECONDARY** | Deep dive |
| Payment / Commerce / Settlement | — | Overview |
| Wallet / Permission / Safe Execution | — | Overview |
| Privacy / Security / Sovereignty | — | Overview |

> Note: Identity and Capability are intentionally merged into a single direction.
> The per-direction briefs further down are authoritative for scope.

## Per-document requirements (all directions)

Each direction document must include:

1. **Intro** — what the direction is and why it matters.
2. **Aim** — the concrete outcome of the document (stated per direction below).
3. **Core problem** — the central problem this direction tries to solve.
4. **Typical entry point** — where a learner/builder realistically starts.
5. **Suitable learner profile** — who this fits, plus recommended external
   resources. Prefer resources already cited in the knowledge base, especially
   `knowledge-base/AIxWeb3/raw/AIxWeb3 Bridge - Introduction.md`. If none exist,
   say so rather than inventing one.
6. **At least one flowchart**, **one typical scenario**, **one counterexample**,
   **one set of key risks**, and **one minimal validation plan**. Add other
   visuals only where they add clarity.
7. **Analysis process & conclusion** — a two-paragraph closing section
   describing how you reached your conclusions and what they are.

## Additional requirements for DEEP-DIVE directions (MAIN + SECONDARY)

8. Identify **at least 5 projects, standards, protocols, tools, or cases**. For
   each, explain specifically **what it lets me evaluate or implement when
   building a project at a hackathon**.

## Sourcing rules (strict)

- **Do not invent facts.** When describing any project, protocol, or standard,
  use existing material from the knowledge base or look it up, and cite it.
- Every external claim needs a **reference** (link or knowledge-base path).
- Protocol/standard names appear throughout (MCP, A2A, ERC-8004, MPP, x402,
  ERC-8183, ERC-4337, Safe, CAW, session keys, etc.). **Verify each one exists
  and is named correctly before relying on it.** If you cannot confirm one,
  flag it as unverified rather than describing it as fact.

## Execution

- You may spawn a sub-agent per direction to parallelize. If you do, give every
  sub-agent the same per-document requirements and sourcing rules above so the
  documents stay consistent in structure and depth.
- Before finalizing, run a **verification pass**: confirm every named
  project/standard is real and correctly described, every reference resolves,
  and each document contains all required sections.

## Resources (background — read before writing)

- AI × Web3 knowledge base: `knowledge-base/AIxWeb3/wiki`
- AI × Web3 Bridge intro + learning resources:
  `knowledge-base/AIxWeb3/raw/AIxWeb3 Bridge - Introduction.md`
- Bridge mental model: `knowledge-base/AIxWeb3/concepts/aixweb3-bridge-mental-model.md`
- Space problem map: `tasks/AIxWeb3-problem-map.md`
- Problem map & main direction selection: `tasks/PROBLEM_MAP_&_MAIN_DIRECTION_SELECTION.md`
- Agentic Commerce workflow analysis: `tasks/AIxWeb3_WORKFLOW.md`

## Deliverables

- One Markdown document per direction, plus any generated assets, saved under
  `tasks/directions/`.
- Suggested file naming: `tasks/directions/<NN>-<direction-slug>.md`
  (e.g. `01-identity-capability.md`), with assets in
  `tasks/directions/assets/`.

---

# Direction Briefs

## 1. Identity / Capability — **MAIN** (deep dive)

> A merge of the Identity and Capability directions. Focuses on how agents are
> discovered, described, invoked, verified, and coordinated. Suitable for
> learners interested in MCP, A2A, ERC-8004, registries, agent profiles, and
> capability claims.

**Aim:** Agent Profile and Capability Claim draft.

- **Choose an agent or workflow you know well** and clearly describe its
  identity, capabilities, inputs and outputs, collaboration partners, and
  failure points.
- **Design a draft agent profile** explaining: who it is, who maintains it, what
  it can do, how it is invoked, how it charges, how it is verified, and how
  failures are handled.
- **Bonus:** compare MCP, A2A, ERC-8004, and MPP — explain what collaboration,
  payment, or interface problem each is suited to solve. Then pick the two most
  relevant and make a final head-to-head comparison.

## 2. Governance / Coordination — **SECONDARY** (deep dive)

> Focuses on how AI can help DAOs, communities, and public-goods projects with
> proposal summaries, meeting action items, contribution records, budget
> checklists, and transparent execution. Suitable for learners interested in
> community collaboration, public goods, and organizational processes.

**Aim:** Governance and Coordination workflow sketch.

- **Choose a DAO / community process** and break down the steps where AI can
  assist versus the steps that must be confirmed by people or a governance
  process.
- **Sketch** one of: a proposal summarizer, a meeting-to-action workflow, a
  contribution tracker, or a budget-execution checklist.
- **Mark clearly** which conclusions are only AI summaries and which actions
  require human confirmation or governance approval.

## 3. Payment / Commerce / Settlement — overview

> Focuses on how machines or agents buy APIs, data, compute, and services, and
> how quoting, acceptance, escrow, dispute handling, and settlement form a
> closed loop. Suitable for learners interested in commercial loops, payments,
> standards, and protocols.

**Aim:** Minimal payment-and-commerce flow breakdown.

- **Choose a scenario** where an agent helps someone complete a task and
  receives payment.
- **Break down the full process:** who places the order, who executes, who
  accepts the result, who pays, and who arbitrates.
- **Design a minimal flow** including at least: quote, budget authorization,
  execution, delivery, acceptance, payment / refund / dispute, and proof of
  record.
- **Bonus:** compare x402, MPP, ERC-8004, and ERC-8183 — explain which segment
  each addresses (payment, verification, identity, settlement, or arbitration).
  Then pick the two most relevant and make a final comparison.

## 4. Wallet / Permission / Safe Execution — overview

> Focuses on permission layering, automation boundaries, human confirmation,
> revocation, and auditing when agents interact with wallets, signatures,
> budgets, and on-chain actions. Suitable for learners interested in account
> abstraction, Safe, policy, guard, and session keys.

**Aim:** Permission strategy for agent-initiated on-chain actions.

- **Draw the execution flow** of an "agent-initiated on-chain action," marking
  which steps can be automated and which must be confirmed by a human.
- **Design a permission strategy** for an agent-wallet scenario, including at
  least: budget, callable contracts, executable actions, human-confirmation
  thresholds, revocation method, logging, and failure handling.
- **Explain** why ERC-4337, Safe, and guard / policy mechanisms matter, and what
  type of risk each addresses.

## 5. Privacy / Security / Sovereignty — overview

> Focuses on prompt injection, tool abuse, sensitive data, dependence on model
> providers, private-key / API-key exposure, local execution, and user
> sovereignty. Suitable for learners interested in security, privacy, trusted
> execution, auditing, and risk control.

**Aim:** Agent-workflow threat model and confirmation strategy.

- **Write a threat model** for an agent workflow covering: assets, permissions,
  data, tool calls, external dependencies, and failure consequences.
- **Design a "low-risk automation / high-risk human confirmation" strategy** and
  explain the conditions that trigger human confirmation.
- **Bonus:** simulate attacks such as prompt injection, forged tool returns, and
  unauthorized instructions. Observe whether wallet / policy / CAW
  infrastructure can intercept them, and record which attacks are blocked and
  which are not.
