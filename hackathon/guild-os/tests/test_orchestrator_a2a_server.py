"""Tests for OrchestratorA2AServer — Issue #36.

Three layers, matching the test_a2a_transport.py pattern:

1. **Executor → EventQueue** — real EventQueueLegacy, verify event types and
   content for each message type (task/delivered, feedback/request, unknown).
2. **Full JSON-RPC integration** — httpx ASGITransport (no port binding).
3. **Agent Card** served at /.well-known/agent-card.json.

Maps to specs/scenarios/07_deliverable_attestation.feature →
"Orchestrator's A2A server receives the proactive task/delivered" and
specs/scenarios/10_reputation_feedback.feature →
"Orchestrator's A2A server receives the proactive feedback/request".
"""

from __future__ import annotations

import asyncio
import hashlib
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
    ROLE_USER,
    TASK_STATE_CANCELED,
    TASK_STATE_COMPLETED,
    TASK_STATE_WORKING,
    Message,
    Part,
    SendMessageRequest,
    StreamResponse,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _guildos_json(payload: dict) -> str:
    return json.dumps(payload)


def _build_request_context(
    msg_type: str, body: dict | None = None
) -> RequestContext:
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


async def _drain_queue(
    queue: EventQueueLegacy, expected: int, timeout: float = 2.0
) -> list:
    events: list = []
    for _ in range(expected):
        try:
            event = await asyncio.wait_for(
                queue.dequeue_event(), timeout=timeout
            )
            events.append(event)
            queue.task_done()
        except asyncio.TimeoutError:
            break
    await queue.close(immediate=True)
    return events


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod
    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


def _build_orchestrator_app():
    from src.orchestrator.a2a_server import create_orchestrator_app
    return create_orchestrator_app()


# ---------------------------------------------------------------------------
# Layer 1: Executor → EventQueue unit tests
# ---------------------------------------------------------------------------

class TestOrchestratorExecutorTransport:
    @pytest.mark.asyncio
    async def test_delivered_emits_working_then_completed(
        self, tmp_trace_dir, tmp_path
    ):
        from src.orchestrator.a2a_server import OrchestratorExecutor

        content = b'{"output": "test deliverable"}'
        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        executor = OrchestratorExecutor()
        context = _build_request_context(
            "task/delivered",
            {
                "task_id": "task-1",
                "deliverable_reference": str(deliv_file),
                "deliverable_hash": expected_hash,
                "attestation_uid": "0xabc",
                "attestation_url": "https://base.easscan.org/attestation/0xabc",
            },
        )
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        assert len(events) == 2
        assert events[0].status.state == TASK_STATE_WORKING
        assert events[1].status.state == TASK_STATE_COMPLETED

        text = events[1].status.message.parts[0].text
        payload = json.loads(text)
        assert payload["type"] == "deliverable_review"
        assert payload["pre_check"]["hash_match"] is True
        assert payload["pre_check"]["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_delivered_with_missing_hash_rejected(
        self, tmp_trace_dir
    ):
        from src.orchestrator.a2a_server import OrchestratorExecutor

        executor = OrchestratorExecutor()
        context = _build_request_context(
            "task/delivered",
            {"task_id": "task-no-hash"},
        )
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        text = events[1].status.message.parts[0].text
        payload = json.loads(text)
        assert payload["status"] == "rejected"
        assert "missing deliverable_hash" in payload["reason"]

    @pytest.mark.asyncio
    async def test_feedback_request_emits_completed_with_stub(
        self, tmp_trace_dir
    ):
        from src.orchestrator.a2a_server import OrchestratorExecutor

        executor = OrchestratorExecutor()
        context = _build_request_context(
            "feedback/request",
            {"task_id": "task-2", "deliverable_hash": "sha256:xyz"},
        )
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        assert events[1].status.state == TASK_STATE_COMPLETED
        text = events[1].status.message.parts[0].text
        payload = json.loads(text)
        assert payload["type"] == "reputation_propose"
        assert payload["status"] == "stubbed"

    @pytest.mark.asyncio
    async def test_unknown_type_rejected(self, tmp_trace_dir):
        from src.orchestrator.a2a_server import OrchestratorExecutor

        executor = OrchestratorExecutor()
        context = _build_request_context("malicious/spoof")
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        assert events[1].status.state == TASK_STATE_COMPLETED
        text = events[1].status.message.parts[0].text
        payload = json.loads(text)
        assert payload["type"] == "error"
        assert "Unrecognized message type" in payload["message"]

    @pytest.mark.asyncio
    async def test_cancel_emits_canceled(self, tmp_trace_dir):
        from src.orchestrator.a2a_server import OrchestratorExecutor

        executor = OrchestratorExecutor()
        context = _build_request_context("task/delivered")
        queue = EventQueueLegacy()

        await executor.cancel(context, queue)
        events = await _drain_queue(queue, expected=1)

        assert events[0].status.state == TASK_STATE_CANCELED

    @pytest.mark.asyncio
    async def test_no_streamresponse_in_events(self, tmp_trace_dir, tmp_path):
        from src.orchestrator.a2a_server import OrchestratorExecutor

        content = b'{"output": "test"}'
        deliv_file = tmp_path / "d.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        executor = OrchestratorExecutor()
        context = _build_request_context(
            "task/delivered",
            {
                "deliverable_reference": str(deliv_file),
                "deliverable_hash": expected_hash,
            },
        )
        queue = EventQueueLegacy()

        await executor.execute(context, queue)
        events = await _drain_queue(queue, expected=2)

        for event in events:
            assert not isinstance(event, StreamResponse)


# ---------------------------------------------------------------------------
# Layer 2: Full JSON-RPC integration via httpx ASGITransport
# ---------------------------------------------------------------------------

class TestOrchestratorA2AIntegration:
    @pytest.fixture
    def tmp_trace_dir(self, tmp_path, monkeypatch):
        import src.shared.a2a as a2a_mod
        monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
        return tmp_path

    @pytest.mark.asyncio
    async def test_agent_card_served_at_well_known(self, tmp_trace_dir):
        app, _ = _build_orchestrator_app()

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/.well-known/agent-card.json")

        assert response.status_code == 200
        card = response.json()
        assert card["name"] == "GuildOS Orchestrator Agent"
        assert len(card["supportedInterfaces"]) >= 1

    @pytest.mark.asyncio
    async def test_send_delivered_returns_completed_with_precheck(
        self, tmp_trace_dir, tmp_path
    ):
        app, _ = _build_orchestrator_app()

        content = b'{"output": "deliverable"}'
        deliv_file = tmp_path / "delivered.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        delivered_json = json.dumps({
            "type": "task/delivered",
            "task_id": "task-int-1",
            "deliverable_reference": str(deliv_file),
            "deliverable_hash": expected_hash,
            "attestation_uid": "0xdef",
            "attestation_url": "https://base.easscan.org/attestation/0xdef",
        })

        rpc_request = {
            "jsonrpc": "2.0",
            "id": "int-1",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": "msg-int-1",
                    "role": "ROLE_USER",
                    "parts": [{"text": delivered_json}],
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

        result_text = task_data["status"]["message"]["parts"][0]["text"]
        result = json.loads(result_text)
        assert result["type"] == "deliverable_review"
        assert result["pre_check"]["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_send_feedback_request_returns_completed_with_stub(
        self, tmp_trace_dir
    ):
        app, _ = _build_orchestrator_app()

        feedback_json = json.dumps({
            "type": "feedback/request",
            "task_id": "task-int-2",
            "deliverable_hash": "sha256:abc",
        })

        rpc_request = {
            "jsonrpc": "2.0",
            "id": "int-2",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": "msg-int-2",
                    "role": "ROLE_USER",
                    "parts": [{"text": feedback_json}],
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

        task_data = data["result"]["task"]
        assert task_data["status"]["state"] == "TASK_STATE_COMPLETED"

        result_text = task_data["status"]["message"]["parts"][0]["text"]
        result = json.loads(result_text)
        assert result["type"] == "reputation_propose"
        assert result["status"] == "stubbed"

    @pytest.mark.asyncio
    async def test_unknown_message_rejected(self, tmp_trace_dir):
        app, _ = _build_orchestrator_app()

        unknown_json = json.dumps({"type": "task/spoof"})

        rpc_request = {
            "jsonrpc": "2.0",
            "id": "int-3",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": "msg-int-3",
                    "role": "ROLE_USER",
                    "parts": [{"text": unknown_json}],
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
        task_data = data["result"]["task"]
        result_text = task_data["status"]["message"]["parts"][0]["text"]
        result = json.loads(result_text)
        assert result["type"] == "error"

    @pytest.mark.asyncio
    async def test_get_task_returns_persisted_result(self, tmp_trace_dir):
        app, _ = _build_orchestrator_app()

        feedback_json = json.dumps({
            "type": "feedback/request",
            "task_id": "task-persist",
            "deliverable_hash": "sha256:persist",
        })

        send_request = {
            "jsonrpc": "2.0",
            "id": "send-persist",
            "method": "SendMessage",
            "params": {
                "message": {
                    "messageId": "msg-persist",
                    "role": "ROLE_USER",
                    "parts": [{"text": feedback_json}],
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
                "id": "get-persist",
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


# ---------------------------------------------------------------------------
# Agent Card transport declarations
# ---------------------------------------------------------------------------

class TestOrchestratorAgentCard:
    def test_agent_card_declares_jsonrpc_interface(self):
        from a2a.utils.constants import (
            PROTOCOL_VERSION_1_0,
            TransportProtocol,
        )
        from src.orchestrator.a2a_server import (
            AGENT_CARD,
            ORCHESTRATOR_BASE_URL,
        )

        assert len(AGENT_CARD.supported_interfaces) > 0
        jsonrpc_interfaces = [
            i for i in AGENT_CARD.supported_interfaces
            if i.protocol_binding == TransportProtocol.JSONRPC
        ]
        assert len(jsonrpc_interfaces) == 1
        interface = jsonrpc_interfaces[0]
        assert interface.url.startswith(ORCHESTRATOR_BASE_URL)
        assert interface.protocol_version == PROTOCOL_VERSION_1_0

    def test_port_is_10000_by_default(self):
        from src.orchestrator.a2a_server import ORCHESTRATOR_PORT

        assert ORCHESTRATOR_PORT == 10000
