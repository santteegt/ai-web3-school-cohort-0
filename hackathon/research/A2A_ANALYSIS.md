# A2A Protocol — Fit Analysis for GuildOS

> **Purpose:** Determine whether A2A v1.0 (with 0.3 compat) provides the message schema,
> agent discovery, and extensibility that GuildOS needs — or whether assumptions in the
> proposal don't hold.  
> **Created:** 2026-06-06  
> **Sources:** A2A GitHub repo · a2a-protocol.org v1.0.0 spec · a2a-python SDK README ·
> helloworld sample · cli host sample · direction-01 deep-dive

---

## TL;DR

A2A v1.0 **fits GuildOS well** as the agent-to-agent communication layer. It directly supports
task delegation, result return, agent capability discovery, streaming updates for long-running
tasks, and auth between agents. The two significant gaps are: (1) no native payment/budget field
in the core message schema — this must live in `Message.metadata` by convention; and (2) no
native deliverable-hash field — this belongs in `Artifact.metadata` or a structured artifact
part. Both gaps are bridgeable with thin conventions on top of the existing spec; neither
requires replacing A2A.

**One correction to the proposal:** The proposal targets "A2A 0.3.0" but the protocol is now at
**v1.0.0** (stable, under Linux Foundation, Python SDK published as `a2a-sdk` on PyPI). The
Python SDK includes 0.3 compat mode, so existing 0.3 messages will still route correctly, but
new builds should target v1.0 to avoid schema drift.

---

## Feature Coverage Matrix

| GuildOS Feature (from Proposal §5–6) | A2A Operation / Field | Status | Notes |
|---|---|---|---|
| Specialist discovers Orchestrator's mandate | `AgentCard` at `/.well-known/agent.json` | ✅ | AgentCard exposes `skills`, endpoint, capabilities. Mandate can go in a skill `description` or `metadata`. |
| Orchestrator sends structured task message to Specialist | `SendMessage` / `SendStreamingMessage` with `Message` | ✅ | `Message.parts` carries task description + input. `Message.metadata` carries payment reference, acceptance criteria, deadline. |
| Task carries payment intent reference | `Message.metadata` (open object) | ⚠️ | No native payment field. Must use `metadata` by convention: `{"guild_contract": "0x...", "payment_intent_id": "...", "budget_eth": "0.3"}`. |
| Task carries acceptance criteria | `Message.metadata` or `TextPart` in `parts` | ⚠️ | No native acceptance-criteria field. Use `metadata` key or encode as a `TextPart` in `parts`. |
| Long-running task execution with progress (GLM-5.1 loop) | `SendStreamingMessage` + SSE events (`TaskStatusUpdateEvent`) | ✅ | SSE streaming built into spec. Requires `AgentCard.capabilities.streaming = true`. |
| Specialist returns deliverable reference + hash | `Artifact` on task result | ⚠️ | Artifact has `parts` (content) and `metadata` (open object). No native `hash` field — put SHA-256 in `Artifact.metadata`. |
| Orchestrator receives result and presents to human | `Task.artifacts` + `Task.status` on completion | ✅ | Terminal state `TASK_STATE_COMPLETED` signals completion. Artifacts contain deliverable. |
| Task cancellation if human rejects | `CancelTask` → `TASK_STATE_CANCELED` | ✅ | Supported. `TASK_STATE_REJECTED` also available if agent declines. |
| Multi-step task lifecycle tracking | Task state machine: SUBMITTED → WORKING → COMPLETED/FAILED | ✅ | 9 distinct states cover all GuildOS flow stages. |
| Auth between Orchestrator and Specialist | `AgentCard.securitySchemes`: Bearer, API Key, OAuth2 | ✅ | Standard HTTP auth schemes. Bearer token is simplest for hackathon. |
| Agent capability manifest (what can Specialist do?) | `AgentCard.skills[]` with `id`, `description`, `input_modes`, `output_modes`, `tags` | ✅ | Well-structured. Capability matching (deferred feature) can query `skills` directly. |
| Session context across task turns | `contextId` on `Message` and `Task` | ✅ | `contextId` groups related messages/tasks into a session — maps to a guild session. |
| Push-based async result notification | `CreateTaskPushNotificationConfig` → webhook | ✅ | For async architecture where Orchestrator doesn't hold open a stream. |
| A2A message log for audit trail | Task `history` (array of `Message`) via `GetTask(historyLength=N)` | ✅ | Full message history retrievable per task. Demo can log each exchange. |

---

## Gaps and Alternatives

### Gap 1: No native payment intent field in Message or Task

**What GuildOS needs:** The A2A task message sent from Orchestrator to Specialist must carry a
reference to the guild treasury contract and the payment intent, so the A2A exchange and the
AgentFightClub settlement are traceable to the same task.

**What A2A provides:** `Message.metadata` — an open `object` (key/value) attached to any
message. `Task.metadata` — same on the task object.

**Delta:** One convention layer. The field is not in the spec, so any A2A client will silently
ignore it. That is fine for GuildOS — the Orchestrator and Specialist are both GuildOS agents
that know to read these keys.

**Proposed alternative / solution:**
```json
{
  "Message.metadata": {
    "guild_contract": "0x<AgentFightClub guild address>",
    "payment_intent_id": "<UUID matching the AgentFightClub proposal ID>",
    "budget_eth": "0.3",
    "deadline_unix": 1750000000
  }
}
```

This is the recommended approach. No replacement needed.

---

### Gap 2: No native deliverable hash field in Artifact

**What GuildOS needs:** The Specialist must return the SHA-256 hash of the deliverable in the
A2A result so the Orchestrator can verify it matches the on-chain committed hash before
presenting to the human.

**What A2A provides:** `Artifact.metadata` — open object. `Artifact.parts` — array of `Part`
(TextPart, FilePart, DataPart).

**Delta:** Thin convention. Two options:
- (A) Put the hash in `Artifact.metadata["sha256_hash"]` alongside the deliverable content
- (B) Return a structured `DataPart` (JSON) as the artifact's primary part, with `hash`,
  `deliverable_url`, and `guild_contract` fields

Option B (structured DataPart) is better for GuildOS because the Orchestrator can parse it
programmatically without inspecting `metadata`.

**Proposed solution:**
```json
{
  "parts": [{
    "data": {
      "deliverable_url": "ipfs://Qm...",
      "sha256_hash": "0xabc123...",
      "task_type": "security_audit",
      "guild_contract": "0x..."
    },
    "media_type": "application/json"
  }]
}
```

No replacement needed.

---

### Gap 3: Proposal targets "A2A 0.3.0" — actual current spec is v1.0.0

**What GuildOS needs:** A stable spec to build against.

**What A2A provides:** v1.0.0 (stable, under Linux Foundation), with the Python SDK publishing
compat mode for 0.3. Breaking changes from 0.3 → 1.0 include: field name casing alignment,
TaskState as proper enum (not string), `messageId` (not `id`) on Message, `supported_interfaces`
replacing `url`.

**Delta:** If you use the `a2a-sdk` Python library, the SDK handles compat automatically. If
building against raw JSON-RPC, target v1.0 schema.

**Proposed solution:** Build against v1.0.0 spec using `pip install a2a-sdk[http-server]`.
Update any internal docs that reference "0.3.0" to "1.0.0". The spec URL for reference:
https://a2a-protocol.org/v1.0.0/specification/

---

## Spec / API Stability Assessment

| Dimension | Assessment |
|---|---|
| **Version maturity** | v1.0.0 released and stable. Under Linux Foundation governance (not Google-only). |
| **SDK status** | Python `a2a-sdk` published on PyPI with CI/CD. Go, JS, Java, .NET SDKs also available. |
| **Spec versioning** | Semantic versioning with documented breaking-change appendix. v0.3 compat maintained in v1.0 SDK. |
| **Hackathon risk level** | **LOW.** A2A is the most stable component in the GuildOS stack — far more stable than AgentFightClub (alpha) or ERC-8004 (draft). |
| **Downtime risk** | A2A is self-hosted (you run the Specialist and Orchestrator servers). No dependency on an external service endpoint. |
| **Schema drift risk** | Low. v1.0 is a stable release. Pin `a2a-sdk==0.x.y` in requirements for deterministic builds. |

---

## Recommended Integration Path

**Use `a2a-sdk` v1.0 (Python) for both Orchestrator and Specialist agents.**

- Specialist: implement `AgentExecutor` interface, expose via FastAPI/Starlette ASGI server
- Orchestrator: use `A2ACardResolver` + `A2AClient` (or `create_client`) to discover and call Specialist
- Transport: JSON-RPC over HTTP (simplest for hackathon; gRPC available if latency becomes an issue)
- Streaming: enable SSE (`ClientConfig(streaming=True)`) for the GLM-5.1 execution loop — judges can watch real-time progress
- Auth: Bearer token between Orchestrator and Specialist (env var `A2A_CLI_BEARER_TOKEN` pattern from CLI host sample)

**Do NOT build a custom A2A message schema from scratch.** The reference implementation is complete
and the Python SDK removes all boilerplate. Estimated integration time: 0.5 days to stand up both
agents with A2A endpoints, 0.5 days to wire in GuildOS metadata conventions.

---

## Day 1 Test Checklist

Run these in order before building the rest of the stack. Each is a go/no-go gate.

1. **AgentCard fetch** — Start the Specialist server (`uv run .`), fetch the card at
   `http://localhost:9999/.well-known/agent.json`. Confirm `skills`, `capabilities.streaming`,
   and the endpoint are all present and match what was declared. Gate: card round-trips without
   error.

2. **SendMessage with metadata** — From the Orchestrator, send a `SendMessage` request with a
   `Message` containing GuildOS metadata fields (`guild_contract`, `payment_intent_id`,
   `budget_eth`). In the Specialist executor, print `context.message.metadata`. Gate: all keys
   present and values are exactly what was sent (no loss, no mutation).

3. **Artifact with structured DataPart** — Have the Specialist executor return an artifact whose
   primary part is `DataPart(data={"sha256_hash": "...", "deliverable_url": "..."})`. In the
   Orchestrator, read `task.artifacts[0].parts[0].data["sha256_hash"]`. Gate: hash value
   round-trips correctly.

4. **SSE streaming** — Send `SendStreamingMessage` with `ClientConfig(streaming=True)`. Confirm
   that `TaskStatusUpdateEvent` events arrive in order: `SUBMITTED → WORKING → COMPLETED`. Gate:
   all three state transitions observed in sequence with no dropped events.

5. **CancelTask** — Start a long-running task (sleep 5s in the executor), immediately call
   `CancelTask`. Confirm the task transitions to `TASK_STATE_CANCELED`. Gate: cancel is
   acknowledged and state reflects cancellation.

---

## Minimum Integration Sketch

The core GuildOS A2A interaction: Orchestrator delegates a task to Specialist and receives
the deliverable reference.

```python
# orchestrator.py — Delegate task to Specialist via A2A

import asyncio, uuid, json
import httpx
from a2a.client import A2ACardResolver, create_client, ClientConfig
from a2a.types import (
    Message, TextPart, Role, MessageSendParams, SendStreamingMessageRequest,
    Task, TaskStatusUpdateEvent, TaskArtifactUpdateEvent, JSONRPCErrorResponse,
)

SPECIALIST_URL = "http://localhost:9998"
GUILD_CONTRACT = "0xABCD..."
PAYMENT_INTENT_ID = "proposal-abc123"

async def delegate_task(task_description: str, input_data: str) -> dict:
    async with httpx.AsyncClient() as http:
        # 1. Discover Specialist Agent via AgentCard
        resolver = A2ACardResolver(http, SPECIALIST_URL)
        specialist_card = await resolver.get_agent_card()
        print(f"Specialist skills: {[s.id for s in specialist_card.skills]}")

        # 2. Build task message with GuildOS metadata convention
        guild_context_id = str(uuid.uuid4())
        message = Message(
            message_id=str(uuid.uuid4()),
            context_id=guild_context_id,         # ties all guild msgs together
            role=Role.ROLE_USER,
            parts=[
                TextPart(text=task_description),  # mandate + instructions
                TextPart(text=f"INPUT:\n{input_data}"),
            ],
            metadata={
                "guild_contract": GUILD_CONTRACT,
                "payment_intent_id": PAYMENT_INTENT_ID,
                "budget_eth": "0.3",
                "acceptance_criteria": json.dumps({
                    "no_critical_findings": True,
                    "owasp_checklist": True,
                }),
                "deadline_unix": 1750000000,
            }
        )

        # 3. Send with streaming (watch GLM-5.1 progress in real-time)
        client = await create_client(specialist_card, ClientConfig(streaming=True))
        request = SendStreamingMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(message=message),
        )

        deliverable = None
        async for event_wrapper in client.send_message(request):
            if isinstance(event_wrapper.root, JSONRPCErrorResponse):
                raise RuntimeError(event_wrapper.root.error)

            event = event_wrapper.root.result
            if isinstance(event, TaskStatusUpdateEvent):
                print(f"Task state: {event.status.state}")

            elif isinstance(event, TaskArtifactUpdateEvent):
                # 4. Extract deliverable hash from structured artifact
                for part in event.artifact.parts:
                    if hasattr(part, 'data'):
                        deliverable = part.data
                        print(f"Deliverable received: {deliverable}")

        await client.close()
        return deliverable  # {"sha256_hash": "...", "deliverable_url": "..."}


# specialist/agent_executor.py — Return structured deliverable

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.helpers import get_message_text, new_task_from_user_message, new_text_message
from a2a.types.a2a_pb2 import TaskState
from a2a.types import DataPart
import hashlib, json

class GuildOSSpecialistExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task or new_task_from_user_message(context.message)
        await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        await updater.update_status(TaskState.TASK_STATE_WORKING,
                                    new_text_message("Starting GLM-5.1 execution..."))

        # Extract GuildOS metadata from incoming message
        meta = context.message.metadata or {}
        guild_contract = meta.get("guild_contract")
        payment_intent = meta.get("payment_intent_id")

        # --- Run GLM-5.1 execution loop here ---
        task_text = get_message_text(context.message)
        deliverable_content = await run_glm_task(task_text)  # your GLM-5.1 call

        # Compute deliverable hash
        sha256 = hashlib.sha256(deliverable_content.encode()).hexdigest()

        # Return structured artifact (deliverable + hash)
        result_data = {
            "deliverable": deliverable_content,
            "sha256_hash": sha256,
            "guild_contract": guild_contract,
            "payment_intent_id": payment_intent,
        }
        await updater.add_artifact(
            parts=[DataPart(data=result_data, media_type="application/json")]
        )
        await updater.update_status(TaskState.TASK_STATE_COMPLETED,
                                    new_text_message("Deliverable committed."))

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError
```

---

## Alternatives Considered

| Gap | Primary (recommended) | Alternative |
|---|---|---|
| No payment field | `Message.metadata` convention | ERC-8183 task/payment envelope (too complex for hackathon scope) |
| No hash field | `Artifact.parts[0]` as `DataPart` | `Artifact.metadata["sha256_hash"]` (also valid; DataPart is more parseable) |
| A2A spec version | Use v1.0.0 (`a2a-sdk`) | Stay on 0.3 with compat mode (more schema drift risk) |
| A2A replaced entirely | — | Direct REST API between agents (loses discoverability and agent card spec; not recommended) |

---

## Open Questions

1. **`DataPart` availability in `a2a-sdk`:** The Python SDK's `DataPart` type was confirmed in
   the spec and CLI host code. Verify `from a2a.types import DataPart` resolves in the installed
   SDK version before building the Specialist executor.

2. **`contextId` as guild session ID:** The spec says `contextId` groups related messages and
   tasks. Test whether the Orchestrator and Specialist can use the same `contextId` (guild UUID)
   to group the entire guild session's task history under one `GetTask(historyLength=...)` call.

3. **A2A between processes on the same machine:** During the hackathon demo the Orchestrator and
   Specialist may run as separate Python processes on one machine. Confirm the A2A HTTP transport
   works on localhost with different ports. (Expected: yes — the helloworld sample runs exactly
   this way on port 9999.)

4. **AgentCard `skills` for mandate scope matching:** The Specialist's AgentCard `skills[].tags`
   can carry tags like `["security-audit", "solidity", "erc-20"]`. Verify the Orchestrator can
   filter by tag when selecting which agent to delegate to (relevant to post-hackathon capability
   matching).

---

*Built: 2026-06-06 | Agent: Sensei (Claude via Cowork)*  
*Sources: A2A v1.0.0 spec (a2a-protocol.org) · a2a-python SDK README · helloworld sample ·
cli host sample · PROJECT_PROPOSAL.md · PROTOTYPING_RESOURCES.md § 3 · directions/01-identity-capability.md § 12*
