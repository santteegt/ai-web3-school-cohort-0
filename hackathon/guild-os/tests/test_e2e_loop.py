"""E2E integration test — validates the full A2A coordination loop.

Exercises the real A2A transport (JSON-RPC over httpx ASGITransport)
against both the Specialist and Orchestrator servers — no port binding,
no mocked _send_to_agent. This is the definitive proof that the #36-#39
transport plumbing (real JSON-RPC wire format, both agent cards, both
servers) works end-to-end.

Loop validated:
  1. send_invite (JSON-RPC) → Specialist returns quote (sync)
  2. send_task (JSON-RPC, return_immediately) → Specialist returns WORKING
  3. poll_task (JSON-RPC tasks/get) → returns COMPLETED with deliverable
  4. proactive push: SpecialistA2AClient → OrchestratorA2AServer (JSON-RPC)

Caveat: SpecialistExecutor.execute() (src/specialist/agent.py) still
completes every task synchronously in one call — WORKING then COMPLETED
before the JSON-RPC response even returns. So step 3's poll exercises the
real GetTask retrieval path, not a genuine in-progress-then-complete race;
there's no window where the harness is still working when the poll fires.
That gap is the harness work engine itself (open #40/#10), not yet built —
see tests/step_defs/test_task_delegation_steps.py's docstring for the same
caveat on the matching 05_task_delegation.feature scenario.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod
    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


def _build_specialist_app():
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
        agent_executor=executor, task_store=task_store, agent_card=AGENT_CARD
    )
    app = FastAPI(title="Specialist (E2E test)")
    add_a2a_routes_to_fastapi(
        app,
        agent_card_routes=create_agent_card_routes(AGENT_CARD),
        jsonrpc_routes=create_jsonrpc_routes(handler, rpc_url=DEFAULT_RPC_URL),
        rest_routes=create_rest_routes(handler),
    )
    return app, task_store


def _build_orchestrator_app():
    from src.orchestrator.a2a_server import create_orchestrator_app
    return create_orchestrator_app()


async def _jsonrpc_send(client: httpx.AsyncClient, method: str, params: dict, req_id: str = "1"):
    """Send a JSON-RPC request and return the parsed result."""
    response = await client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params,
        },
        headers={"A2A-Version": "1.0"},
    )
    assert response.status_code == 200
    return response.json()


class TestE2ECoordinationLoop:
    """Full loop: invite → quote → send → poll → delivered → proactive push."""

    @pytest.fixture
    def tmp_trace_dir(self, tmp_path, monkeypatch):
        import src.shared.a2a as a2a_mod
        monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
        return tmp_path

    @pytest.mark.asyncio
    async def test_full_invite_send_poll_loop(self, tmp_trace_dir, tmp_path):
        """Steps 4-9 of the 15-step loop via real JSON-RPC transport.

        The poll (step 8-9) retrieves an already-COMPLETED task — see the
        module docstring's caveat, the harness that would make this a real
        in-progress race doesn't exist yet (#40/#10).
        """
        app, task_store = _build_specialist_app()

        invite_json = json.dumps({"type": "task/invite", "task_spec": {"task_description": "E2E test"}})

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Step 4: send_invite → get quote back
            data = await _jsonrpc_send(
                client,
                "SendMessage",
                {"message": {"messageId": "msg-1", "role": "ROLE_USER", "parts": [{"text": invite_json}]}},
                req_id="invite",
            )
            assert "result" in data
            task_data = data["result"]["task"]
            assert task_data["status"]["state"] == "TASK_STATE_COMPLETED"
            quote = json.loads(task_data["status"]["message"]["parts"][0]["text"])
            assert quote["type"] == "task/quote"
            assert "estimated_cost_wei" in quote

            # Step 6: send_task → get WORKING or COMPLETED
            task_payload = {
                "task_id": "e2e-task-1",
                "task_description": "E2E test task",
                "github_issue_url": "https://github.com/test/repo/issues/1",
                "acceptance_criteria": ["Deliverable is non-empty"],
                "deliverable_format": "github_commit",
                "orchestrator_endpoint": "http://localhost:10000",
            }
            send_json = json.dumps({"type": "task/send", "task": task_payload})
            data = await _jsonrpc_send(
                client,
                "SendMessage",
                {"message": {"messageId": "msg-2", "role": "ROLE_USER", "parts": [{"text": send_json}]}},
                req_id="send",
            )
            assert "result" in data
            task_data = data["result"]["task"]
            task_id = task_data["id"]

            # Step 8-9: poll_task → get COMPLETED with deliverable
            data = await _jsonrpc_send(
                client, "GetTask", {"id": task_id}, req_id="poll"
            )
            assert "result" in data
            task = data["result"]
            assert task["status"]["state"] == "TASK_STATE_COMPLETED"

            delivered = json.loads(task["status"]["message"]["parts"][0]["text"])
            assert delivered["type"] == "task/delivered"
            assert delivered["deliverable_hash"].startswith("sha256:")

    @pytest.mark.asyncio
    async def test_proactive_push_to_orchestrator(self, tmp_trace_dir, tmp_path):
        """SpecialistA2AClient → OrchestratorA2AServer via JSON-RPC."""
        app, _ = _build_orchestrator_app()

        content = b'{"output": "e2e deliverable"}'
        deliv_file = tmp_path / "e2e_deliverable.json"
        deliv_file.write_bytes(content)
        import hashlib
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        delivered_json = json.dumps({
            "type": "task/delivered",
            "task_id": "e2e-task-2",
            "deliverable_reference": str(deliv_file),
            "deliverable_hash": expected_hash,
            "attestation_uid": "0xe2e",
            "attestation_url": "https://base.easscan.org/attestation/0xe2e",
        })

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            # Simulate what SpecialistA2AClient.send_delivered does at the wire level
            data = await _jsonrpc_send(
                client,
                "SendMessage",
                {"message": {"messageId": "msg-proactive", "role": "ROLE_USER", "parts": [{"text": delivered_json}]}},
                req_id="delivered",
            )

            assert "result" in data
            task_data = data["result"]["task"]
            assert task_data["status"]["state"] == "TASK_STATE_COMPLETED"

            result = json.loads(task_data["status"]["message"]["parts"][0]["text"])
            assert result["type"] == "deliverable_review"
            assert result["pre_check"]["hash_match"] is True
            assert result["pre_check"]["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_feedback_request_to_orchestrator(self, tmp_trace_dir):
        """Proactive feedback/request → OrchestratorA2AServer stubs reputation_propose."""
        app, _ = _build_orchestrator_app()

        feedback_json = json.dumps({
            "type": "feedback/request",
            "task_id": "e2e-task-3",
            "deliverable_hash": "sha256:e2e",
        })

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            data = await _jsonrpc_send(
                client,
                "SendMessage",
                {"message": {"messageId": "msg-fb", "role": "ROLE_USER", "parts": [{"text": feedback_json}]}},
                req_id="feedback",
            )

            assert "result" in data
            task_data = data["result"]["task"]
            assert task_data["status"]["state"] == "TASK_STATE_COMPLETED"

            result = json.loads(task_data["status"]["message"]["parts"][0]["text"])
            assert result["type"] == "reputation_propose"
            assert result["status"] == "stubbed"

    @pytest.mark.asyncio
    async def test_both_agent_cards_served(self, tmp_trace_dir):
        """Both agents publish their Agent Card at /.well-known/agent-card.json."""
        specialist_app, _ = _build_specialist_app()
        orchestrator_app, _ = _build_orchestrator_app()

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=specialist_app), base_url="http://test"
        ) as s_client, httpx.AsyncClient(
            transport=httpx.ASGITransport(app=orchestrator_app), base_url="http://test"
        ) as o_client:
            s_card = (await s_client.get("/.well-known/agent-card.json")).json()
            o_card = (await o_client.get("/.well-known/agent-card.json")).json()

            assert s_card["name"] == "GuildOS Specialist Agent"
            assert o_card["name"] == "GuildOS Orchestrator Agent"
            assert len(s_card["supportedInterfaces"]) >= 1
            assert len(o_card["supportedInterfaces"]) >= 1
