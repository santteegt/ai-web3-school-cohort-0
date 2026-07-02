"""Tests for Orchestrator automated deliverable pre-check — Issue #12.

Tests cover:
- deliverable_review MCP tool returns structured report dict
- Pre-check runs automatically after task/delivered received
- All 3 checks produce correct boolean results
- Report surfaced to human before Gate 2 prompt
- Hash + format check only (no full evaluator)
- Validation plan section 6.6
"""

from __future__ import annotations

import hashlib
import json
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# deliverable_review MCP tool — structured report
# ---------------------------------------------------------------------------

class TestDeliverableReviewReport:
    """deliverable_review returns a structured dict with 4 keys."""

    @pytest.mark.asyncio
    async def test_returns_four_required_keys(self, tmp_path):
        """Report contains hash_match, format_valid, size_check, evaluator_verdict."""
        from src.orchestrator.tools import deliverable_review

        content = b'{"output": "test deliverable"}'
        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        result = await deliverable_review(str(deliv_file), expected_hash)

        assert "hash_match" in result
        assert "format_valid" in result
        assert "size_check" in result
        assert "evaluator_verdict" in result

    @pytest.mark.asyncio
    async def test_all_checks_pass_for_valid_deliverable(self, tmp_path):
        """All 3 checks produce True for a valid JSON deliverable."""
        from src.orchestrator.tools import deliverable_review

        content = b'{"task_id": "test-123", "output": "success"}'
        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        result = await deliverable_review(str(deliv_file), expected_hash)

        assert result["hash_match"] is True
        assert result["format_valid"] is True
        assert result["size_check"] is True
        assert result["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_hash_mismatch_detected(self, tmp_path):
        """hash_match is False when hashes don't match."""
        from src.orchestrator.tools import deliverable_review

        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(b'{"output": "test"}')

        result = await deliverable_review(str(deliv_file), "sha256:badhash0000000000000000000000000000000000000000000000000000000000")

        assert result["hash_match"] is False
        assert result["evaluator_verdict"] == "FAIL"

    @pytest.mark.asyncio
    async def test_invalid_format_detected(self, tmp_path):
        """format_valid is False for empty file (size_check also False)."""
        from src.orchestrator.tools import deliverable_review

        deliv_file = tmp_path / "empty.json"
        deliv_file.write_bytes(b"")

        result = await deliverable_review(str(deliv_file), "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

        assert result["format_valid"] is False
        assert result["size_check"] is False

    @pytest.mark.asyncio
    async def test_non_json_but_nonempty_is_valid(self, tmp_path):
        """Non-JSON but non-empty file passes format check."""
        from src.orchestrator.tools import deliverable_review

        content = b"This is plain text output."
        deliv_file = tmp_path / "output.txt"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        result = await deliverable_review(str(deliv_file), expected_hash)

        assert result["format_valid"] is True
        assert result["size_check"] is True
        assert result["hash_match"] is True
        assert result["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_missing_file_returns_fail(self, tmp_path):
        """Missing file returns all False with error message."""
        from src.orchestrator.tools import deliverable_review

        result = await deliverable_review("/nonexistent/path.json", "sha256:abc")

        assert result["hash_match"] is False
        assert result["format_valid"] is False
        assert result["size_check"] is False
        assert result["evaluator_verdict"] == "FAIL"
        assert "error" in result

    @pytest.mark.asyncio
    async def test_verdict_pass_only_when_all_true(self, tmp_path):
        """evaluator_verdict is PASS only when all 3 checks pass."""
        from src.orchestrator.tools import deliverable_review

        # Valid content but wrong hash → verdict FAIL
        content = b'{"output": "test"}'
        deliv_file = tmp_path / "test.json"
        deliv_file.write_bytes(content)

        result = await deliverable_review(str(deliv_file), "sha256:wronghash")

        # format_valid and size_check should be True, but hash_match False
        assert result["format_valid"] is True
        assert result["size_check"] is True
        assert result["hash_match"] is False
        assert result["evaluator_verdict"] == "FAIL"


# ---------------------------------------------------------------------------
# Pre-check auto-trigger after task/delivered
# ---------------------------------------------------------------------------

class TestPreCheckAutoTrigger:
    """Pre-check runs automatically after task/delivered received."""

    @pytest.mark.asyncio
    async def test_pre_check_after_specialist_delivered(self, tmp_path, monkeypatch):
        """After handle_task_send returns task/delivered, pre-check can verify it."""
        from src.orchestrator.tools import deliverable_review
        from src.specialist.agent import handle_task_send

        # Run from tmp_path so deliverable file lands there
        monkeypatch.chdir(tmp_path)

        delivered = await handle_task_send({
            "type": "task/send",
            "task_id": "pre-check-test",
            "task": {"task_description": "test"},
        })

        # Verify deliverable file was written
        assert "deliverable_reference" in delivered
        assert "deliverable_hash" in delivered

        # Run pre-check on the delivered file
        report = await deliverable_review(
            delivered["deliverable_reference"],
            delivered["deliverable_hash"],
        )

        assert report["hash_match"] is True
        assert report["format_valid"] is True
        assert report["size_check"] is True
        assert report["evaluator_verdict"] == "PASS"


# ---------------------------------------------------------------------------
# Validation 6.6 — Orchestrator pre-check passes
# ---------------------------------------------------------------------------

class TestValidation66:
    """Validation 6.6: Report hash ✅ · format ✅ · size ✅."""

    @pytest.mark.asyncio
    async def test_pre_check_report_all_pass(self, tmp_path):
        """Pre-check report shows all 3 checks passing."""
        from src.orchestrator.tools import deliverable_review

        content = json.dumps({
            "task_id": "val-6-6",
            "output": "GLM-5.1 task result",
        }).encode()
        deliv_file = tmp_path / "deliverable.json"
        deliv_file.write_bytes(content)
        expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

        report = await deliverable_review(str(deliv_file), expected_hash)

        # Validation 6.6: hash ✅ · format ✅ · size ✅
        assert report["hash_match"] is True, "Hash check failed"
        assert report["format_valid"] is True, "Format check failed"
        assert report["size_check"] is True, "Size check failed"
        assert report["evaluator_verdict"] == "PASS"


# ---------------------------------------------------------------------------
# Report surfaced to human before Gate 2 (validation 8.4)
# ---------------------------------------------------------------------------

class TestReportSurfacedAtGate2:
    """Pre-check report is surfaced to human before Gate 2 prompt."""

    def test_gate_2_displays_report(self, capsys):
        """Gate 2 shows the pre-check report hash/format/size/verdict."""
        from src.cli.gates import gate_2_deliverable_acceptance

        report = {
            "hash_match": True,
            "format_valid": True,
            "size_check": True,
            "evaluator_verdict": "PASS",
        }
        with patch("builtins.input", return_value="y"):
            gate_2_deliverable_acceptance("output/test.json", report)

        captured = capsys.readouterr()
        assert "GATE 2" in captured.out
        # Check individual report items are shown
        assert "✅" in captured.out  # Hash present
        assert "PASS" in captured.out  # Verdict

    def test_gate_2_shows_failures(self, capsys):
        """Gate 2 shows ❌ for failed checks."""
        from src.cli.gates import gate_2_deliverable_acceptance

        report = {
            "hash_match": False,
            "format_valid": False,
            "size_check": False,
            "evaluator_verdict": "FAIL — hash mismatch",
        }
        with patch("builtins.input", return_value="n"):
            gate_2_deliverable_acceptance("output/bad.json", report)

        captured = capsys.readouterr()
        assert "❌" in captured.out
        assert "FAIL" in captured.out
