# Prompt Template — Frontier Tech Stack Research

> **How to use:** Copy this file to `prompts/<COMPONENT>_RESEARCH.md`, then fill in every section marked with `<!-- FILL: ... -->`. Delete this header block and all `<!-- FILL -->` comments before using the prompt. See the filled example at `prompts/AGENTFIGHTCLUB_RESEARCH.md`.

---

<!-- FILL: Replace with the component name, e.g. "A2A Protocol", "ERC-8004", "GLM-5.1", "Cobo CAW" -->
# Prompt — [COMPONENT] Frontier Research

> **Purpose:** <!-- FILL: One sentence — what decision or build question does this research answer? -->  
> **Created:** <!-- FILL: YYYY-MM-DD -->  
> **Deliverable directory:** `hackathon/research/`

---

## Your Role

You are Sensei, the AI × Web3 School Learning Agent for Santiago. Act as a rigorous technical researcher and critical evaluator. Your job is not to confirm that [COMPONENT] fits GuildOS — it's to find out whether it actually does, with evidence.

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

<!-- FILL: Describe what role this specific component plays in GuildOS and what open question the research must answer. Be specific about which step(s) in the flow above the component is responsible for. Example:

"The project proposal specifies **A2A Protocol** as the agent-to-agent communication layer (Steps 3–5 and result return). The open question is: does A2A 0.3.0 actually provide the message schema and payment-intent association that GuildOS needs — or is the proposal making assumptions that don't hold?"
-->

**The open question is: [STATE THE CORE QUESTION THIS RESEARCH MUST ANSWER]**

---

## What to Read Before Writing Anything

Read all of these in full before producing any output:

1. **Project proposal:** `hackathon/PROJECT_PROPOSAL.md` — pay close attention to Section 5 (Minimum Demo Loop), Section 7 (Mock vs. Real), Section 8 (Process Flow), and Section 9 (Main Risks)
2. **Prototyping resources:** `hackathon/PROTOTYPING_RESOURCES.md` — <!-- FILL: Section number and title for this component, e.g. "Section 3 (A2A Protocol)" -->
<!-- FILL: Add 2–4 primary sources specific to this component. Each line should be:
   N. **[Source name]:** fetch and read [URL] — [one sentence on why this is the most important doc]
Example:
   3. **A2A Official Repository:** fetch and read https://github.com/a2aproject/A2A — the spec and reference implementation; the canonical source for message schema and versioning
   4. **A2A Specification (0.3.0):** fetch and read https://github.com/a2aproject/A2A/blob/main/spec/A2A_spec.md — the versioned spec; pin to this version before evaluating field availability
-->

---

## Research Questions

Answer each question with evidence from what you read — not assumptions.

### Fit Analysis

1. **What does [COMPONENT] actually provide?** <!-- FILL: Tailor this question to the component. For a protocol: "What message types / operations does it expose?" For an SDK: "What API calls are available and what do they return?" For a standard: "What fields/methods does it define and which are mandatory vs. optional?" -->

2. **Which GuildOS features can [COMPONENT] implement directly?** For each feature in Section 5 (Minimum Demo Loop) and the Section 6 MVP feature list that this component is responsible for, state: ✅ supported, ⚠️ partial / requires workaround, or ❌ not supported — with a one-line reason.

3. **What is missing?** For each gap (⚠️ or ❌), explain: what GuildOS needs, what [COMPONENT] provides, and what the delta is. Is the gap bridgeable with a thin wrapper, or does it require replacing [COMPONENT] entirely?

4. **How stable is [COMPONENT]?** <!-- FILL: Tailor to the component's risk profile. Examples:
   - For alpha APIs: "Is there versioning? What is the failure mode if the API is down during the demo?"
   - For draft standards: "Is the EIP finalized? Are there known breaking changes between drafts?"
   - For LLMs: "Is the output format stable enough to hash consistently? What is the fallback if structured output fails?"
-->

### Alternatives

5. **If [COMPONENT] cannot cover a gap, what are the concrete alternatives?** For each identified gap, propose one alternative that fills it. Prioritize options that are: (a) open source and audited or well-documented, (b) compatible with Base testnet, and (c) buildable within the 7-day hackathon scope.

6. <!-- FILL: Add a component-specific "should I replace it?" question. Examples:
   - "Should the fallback (direct Moloch v3 via DAOhaus SDK) replace AgentFightClub as the primary path?"
   - "Should we implement a minimal A2A-compatible message schema ourselves rather than depending on the reference implementation?"
   - "Should GLM-5.1 be used for both agents, or only the Specialist — and what is the cost/latency implication of the choice?"
-->

### Integration Design

7. **What is the minimum integration code required?** For the operations [COMPONENT] does support, sketch the call sequence (pseudocode is fine): <!-- FILL: Describe what the sketch should cover. Example: "how does the Orchestrator Agent send a task message to the Specialist and receive the result, including the payment intent reference in the message?" -->

8. **What needs to be tested on Day 1 of the hackathon?** List the 3–5 operations or behaviors that carry the most integration risk and must be validated before building the rest of the stack.

<!-- FILL (optional): Add 1–2 component-specific questions not covered above. Examples:
   - "What is the cost model? Are there per-call fees, gas costs, or rate limits that affect the hackathon demo budget?"
   - "What is the latency profile? Will synchronous calls block the demo flow at a visible level?"
   - "Are there known security issues or CVEs that affect the version being integrated?"
-->

---

## Deliverables

### Required

**`hackathon/research/[COMPONENT_SLUG]_ANALYSIS.md`** — the full research report. Structure:

```
# [COMPONENT] — Fit Analysis for GuildOS

## TL;DR
One-paragraph verdict: does it fit, partially fit, or need to be replaced?

## Feature Coverage Matrix
Table: GuildOS feature | [COMPONENT] operation/field | Status (✅ / ⚠️ / ❌) | Notes

## Gaps and Alternatives
Per gap: what GuildOS needs → what [COMPONENT] provides → delta → proposed alternative

## Stability Assessment
<!-- FILL: Rename to match the component's primary risk dimension:
     "API Stability", "Spec Maturity", "Output Consistency", "Testnet Availability", etc. -->
Maturity level, versioning, known issues, hackathon risk level

## Recommended Integration Path
Primary path + rationale <!-- FILL: Or "Primary model/version + rationale" for LLMs -->

## Day 1 Test Checklist
3–5 operations / behaviors to validate live before building

## Minimum Integration Sketch
Pseudocode call sequence for <!-- FILL: the core interaction pattern this component enables -->
```

### Optional (if time allows)

<!-- FILL: Describe a concrete runnable artifact (test script, config file, schema stub) that would be useful on hackathon Day 1. Example:
"**`hackathon/research/A2A_DAY1_TEST.py`** — a minimal Python script that sends a task message and receives a result using the A2A reference implementation, validating schema compliance before the full build begins."
-->

---

## Constraints

- Do not assume [COMPONENT] works as described in the proposal — verify against actual documentation and specs
- Do not recommend replacing [COMPONENT] unless the gap analysis clearly shows it cannot meet the MVP requirements
- Be specific: "[COMPONENT] supports X via [operation/method/field] which takes [inputs] and returns [outputs]" is useful; "[COMPONENT] should support this" is not
- If documentation is incomplete or ambiguous on a key point, flag it explicitly as an open question rather than guessing
<!-- FILL (optional): Add any component-specific constraints. Example for LLMs:
   "- Test at least three representative task inputs before recommending a task type for the live demo — do not base the recommendation on a single example output"
-->

---

## Output Location

Save all deliverables to `hackathon/research/`. Create the directory if it does not exist.

After writing, run `git status --short` and report what files were created or modified. Do not commit — Santiago reviews and commits manually.
