# Prompt — AgentFightClub Frontier Research

> **Purpose:** Deep research on AgentFightClub as the treasury and governance layer for GuildOS  
> **Created:** 2026-06-03  
> **Deliverable directory:** `hackathon/research/`

---

## Your Role

You are Sensei, the AI × Web3 School Learning Agent for Santiago. Act as a rigorous technical researcher and critical evaluator. Your job is not to confirm that AgentFightClub fits GuildOS — it's to find out whether it actually does, with evidence.

---

## Context

Santiago is building **GuildOS** for a one-week hackathon sprint starting June 7. GuildOS is a programmable agent coordination studio where:

1. A human founder launches a guild with a mandate and funds a shared treasury
2. A Specialist Agent with an ERC-8004 reputation profile joins via a governance proposal vote
3. An Orchestrator Agent delegates a real task to the Specialist via A2A
4. The Specialist executes the task (using GLM-5.1), commits a deliverable hash on Base testnet
5. The human reviews and accepts
6. The shared treasury releases payment to the Specialist
7. The Specialist's ERC-8004 reputation is updated on-chain

The project proposal specifies **AgentFightClub** (built on Moloch v3) as the governance and treasury layer, with a fallback to deploying Moloch v3 directly via DAOhaus SDK if AgentFightClub's API is too unstable.

**The open question is: does AgentFightClub actually provide what GuildOS needs — or is the proposal making assumptions that don't hold?**

---

## What to Read Before Writing Anything

Read all of these in full before producing any output:

1. **Project proposal:** `hackathon/PROJECT_PROPOSAL.md` — pay close attention to Section 5 (Minimum Demo Loop), Section 7 (Mock vs. Real), Section 8 (Process Flow), and Section 9 (Main Risks)
2. **Prototyping resources:** `hackathon/PROTOTYPING_RESOURCES.md` — Section 1 (AgentFightClub + Moloch v3)
3. **AgentFightClub Skill:** fetch and read https://agentfightclub.xyz/skill.md — this is the primary integration surface and the most important document for this research
4. **AgentFightClub — How It Works:** fetch and read https://agentfightclub.xyz/how-it-works
5. **DAOhaus / Moloch v3 docs:** fetch https://docs.daohaus.club/contracts — understand the fallback path

---

## Research Questions

Answer each question with evidence from what you read — not assumptions.

### Fit Analysis

1. **What operations does AgentFightClub actually expose?** List every available action (skill commands, API endpoints, contract calls) and map each one to the GuildOS process flow step it would fulfill.

2. **Which GuildOS features can AgentFightClub implement directly?** For each feature in Section 5 (Minimum Demo Loop) and Section 6 MVP feature list of the proposal, state: ✅ supported, ⚠️ partial / requires workaround, or ❌ not supported — with a one-line reason.

3. **What is missing?** For each gap (⚠️ or ❌), explain: what GuildOS needs, what AgentFightClub provides, and what the delta is. Is the gap bridgeable with a thin wrapper, or does it require replacing AgentFightClub entirely?

4. **How stable is the integration surface?** Based on the skill.md and how-it-works docs: is this alpha/beta/production? Are there versioning guarantees? What is the failure mode if the API goes down during the hackathon demo?

### Alternatives

5. **If AgentFightClub cannot cover a gap, what are the concrete alternatives?** For each identified gap, propose one alternative (protocol, contract, SDK, or pattern) that fills it. Prioritize options that are: (a) open source and audited, (b) deployable on Base testnet, and (c) buildable within the 7-day hackathon scope.

6. **Should the fallback (direct Moloch v3 via DAOhaus SDK) replace AgentFightClub as the primary path?** Make a recommendation with reasoning.

### Integration Design

7. **What is the minimum integration code required?** For the operations AgentFightClub does support, sketch the call sequence (pseudocode is fine): how does the Orchestrator Agent call AgentFightClub to launch a guild, submit a membership proposal, vote, and settle payment? What inputs are required, what does the response look like?

8. **What needs to be tested on Day 1 of the hackathon?** List the 3–5 operations that carry the most integration risk and must be validated with live API calls before building the rest of the stack.

---

## Deliverables

### Required

**`hackathon/research/AGENTFIGHTCLUB_ANALYSIS.md`** — the full research report. Structure:

```
# AgentFightClub — Fit Analysis for GuildOS

## TL;DR
One-paragraph verdict: does it fit, partially fit, or need to be replaced?

## Feature Coverage Matrix
Table: GuildOS feature | AgentFightClub operation | Status (✅ / ⚠️ / ❌) | Notes

## Gaps and Alternatives
Per gap: what GuildOS needs → what AFC provides → delta → proposed alternative

## Integration Stability Assessment
API maturity, versioning, failure modes, hackathon risk level

## Recommended Integration Path
Primary path (AFC or fallback) + rationale

## Day 1 Test Checklist
3–5 operations to validate live before building

## Minimum Integration Sketch
Pseudocode call sequence for the core guild lifecycle
```

### Optional (if time allows)

**`hackathon/research/AGENTFIGHTCLUB_DAY1_TEST.py`** — a minimal Python or TypeScript script that tests the 3–5 highest-risk operations against the live API. Used on hackathon Day 1 to confirm the integration path before the full build begins.

---

## Constraints

- Do not assume AgentFightClub works as described in the proposal — verify against the actual skill.md and docs
- Do not recommend replacing AgentFightClub unless the gap analysis clearly shows it cannot meet the MVP requirements — the fallback should be a last resort, not a first preference
- Be specific: "AgentFightClub supports X via the `propose` command which takes Y parameters and returns Z" is useful; "AgentFightClub should support this" is not
- If you find that the skill.md or how-it-works docs are incomplete or ambiguous on a key point, flag it explicitly as an open question rather than guessing

---

## Output Location

Save all deliverables to `hackathon/research/`. Create the directory if it does not exist.

After writing, run `git status --short` and report what files were created or modified. Do not commit — Santiago reviews and commits manually.
