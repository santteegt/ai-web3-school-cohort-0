# Execution Plan: Issues #36, #37, #38, #39 — Phase 1a A2A Plumbing

## Architecture (confirmed)

All inter-agent state coordination through A2A — no local-file coupling between agents.

- **Runner** polls Specialist's `tasks/get` via `poll_task()` for deliverable data
- **OrchestratorA2AServer** uses `InMemoryTaskStore` (NOT guild_context.json)
- **guild_context.json** = CLI runner's local tracking only
- **Two independent A2A channels**: polling (Specialist endpoint) + proactive push (Orchestrator endpoint)
- Runner uses polling channel; OrchestratorA2AServer validated independently

## Resolved blockers

- **BQ1**: reputation_propose stubbed (log + return ack) — Phase 3 tool
- **BQ2**: `send_invite()` returns full response dict (enables runner to get quote from real transport)
- **BQ3**: asyncio.Queue → replaced with polling-only approach (A2A-native)

## Build order: #36 → #37 → #38 → #39 (one branch, one PR per issue)

---

## PR 1: Issue #36 — Orchestrator A2A server

**Branch:** `feat/issue-36-orchestrator-a2a-server`

### Files

**`src/orchestrator/a2a_server.py`** (new):
- `ORCHESTRATOR_PORT = int(os.getenv("ORCHESTRATOR_A2A_PORT", "10000"))`
- `ORCHESTRATOR_BASE_URL`, `AGENT_CARD` (mirror Specialist pattern: JSONRPC + REST interfaces)
- `OrchestratorExecutor(AgentExecutor)`:
  - `execute()`: parse inbound message → validate type ∈ {task/delivered, feedback/request} → emit WORKING → dispatch → emit COMPLETED with result
  - `_handle_delivered()`: log incoming, call `tools.deliverable_review()`, return pre-check result
  - `_handle_feedback_request()`: log incoming, stub reputation_propose, return ack
  - `_reject_unknown()`: fail closed for unrecognized types
  - `cancel()`: emit CANCELED
- `create_orchestrator_app()`: build FastAPI app with A2A routes, return (app, task_store) for testing
- `main()`: start uvicorn on ORCHESTRATOR_PORT
- Reuses `_log_message` from `src/shared/a2a.py`

**`tests/test_orchestrator_a2a_server.py`** (new):
- Agent Card served at `/.well-known/agent-card.json` (httpx ASGITransport)
- `task/delivered` → triggers pre-check → COMPLETED with result
- `feedback/request` → stub → COMPLETED with ack
- Unknown message type → rejected (COMPLETED with error)
- Executor → EventQueue unit tests (real EventQueueLegacy, like test_a2a_transport.py)
- Full JSON-RPC integration smoke test

### Pattern reference
- Mirror `src/specialist/agent.py` (AGENT_CARD, SpecialistExecutor, main)
- Mirror `tests/test_a2a_transport.py` (3-layer testing: extract, executor, integration)

---

## PR 2: Issue #37 — Specialist A2A client

**Branch:** `feat/issue-37-specialist-a2a-client`

### Files

**`src/specialist/a2a_client.py`** (new):
- `send_delivered(orchestrator_endpoint, task_id, deliverable_hash, attestation_uid, attestation_url) -> dict`
  - Build `task/delivered` payload with all 4 fields
  - Call `_send_to_agent(orchestrator_endpoint, message)` (reused from `src/shared/a2a.py`)
  - Log outgoing via `_log_message`
  - Return response dict
  - On failure: raise + log (not silent)
- `send_feedback_request(orchestrator_endpoint, task_id, deliverable_hash) -> dict`
  - Same pattern for `feedback/request`
- Imports `_build_message`, `_extract_response`, `_send_to_agent`, `_log_message` from `src/shared/a2a.py` — does NOT modify that file

**`tests/test_specialist_a2a_client.py`** (new):
- `send_delivered()` constructs correct message with all fields
- `send_feedback_request()` constructs correct message
- Both log to a2a_trace
- Unreachable endpoint raises surfaced, logged error (mock `_send_to_agent` to raise)
- Mock `_send_to_agent` pattern (same as test_a2a.py)

---

## PR 3: Issue #38 — Non-blocking task/send + polling

**Branch:** `feat/issue-38-nonblocking-task-send`

### Files

**`src/shared/a2a.py`** (modify):
1. `_build_send_request()`: accept optional `configuration` param
2. `_send_to_agent()`: accept optional `configuration` param, pass to request
3. `send_task()`:
   - Validate `task.get("orchestrator_endpoint")` — raise ValueError if missing
   - Set `SendMessageConfiguration(return_immediately=True)`
   - Return `task_id` from WORKING response (not `message.message_id`)
   - Log incoming as `task/send_response` (not `task/delivered`)
4. `send_invite()`:
   - Return full response dict (not just `message.message_id`) — BQ2 resolution
   - Response already has quote data + message_id from `_extract_response()`
5. Add `poll_task(endpoint, task_id) -> dict`:
   - Use `ClientFactory` → `client.get_task(GetTaskRequest(id=task_id))`
   - Return dict: `{task_id, task_state, ...payload_from_status_message}`
6. `send_accepted()` — unchanged (synchronous, unaffected)

**`tests/test_a2a.py`** (modify):
- Update `test_send_invite_builds_correct_message`: expect dict return, verify quote fields
- Update `test_send_task_builds_correct_message`: expect task_id return, verify return_immediately config
- Add `test_send_task_rejects_missing_orchestrator_endpoint`
- Add `test_poll_task_returns_state`

**`tests/test_task_delegation.py`** (modify):
- Add `orchestrator_endpoint` to `well_formed_task` fixture
- Update TextBodyFallback test for new send_task behavior

**Note:** `send_task()` validation will temporarily break the runner (no `orchestrator_endpoint` in `full_task` until #39). This is acceptable — the runner is being rewritten in #39 and already bypasses A2A.

---

## PR 4: Issue #39 — Runner async flow rewrite

**Branch:** `feat/issue-39-runner-async-rewrite`

### Files

**`src/cli/runner.py`** (modify):
1. Remove imports: `from src.specialist.agent import handle_task_invite, handle_task_send`
2. Add imports: `send_invite`, `send_task`, `poll_task` from `src.shared.a2a`
3. Step 4 (invite):
   - Call `send_invite(specialist_endpoint, task_spec)` → get response dict
   - Extract quote from response (response contains scope, estimated_cost_wei, deadline_iso)
4. Step 6 (delegate):
   - Add `orchestrator_endpoint` to `full_task` dict (e.g., `http://localhost:10000`)
   - Call `send_task(specialist_endpoint, full_task)` → get task_id
5. Steps 8-9 (wait for deliverable):
   - Poll loop: `poll_task(specialist_endpoint, task_id)` until task_state == COMPLETED (with timeout)
   - Extract deliverable_hash + deliverable_reference from poll response's status.message
   - Remove simulated deliverable block (handle_task_send call)
6. After settlement:
   - Wait for feedback/request is NOT needed for Phase 1a (reputation is Phase 3 stub)
   - Keep existing reputation_write stub
7. All 6 gates preserved exactly — no changes to gates.py calls

**`tests/test_runner.py`** (new):
- Mock A2A transport (send_invite, send_task, poll_task)
- Verify runner calls send_invite/send_task/poll_task (not handle_task_invite/handle_task_send)
- Verify quote extracted from send_invite response
- Verify orchestrator_endpoint set in full_task
- Verify poll loop runs until COMPLETED
- Verify all gates still halt (mock gates to return True for fast test)
- Verify simulated deliverable block removed

### E2E validation approach
- Unit tests with mocked transport (same pattern as existing tests)
- Integration test: Specialist app + Orchestrator app via httpx ASGITransport
- `make test` + `make lint` must pass after each PR

---

## PR body template (all 4 PRs)

Each PR follows `templates/TASK_EXECUTION_PROMPT.md`:
- Vibe Diff (3 parts: what changed, breakage points, risk assessment)
- Closes #N
- What changed (files → Component Map names → spec steps)
- Implementation details
- Verification steps
- Acceptance criteria (checked + how satisfied)
- Validation (.feature scenarios)
- Resource Usage (AgBOM audit)
- Out-of-scope findings

## Co-author trailer

```
Co-Authored-By: Sensei (GLM-5.2 via OpenCode) <noreply@aiweb3.school>
```
