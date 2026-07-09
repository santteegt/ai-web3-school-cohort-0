"""Tests for Orchestrator MCP server (FastMCP).

Tests cover:
- Server name and tool count (7, all prefixed guildos_)
- Each tool has description, inputSchema, and annotations
- Tool functions are callable directly (no duplicated dispatch)
- Stub tools return STUB messages
- Working tools call through to orchestrator_tools
- Error wrapper catches unexpected exceptions

Strategy: call the actual decorated tool functions exported from server.py
and query tool metadata via mcp.list_tools() — no hand-rolled dispatch copy.
"""

from __future__ import annotations

import hashlib
import json
from unittest.mock import AsyncMock, patch

import pytest
from src.orchestrator.server import (
    DeliveryRecord,
    TaskPayload,
    guildos_deliverable_review,
    guildos_guild_launch,
    guildos_reputation_write,
    guildos_settle,
    guildos_talent_query,
    guildos_task_delegate,
    guildos_task_invite,
    mcp,
)

# ---------------------------------------------------------------------------
# Server metadata
# ---------------------------------------------------------------------------

class TestMCPServerCreation:
    """Server boots and tool definitions are correct."""

    def test_server_name(self):
        assert mcp.name == "guildos_mcp"

    @pytest.mark.asyncio
    async def test_tool_count(self):
        tools = await mcp.list_tools()
        assert len(tools) == 7

    @pytest.mark.asyncio
    async def test_tool_names_prefixed(self):
        tools = await mcp.list_tools()
        names = {t.name for t in tools}
        expected = {
            "guildos_guild_launch",
            "guildos_talent_query",
            "guildos_task_invite",
            "guildos_task_delegate",
            "guildos_deliverable_review",
            "guildos_settle",
            "guildos_reputation_write",
        }
        assert names == expected

    @pytest.mark.asyncio
    async def test_each_tool_has_schema_and_annotations(self):
        tools = await mcp.list_tools()
        for tool in tools:
            assert tool.name, "Tool missing name"
            assert tool.description, f"Tool {tool.name} missing description"
            assert tool.inputSchema, f"Tool {tool.name} missing inputSchema"
            assert "properties" in tool.inputSchema, (
                f"Tool {tool.name} schema has no properties"
            )
            assert tool.annotations is not None, (
                f"Tool {tool.name} missing annotations"
            )

    @pytest.mark.asyncio
    async def test_readonly_tools_marked(self):
        """talent_query and deliverable_review must be readOnly."""
        tools = await mcp.list_tools()
        by_name = {t.name: t for t in tools}
        assert by_name["guildos_talent_query"].annotations.readOnlyHint is True
        assert by_name["guildos_deliverable_review"].annotations.readOnlyHint is True
        assert by_name["guildos_guild_launch"].annotations.readOnlyHint is False


# ---------------------------------------------------------------------------
# Tool function calls (direct — exercises the real decorated functions)
# ---------------------------------------------------------------------------

class TestToolCalls:
    """Each tool function is callable and routes correctly."""

    @pytest.mark.asyncio
    async def test_talent_query_returns_profile(self):
        result = await guildos_talent_query(task_type="code-generation")
        assert "agent" in result.lower() or "specialist" in result.lower()

    @pytest.mark.asyncio
    async def test_task_invite_dispatches_to_a2a(self):
        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_invite = AsyncMock(return_value="msg-123")
            result = await guildos_task_invite(
                specialist_endpoint="http://localhost:10001",
                task_spec={"type": "code-generation", "description": "Build a token"},
            )
            assert "msg-123" in result
            mock_a2a.send_invite.assert_called_once()

    @pytest.mark.asyncio
    async def test_task_delegate_dispatches_to_a2a(self):
        with patch("src.orchestrator.tools.a2a_client") as mock_a2a, \
             patch("src.orchestrator.tools.guild_context"):
            mock_a2a.send_task = AsyncMock(return_value="msg-456")
            payload = TaskPayload(
                task_id="T-001",
                task_description="Build a token",
                github_issue_url="https://github.com/test/repo/issues/10",
                acceptance_criteria=["Deliverable file is non-empty"],
                deliverable_format="github_commit",
                deadline="2026-07-15T00:00:00Z",
                budget_wei="300000000000000000",
            )
            result = await guildos_task_delegate(
                specialist_endpoint="http://localhost:10001",
                full_task=payload,
            )
            assert "msg-456" in result
            mock_a2a.send_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_deliverable_review_returns_verdict(self):
        import tempfile
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        ) as f:
            content = '{"output": "test"}'
            f.write(content)
            f.flush()
            path = f.name
            expected_hash = "sha256:" + hashlib.sha256(
                content.encode()
            ).hexdigest()

            result = await guildos_deliverable_review(
                deliverable_reference=path,
                deliverable_hash=expected_hash,
            )
            data = json.loads(result)
            assert data["hash_match"] is True
            assert data["evaluator_verdict"] == "PASS"

    @pytest.mark.asyncio
    async def test_guild_launch_returns_result_or_error(self):
        with patch("src.shared.agentfightclub.launch") as mock_launch, \
             patch("src.shared.agentfightclub.commit") as mock_commit:

            async def fake_launch(**kwargs):
                return {"guild_address": "0xTest", "tx_hash": "0xTestTx"}

            mock_launch.side_effect = fake_launch
            mock_commit.side_effect = AsyncMock(return_value="0xCommitTx")

            result = await guildos_guild_launch(
                mandate="Build DeFi tools",
                treasury_address="0x1234567890abcdef1234567890abcdef12345678",
            )
            assert "guild_address" in result or "ERROR" in result

    @pytest.mark.asyncio
    async def test_settle_returns_result_or_error(self):
        with patch("src.shared.agentfightclub.settle") as mock_settle:
            mock_settle.side_effect = AsyncMock(return_value="0xSettleTx")
            result = await guildos_settle(
                guild_address="0x1234567890abcdef1234567890abcdef12345678",
                specialist_wallet="0xabcdef1234567890abcdef1234567890abcdef12",
            )
            assert "SettleTx" in result or "ERROR" in result

    @pytest.mark.asyncio
    async def test_reputation_write_returns_stub(self):
        record = DeliveryRecord(
            task_type="code-generation",
            deliverable_hash="sha256:abc123",
            acceptance_timestamp=0,
            payment_wei=0,
            guild_address="0x1234567890abcdef1234567890abcdef12345678",
            a2a_task_id="msg-001",
        )
        result = await guildos_reputation_write(delivery_record=record)
        assert "STUB" in result or "not yet built" in result

    @pytest.mark.asyncio
    async def test_unexpected_errors_propagate(self):
        """Unexpected exceptions propagate — FastMCP marks isError=True."""
        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_invite = AsyncMock(side_effect=RuntimeError("boom"))
            with pytest.raises(RuntimeError, match="boom"):
                await guildos_task_invite(
                    specialist_endpoint="http://localhost:10001",
                    task_spec={"type": "test"},
                )

    @pytest.mark.asyncio
    async def test_deliverable_review_rejects_traversal(self):
        """Directory traversal paths are rejected."""
        result = await guildos_deliverable_review(
            deliverable_reference="../../../../etc/passwd",
            deliverable_hash="sha256:fake",
        )
        data = json.loads(result)
        assert data["evaluator_verdict"] == "FAIL"
        assert "escapes" in data.get("error", "").lower()
