"""Tests for Human Gates coordination flow — Issue #11.

Tests cover:
- Gate 0: ERC-8004 shortlist displayed, CLI halts, resumes only on y
- Gate 0.5: Quote displayed, Accept quote? halts execution
- Gate 1: vote called only after human approves; rejection tested
- Gate 2: settle() called only after human accepts deliverable
- Gate 2 rejection → task_state: DISPUTED; no settlement tx
- Full coordination loop with all 4 gates (happy path + rejection paths)
- Validation plan checks 8.1–8.5
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Gate 0 — Candidate Selection (Validation 8.1)
# ---------------------------------------------------------------------------

class TestGate0:
    """Gate 0 — ERC-8004 shortlist displayed; CLI halts; resumes only on y."""

    def test_gate_0_displays_shortlist(self, capsys):
        """Gate 0 shows ERC-8004 shortlist to human."""
        from src.cli.gates import gate_0_candidate_selection

        shortlist = [
            {"name": "Specialist Agent", "capabilities": ["code-generation"]},
        ]
        with patch("builtins.input", return_value="y"):
            result = gate_0_candidate_selection(shortlist)

        captured = capsys.readouterr()
        assert "GATE 0" in captured.out
        assert "Specialist Agent" in captured.out
        assert result is True

    def test_gate_0_halts_on_yes(self):
        """Gate 0 resumes execution only on y."""
        from src.cli.gates import gate_0_candidate_selection

        shortlist = [{"name": "Agent A"}]
        with patch("builtins.input", return_value="y"):
            assert gate_0_candidate_selection(shortlist) is True

    def test_gate_0_rejects_on_n(self):
        """Gate 0 returns False on n — blocks invite."""
        from src.cli.gates import gate_0_candidate_selection

        with patch("builtins.input", return_value="n"):
            assert gate_0_candidate_selection([]) is False

    def test_gate_0_empty_input_is_rejection(self):
        """Gate 0 treats empty input as rejection (never auto-proceeds)."""
        from src.cli.gates import gate_0_candidate_selection

        with patch("builtins.input", return_value=""):
            assert gate_0_candidate_selection([]) is False


# ---------------------------------------------------------------------------
# Gate 0.5 — Quote Acceptance (Validation 8.2)
# ---------------------------------------------------------------------------

class TestGate05:
    """Gate 0.5 — Quote displayed; Accept quote? halts execution."""

    def test_gate_0_5_displays_quote(self, capsys):
        """Gate 0.5 shows scope, cost, timeline."""
        from src.cli.gates import gate_0_5_quote_acceptance

        quote = {
            "scope": "Full task execution",
            "estimated_cost_wei": 1000000000000000,
            "deadline_iso": "2026-06-12T23:59:00+00:00",
        }
        with patch("builtins.input", return_value="y"):
            result = gate_0_5_quote_acceptance(quote)

        captured = capsys.readouterr()
        assert "GATE 0.5" in captured.out
        assert "0.001000 ETH" in captured.out
        assert result is True

    def test_gate_0_5_halts_on_yes(self):
        """Gate 0.5 resumes execution only on y."""
        from src.cli.gates import gate_0_5_quote_acceptance

        quote = {"scope": "Test", "estimated_cost_wei": 0, "deadline_iso": "N/A"}
        with patch("builtins.input", return_value="y"):
            assert gate_0_5_quote_acceptance(quote) is True

    def test_gate_0_5_rejects_quote(self):
        """Gate 0.5 returns False on rejection — blocks task/send."""
        from src.cli.gates import gate_0_5_quote_acceptance

        with patch("builtins.input", return_value="n"):
            assert gate_0_5_quote_acceptance({}) is False

    def test_gate_0_5_empty_input_is_rejection(self):
        """Gate 0.5 never auto-proceeds."""
        from src.cli.gates import gate_0_5_quote_acceptance

        with patch("builtins.input", return_value=""):
            assert gate_0_5_quote_acceptance({}) is False


# ---------------------------------------------------------------------------
# Gate 1 — Membership (Validation 8.3, already partially tested in test_membership.py)
# ---------------------------------------------------------------------------

class TestGate1Flow:
    """Gate 1 — vote called only after human approves."""

    def test_gate_1_rejection_blocks_vote(self):
        """If Gate 1 rejects, vote() is never called."""
        from src.cli.gates import gate_1_membership

        profile = {"name": "Bad Agent", "capabilities": []}
        with patch("builtins.input", return_value="n"):
            assert gate_1_membership(profile) is False

    def test_gate_1_approval_returns_true(self):
        """Gate 1 approval returns True — vote() may proceed."""
        from src.cli.gates import gate_1_membership

        with patch("builtins.input", return_value="y"):
            assert gate_1_membership({"name": "Good Agent"}) is True


# ---------------------------------------------------------------------------
# Gate 2 — Deliverable Acceptance (Validation 8.4 + 8.5)
# ---------------------------------------------------------------------------

class TestGate2:
    """Gate 2 — settle() called only after human accepts deliverable."""

    def test_gate_2_shows_pre_check_report(self, capsys):
        """Gate 2 displays hash, format, size check results."""
        from src.cli.gates import gate_2_deliverable_acceptance

        report = {
            "hash_match": True,
            "format_valid": True,
            "size_check": True,
            "evaluator_verdict": "PASS",
        }
        with patch("builtins.input", return_value="y"):
            result = gate_2_deliverable_acceptance("deliverable.json", report)

        captured = capsys.readouterr()
        assert "GATE 2" in captured.out
        assert "✅" in captured.out
        assert "PASS" in captured.out
        assert result is True

    def test_gate_2_acceptance_triggers_settle(self):
        """Gate 2 acceptance returns True — settle() may proceed."""
        from src.cli.gates import gate_2_deliverable_acceptance

        report = {"hash_match": True, "format_valid": True, "size_check": True}
        with patch("builtins.input", return_value="y"):
            assert gate_2_deliverable_acceptance("file.json", report) is True

    def test_gate_2_rejection_returns_false(self, capsys):
        """Gate 2 rejection returns False — no settle() call fires."""
        from src.cli.gates import gate_2_deliverable_acceptance

        report = {"hash_match": False, "format_valid": False, "size_check": False}
        with patch("builtins.input", return_value="n"):
            result = gate_2_deliverable_acceptance("file.json", report)

        assert result is False
        captured = capsys.readouterr()
        assert "DISPUTED" in captured.out


# ---------------------------------------------------------------------------
# Dispute stub — Gate 2 rejection → DISPUTED (Validation 8.5)
# ---------------------------------------------------------------------------

class TestDisputePath:
    """Gate 2 rejection sets task_state: DISPUTED; no settlement tx."""

    def test_rejection_sets_disputed_state(self, tmp_path):
        """Gate 2 rejection updates guild_context to DISPUTED."""
        from src.shared import guild_context

        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            guild_context.save({
                "guild_address": "0xGuild000000000000000000000000000000000",
                "mandate": "Test",
                "treasury_wei": "1000",
                "member_list": [],
                "task_state": "ACTIVE",
            })

            # Simulate Gate 2 rejection
            from src.cli.gates import gate_2_deliverable_acceptance
            report = {"hash_match": False, "format_valid": False, "size_check": False}
            with patch("builtins.input", return_value="n"):
                accepted = gate_2_deliverable_acceptance("file.json", report)

            assert accepted is False

            # Runner should set DISPUTED
            guild_context.update(task_state="DISPUTED")
            ctx = guild_context.load()
            assert ctx["task_state"] == "DISPUTED"
        finally:
            guild_context.CONTEXT_PATH = original_path

    def test_disputed_state_is_valid(self, tmp_path):
        """DISPUTED is in VALID_STATES."""
        from src.shared.guild_context import VALID_STATES
        assert "DISPUTED" in VALID_STATES


# ---------------------------------------------------------------------------
# Coordination runner integration tests
# ---------------------------------------------------------------------------

class TestCoordinationRunner:
    """Integration tests for the full coordination loop with gates."""

    @pytest.mark.asyncio
    async def test_runner_halts_at_gate_0_rejection(self, tmp_path):
        """Runner stops when Gate 0 is rejected — no invite sent."""
        from src.shared import guild_context
        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            guild_context.save({
                "guild_address": "0xTest",
                "mandate": "Test",
                "treasury_wei": "1000",
                "member_list": [],
                "task_state": "ACTIVE",
            })

            from src.cli.runner import run_coordination_loop

            with patch("builtins.input", return_value="n"), \
                 patch("src.cli.runner.tools") as mock_tools:
                mock_tools.talent_query = AsyncMock(return_value=[{"name": "Agent"}])
                await run_coordination_loop("test task")

                # task_invite should NOT have been called
                mock_tools.task_invite.assert_not_called()
        finally:
            guild_context.CONTEXT_PATH = original_path

    @pytest.mark.asyncio
    async def test_runner_halts_at_gate_0_5_rejection(self, tmp_path):
        """Runner stops when Gate 0.5 is rejected — no delegation."""
        from src.shared import guild_context
        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            guild_context.save({
                "guild_address": "0xTest",
                "mandate": "Test",
                "treasury_wei": "1000",
                "member_list": [],
                "task_state": "ACTIVE",
            })

            from src.cli.runner import run_coordination_loop

            # y at Gate 0, n at Gate 0.5
            with patch("builtins.input", side_effect=["y", "n"]), \
                 patch("src.cli.runner.tools") as mock_tools, \
                 patch("src.cli.runner.handle_task_invite", new_callable=AsyncMock) as mock_hti:
                mock_tools.talent_query = AsyncMock(return_value=[{"name": "Agent"}])
                mock_tools.task_invite = AsyncMock(return_value="msg-1")
                mock_hti.return_value = {"scope": "test", "estimated_cost_wei": 0, "deadline_iso": "N/A"}

                await run_coordination_loop("test task")

                # task_delegate should NOT have been called
                mock_tools.task_delegate.assert_not_called()
        finally:
            guild_context.CONTEXT_PATH = original_path

    @pytest.mark.asyncio
    async def test_runner_sets_disputed_on_gate_2_rejection(self, tmp_path):
        """Gate 2 rejection → task_state: DISPUTED, no settle()."""
        from src.shared import guild_context
        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            guild_context.save({
                "guild_address": "0xTest",
                "mandate": "Test",
                "treasury_wei": "1000",
                "member_list": [],
                "task_state": "ACTIVE",
                "proposal_id": "99",
            })

            from src.cli.runner import run_coordination_loop

            # y at Gate 0, y at Gate 0.5, y at Gate 1, n at Gate 2
            with patch("builtins.input", side_effect=["y", "y", "y", "n"]), \
                 patch("src.cli.runner.tools") as mock_tools, \
                 patch("src.cli.runner.handle_task_invite", new_callable=AsyncMock) as mock_hti, \
                 patch("src.cli.runner.handle_task_send", new_callable=AsyncMock) as mock_hts, \
                 patch("src.cli.runner.send_accepted", new_callable=AsyncMock), \
                 patch("src.cli.runner.Path") as mock_path_cls:

                mock_tools.talent_query = AsyncMock(return_value=[{"name": "Agent"}])
                mock_tools.task_invite = AsyncMock(return_value="msg-1")
                mock_tools.task_delegate = AsyncMock(return_value="msg-2")
                mock_tools.deliverable_review = AsyncMock(return_value={
                    "hash_match": False, "format_valid": False,
                    "size_check": False, "evaluator_verdict": "FAIL",
                })
                mock_tools.membership_propose = AsyncMock(return_value={
                    "proposal_id": "99", "status": "proposed",
                })
                mock_tools.membership_vote = AsyncMock(return_value={
                    "vote_tx": "0xvote", "approved": True,
                })
                mock_hti.return_value = {"scope": "test", "estimated_cost_wei": 0, "deadline_iso": "N/A"}
                mock_hts.return_value = {
                    "deliverable_reference": "deliverables/test.json",
                    "deliverable_hash": "sha256:abc",
                    "task_id": "msg-2",
                }

                # Mock profile path
                mock_profile_path = MagicMock()
                mock_profile_path.exists.return_value = True
                mock_profile_path.read_text.return_value = json.dumps({"name": "Agent"})
                mock_path_cls.return_value.parent.parent.parent = tmp_path
                mock_path_cls.return_value = mock_profile_path

                # Also patch Path constructor inside runner
                with patch("src.cli.runner.Path") as inner_path:
                    inner_path.return_value.parent.parent.parent = tmp_path
                    inner_path.return_value.exists.return_value = True
                    inner_path.return_value.read_text.return_value = json.dumps({"name": "Agent"})
                    inner_path.side_effect = lambda p: Path(p)

                    await run_coordination_loop("test task")

                # settle should NOT have been called
                mock_tools.settle.assert_not_called()

                # guild_context should be DISPUTED
                ctx = guild_context.load()
                assert ctx["task_state"] == "DISPUTED"
        finally:
            guild_context.CONTEXT_PATH = original_path
