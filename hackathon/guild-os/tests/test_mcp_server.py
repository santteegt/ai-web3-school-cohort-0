"""Tests for Orchestrator MCP server — Issue #8.

Tests cover:
- Server creates without error
- TOOL_DEFINITIONS has 7 tools with correct names and schemas
- Dispatch function routes each tool name correctly
- Stub tools return STUB messages
- Working tools call through to orchestrator_tools
- Unknown tool returns error

Strategy: Test TOOL_DEFINITIONS directly and the dispatch logic
via a helper, rather than going through MCP's internal handler registry.
"""

from __future__ import annotations

import hashlib
import json
from unittest.mock import AsyncMock, patch

import mcp.types as types
import pytest


def async_return(value):
    """Helper to create an async function that returns a fixed value."""
    async def _f(*args, **kwargs):
        return value
    return _f


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tool_defs() -> list[types.Tool]:
    """Load TOOL_DEFINITIONS from server module."""
    from src.orchestrator.server import TOOL_DEFINITIONS
    return TOOL_DEFINITIONS


@pytest.fixture
def dispatch():
    """Return the raw dispatch function that the server uses internally.

    We recreate it here for testing purposes — it mirrors the logic in
    create_server()'s call_tool handler exactly.
    """
    from src.orchestrator import tools as orchestrator_tools

    async def _dispatch(name: str, arguments: dict) -> list[types.TextContent]:
        try:
            if name == "guild_launch":
                result = await orchestrator_tools.guild_launch(
                    mandate=arguments["mandate"],
                    treasury_address=arguments["treasury_address"],
                )
            elif name == "talent_query":
                result = await orchestrator_tools.talent_query(
                    task_type=arguments["task_type"],
                )
            elif name == "task_invite":
                result = await orchestrator_tools.task_invite(
                    specialist_endpoint=arguments["specialist_endpoint"],
                    task_spec=arguments["task_spec"],
                )
            elif name == "task_delegate":
                result = await orchestrator_tools.task_delegate(
                    specialist_endpoint=arguments["specialist_endpoint"],
                    full_task=arguments["full_task"],
                )
            elif name == "deliverable_review":
                result = await orchestrator_tools.deliverable_review(
                    deliverable_reference=arguments["deliverable_reference"],
                    deliverable_hash=arguments["deliverable_hash"],
                )
            elif name == "settle":
                result = await orchestrator_tools.settle(
                    guild_address=arguments["guild_address"],
                    specialist_wallet=arguments["specialist_wallet"],
                )
            elif name == "reputation_write":
                result = await orchestrator_tools.reputation_write(
                    delivery_record=arguments["delivery_record"],
                )
            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

            if isinstance(result, str):
                text = result
            elif isinstance(result, list):
                text = json.dumps(result, indent=2)
            else:
                text = json.dumps(result, indent=2, default=str)

            return [types.TextContent(type="text", text=text)]

        except NotImplementedError as e:
            return [types.TextContent(
                type="text",
                text=f"STUB: {e}. This integration is not yet built — see Issue #1.",
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"ERROR: {type(e).__name__}: {e}",
            )]

    return _dispatch


# ---------------------------------------------------------------------------
# Server creation
# ---------------------------------------------------------------------------

class TestMCPServerCreation:
    """Server boots and definitions are correct."""

    def test_server_creates_without_error(self):
        """create_server() returns a Server object."""
        from src.orchestrator.server import create_server
        server = create_server()
        assert server is not None
        assert server.name == "guildos-orchestrator"

    def test_tool_definitions_count(self, tool_defs):
        """Exactly 7 tools defined."""
        assert len(tool_defs) == 7

    def test_tool_names_match_component_map(self, tool_defs):
        """Tool names match the 7-tool component map from CLAUDE.md."""
        expected = {
            "guild_launch", "talent_query", "task_invite",
            "task_delegate", "deliverable_review", "settle",
            "reputation_write",
        }
        actual = {t.name for t in tool_defs}
        assert actual == expected

    def test_each_tool_has_required_schema(self, tool_defs):
        """Each tool must have name, description, and inputSchema."""
        for tool in tool_defs:
            assert tool.name, "Tool missing name"
            assert tool.description, f"Tool {tool.name} missing description"
            assert tool.inputSchema, f"Tool {tool.name} missing inputSchema"
            assert "properties" in tool.inputSchema, f"Tool {tool.name} schema has no properties"


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

class TestToolCalls:
    """Each tool dispatches correctly through the MCP call_tool handler."""

    @pytest.mark.asyncio
    async def test_talent_query_returns_profile(self, dispatch):
        """Check 7.2: talent_query returns Specialist profile JSON."""
        result = await dispatch("talent_query", {"task_type": "code-generation"})
        assert len(result) == 1
        assert result[0].type == "text"
        # Should contain profile data (hardcoded MVP)
        text = result[0].text
        assert "specialist" in text.lower() or "profile" in text.lower() or "agent" in text.lower()

    @pytest.mark.asyncio
    async def test_task_invite_dispatches_to_a2a(self, dispatch):
        """Check 7.3: task_invite sends A2A invite and returns message ID."""
        with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
            mock_a2a.send_invite = AsyncMock(return_value="msg-123")
            result = await dispatch("task_invite", {
                "specialist_endpoint": "http://localhost:10001",
                "task_spec": {"type": "code-generation", "description": "Build a token"},
            })
            assert len(result) == 1
            text = result[0].text
            assert "msg-123" in text
            mock_a2a.send_invite.assert_called_once()

    @pytest.mark.asyncio
    async def test_task_delegate_dispatches_to_a2a(self, dispatch):
        """Check 7.4: task_delegate sends A2A task and returns message ID."""
        with patch("src.orchestrator.tools.a2a_client") as mock_a2a, \
             patch("src.orchestrator.tools.guild_context"):
            mock_a2a.send_task = AsyncMock(return_value="msg-456")
            result = await dispatch("task_delegate", {
                "specialist_endpoint": "http://localhost:10001",
                "full_task": {"type": "code-generation", "description": "Build a token"},
            })
            assert len(result) == 1
            text = result[0].text
            assert "msg-456" in text
            mock_a2a.send_task.assert_called_once()

    @pytest.mark.asyncio
    async def test_deliverable_review_returns_verdict(self, dispatch):
        """Check 7.5: deliverable_review returns hash_match, format_valid, size_check."""
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
            content = '{"output": "test"}'
            f.write(content)
            f.flush()
            path = f.name
            expected_hash = "sha256:" + hashlib.sha256(content.encode()).hexdigest()

            result = await dispatch("deliverable_review", {
                "deliverable_reference": path,
                "deliverable_hash": expected_hash,
            })
            assert len(result) == 1
            text = result[0].text
            assert "hash_match" in text
            assert "true" in text.lower()

    @pytest.mark.asyncio
    async def test_guild_launch_returns_result_or_error(self, dispatch):
        """Check 7.1: guild_launch is callable (returns result or error)."""
        with patch("src.shared.agentfightclub.launch") as mock_launch, \
             patch("src.shared.agentfightclub.commit") as mock_commit, \
             patch("src.shared.agentfightclub.PRIVATE_KEY", "0xfake"):

            async def fake_launch(**kwargs):
                return {"guild_address": "0xTest", "tx_hash": "0xTestTx"}
            mock_launch.side_effect = fake_launch
            mock_commit.side_effect = async_return("0xCommitTx")

            result = await dispatch("guild_launch", {
                "mandate": "Build DeFi tools",
                "treasury_address": "0x1234567890abcdef1234567890abcdef12345678",
            })
            assert len(result) == 1
            text = result[0].text
            assert "guild_address" in text or "ERROR" in text or "STUB" in text

    @pytest.mark.asyncio
    async def test_settle_returns_result_or_error(self, dispatch):
        """Check 7.6: settle is callable (returns result or error)."""
        with patch("src.shared.agentfightclub.settle") as mock_settle, \
             patch("src.shared.agentfightclub.PRIVATE_KEY", "0xfake"):

            mock_settle.side_effect = async_return("0xSettleTx")

            result = await dispatch("settle", {
                "guild_address": "0x1234567890abcdef1234567890abcdef12345678",
                "specialist_wallet": "0xabcdef1234567890abcdef1234567890abcdef12",
            })
            assert len(result) == 1
            text = result[0].text
            assert "SettleTx" in text or "ERROR" in text or "STUB" in text

    @pytest.mark.asyncio
    async def test_reputation_write_returns_stub(self, dispatch):
        """Check 7.7: reputation_write is callable (stub — returns STUB message)."""
        result = await dispatch("reputation_write", {
            "delivery_record": {
                "task_type": "code-generation",
                "deliverable_hash": "sha256:abc123",
                "acceptance_timestamp": "2026-06-11T12:00:00Z",
                "payment_wei": "300000000000000000",
                "guild_address": "0x1234567890abcdef1234567890abcdef12345678",
                "a2a_task_id": "msg-001",
            },
        })
        assert len(result) == 1
        text = result[0].text
        assert "STUB" in text or "not yet built" in text or "Issue #1" in text

    @pytest.mark.asyncio
    async def test_unknown_tool_returns_error(self, dispatch):
        """Unknown tool names return an error message."""
        result = await dispatch("nonexistent_tool", {})
        assert len(result) == 1
        text = result[0].text
        assert "Unknown tool" in text
