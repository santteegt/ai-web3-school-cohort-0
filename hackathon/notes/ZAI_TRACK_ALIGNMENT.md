# Z.AI Track Alignment — GuildOS Specialist Agent

> Track: Z.AI | Web3 × Long-Horizon Task  
> Focus: GLM-5.1 as the autonomous execution engine for the GuildOS Specialist Agent  
> Last updated: 2026-06-07 | Agent: Sensei (Claude via Cowork)

---

## 1. Track Thesis — Why This Matters

The Z.AI track asks a direct question: **can an AI agent execute a real, multi-step Web3 workflow from a natural-language mandate all the way to a verifiable on-chain deliverable — without a human in the loop at every step?**

GuildOS answers with a running system. The Specialist Agent, powered by GLM-5.1, receives a structured task via A2A protocol, decomposes it autonomously, runs a continuous tool-use loop across multiple execution phases, self-corrects on failure, and produces a cryptographically committed deliverable on Base testnet — then returns the result to the Orchestrator Agent through A2A. The human only appears twice: to approve the hire, and to accept the finished work.

Everything in between is long-horizon autonomous execution.

---

## 2. What "Long-Horizon" Means in GuildOS

Most agent demos are one-shot: send a prompt, get a response. Long-horizon task execution is qualitatively different — it requires the agent to:

1. **Decompose** an underspecified requirement into a concrete, ordered plan
2. **Persist state** across multiple tool calls without losing context
3. **Use tools iteratively** — read, write, call, check, retry
4. **Self-correct** when a tool call fails or an intermediate output is wrong
5. **Produce structured output** that satisfies an external acceptance criterion, not just one that looks reasonable to the agent

In GuildOS, "long-horizon" is enforced by the economics: the Specialist Agent's payment is locked in a Moloch v3 treasury and only releases if the deliverable hash passes a pre-check and the human accepts it. There is no partial credit. The agent must complete the full workflow or nothing.

This is the hardest possible test for a long-horizon model — not a synthetic benchmark, but a real payment gate.

---

## 3. The Full Execution Flow — Requirement to Delivery

### Entry Point: A2A Task Message

The Orchestrator Agent sends a structured A2A `task/send` message to the Specialist Agent. The message contains:

```json
{
  "taskId": "<uuid>",
  "type": "smart-contract-audit",
  "input": {
    "source": "<Solidity source or IPFS CID>",
    "scope": "ERC-20 staking contract",
    "acceptanceCriteria": [
      "OWASP Smart Contract Top 10 checklist completed",
      "No critical or high findings left unmitigated",
      "Audit report in structured Markdown: findings, severity, recommendation, status"
    ]
  },
  "budget": "0.3 ETH",
  "deadline": "<ISO-8601>",
  "guildContract": "0x...",
  "orchestratorA2AEndpoint": "https://..."
}
```

This is the Specialist Agent's full brief. It receives this cold — no prior context, no pre-loaded knowledge of the contract. Everything that follows is autonomous.

---

### Phase 1: Task Decomposition (GLM-5.1 Planning)

GLM-5.1's long-horizon planning head converts the acceptance criteria into an ordered execution plan before any tool is called. The plan is not hidden chain-of-thought — it is written to the guild context store so the Orchestrator can observe progress without polling the agent directly.

**Decomposition output (written to guild context):**

```
PLAN — smart-contract-audit / task <uuid>
─────────────────────────────────────────
Step 1: Fetch contract source
  Tool: fetch_source(cid or raw)
  Output: Solidity text

Step 2: Static analysis pass — automated vulnerability scan
  Tool: call_slither(source_text)
  Output: JSON finding list

Step 3: Manual review — OWASP Top 10 checklist
  Tool: llm_review(source_text, checklist=OWASP_SC_TOP10)
  Output: checklist JSON (item → pass/fail/finding)

Step 4: Cross-reference — merge automated + manual findings
  Tool: merge_findings(slither_output, checklist_output)
  Output: unified finding list with deduplication

Step 5: Classify and triage findings
  Tool: classify_findings(finding_list)
  Output: findings annotated with severity (Critical/High/Medium/Low/Informational)

Step 6: Generate mitigation recommendations
  Tool: llm_recommend(finding, context=source_text)
  Output: per-finding recommendation

Step 7: Compile audit report
  Tool: render_report(findings, recommendations, metadata)
  Output: Markdown report

Step 8: Self-check — verify report satisfies acceptance criteria
  Tool: evaluate_report(report, acceptance_criteria)
  Output: pass/fail per criterion

Step 9 (conditional): Iterate — if any criterion fails, loop back to Step 3 or 6
  Trigger: evaluate_report returns any fail

Step 10: Hash and commit deliverable
  Tool: sha256(report), commit_hash(hash, guild_contract, task_id)
  Output: tx_hash

Step 11: Return deliverable via A2A
  Tool: a2a_send(task/delivered, deliverable_ref, hash, tx_hash)
```

The plan is written once and then executed step by step. If an early step fails (tool error, empty output, malformed JSON), the agent does not abandon the task — it retries with backoff, logs the failure reason, and adapts the downstream steps if needed.

---

### Phase 2: Continuous Tool-Use Loop

Each plan step maps to one or more tool calls. GLM-5.1 holds the full plan in context throughout execution, so intermediate outputs from Step 2 inform Step 5, and a revision in Step 3 triggers a re-check in Step 8.

**Tool manifest available to the Specialist Agent:**

| Tool | Purpose | Failure mode handled |
|---|---|---|
| `fetch_source(cid)` | Retrieve contract source via IPFS or direct URL | Retry with alternate gateway; fallback to inline source if provided |
| `call_slither(source)` | Run static analysis via Slither subprocess | Parse stderr for install errors; retry; skip if unavailable, flag in report |
| `llm_review(source, checklist)` | GLM-5.1 self-call for structured checklist evaluation | Retry with narrowed scope if context too long |
| `merge_findings(a, b)` | Deduplicate and merge finding lists | Normalize schemas before merge; log conflicts |
| `classify_findings(list)` | Assign CVSS-adjacent severity tiers | Prompt-based; retry on schema mismatch |
| `llm_recommend(finding, context)` | Generate per-finding remediation | Skipped for Informational severity; retried on empty output |
| `render_report(findings, meta)` | Compile structured Markdown report | Template-based; deterministic |
| `evaluate_report(report, criteria)` | Self-check against acceptance criteria | Returns structured pass/fail per criterion with rationale |
| `sha256(content)` | Hash deliverable deterministically | Pure function; no failure mode |
| `commit_hash(hash, contract, task_id)` | Write hash to Base Sepolia via `eth_sendTransaction` | Retry on gas estimation failure; exponential backoff on RPC error |
| `a2a_send(message_type, payload)` | Send A2A message to Orchestrator endpoint | Retry with 3× backoff; log failure if endpoint unreachable |

---

### Phase 3: Self-Correction Loop

The `evaluate_report` step is the agent's self-correction gate. It runs after the full report is compiled, before the hash is committed. If any acceptance criterion fails, the agent does not stop — it identifies the specific failing criterion, traces it back to the responsible plan step, and re-runs only that step.

**Self-correction triggers and responses:**

| Failure | Agent response |
|---|---|
| OWASP checklist incomplete (missing items) | Re-run `llm_review` with explicit item list; merge delta into finding list |
| Critical finding has no mitigation | Re-run `llm_recommend` for that finding with stricter prompt |
| Report format does not match required schema | Re-run `render_report` with corrected template |
| Slither not available in environment | Mark automated analysis as skipped; add explicit note in report; continue |
| `commit_hash` RPC timeout | Retry up to 5× with exponential backoff; if all fail, deliver report without hash and flag for manual commit |

The loop terminates when all acceptance criteria pass or after a configurable maximum iteration count (default: 3 correction cycles). If the maximum is reached without convergence, the agent delivers the best available report with a `PARTIAL` status flag, so the Orchestrator can present it to the human with context rather than silently failing.

This is the core long-horizon property: **the agent does not give up after one attempt**. It iterates toward the specification.

---

### Phase 4: On-Chain Commitment and A2A Return

Once `evaluate_report` returns all-pass, the agent:

1. Computes `SHA-256(report)` — deterministic, byte-for-byte reproducible
2. Calls `commit_hash(hash, guild_contract, task_id)` — writes the hash to the GuildOS contract on Base Sepolia, producing a `DeliverableCommitted` event with block timestamp
3. Receives `tx_hash` from the RPC response
4. Sends an A2A `task/delivered` message to the Orchestrator:

```json
{
  "taskId": "<uuid>",
  "status": "delivered",
  "deliverable": {
    "type": "audit-report",
    "content": "<Markdown report>",
    "sha256": "<hash>",
    "commitTx": "<tx_hash>",
    "commitBlock": <block_number>,
    "network": "base-sepolia"
  },
  "executionSummary": {
    "stepsCompleted": 11,
    "correctionCycles": 1,
    "toolCallCount": 23,
    "durationSeconds": 142
  }
}
```

The `executionSummary` is not decoration — it is evidence. Judges can verify that the agent ran a real multi-step workflow, not a single LLM call with a canned response.

---

## 4. What GLM-5.1 Contributes Specifically

GLM-5.1 is not a drop-in general-purpose model in this stack. It is chosen for three capabilities that make the long-horizon loop possible:

**Long context window.** The full Solidity source, the running plan, intermediate tool outputs, and the partial report are all held in context simultaneously. Models with shorter context windows would lose earlier steps and produce incoherent reports. GLM-5.1 maintains coherence across all 11 plan steps.

**Structured output reliability.** Every tool that feeds into the next step produces structured JSON. GLM-5.1's instruction-following on schema-constrained outputs is what makes `merge_findings` and `evaluate_report` work without manual parsing. If the model drifts from the schema, the `evaluate_report` gate catches it and forces a retry — but in practice, schema adherence is high enough that correction cycles are infrequent.

**Multi-step planning without prompt-injection from tool outputs.** Tool outputs (especially Slither JSON, which can contain arbitrary text from the contract under analysis) are processed by GLM-5.1 without losing track of the plan. The model treats tool outputs as data, not as new instructions — a property that is critical for security-sensitive workflows where the contract being analyzed could attempt to manipulate the auditor.

---

## 5. Web3 Proof Points

The Z.AI track requires demonstrable Web3 integration, not just a Web3-themed prompt. GuildOS provides three on-chain proof points generated entirely by autonomous agent execution:

| Proof | Source | Verifiable at |
|---|---|---|
| Deliverable hash committed before human review | `commit_hash` tool call in Phase 4 | Basescan — `DeliverableCommitted` event, block timestamp |
| Hash matches final report byte-for-byte | SHA-256 recomputable from the delivered Markdown | Recompute locally: `sha256sum report.md` |
| Payment released only after human acceptance | `settle()` call in AgentFightClub contract | Basescan — treasury outflow tx, triggered post-acceptance |

These three transactions together prove: the agent delivered something real before payment, the deliverable was not modified after commitment, and payment moved on acceptance — not on the agent's say-so.

---

## 6. Why This Satisfies the Track Criteria

The Z.AI track rubric centers on three axes: **long-horizon execution**, **Web3 integration**, and **real GLM-5.1 usage**. GuildOS hits all three:

**Long-horizon execution:** The Specialist Agent runs an 11-step plan with up to 3 self-correction cycles and ~20 tool calls. No human touches it between task receipt and `task/delivered`. The execution log (step names, timestamps, tool call counts, correction cycles) is returned with the deliverable and visible to judges.

**Web3 integration:** The deliverable hash, the payment settlement, and the reputation record are all on-chain. The agent holds and uses a wallet (Cobo CAW, pact-scoped to the guild mandate) to sign and submit transactions. The workflow could not run on a Web2 backend — the payment gate and the tamper-proof commitment are protocol-level, not database rows.

**Real GLM-5.1 usage:** The model drives the full execution loop — planning, tool orchestration, checklist evaluation, recommendation generation, self-correction, and report compilation. It is not a fallback or a summarizer — it is the engine. The task type (smart contract audit) is chosen specifically because it requires multi-step reasoning over technical content, not just retrieval or formatting. A one-shot model call cannot complete it.

---

## 7. Demo Sequence for Z.AI Judges

The recommended demo walkthrough emphasizing the Z.AI axis:

1. **Show the A2A task message** — structured mandate arriving at the Specialist Agent endpoint
2. **Show the plan** — GLM-5.1's decomposition written to the guild context store before any tool runs
3. **Live-stream the tool call log** — each step name, tool called, and status as execution progresses (terminal tail or simple web log view)
4. **Show a correction cycle** (if one occurs naturally, or trigger it by injecting a deliberate schema error in the test contract) — agent identifies the failing criterion, re-runs the step, re-evaluates
5. **Show the compiled report** — structured Markdown with findings, severities, recommendations
6. **Show the `commit_hash` transaction** on Basescan — deliverable hash on-chain before human sees the result
7. **Show the `task/delivered` A2A message** — execution summary with step count, duration, and correction cycles
8. **Human accepts** — Orchestrator sends `task/accepted`, AgentFightClub `settle()` releases payment
9. **Show the settlement transaction** on Basescan — payment moved on acceptance, not on agent promise
10. **Show the ERC-8004 reputation delta** — Specialist Agent's profile before (0 deliveries) → after (1 verified delivery with hash, timestamp, guild address)

Total live demo duration: ~4–6 minutes if Base Sepolia is fast. Pre-stage Steps 1–3 (plan written) before the demo starts so the live portion is Steps 4–10.

---

## 8. Risk Register (Z.AI Axis)

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| GLM-5.1 fails to complete the audit report in one session | Low | High | Pre-test 3 contract sizes on Day 1; pick the size that completes reliably; cap scope if needed |
| Tool call count causes context overflow | Medium | Medium | Truncate Slither output to top 20 findings; summarize intermediate outputs before appending to context |
| Self-correction loop does not converge | Low | Medium | Cap at 3 cycles; deliver `PARTIAL` status with best-effort report; document in demo |
| Base Sepolia RPC congestion during demo | Medium | Medium | Pre-submit `commit_hash` before demo starts; show pre-staged tx hash as fallback |
| GLM-5.1 API latency > demo budget | Low | Low | Run locally cached replay if latency is unacceptable; full live run is preferred |

---

*Section references: PROJECT_PROPOSAL.md §4 (Real Scenario), §5 (Minimum Demo Loop), §9 (Track Alignment), §13 (Architecture Decision)*  
*Track: Z.AI | Web3 × Long-Horizon Task*  
*Submission deadline: 2026-06-13 12:00 UTC+8*
