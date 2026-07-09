"""Tests for A2A full task flow — Issue #9.

Tests cover:
- A2AClient message sending (mocked transport)
- SpecialistAgent handlers (invite, task, accepted)
- OrchestratorTools A2A wiring (task_invite, task_delegate)
- Trace logging to a2a_trace_{date}.json
- Deliverable review pre-check
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    """Redirect A2A trace logs to a temp directory."""
    import src.shared.a2a as a2a_mod
    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def sample_task_spec():
    return {
        "task_description": "Write a Python function that computes SHA-256",
        "task_type": "code-generation",
        "acceptance_criteria": ["Function works", "Returns hex digest"],
        "deadline": "2026-06-13T23:59:00Z",
        "budget_wei": 1000000000000000,
    }


@pytest.fixture
def sample_quote():
    return {
        "type": "task/quote",
        "scope": "Full task execution with GLM-5.1 long-horizon planning",
        "estimated_cost_wei": 1000000000000000,
        "deadline_iso": "2026-06-13T23:59:00Z",
    }


# ---------------------------------------------------------------------------
# Trace logging tests
# ---------------------------------------------------------------------------

class TestTraceLogging:
    def test_log_message_creates_file(self, tmp_trace_dir):
        from src.shared.a2a import _log_message

        _log_message("outgoing", "task/invite", {"task_id": "abc123"})

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        assert trace_file.exists()

        entries = json.loads(trace_file.read_text())
        assert len(entries) == 1
        assert entries[0]["direction"] == "outgoing"
        assert entries[0]["type"] == "task/invite"
        assert entries[0]["payload"]["task_id"] == "abc123"
        assert "timestamp" in entries[0]

    def test_log_message_appends(self, tmp_trace_dir):
        from src.shared.a2a import _log_message

        _log_message("outgoing", "task/invite", {"task_id": "1"})
        _log_message("incoming", "task/quote", {"task_id": "1", "scope": "test"})

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert len(entries) == 2
        assert entries[0]["type"] == "task/invite"
        assert entries[1]["type"] == "task/quote"

    def test_trace_contains_all_7_events(self, tmp_trace_dir):
        """Simulate the full 7-event A2A trace (5 messages + 2 internal)."""
        from src.shared.a2a import _log_message

        _log_message("outgoing", "task/invite", {"task_id": "t1"})
        _log_message("incoming", "task/quote", {"task_id": "t1"})
        _log_message("outgoing", "task/send", {"task_id": "t1"})
        _log_message("incoming", "task/delivered", {"task_id": "t1"})
        _log_message("internal", "gate_2_check", {"task_id": "t1"})
        _log_message("outgoing", "task/accepted", {"task_id": "t1"})
        _log_message("internal", "flow_complete", {"task_id": "t1"})

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert len(entries) == 7


# ---------------------------------------------------------------------------
# SpecialistAgent handler tests
# ---------------------------------------------------------------------------

class TestSpecialistHandlers:
    @pytest.mark.asyncio
    async def test_handle_task_invite_returns_quote(self):
        from src.specialist.agent import handle_task_invite

        result = await handle_task_invite({"type": "task/invite", "task_spec": {}})

        assert result["type"] == "task/quote"
        assert "scope" in result
        assert "estimated_cost_wei" in result
        assert "deadline_iso" in result
        assert result["estimated_cost_wei"] > 0

    @pytest.mark.asyncio
    async def test_handle_task_send_returns_delivered(self):
        from src.specialist.agent import handle_task_send

        result = await handle_task_send({
            "type": "task/send",
            "task_id": "test-123",
            "task": {"task_description": "Write a SHA-256 function"},
        })

        assert result["type"] == "task/delivered"
        assert result["task_id"] == "test-123"
        assert result["deliverable_hash"].startswith("sha256:")
        assert result["deliverable_reference"]
        assert len(result["deliverable_hash"]) == 71  # "sha256:" + 64 hex chars

    @pytest.mark.asyncio
    async def test_deliverable_hash_is_valid_sha256(self):
        from src.specialist.agent import handle_task_send

        result = await handle_task_send({
            "type": "task/send",
            "task_id": "hash-test",
            "task": {"task_description": "test"},
        })

        hex_digest = result["deliverable_hash"].replace("sha256:", "")
        assert len(hex_digest) == 64
        # Must be valid hex
        int(hex_digest, 16)


# ---------------------------------------------------------------------------
# Specialist AGENT_CARD transport declaration
# ---------------------------------------------------------------------------

class TestAgentCardTransport:
    """AGENT_CARD must declare supported_interfaces or a2a.client.client_factory.
    ClientFactory.create() raises 'no compatible transports found' regardless
    of message content, since it has nothing to match its client_set against.
    """

    def test_agent_card_declares_a_jsonrpc_interface(self):
        from a2a.utils.constants import PROTOCOL_VERSION_1_0, TransportProtocol
        from src.specialist.agent import AGENT_CARD, SPECIALIST_BASE_URL

        assert len(AGENT_CARD.supported_interfaces) > 0
        jsonrpc_interfaces = [
            i for i in AGENT_CARD.supported_interfaces
            if i.protocol_binding == TransportProtocol.JSONRPC
        ]
        assert len(jsonrpc_interfaces) == 1
        interface = jsonrpc_interfaces[0]
        assert interface.url.startswith(SPECIALIST_BASE_URL)
        assert interface.protocol_version == PROTOCOL_VERSION_1_0


# ---------------------------------------------------------------------------
# OrchestratorTools tests (A2A-wired tools)
# ---------------------------------------------------------------------------

class TestOrchestratorTools:
    @pytest.mark.asyncio
    async def test_task_invite_calls_send_invite(self, tmp_trace_dir):
        """task_invite tool should call A2AClient.send_invite and return message ID."""
        from src.orchestrator import tools

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_invite = AsyncMock(return_value="msg-invite-123")
            result = await tools.task_invite(
                "http://localhost:10001",
                {"task_description": "test task"},
            )
            assert result == "msg-invite-123"
            mock_a2a.send_invite.assert_called_once_with(
                "http://localhost:10001",
                {"task_description": "test task"},
            )

    @pytest.mark.asyncio
    async def test_task_delegate_calls_send_task(self, tmp_trace_dir):
        """task_delegate tool should call A2AClient.send_task and update guild_context."""
        from src.orchestrator import tools

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a, \
             patch("src.orchestrator.tools.guild_context") as mock_ctx:
            mock_a2a.send_task = AsyncMock(return_value="msg-delegate-456")
            mock_ctx.update.return_value = {"a2a_task_id": "msg-delegate-456"}

            result = await tools.task_delegate(
                "http://localhost:10001",
                {
                    "task_description": "full task",
                    "github_issue_url": "https://github.com/santteegt/ai-web3-school-cohort-0/issues/10",
                    "acceptance_criteria": ["Deliverable file is non-empty"],
                    "deliverable_format": "github_commit",
                },
            )
            assert result == "msg-delegate-456"
            mock_a2a.send_task.assert_called_once()
            mock_ctx.update.assert_called_once_with(a2a_task_id="msg-delegate-456")

    @pytest.mark.asyncio
    async def test_talent_query_returns_profile(self):
        from src.orchestrator import tools

        result = await tools.talent_query("code-generation")
        assert isinstance(result, list)
        assert len(result) >= 1
        assert "name" in result[0]

    @pytest.mark.asyncio
    async def test_deliverable_review_passes_valid(self, tmp_path):
        from src.orchestrator import tools

        # Create a test deliverable file
        content = b'{"output": "test deliverable"}'
        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        result = await tools.deliverable_review(str(deliv_file), expected_hash)

        assert result["hash_match"] is True
        assert result["format_valid"] is True
        assert result["size_check"] is True
        assert result["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_deliverable_review_fails_hash_mismatch(self, tmp_path):
        from src.orchestrator import tools

        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(b"test content")

        result = await tools.deliverable_review(str(deliv_file), "sha256:badhash")

        assert result["hash_match"] is False
        assert result["evaluator_verdict"] == "FAIL"


# ---------------------------------------------------------------------------
# A2AClient transport tests (mocked)
# ---------------------------------------------------------------------------

class TestA2AClient:
    @pytest.mark.asyncio
    async def test_send_invite_builds_correct_message(self, tmp_trace_dir):
        from src.shared.a2a import send_invite

        mock_response = {
            "type": "task/quote",
            "scope": "test",
            "estimated_cost_wei": 1000,
        }

        with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
            mock_send.return_value = mock_response
            msg_id = await send_invite("http://localhost:10001", {"task": "test"})

            assert msg_id  # non-empty message ID
            mock_send.assert_called_once()

            # Verify trace was logged
            trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
            entries = json.loads(trace_file.read_text())
            assert any(e["type"] == "task/invite" for e in entries)
            assert any(e["type"] == "task/quote" for e in entries)

    @pytest.mark.asyncio
    async def test_send_task_builds_correct_message(self, tmp_trace_dir):
        from src.shared.a2a import send_task

        mock_response = {
            "type": "task/delivered",
            "deliverable_hash": "sha256:abc123",
        }

        with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
            mock_send.return_value = mock_response
            msg_id = await send_task("http://localhost:10001", {"task_description": "test"})

            assert msg_id
            mock_send.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_accepted_sends_message(self, tmp_trace_dir):
        from src.shared.a2a import send_accepted

        with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
            mock_send.return_value = {}
            await send_accepted("http://localhost:10001", "task-xyz")

            mock_send.assert_called_once()

            trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
            entries = json.loads(trace_file.read_text())
            assert any(e["type"] == "task/accepted" for e in entries)


# ---------------------------------------------------------------------------
# GuildContext tests
# ---------------------------------------------------------------------------

class TestGuildContext:
    def test_update_preserves_fields(self, tmp_path, monkeypatch):
        from src.shared import guild_context

        # Redirect to temp file
        ctx_file = tmp_path / "guild_context.json"
        ctx_file.write_text(json.dumps({
            "guild_address": None,
            "mandate": None,
            "treasury_wei": "0",
            "member_list": [],
            "task_state": "INIT",
            "proposal_id": None,
            "a2a_task_id": None,
            "deliverable_hash": None,
            "deliverable_tx": None,
            "settlement_tx": None,
            "reputation_tx": None,
        }))
        monkeypatch.setattr(guild_context, "CONTEXT_PATH", ctx_file)

        ctx = guild_context.update(a2a_task_id="msg-123", task_state="ACTIVE")
        assert ctx["a2a_task_id"] == "msg-123"
        assert ctx["task_state"] == "ACTIVE"

    def test_rejects_invalid_state(self, tmp_path, monkeypatch):
        from src.shared import guild_context

        ctx_file = tmp_path / "guild_context.json"
        ctx_file.write_text(json.dumps({"task_state": "INIT"}))
        monkeypatch.setattr(guild_context, "CONTEXT_PATH", ctx_file)

        with pytest.raises(ValueError, match="Invalid task_state"):
            guild_context.update(task_state="BOGUS")
