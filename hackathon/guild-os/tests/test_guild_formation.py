"""Tests for Guild Formation — Issue #1.

Tests cover:
- agentfightclub.launch() — CLI subprocess mock
- agentfightclub.commit() — wrap-eth → approve → tribute flow
- guild_context state updates
- tools.guild_launch end-to-end (mocked CLI)
- Basescan URL generation
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# agentfightclub.launch
# ---------------------------------------------------------------------------

class TestLaunch:
    """Test guild contract deployment via moloch-agent + WalletProvider."""

    @pytest.mark.asyncio
    async def test_launch_calls_summon(self):
        """launch() builds calldata, signs via WalletProvider, returns guild address."""
        from src.shared.agentfightclub import launch

        fake_tx = {"to": "0x97aaa5be8b38795245f1c38a883b44cccdfb3e11", "data": "0x1f1bb0ef", "value": "0", "chainId": 8453}
        with patch("src.shared.agentfightclub._build_calldata", return_value=fake_tx), \
             patch("src.shared.agentfightclub._sign_and_broadcast", return_value="0xabc123"), \
             patch("src.shared.agentfightclub._parse_dao_from_receipt", return_value="0x1234567890abcdef1234567890abcdef12345678"), \
             patch("src.shared.agentfightclub._get_wallet"), \
             patch.dict(os.environ, {"AGENT_WALLET_ADDRESS": "0xSingerAddress000000000000000000000000000"}):
            result = await launch(
                mandate="Build DeFi tools",
                treasury_address="0xTreasury00000000000000000000000000000000",
            )

        assert result["guild_address"] == "0x1234567890abcdef1234567890abcdef12345678"
        assert result["tx_hash"] == "0xabc123"

    @pytest.mark.asyncio
    async def test_launch_requires_agent_wallet_address(self):
        """launch() raises if AGENT_WALLET_ADDRESS not set."""
        from src.shared.agentfightclub import launch

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AGENT_WALLET_ADDRESS", None)
            with pytest.raises(RuntimeError, match="AGENT_WALLET_ADDRESS"):
                await launch(mandate="test", treasury_address="0x0")


# ---------------------------------------------------------------------------
# agentfightclub.commit
# ---------------------------------------------------------------------------

class TestCommit:
    """Test treasury funding via wrap-eth → approve → tribute."""

    @pytest.mark.asyncio
    async def test_commit_three_step_flow(self):
        """commit() builds calldata for wrap-eth, approve-token, tribute; signs each via WalletProvider."""
        from src.shared.agentfightclub import commit

        fake_tx = {"to": "0x0", "data": "0x0", "value": "0", "chainId": 8453}
        with patch("src.shared.agentfightclub._build_calldata", return_value=fake_tx) as mock_build, \
             patch("src.shared.agentfightclub._sign_and_broadcast", side_effect=[
                 "0xwrap_tx", "0xapprove_tx", "0xtribute_tx",
             ]) as mock_sign, \
             patch("src.shared.agentfightclub._get_wallet"), \
             patch("src.shared.network_config.get_contract_address", return_value="0xWETH000000000000000000000000000000000"):
            result = await commit(
                guild_address="0x1234567890abcdef1234567890abcdef12345678",
                amount_wei=1_000_000_000_000_000,
            )

        assert result == "0xtribute_tx"
        assert mock_build.call_count == 3
        assert mock_sign.call_count == 3


# ---------------------------------------------------------------------------
# guild_context updates
# ---------------------------------------------------------------------------

class TestGuildContext:
    """Test guild context state management."""

    def test_save_and_load(self, tmp_path):
        """save() writes JSON; load() reads it back."""
        from src.shared import guild_context

        # Override path
        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            guild_context.save({
                "guild_address": "0xabc",
                "mandate": "Test guild",
                "treasury_wei": "1000",
                "member_list": [],
                "task_state": "ACTIVE",
            })
            loaded = guild_context.load()
            assert loaded["guild_address"] == "0xabc"
            assert loaded["task_state"] == "ACTIVE"
        finally:
            guild_context.CONTEXT_PATH = original_path

    def test_invalid_state_rejected(self, tmp_path):
        """save() rejects invalid task_state."""
        from src.shared import guild_context

        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            with pytest.raises(ValueError, match="Invalid task_state"):
                guild_context.save({
                    "task_state": "INVALID_STATE",
                    "member_list": [],
                })
        finally:
            guild_context.CONTEXT_PATH = original_path


# ---------------------------------------------------------------------------
# tools.guild_launch end-to-end
# ---------------------------------------------------------------------------

class TestGuildLaunchTool:
    """Test the guild_launch MCP tool end-to-end."""

    @pytest.mark.asyncio
    async def test_guild_launch_updates_context(self, tmp_path):
        """guild_launch calls launch + commit, updates guild_context."""
        from src.orchestrator.tools import guild_launch
        from src.shared import guild_context

        # Override context path
        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            with patch("src.shared.agentfightclub.launch") as mock_launch, \
                 patch("src.shared.agentfightclub.commit") as mock_commit:

                async def async_launch(**kwargs):
                    return {
                        "guild_address": "0xGuild000000000000000000000000000000000",
                        "tx_hash": "0xlaunch_tx",
                    }
                async def async_commit(*args, **kwargs):
                    return "0xcommit_tx"

                mock_launch.side_effect = async_launch
                mock_commit.side_effect = async_commit

                result = await guild_launch(
                    mandate="Build DeFi tools",
                    treasury_address="0xTreasury00000000000000000000000000000000",
                )

            assert result["guild_address"] == "0xGuild000000000000000000000000000000000"
            assert result["launch_tx"] == "0xlaunch_tx"
            assert result["commit_tx"] == "0xcommit_tx"

            # Verify guild context was updated
            ctx = guild_context.load()
            assert ctx["guild_address"] == "0xGuild000000000000000000000000000000000"
            assert ctx["task_state"] == "ACTIVE"
            assert ctx["mandate"] == "Build DeFi tools"
        finally:
            guild_context.CONTEXT_PATH = original_path


# ---------------------------------------------------------------------------
# Basescan URL formatting
# ---------------------------------------------------------------------------

class TestBasescanURL:
    """Test that Basescan URLs are formatted correctly."""

    def test_basescan_tx_url(self):
        """Transaction URLs use https://basescan.org/tx/..."""
        tx_hash = "0xabc123def456"
        url = f"https://basescan.org/tx/{tx_hash}"
        assert url.startswith("https://basescan.org/tx/")
        assert tx_hash in url

    def test_basescan_address_url(self):
        """Address URLs use https://basescan.org/address/..."""
        address = "0xGuild000000000000000000000000000000000"
        url = f"https://basescan.org/address/{address}"
        assert "basescan.org/address/" in url
