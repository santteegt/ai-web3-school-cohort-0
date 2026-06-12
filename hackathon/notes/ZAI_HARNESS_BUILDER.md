# Z.AI Track Alignment — GuildOS Harness Builder Specialist

> Track: Z.AI | Web3 × Long-Horizon Task
> Focus: GLM-5.1 as the autonomous execution engine for a Specialist Agent that builds complete agent harnesses
> Last updated: 2026-06-09 | Agent: Sensei (Claude via Cowork)

---

## 1. Track Thesis — Why This Matters

The Z.AI track asks a direct question: **can an AI agent execute a real, multi-step workflow from a natural-language mandate all the way to a verifiable, usable deliverable — without a human in the loop at every step?**

GuildOS answers with a running system. The Harness Builder Specialist, powered by GLM-5.1, receives a structured intake survey describing a project's goals and the user's profile, then autonomously assembles a **complete agent harness** — the agent's soul (system prompt and operating principles), user settings, and the full set of tools, MCP servers, and skills needed to make that agent a working specialist. The human appears twice: to fill in the initial survey, and to accept the finished harness.

Everything in between is long-horizon autonomous execution: surveying online hubs, evaluating candidate tools, resolving compatibility, composing the harness, validating it, and committing a verifiable manifest on Base testnet.

---

## 2. What "Long-Horizon" Means in GuildOS Harness Building

Most agent demos are one-shot: send a prompt, get a config. Building a real harness is qualitatively different — it requires the agent to:

1. **Decompose** an underspecified goal ("I want an Ethereum dev agent") into a concrete capability spec
2. **Discover** candidate tools, MCP servers, and skills by browsing live online hubs, not a frozen list
3. **Evaluate and select** — match each candidate against the capability spec, deduplicate overlapping tools, resolve version and runtime conflicts
4. **Compose** the soul, settings, and tooling into a coherent, internally consistent harness
5. **Self-correct** when a selected MCP server is unreachable, a skill is incompatible, or a validation check fails
6. **Produce structured output** that satisfies an external acceptance criterion — a harness that actually loads and runs in the target runtime, not one that merely looks plausible

In GuildOS, "long-horizon" is enforced by the deliverable contract: the harness manifest hash is committed on-chain before the human reviews it, and payment only releases if the harness passes a pre-check (loads cleanly, declared tools resolve) and the human accepts it. There is no partial credit for a config that doesn't boot.

This is a demanding test for a long-horizon model — not a synthetic benchmark, but a real build that must run.

---

## 3. The Long-Horizon Mission — Two Harnesses, Then the Builder

The submission scopes the long-horizon task into a deliberate arc that produces both concrete artifacts and a reusable tool:

**Stage A — Build the Ethereum / Web3 Developer harness.** The Specialist surveys Web3-tooling hubs (MCP registries, skill marketplaces, plugin directories) and assembles a harness for an Ethereum developer agent: a soul tuned for Solidity, EVM, and on-chain reasoning; settings scoped to testnet safety; and a toolset spanning an EVM MCP server, contract verification tooling, RPC/explorer access, and skills for audit checklists and gas analysis.

**Stage B — Build the Agentic AI Developer harness.** The Specialist repeats the process for an agentic-AI developer agent: a soul tuned for agent design, evaluation, and orchestration; settings for model and context management; and a toolset spanning an MCP-registry client, an eval/skill-authoring toolkit, and skills for prompt design, tool-use patterns, and agent testing.

**Stage C — Extract design patterns.** Across Stage A and B, the Specialist records the recurring decisions: how souls are templated, how settings map to user-profile fields, how tool overlaps are resolved, how runtime-specific packaging differs. These become the design patterns that generalize the build.

**Stage D — Implement the Harness Builder tool.** The patterns are folded into a **modular harness-builder**: a system that takes a survey + profile and emits a specialist harness for any of the supported runtimes — **Hermes, Openclaw, and Claude Code**. Stage A and B are not throwaway demos; they are the two ground-truth examples the builder is derived from and validated against.

The long-horizon property is that **the final tool is a product of the work, not a precondition of it** — the agent has to do the two builds first to learn how to generalize the third.

---

## 4. The Full Execution Flow — Survey to Harness

### Entry Point: Intake Survey (A2A Task Message)

The Orchestrator Agent sends a structured A2A `task/send` message to the Harness Builder Specialist. The message contains the survey and profile:

```json
{
  "taskId": "<uuid>",
  "type": "harness-build",
  "input": {
    "targetRuntime": "claude-code",
    "specialization": "ethereum-web3-developer",
    "projectGoals": [
      "Write and audit Solidity contracts on Base testnet",
      "Automate testnet deploy + verify loops",
      "Reason over on-chain state during development"
    ],
    "userProfile": {
      "web3": "familiar (DeFi, L2s, ABIs, account abstraction)",
      "ai": "intermediate",
      "coding": "independent developer",
      "safety": "testnet-only, no mainnet keys"
    },
    "acceptanceCriteria": [
      "Harness loads in target runtime without errors",
      "All declared MCP servers resolve and respond to a health probe",
      "Soul + settings + toolset are internally consistent (no conflicting tools)",
      "Harness manifest emitted as structured, reproducible artifact"
    ]
  },
  "budget": "0.3 ETH",
  "deadline": "<ISO-8601>",
  "guildContract": "0x...",
  "orchestratorA2AEndpoint": "https://..."
}
```

This is the Specialist's full brief. It receives this cold — no pre-loaded knowledge of which tools exist. Everything that follows is autonomous.

---

### Phase 1: Task Decomposition (GLM-5.1 Planning)

GLM-5.1's long-horizon planning head converts the survey into a capability spec and an ordered build plan before any hub is queried. The plan is written to the guild context store so the Orchestrator can observe progress without polling the agent directly.

**Decomposition output (written to guild context):**

```
PLAN — harness-build / ethereum-web3-developer / task <uuid>
────────────────────────────────────────────────────────────
Step 1: Derive capability spec from goals + profile
  Tool: derive_capabilities(goals, profile)
  Output: capability list (e.g. solidity-authoring, static-audit,
          rpc-read, explorer-verify, gas-analysis, testnet-deploy)

Step 2: Survey online hubs for candidate components
  Tool: search_hubs(capability, kind=tool|mcp|skill)
  Output: ranked candidate list per capability

Step 3: Probe candidates — reachability + metadata
  Tool: probe_component(ref)
  Output: health, runtime compatibility, declared scopes

Step 4: Select + deduplicate components
  Tool: select_components(candidates, capability_spec)
  Output: chosen set, overlaps removed, conflicts flagged

Step 5: Resolve conflicts (version / runtime / scope)
  Tool: resolve_conflicts(chosen_set, target_runtime)
  Output: compatible component set

Step 6: Author the soul
  Tool: compose_soul(specialization, goals, profile)
  Output: system prompt + operating principles

Step 7: Compose user settings
  Tool: compose_settings(profile, safety, target_runtime)
  Output: settings block (model, scopes, safety rails)

Step 8: Assemble harness manifest
  Tool: assemble_harness(soul, settings, components, runtime)
  Output: runtime-specific manifest (Hermes / Openclaw / Claude Code)

Step 9: Validate — load + health-probe + consistency check
  Tool: validate_harness(manifest, acceptance_criteria)
  Output: pass/fail per criterion

Step 10 (conditional): Iterate — on any fail, loop to Step 4/6/7
  Trigger: validate_harness returns any fail

Step 11: Record design patterns observed in this build
  Tool: log_patterns(plan_trace, decisions)
  Output: pattern entries appended to pattern library

Step 12: Hash + commit harness manifest
  Tool: sha256(manifest), commit_hash(hash, guild_contract, task_id)
  Output: tx_hash

Step 13: Return deliverable via A2A
  Tool: a2a_send(task/delivered, harness_ref, hash, tx_hash)
```

The plan is written once and executed step by step. If an early step fails (hub timeout, unreachable MCP, malformed metadata), the agent does not abandon the task — it retries with backoff, logs the reason, and adapts downstream steps.

---

### Phase 2: Continuous Tool-Use Loop

Each plan step maps to one or more tool calls. GLM-5.1 holds the full plan and capability spec in context throughout, so a candidate found in Step 2 informs the dedup in Step 4, and a conflict resolved in Step 5 changes what the soul in Step 6 may assume.

**Tool manifest available to the Harness Builder Specialist:**

| Tool | Purpose | Failure mode handled |
|---|---|---|
| `derive_capabilities(goals, profile)` | Map goals + profile to a concrete capability spec | Retry with narrowed scope; flag ambiguous goals for default |
| `search_hubs(capability, kind)` | Query online tool/MCP/skill hubs for candidates | Retry alternate hub; fall back to cached index if hub down |
| `probe_component(ref)` | Health-check and read metadata of a candidate | Mark unreachable; exclude from selection; log reason |
| `select_components(cands, spec)` | Choose + deduplicate components per capability | Prefer maintained + compatible; log dropped overlaps |
| `resolve_conflicts(set, runtime)` | Resolve version / runtime / scope conflicts | Pin compatible versions; drop incompatible with note |
| `compose_soul(spec, goals, profile)` | GLM-5.1 self-call to author the agent soul | Retry on schema drift; constrain to soul template |
| `compose_settings(profile, safety, runtime)` | Build settings block with safety rails | Default to most-restrictive safe profile on ambiguity |
| `assemble_harness(soul, settings, comps, runtime)` | Emit runtime-specific manifest | Template-based per runtime; deterministic |
| `validate_harness(manifest, criteria)` | Load, health-probe, consistency-check | Returns structured pass/fail per criterion with rationale |
| `log_patterns(trace, decisions)` | Record reusable design patterns | Append-only; pure |
| `sha256(content)` | Hash manifest deterministically | Pure function; no failure mode |
| `commit_hash(hash, contract, task_id)` | Write hash to Base Sepolia via `eth_sendTransaction` | Retry on gas estimation failure; backoff on RPC error |
| `a2a_send(message_type, payload)` | Send A2A message to Orchestrator endpoint | Retry with 3× backoff; log if endpoint unreachable |

---

### Phase 3: Self-Correction Loop

The `validate_harness` step is the agent's self-correction gate. It runs after the manifest is assembled, before the hash is committed. If any acceptance criterion fails, the agent traces it to the responsible plan step and re-runs only that step.

**Self-correction triggers and responses:**

| Failure | Agent response |
|---|---|
| Declared MCP server fails health probe | Re-run `select_components` for that capability; pick next-best candidate |
| Two selected tools expose conflicting commands | Re-run `resolve_conflicts`; drop the lower-ranked tool, note in manifest |
| Soul references a tool that was dropped in dedup | Re-run `compose_soul` with the final component set as ground truth |
| Settings grant a scope the runtime rejects | Re-run `compose_settings` with runtime's allowed-scope list |
| Manifest fails to load in target runtime | Re-run `assemble_harness` with corrected runtime template |
| `commit_hash` RPC timeout | Retry up to 5× with backoff; deliver manifest without hash, flag for manual commit |

The loop terminates when all criteria pass or after a configurable max iteration count (default: 3 cycles). If the max is reached without convergence, the agent delivers the best harness with a `PARTIAL` status flag and an explicit list of unmet criteria, so the Orchestrator can present it to the human with context rather than silently shipping a broken harness.

This is the core long-horizon property: **the agent does not give up after one attempt**. It iterates toward a harness that actually boots.

---

### Phase 4: On-Chain Commitment and A2A Return

Once `validate_harness` returns all-pass, the agent:

1. Computes `SHA-256(manifest)` — deterministic, byte-for-byte reproducible
2. Calls `commit_hash(hash, guild_contract, task_id)` — writes the hash to the GuildOS contract on Base Sepolia, producing a `DeliverableCommitted` event with block timestamp
3. Receives `tx_hash` from the RPC response
4. Sends an A2A `task/delivered` message to the Orchestrator:

```json
{
  "taskId": "<uuid>",
  "status": "delivered",
  "deliverable": {
    "type": "agent-harness",
    "specialization": "ethereum-web3-developer",
    "targetRuntime": "claude-code",
    "manifest": "<harness manifest: soul + settings + components>",
    "componentCount": { "tools": 4, "mcp": 2, "skills": 3 },
    "sha256": "<hash>",
    "commitTx": "<tx_hash>",
    "commitBlock": <block_number>,
    "network": "base-sepolia"
  },
  "executionSummary": {
    "stepsCompleted": 13,
    "correctionCycles": 1,
    "hubsQueried": 5,
    "candidatesEvaluated": 41,
    "toolCallCount": 37,
    "durationSeconds": 218
  }
}
```

The `executionSummary` is not decoration — it is evidence. Judges can verify the agent ran a real multi-step build (queried hubs, evaluated dozens of candidates, corrected itself), not a single LLM call emitting a canned config.

---

## 5. What GLM-5.1 Contributes Specifically

GLM-5.1 is not a drop-in general-purpose model in this stack. It is chosen for three capabilities that make the long-horizon harness build possible:

**Long context window.** The capability spec, the running plan, dozens of candidate-component metadata blobs, conflict-resolution state, and the partial manifest are all held in context simultaneously. Shorter-context models would lose earlier candidates and produce a soul that references tools already dropped. GLM-5.1 maintains coherence across all 13 plan steps and both ground-truth builds.

**Structured output reliability.** Every tool feeding the next step produces structured JSON — capability specs, candidate rankings, the manifest itself. GLM-5.1's instruction-following on schema-constrained outputs is what makes `select_components` and `validate_harness` compose without manual parsing. When the model drifts, the validation gate catches it and forces a retry.

**Multi-step reasoning without prompt-injection from hub content.** Component metadata pulled from public hubs (descriptions, READMEs) can contain arbitrary text. GLM-5.1 treats hub content as data to evaluate, not as new instructions — critical when assembling a harness from untrusted third-party tool descriptions that could attempt to inject scopes or override the soul.

---

## 6. Web3 Proof Points

The Z.AI track requires demonstrable Web3 integration, not just a Web3-themed prompt. GuildOS provides three on-chain proof points generated entirely by autonomous agent execution:

| Proof | Source | Verifiable at |
|---|---|---|
| Harness manifest hash committed before human review | `commit_hash` tool call in Phase 4 | Basescan — `DeliverableCommitted` event, block timestamp |
| Hash matches final manifest byte-for-byte | SHA-256 recomputable from the delivered manifest | Recompute locally: `sha256sum harness.json` |
| Payment released only after human acceptance | `settle()` call in the GuildOS treasury contract | Basescan — treasury outflow tx, triggered post-acceptance |

These three transactions together prove: the agent delivered a real, validated harness before payment, the deliverable was not modified after commitment, and payment moved on acceptance — not on the agent's say-so. The Ethereum/Web3 harness itself ships an EVM MCP server and testnet tooling, so its first run is also a Web3 action.

---

## 7. Why This Satisfies the Track Criteria

The Z.AI track rubric centers on three axes: **long-horizon execution**, **Web3 integration**, and **real GLM-5.1 usage**. GuildOS hits all three:

**Long-horizon execution:** Building one harness is a 13-step plan with up to 3 self-correction cycles, ~5 hubs queried, ~40 candidates evaluated, and ~35 tool calls. The full mission chains two complete builds (Ethereum/Web3 dev, agentic-AI dev), extracts design patterns from them, and produces a third deliverable — the modular harness-builder — derived from the first two. No human touches any single build between task receipt and `task/delivered`.

**Web3 integration:** The manifest hash, the payment settlement, and the reputation record are all on-chain. The agent holds and uses a wallet (pact-scoped to the guild mandate) to sign and submit transactions. The Web3 harness it produces is itself testnet tooling. The workflow could not run on a Web2 backend — the commitment and payment gate are protocol-level, not database rows.

**Real GLM-5.1 usage:** The model drives the full loop — capability derivation, hub survey, candidate evaluation, conflict resolution, soul authoring, settings composition, validation, self-correction, and pattern extraction. It is the engine, not a summarizer. The task (assemble a harness that must actually boot across three distinct runtimes) requires sustained multi-step reasoning over heterogeneous technical content; a one-shot call cannot complete it.

---

## 8. Demo Sequence for Z.AI Judges

The recommended demo walkthrough emphasizing the Z.AI axis:

1. **Show the intake survey** — the structured goals + profile arriving at the Harness Builder endpoint
2. **Show the plan** — GLM-5.1's decomposition into capability spec + 13-step build plan, written to guild context before any hub is queried
3. **Live-stream the build log** — capability derivation, hub queries, candidates evaluated and dropped, conflicts resolved, each step name and status
4. **Show a correction cycle** — naturally (an MCP health probe fails) or triggered (inject an unreachable server into the candidate set); agent re-selects, re-validates
5. **Show the assembled harness** — soul, settings, and the resolved tool/MCP/skill set for the Ethereum/Web3 dev agent
6. **Boot the harness** — load it in the target runtime (Claude Code) and run one specialist action (e.g. an EVM read) to prove it works
7. **Show the second build** — the agentic-AI dev harness, demonstrating the same pipeline generalizes
8. **Show the extracted design patterns + the modular builder** — how A and B fed the final harness-builder tool, and emit a third harness for a different runtime (Hermes or Openclaw)
9. **Show the `commit_hash` transaction** on Basescan — manifest hash on-chain before human review
10. **Human accepts** — Orchestrator sends `task/accepted`, treasury `settle()` releases payment; show the settlement tx and the ERC-8004 reputation delta (0 → verified builds)

Total live demo duration: ~5–7 minutes. Pre-stage Steps 1–3 (plan written) and pre-run one of the two builds before the demo so the live portion is the second build + builder generalization + on-chain settlement.

---

## 9. Risk Register (Z.AI Axis)

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Online hubs are slow / unreachable during the build | Medium | High | Cache a hub index snapshot on Day 1; fall back to cache if live query times out |
| Selected MCP server is incompatible with target runtime | Medium | Medium | `resolve_conflicts` filters by runtime up front; validation re-probes before commit |
| GLM-5.1 fails to keep soul consistent with final component set | Low | High | `validate_harness` consistency check forces a `compose_soul` re-run on mismatch |
| Candidate metadata attempts prompt injection | Low | Medium | Treat hub content strictly as data; sandbox evaluation; never let descriptions alter scopes |
| Generalizing to all three runtimes (Hermes/Openclaw/Claude Code) overruns scope | Medium | Medium | Ship Claude Code as the primary validated target; mark Hermes/Openclaw emitters as beta in the manifest |
| Base Sepolia RPC congestion during demo | Medium | Medium | Pre-submit `commit_hash` before demo; show pre-staged tx as fallback |
| GLM-5.1 API latency > demo budget | Low | Low | Pre-run one build; live-run the second; cached replay as last resort |

---

*Section references: PROJECT_PROPOSAL.md §4 (Real Scenario), §5 (Minimum Demo Loop), §9 (Track Alignment), §13 (Architecture Decision)*
*Track: Z.AI | Web3 × Long-Horizon Task*
*Submission deadline: 2026-06-13 12:00 UTC+8*
