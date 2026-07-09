"""Transport-layer tests for the A2A protocol implementation.

Three layers, each catching a different class of bug that mocking
``_send_to_agent`` cannot reach:

1. **Response extraction** (``_extract_response``) — pure-function unit
   tests that construct protobuf objects and verify the GuildOS payload
   is correctly parsed from both the ``message`` and ``task`` oneof arms.
   Would have caught the ``"response"`` vs ``"payload"`` oneof-name bug.

2. **Executor → EventQueue** — creates a real ``EventQueueLegacy``, calls
   ``SpecialistExecutor.execute()``, and drains the queue to verify the
   event types and content. Would have caught the ``enqueue`` vs
   ``enqueue_event`` and ``StreamResponse`` wrapping bugs.

3. **Integration smoke test** — full JSON-RPC round-trip through the
   FastAPI app via ``httpx.ASGITransport`` (no port binding). Exercises
   the entire stack: JSON-RPC dispatcher → request handler → executor →
   event queue → result aggregator → response serialization.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from a2a.server.agent_execution.context import RequestContext
from a2a.server.context import ServerCallContext
from a2a.server.events.event_queue import EventQueueLegacy
from a2a.types.a2a_pb2 import (
    ROLE_AGENT,
    ROLE_USER,
    TASK_STATE_CANCELED,
    TASK_STATE_COMPLETED,
    TASK_STATE_WORKING,
    Message,
    Part,
    SendMessageRequest,
    StreamResponse,
    Task,
    TaskStatus,
    TaskStatusUpdateEvent,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _guildos_json(payload: dict) -> str:
    """Serialize a GuildOS message dict to the JSON string carried in Part.text."""
    return json.dumps(payload)


def _build_request_context(msg_type: str, body: dict | None = None) -> RequestContext:
    """Build a minimal RequestContext carrying a GuildOS message."""
    payload = {"type": msg_type}
    if body:
        payload.update(body)
    message = Message(
        message_id="test-msg-id",
        role=ROLE_USER,
        parts=[Part(text=_guildos_json(payload))],
    )
    request = SendMessageRequest(message=message)
    return RequestContext(
        call_context=ServerCallContext(),
        request=request,
        task_id="test-task-id",
        context_id="test-context-id",
    )


async def _drain_queue(queue: EventQueueLegacy, expected: int, timeout: float = 2.0) -> list:
    """Drain *expected* events from the queue without hanging."""
    events: list = []
    for _ in range(expected):
        try:
            event = await asyncio.wait_for(queue.dequeue_event(), timeout=timeout)
            events.append(event)
            queue.task_done()
        except asyncio.TimeoutError:
            break
    await queue.close(immediate=True)
    return events


# ---------------------------------------------------------------------------
# Layer 1: _extract_response unit tests
# ---------------------------------------------------------------------------

class TestExtractResponse:
    """Test the pure-function response parser — no server, no client, no mocks."""

    def test_extract_message_oneof(self):
        from src.shared.a2a import _extract_response

        payload = {"type": "task/quote", "scope": "test", "estimated_cost_wei": 1000}
        msg = Message(
            message_id="msg-1",
            role=ROLE_AGENT,
            parts=[Part(text=json.dumps(payload))],
            task_id="task-1",
        )
        resp = StreamResponse(message=msg)

        result = _extract_response(resp)

        assert result["type"] == "task/quote"
        assert result["scope"] == "test"
        assert result["estimated_cost_wei"] == 1000
        assert result["message_id"] == "msg-1"
        assert result["task_id"] == "task-1"

    def test_extract_task_oneof_with_status_message(self):
        from src.shared.a2a import _extract_response

        payload = {"type": "task/delivered", "deliverable_hash": "sha256:abc"}
        inner_msg = Message(
            message_id="msg-2",
            role=ROLE_AGENT,
            parts=[Part(text=json.dumps(payload))],
        )
        task = Task(
            id="task-99",
            status=TaskStatus(
                state=TASK_STATE_COMPLETED,
                message=inner_msg,
            ),
        )
        resp = StreamResponse(task=task)

        result = _extract_response(resp)

        assert result["type"] == "task/delivered"
        assert result["deliverable_hash"] == "sha256:abc"
        assert result["message_id"] == "msg-2"
        assert result["task_id"] == "task-99"
        assert result["task_state"] == "TASK_STATE_COMPLETED"

    def test_extract_task_oneof_without_status_message(self):
        """A task with no status.message should still return task_id + task_state."""
        from src.shared.a2a import _extract_response

        task = Task(
            id="task-empty",
            status=TaskStatus(state=TASK_STATE_WORKING),
        )
        resp = StreamResponse(task=task)

        result = _extract_response(resp)

        assert result["task_id"] == "task-empty"
        assert result["task_state"] == "TASK_STATE_WORKING"
        assert "message_id" not in result

    def test_extract_empty_response(self):
        """A StreamResponse with neither oneof set returns an empty dict."""
        from src.shared.a2a import _extract_response

        resp = StreamResponse()
        result = _extract_response(resp)
        assert result == {}


# ---------------------------------------------------------------------------
# Layer 2: Executor → EventQueue transport unit tests
# ---------------------------------------------------------------------------

class TestSpecialistExecutorTransport:
    """Test SpecialistExecutor against a real EventQueueLegacy — no mocks."""

    @pytest.fixture
    def tmp_trace_dir(self, tmp_path, monkeypatch):
        import src.shared.a2a as a2a_mod
        monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
        return tmp_path

    @pytest.mark.asyncio
    async def test_execute_emits_working_then_completed(self, tmp_trace_dir):
        from src.specialist.agent import SpecialistExecutor

        executor = SpecialistExecutor()
        context = _build_request_context("task/invite", {"task_spec": {}})
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        assert len(events) == 2
        assert isinstance(events[0], TaskStatusUpdateEvent)
        assert events[0].status.state == TASK_STATE_WORKING
        assert isinstance(events[1], TaskStatusUpdateEvent)
        assert events[1].status.state == TASK_STATE_COMPLETED

    @pytest.mark.asyncio
    async def test_execute_completed_message_contains_quote(self, tmp_trace_dir):
        from src.specialist.agent import SpecialistExecutor

        executor = SpecialistExecutor()
        context = _build_request_context("task/invite", {"task_spec": {}})
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        completed = events[1]
        assert completed.status.HasField("message")
        text = completed.status.message.parts[0].text
        payload = json.loads(text)

        assert payload["type"] == "task/quote"
        assert "scope" in payload
        assert "estimated_cost_wei" in payload
        assert "deadline_iso" in payload

    @pytest.mark.asyncio
    async def test_execute_emits_no_streamresponse(self, tmp_trace_dir):
        """Regression guard: StreamResponse is not a valid queue event type."""
        from src.specialist.agent import SpecialistExecutor

        executor = SpecialistExecutor()
        context = _build_request_context("task/invite", {"task_spec": {}})
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        for event in events:
            assert not isinstance(event, StreamResponse)

    @pytest.mark.asyncio
    async def test_cancel_emits_canceled_status(self, tmp_trace_dir):
        from src.specialist.agent import SpecialistExecutor

        executor = SpecialistExecutor()
        context = _build_request_context("task/invite")
        queue = EventQueueLegacy()

        await executor.cancel(context, queue)
        events = await _drain_queue(queue, expected=1)

        assert len(events) == 1
        assert isinstance(events[0], TaskStatusUpdateEvent)
        assert events[0].status.state == TASK_STATE_CANCELED

    @pytest.mark.asyncio
    async def test_execute_unknown_type_emits_completed_with_error(self, tmp_trace_dir):
        """An unknown message type should still complete (not hang)."""
        from src.specialist.agent import SpecialistExecutor

        executor = SpecialistExecutor()
        context = _build_request_context("unknown/type")
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        assert events[1].status.state == TASK_STATE_COMPLETED
        text = events[1].status.message.parts[0].text
        payload = json.loads(text)
        assert payload["type"] == "error"


# ---------------------------------------------------------------------------
# Layer 3: Full JSON-RPC integration smoke test
# ---------------------------------------------------------------------------

def _build_specialist_app():
    """Build the Specialist FastAPI app without starting uvicorn."""
    from a2a.server.request_handlers.default_request_handler import (
        LegacyRequestHandler,
    )
    from a2a.server.routes.agent_card_routes import create_agent_card_routes
    from a2a.server.routes.fastapi_routes import add_a2a_routes_to_fastapi
    from a2a.server.routes.jsonrpc_routes import create_jsonrpc_routes
    from a2a.server.routes.rest_routes import create_rest_routes
    from a2a.server.tasks.inmemory_task_store import InMemoryTaskStore
    from a2a.utils.constants import DEFAULT_RPC_URL
    from fastapi import FastAPI
    from src.specialist.agent import AGENT_CARD, SpecialistExecutor

    task_store = InMemoryTaskStore()
    executor = SpecialistExecutor()
    handler = LegacyRequestHandler(
        agent_executor=executor,
        task_store=task_store,
        agent_card=AGENT_CARD,
    )
    app = FastAPI(title="GuildOS Specialist Agent (test)")
    add_a2a_routes_to_fastapi(
        app,
        agent_card_routes=create_agent_card_routes(AGENT_CARD),
        jsonrpc_routes=create_jsonrpc_routes(handler, rpc_url=DEFAULT_RPC_URL),
        rest_routes=create_rest_routes(handler),
    )
    return app, task_store


class TestSpecialistA2AIntegration:
    """Full JSON-RPC round-trip via httpx ASGI transport — no port binding."""

    @pytest.fixture
    def tmp_trace_dir(self, tmp_path, monkeypatch):
        import src.shared.a2a as a2a_mod
        monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
        return tmp_path

    @pytest.mark.asyncio
    async def test_agent_card_served_at_well_known(self, tmp_trace_dir):
        app, _ = _build_specialist_app()

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/.well-known/agent-card.json")

        assert response.status_code == 200
        card = response.json()
        assert card["name"] == "GuildOS Specialist Agent"
        assert "supportedInterfaces" in card
        assert len(card["supportedInterfaces"]) >= 1

    @pytest.mark.asyncio
    async def test_send_message_returns_completed_task_with_quote(self, tmp_trace_dir):
        app, _ = _build_specialist_app()
        invite_json = json.dumps({"type": "task/invite", "task_spec": {}})

        rpc_request = {
            "jsonrpc": "2.0",
            "id": "int-1",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": "msg-int-1",
                    "role": "ROLE_USER",
                    "parts": [{"text": invite_json}],
                }
            },
        }

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/",
                json=rpc_request,
                headers={"A2A-Version": "1.0"},
            )

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "error" not in data

        task_data = data["result"]["task"]
        assert task_data["status"]["state"] == "TASK_STATE_COMPLETED"

        quote_text = task_data["status"]["message"]["parts"][0]["text"]
        quote = json.loads(quote_text)
        assert quote["type"] == "task/quote"
        assert "estimated_cost_wei" in quote

    @pytest.mark.asyncio
    async def test_get_task_returns_persisted_task(self, tmp_trace_dir):
        app, _ = _build_specialist_app()
        invite_json = json.dumps({"type": "task/invite", "task_spec": {}})

        send_request = {
            "jsonrpc": "2.0",
            "id": "send-1",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": "msg-persist-1",
                    "role": "ROLE_USER",
                    "parts": [{"text": invite_json}],
                }
            },
        }

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            send_resp = await client.post(
                "/",
                json=send_request,
                headers={"A2A-Version": "1.0"},
            )
            task_id = send_resp.json()["result"]["task"]["id"]

            get_request = {
                "jsonrpc": "2.0",
                "id": "get-1",
                "method": "GetTask",
                "params": {"id": task_id},
            }
            get_resp = await client.post(
                "/",
                json=get_request,
                headers={"A2A-Version": "1.0"},
            )

        assert get_resp.status_code == 200
        get_data = get_resp.json()
        assert "result" in get_data
        task = get_data["result"]
        assert task["id"] == task_id
        assert task["status"]["state"] == "TASK_STATE_COMPLETED"
