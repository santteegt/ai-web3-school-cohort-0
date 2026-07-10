"""Tests for the coordination runner async flow rewrite — Issue #39.

Verifies the runner uses real A2A transport (send_invite / send_task /
poll_task) instead of calling Specialist handler functions directly, and
that orchestrator_endpoint is set in the task/send payload.

Maps to specs/scenarios/05_task_delegation.feature (non-blocking task/send),
07_deliverable_attestation.feature (proactive push polling), and
10_reputation_feedback.feature — the runner is the orchestration point
for the full sequence.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod
    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def mock_guild_context():
    """Mock guild_context so the runner doesn't read/write a real file."""
    state = {
        "guild_address": "0xguild123",
        "task_state": "ACTIVE",
        "mandate": "test",
        "treasury_wei": "1000000000000000",
        "member_list": [],
        "proposal_id": "prop-1",
    }
    with patch("src.cli.runner.guild_context") as mock_ctx:
        mock_ctx.load.return_value = state
        mock_ctx.update.return_value = state
        yield mock_ctx


@pytest.fixture
def mock_gates():
    """Mock all gates to auto-approve (return True) for fast testing."""
    with patch("src.cli.runner.gates") as mock_g:
        mock_g.gate_0_candidate_selection.return_value = True
        mock_g.gate_0_5_quote_acceptance.return_value = True
        mock_g.gate_1_membership.return_value = True
        mock_g.gate_2_deliverable_acceptance.return_value = True
        yield mock_g


@pytest.fixture
def mock_orchestrator_tools():
    """Mock the on-chain tools so the runner doesn't hit the network."""
    with patch("src.cli.runner.tools") as mock_tools:
        mock_tools.guild_launch = AsyncMock(return_value={
            "guild_address": "0xguild123",
            "launch_tx": "0xlaunch",
            "commit_tx": "0xcommit",
        })
        mock_tools.talent_query = AsyncMock(return_value=[
            {"name": "Specialist", "agent_id": "erc8004:1", "capabilities": ["code-generation"]}
        ])
        mock_tools.membership_propose = AsyncMock(return_value={
            "proposal_id": "prop-1",
        })
        mock_tools.membership_vote = AsyncMock(return_value={
            "vote_tx": "0xvote",
        })
        mock_tools.deliverable_review = AsyncMock(return_value={
            "hash_match": True,
            "format_valid": True,
            "size_check": True,
            "evaluator_verdict": "PASS",
        })
        mock_tools.settle = AsyncMock(return_value="0xsettle")
        mock_tools.reputation_write = AsyncMock(side_effect=NotImplementedError("Phase 3"))
        yield mock_tools


# ---------------------------------------------------------------------------
# Verify runner uses A2A transport, not direct handler calls
# ---------------------------------------------------------------------------

class TestRunnerUsesA2ATransport:
    @pytest.mark.asyncio
    async def test_calls_send_invite_not_handle_task_invite(
        self, tmp_trace_dir, mock_guild_context, mock_gates, mock_orchestrator_tools
    ):
        from src.cli import runner

        mock_quote = {
            "type": "task/quote",
            "scope": "Full task execution",
            "estimated_cost_wei": 1000000000000000,
            "deadline_iso": "2026-07-15T23:59:00+00:00",
            "message_id": "msg-quote-1",
        }

        with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite, \
             patch("src.cli.runner.send_task", new_callable=AsyncMock) as mock_send, \
             patch("src.cli.runner.send_accepted", new_callable=AsyncMock), \
             patch("src.cli.runner.poll_task", new_callable=AsyncMock) as mock_poll:

            mock_invite.return_value = mock_quote
            mock_send.return_value = "task-working-1"
            mock_poll.return_value = {
                "task_id": "task-working-1",
                "task_state": "TASK_STATE_COMPLETED",
                "type": "task/delivered",
                "deliverable_hash": "sha256:abc",
                "deliverable_reference": "/tmp/deliv.json",
            }

            await runner.run_coordination_loop(
                task_description="Test task",
                specialist_endpoint="http://localhost:10001",
            )

            mock_invite.assert_called_once()
            mock_send.assert_called_once()
            mock_poll.assert_called()

    @pytest.mark.asyncio
    async def test_orchestrator_endpoint_set_in_task(
        self, tmp_trace_dir, mock_guild_context, mock_gates, mock_orchestrator_tools
    ):
        from src.cli import runner

        mock_quote = {
            "type": "task/quote",
            "scope": "test",
            "estimated_cost_wei": 1000,
            "deadline_iso": "2026-07-15T23:59:00+00:00",
        }

        captured_task = {}

        async def capture_send(endpoint, task):
            captured_task.update(task)
            return "task-id-1"

        with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite, \
             patch("src.cli.runner.send_task", side_effect=capture_send), \
             patch("src.cli.runner.send_accepted", new_callable=AsyncMock), \
             patch("src.cli.runner.poll_task", new_callable=AsyncMock) as mock_poll:

            mock_invite.return_value = mock_quote
            mock_poll.return_value = {
                "task_id": "task-id-1",
                "task_state": "TASK_STATE_COMPLETED",
                "deliverable_hash": "sha256:abc",
                "deliverable_reference": "/tmp/test.json",
            }

            await runner.run_coordination_loop(
                task_description="Test task",
                specialist_endpoint="http://localhost:10001",
            )

            assert "orchestrator_endpoint" in captured_task
            assert captured_task["orchestrator_endpoint"].startswith("http://localhost:")

    @pytest.mark.asyncio
    async def test_quote_extracted_from_send_invite_response(
        self, tmp_trace_dir, mock_guild_context, mock_gates, mock_orchestrator_tools
    ):
        from src.cli import runner

        mock_quote = {
            "type": "task/quote",
            "scope": "Full scope from real transport",
            "estimated_cost_wei": 2000000000000000,
            "deadline_iso": "2026-07-20T23:59:00+00:00",
        }

        with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite, \
             patch("src.cli.runner.send_task", new_callable=AsyncMock), \
             patch("src.cli.runner.send_accepted", new_callable=AsyncMock), \
             patch("src.cli.runner.poll_task", new_callable=AsyncMock) as mock_poll:

            mock_invite.return_value = mock_quote
            mock_poll.return_value = {
                "task_id": "task-1",
                "task_state": "TASK_STATE_COMPLETED",
                "deliverable_hash": "sha256:abc",
                "deliverable_reference": "/tmp/test.json",
            }

            await runner.run_coordination_loop(
                task_description="Test task",
                specialist_endpoint="http://localhost:10001",
            )

            gate_0_5_call = mock_gates.gate_0_5_quote_acceptance.call_args[0][0]
            assert gate_0_5_call["scope"] == "Full scope from real transport"
            assert gate_0_5_call["estimated_cost_wei"] == 2000000000000000


# ---------------------------------------------------------------------------
# Polling behavior
# ---------------------------------------------------------------------------

class TestRunnerPolling:
    @pytest.mark.asyncio
    async def test_poll_loops_until_completed(
        self, tmp_trace_dir, mock_guild_context, mock_gates, mock_orchestrator_tools
    ):
        from src.cli import runner

        mock_quote = {
            "type": "task/quote",
            "scope": "test",
            "estimated_cost_wei": 1000,
            "deadline_iso": "2026-07-15T23:59:00+00:00",
        }

        call_count = 0

        async def mock_poll(endpoint, task_id):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                return {"task_id": task_id, "task_state": "TASK_STATE_WORKING"}
            return {
                "task_id": task_id,
                "task_state": "TASK_STATE_COMPLETED",
                "deliverable_hash": "sha256:done",
                "deliverable_reference": "/tmp/done.json",
            }

        with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite, \
             patch("src.cli.runner.send_task", new_callable=AsyncMock) as mock_send, \
             patch("src.cli.runner.send_accepted", new_callable=AsyncMock), \
             patch("src.cli.runner.poll_task", side_effect=mock_poll), \
             patch("src.cli.runner.asyncio.sleep", new_callable=AsyncMock):

            mock_invite.return_value = mock_quote
            mock_send.return_value = "task-poll-1"

            await runner.run_coordination_loop(
                task_description="Test poll",
                specialist_endpoint="http://localhost:10001",
            )

            assert call_count == 3

    @pytest.mark.asyncio
    async def test_timeout_raises(
        self, tmp_trace_dir, mock_guild_context, mock_gates, mock_orchestrator_tools
    ):
        from src.cli import runner

        mock_quote = {
            "type": "task/quote",
            "scope": "test",
            "estimated_cost_wei": 1000,
            "deadline_iso": "2026-07-15T23:59:00+00:00",
        }

        with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite, \
             patch("src.cli.runner.send_task", new_callable=AsyncMock), \
             patch("src.cli.runner.send_accepted", new_callable=AsyncMock), \
             patch("src.cli.runner.poll_task", new_callable=AsyncMock) as mock_poll, \
             patch("src.cli.runner.asyncio.sleep", new_callable=AsyncMock), \
             patch("src.cli.runner.POLL_TIMEOUT_SECONDS", 0):

            mock_invite.return_value = mock_quote
            mock_poll.return_value = {
                "task_id": "task-1",
                "task_state": "TASK_STATE_WORKING",
            }

            with pytest.raises(TimeoutError, match="did not complete"):
                await runner.run_coordination_loop(
                    task_description="Test timeout",
                    specialist_endpoint="http://localhost:10001",
                )


# ---------------------------------------------------------------------------
# Gate preservation — all 6 gates still halt
# ---------------------------------------------------------------------------

class TestGatePreservation:
    @pytest.mark.asyncio
    async def test_gate_0_aborts_loop(
        self, tmp_trace_dir, mock_guild_context, mock_orchestrator_tools
    ):
        from src.cli import runner

        with patch("src.cli.runner.gates") as mock_g:
            mock_g.gate_0_candidate_selection.return_value = False

            with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite:
                await runner.run_coordination_loop("test")

                mock_invite.assert_not_called()

    @pytest.mark.asyncio
    async def test_gate_0_5_aborts_loop(
        self, tmp_trace_dir, mock_guild_context, mock_orchestrator_tools
    ):
        from src.cli import runner

        mock_quote = {"scope": "test", "estimated_cost_wei": 1000, "deadline_iso": "x"}

        with patch("src.cli.runner.gates") as mock_g:
            mock_g.gate_0_candidate_selection.return_value = True
            mock_g.gate_0_5_quote_acceptance.return_value = False

            with patch("src.cli.runner.send_invite", new_callable=AsyncMock) as mock_invite, \
                 patch("src.cli.runner.send_task", new_callable=AsyncMock) as mock_send:

                mock_invite.return_value = mock_quote

                await runner.run_coordination_loop("test")

                mock_send.assert_not_called()


# ---------------------------------------------------------------------------
# No direct handler imports
# ---------------------------------------------------------------------------

class TestNoDirectHandlerImports:
    def test_runner_module_does_not_import_specialist_handlers(self):
        import importlib
        import inspect

        runner_mod = importlib.import_module("src.cli.runner")
        source = inspect.getsource(runner_mod)

        assert "handle_task_invite" not in source
        assert "handle_task_send" not in source
        assert "from src.specialist.agent" not in source

    def test_runner_imports_a2a_transport_functions(self):
        from src.cli.runner import poll_task, send_accepted, send_invite, send_task

        assert callable(poll_task)
        assert callable(send_accepted)
        assert callable(send_invite)
        assert callable(send_task)


# ---------------------------------------------------------------------------
# _wait_for_deliverable helper
# ---------------------------------------------------------------------------

class TestWaitForDeliverable:
    @pytest.mark.asyncio
    async def test_returns_on_completed(self):
        from src.cli.runner import _wait_for_deliverable

        with patch("src.cli.runner.poll_task", new_callable=AsyncMock) as mock_poll:
            mock_poll.return_value = {
                "task_id": "t1",
                "task_state": "TASK_STATE_COMPLETED",
                "deliverable_hash": "sha256:x",
            }

            result = await _wait_for_deliverable("http://localhost:10001", "t1", timeout=5)

            assert result["task_state"] == "TASK_STATE_COMPLETED"
            assert result["deliverable_hash"] == "sha256:x"

    @pytest.mark.asyncio
    async def test_times_out_on_perpetual_working(self):
        from src.cli.runner import _wait_for_deliverable

        with patch("src.cli.runner.poll_task", new_callable=AsyncMock) as mock_poll, \
             patch("src.cli.runner.asyncio.sleep", new_callable=AsyncMock):
            mock_poll.return_value = {
                "task_id": "t2",
                "task_state": "TASK_STATE_WORKING",
            }

            with pytest.raises(TimeoutError, match="did not complete"):
                await _wait_for_deliverable("http://localhost:10001", "t2", timeout=0)
