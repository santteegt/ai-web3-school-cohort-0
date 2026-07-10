"""Tests for SpecialistA2AClient — Issue #37.

Tests cover:
- send_delivered() constructs correct message with all fields
- send_feedback_request() constructs correct message
- Both messages logged to a2a_trace
- Unreachable/malformed endpoint raises surfaced, logged error
- Mock _send_to_agent pattern (same as test_a2a.py)

Maps to specs/scenarios/07_deliverable_attestation.feature →
"Orchestrator's A2A server receives the proactive task/delivered" (send side)
and the fail-closed negative scenario; and specs/scenarios/
10_reputation_feedback.feature → "Orchestrator's A2A server receives the
proactive feedback/request" (send side) and its fail-closed negative.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod
    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


# ---------------------------------------------------------------------------
# send_delivered
# ---------------------------------------------------------------------------

class TestSendDelivered:
    @pytest.mark.asyncio
    async def test_constructs_correct_payload(self, tmp_trace_dir):
        from src.specialist.a2a_client import send_delivered

        mock_response = {"type": "deliverable_review", "pre_check": {"evaluator_verdict": "PASS"}}

        with patch(
            "src.specialist.a2a_client._send_to_agent",
            new_callable=AsyncMock,
        ) as mock_send:
            mock_send.return_value = mock_response
            result = await send_delivered(
                orchestrator_endpoint="http://localhost:10000",
                task_id="task-123",
                deliverable_hash="sha256:abc",
                attestation_uid="0xdef",
                attestation_url="https://base.easscan.org/attestation/0xdef",
            )

            assert result == mock_response
            mock_send.assert_called_once()

            sent_endpoint, sent_message = mock_send.call_args[0]
            assert sent_endpoint == "http://localhost:10000"

            text = sent_message.parts[0].text
            payload = json.loads(text)
            assert payload["type"] == "task/delivered"
            assert payload["task_id"] == "task-123"
            assert payload["deliverable_hash"] == "sha256:abc"
            assert payload["attestation_uid"] == "0xdef"
            assert payload["attestation_url"] == "https://base.easscan.org/attestation/0xdef"

    @pytest.mark.asyncio
    async def test_logs_to_a2a_trace(self, tmp_trace_dir):
        from src.specialist.a2a_client import send_delivered

        with patch(
            "src.specialist.a2a_client._send_to_agent",
            new_callable=AsyncMock,
        ) as mock_send:
            mock_send.return_value = {"type": "ack"}
            await send_delivered(
                orchestrator_endpoint="http://localhost:10000",
                task_id="task-trace",
                deliverable_hash="sha256:trace",
                attestation_uid="0xtrace",
                attestation_url="https://base.easscan.org/attestation/0xtrace",
            )

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert any(e["type"] == "task/delivered" and e["direction"] == "outgoing" for e in entries)

    @pytest.mark.asyncio
    async def test_unreachable_endpoint_raises(self, tmp_trace_dir):
        from src.specialist.a2a_client import send_delivered

        with patch(
            "src.specialist.a2a_client._send_to_agent",
            new_callable=AsyncMock,
            side_effect=ConnectionError("Connection refused"),
        ):
            with pytest.raises(ConnectionError, match="Connection refused"):
                await send_delivered(
                    orchestrator_endpoint="http://unreachable:9999",
                    task_id="task-fail",
                    deliverable_hash="sha256:fail",
                    attestation_uid="0xfail",
                    attestation_url="https://base.easscan.org/attestation/0xfail",
                )

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert any(
            e["type"] == "task/delivered" and e["direction"] == "outgoing"
            for e in entries
        )


# ---------------------------------------------------------------------------
# send_feedback_request
# ---------------------------------------------------------------------------

class TestSendFeedbackRequest:
    @pytest.mark.asyncio
    async def test_constructs_correct_payload(self, tmp_trace_dir):
        from src.specialist.a2a_client import send_feedback_request

        mock_response = {"type": "reputation_propose", "status": "stubbed"}

        with patch(
            "src.specialist.a2a_client._send_to_agent",
            new_callable=AsyncMock,
        ) as mock_send:
            mock_send.return_value = mock_response
            result = await send_feedback_request(
                orchestrator_endpoint="http://localhost:10000",
                task_id="task-456",
                deliverable_hash="sha256:xyz",
            )

            assert result == mock_response
            mock_send.assert_called_once()

            sent_endpoint, sent_message = mock_send.call_args[0]
            assert sent_endpoint == "http://localhost:10000"

            text = sent_message.parts[0].text
            payload = json.loads(text)
            assert payload["type"] == "feedback/request"
            assert payload["task_id"] == "task-456"
            assert payload["deliverable_hash"] == "sha256:xyz"

    @pytest.mark.asyncio
    async def test_logs_to_a2a_trace(self, tmp_trace_dir):
        from src.specialist.a2a_client import send_feedback_request

        with patch(
            "src.specialist.a2a_client._send_to_agent",
            new_callable=AsyncMock,
        ) as mock_send:
            mock_send.return_value = {"type": "ack"}
            await send_feedback_request(
                orchestrator_endpoint="http://localhost:10000",
                task_id="task-trace-fb",
                deliverable_hash="sha256:fbtrace",
            )

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert any(
            e["type"] == "feedback/request" and e["direction"] == "outgoing"
            for e in entries
        )

    @pytest.mark.asyncio
    async def test_unreachable_endpoint_raises(self, tmp_trace_dir):
        from src.specialist.a2a_client import send_feedback_request

        with patch(
            "src.specialist.a2a_client._send_to_agent",
            new_callable=AsyncMock,
            side_effect=ConnectionError("Connection refused"),
        ):
            with pytest.raises(ConnectionError, match="Connection refused"):
                await send_feedback_request(
                    orchestrator_endpoint="http://unreachable:9999",
                    task_id="task-fail-fb",
                    deliverable_hash="sha256:fbfail",
                )

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert any(
            e["type"] == "feedback/request" and e["direction"] == "outgoing"
            for e in entries
        )


# ---------------------------------------------------------------------------
# Reuse of shared helpers — verify imports work without modification
# ---------------------------------------------------------------------------

class TestSharedHelperReuse:
    def test_imports_build_message_from_shared(self):
        from src.shared.a2a import _build_message as shared_build
        from src.specialist.a2a_client import _build_message

        assert _build_message is shared_build

    def test_imports_log_message_from_shared(self):
        from src.shared.a2a import _log_message as shared_log
        from src.specialist.a2a_client import _log_message

        assert _log_message is shared_log

    def test_imports_send_to_agent_from_shared(self):
        from src.shared.a2a import _send_to_agent as shared_send
        from src.specialist.a2a_client import _send_to_agent

        assert _send_to_agent is shared_send
