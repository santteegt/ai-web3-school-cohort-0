"""Tests for task delegation — Issue #32.

Maps directly to specs/scenarios/05_task_delegation.feature:
- Delegate a complete, well-formed task
- Reject a task missing acceptance criteria
- Reject a task missing the GitHub issue link
- Reject a task with an unrecognized deliverable format
- Carry GuildOS fields in the text body when metadata is rejected
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
    """Redirect A2A trace logs to a temp directory."""
    import src.shared.a2a as a2a_mod
    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def well_formed_task() -> dict:
    """A complete task/send payload matching specs/20-api-contracts.md §3."""
    return {
        "task_id": "task-abc-123",
        "task_description": "Implement the EAS attestation module (EASClient)",
        "github_issue_url": "https://github.com/santteegt/ai-web3-school-cohort-0/issues/10",
        "input_data": "See linked GitHub issue for full ticket context.",
        "technical_constraints": {
            "repo_branch": "main",
            "library_versions": ["a2a-sdk[http-server]==1.1.0", "web3==7.16.0"],
            "env_vars": ["GLM_API_KEY"],
        },
        "agbom": {
            "tools": ["GLM-5.1 API client (Z.AI, via Hermes)", "file I/O", "git"],
            "mcp_servers": [],
            "data_sources": ["specs/scenarios/06_specialist_execution.feature"],
        },
        "acceptance_criteria": [
            "Plan contains at least 3 steps",
            "Output satisfies every BDD test listed in task.acceptance_criteria",
        ],
        "deliverable_format": "github_commit",
        "deadline": "2026-07-08T00:00:00+00:00",
        "budget_wei": "1000000000000000",
        "orchestrator_endpoint": "http://localhost:10000",
    }


# ---------------------------------------------------------------------------
# Scenario: Delegate a complete, well-formed task
# ---------------------------------------------------------------------------

class TestDelegateWellFormedTask:
    @pytest.mark.asyncio
    async def test_well_formed_task_is_sent_and_context_updated(
        self, tmp_trace_dir, well_formed_task
    ):
        from src.orchestrator import tools

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a, \
             patch("src.orchestrator.tools.guild_context") as mock_ctx:
            mock_a2a.send_task = AsyncMock(return_value="msg-well-formed")

            message_id = await tools.task_delegate(
                "http://localhost:10001", well_formed_task
            )

            assert message_id == "msg-well-formed"
            # Sent with every required field intact — no field dropped/renamed.
            sent_task = mock_a2a.send_task.call_args[0][1]
            assert sent_task["github_issue_url"] == well_formed_task["github_issue_url"]
            assert sent_task["technical_constraints"] == well_formed_task["technical_constraints"]
            assert sent_task["agbom"] == well_formed_task["agbom"]
            assert sent_task["acceptance_criteria"] == well_formed_task["acceptance_criteria"]
            assert sent_task["deliverable_format"] == well_formed_task["deliverable_format"]
            assert sent_task["deadline"] == well_formed_task["deadline"]
            assert sent_task["budget_wei"] == well_formed_task["budget_wei"]

            # Message id captured to guild_context.a2a_task_id
            mock_ctx.update.assert_called_once_with(a2a_task_id="msg-well-formed")

    @pytest.mark.asyncio
    async def test_send_task_logs_to_a2a_trace(self, tmp_trace_dir, well_formed_task):
        """The message is logged to ./logs/a2a_trace_{date}.json."""
        from src.shared.a2a import send_task

        with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
            mock_send.return_value = {"type": "task/delivered"}
            await send_task("http://localhost:10001", well_formed_task)

        trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
        entries = json.loads(trace_file.read_text())
        assert any(e["type"] == "task/send" for e in entries)
        outgoing = next(e for e in entries if e["type"] == "task/send")
        assert outgoing["payload"]["task"]["github_issue_url"] == well_formed_task["github_issue_url"]


# ---------------------------------------------------------------------------
# Negative scenarios — under-specified payloads must never reach the Specialist
# ---------------------------------------------------------------------------

class TestRejectUnderspecifiedTask:
    @pytest.mark.asyncio
    async def test_rejects_empty_acceptance_criteria(self, well_formed_task):
        from src.orchestrator import tools

        bad_task = {**well_formed_task, "acceptance_criteria": []}

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_task = AsyncMock()
            with pytest.raises(tools.UnderspecifiedTaskError):
                await tools.task_delegate("http://localhost:10001", bad_task)
            mock_a2a.send_task.assert_not_called()

    @pytest.mark.asyncio
    async def test_rejects_missing_acceptance_criteria(self, well_formed_task):
        from src.orchestrator import tools

        bad_task = dict(well_formed_task)
        del bad_task["acceptance_criteria"]

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_task = AsyncMock()
            with pytest.raises(tools.UnderspecifiedTaskError):
                await tools.task_delegate("http://localhost:10001", bad_task)
            mock_a2a.send_task.assert_not_called()

    @pytest.mark.asyncio
    async def test_rejects_missing_github_issue_url(self, well_formed_task):
        from src.orchestrator import tools

        bad_task = dict(well_formed_task)
        del bad_task["github_issue_url"]

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_task = AsyncMock()
            with pytest.raises(tools.UnderspecifiedTaskError):
                await tools.task_delegate("http://localhost:10001", bad_task)
            mock_a2a.send_task.assert_not_called()

    @pytest.mark.asyncio
    async def test_rejects_unrecognized_deliverable_format(self, well_formed_task):
        from src.orchestrator import tools

        bad_task = {**well_formed_task, "deliverable_format": "pdf"}

        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_task = AsyncMock()
            with pytest.raises(tools.UnderspecifiedTaskError):
                await tools.task_delegate("http://localhost:10001", bad_task)
            mock_a2a.send_task.assert_not_called()


# ---------------------------------------------------------------------------
# Scenario: Carry GuildOS fields in the text body when metadata is rejected
# ---------------------------------------------------------------------------

class TestTextBodyFallback:
    @pytest.mark.asyncio
    async def test_full_nested_payload_round_trips_through_text_body(
        self, tmp_trace_dir, well_formed_task
    ):
        """The A2A transport carries the whole task as a JSON string in Part.text —
        verify no field is dropped or truncated for the larger, deeply-nested payload.
        """
        from src.shared.a2a import send_task

        captured_messages = []

        async def fake_send_to_agent(agent_url, message, configuration=None):
            captured_messages.append(message)
            return {"type": "task/delivered"}

        with patch("src.shared.a2a._send_to_agent", side_effect=fake_send_to_agent):
            await send_task("http://localhost:10001", well_formed_task)

        assert len(captured_messages) == 1
        sent_message = captured_messages[0]
        text_part = sent_message.parts[0].text
        parsed = json.loads(text_part)

        assert parsed["type"] == "task/send"
        assert parsed["task"] == well_formed_task
