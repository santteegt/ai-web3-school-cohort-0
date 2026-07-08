"""Tests for Specialist Membership — Issue #2.

Tests cover:
- agentfightclub.propose() — mint-shares CLI subprocess mock
- agentfightclub.vote() — sponsor + vote CLI flow
- tools.membership_propose — end-to-end with guild_context update
- tools.membership_vote — end-to-end with member_list update
- Gate 1 CLI halt behavior
- guild_context state transitions
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------------------
# agentfightclub.propose
# ---------------------------------------------------------------------------

class TestPropose:
    """Test Specialist membership proposal via moloch-agent + WalletProvider."""

    @pytest.mark.asyncio
    async def test_propose_calls_mint_shares(self):
        """propose() builds mint-shares calldata, signs via WalletProvider, returns proposal ID."""
        from src.shared.agentfightclub import propose

        fake_tx = {"to": "0x0", "data": "0x0", "value": "0", "chainId": 8453}
        with patch("src.shared.agentfightclub._build_calldata", return_value=fake_tx), \
             patch("src.shared.agentfightclub._sign_and_broadcast", return_value="0xpropose_tx"), \
             patch("src.shared.agentfightclub._read_latest_proposal_id", return_value="42"), \
             patch("src.shared.agentfightclub._get_wallet"):
            with patch.dict(os.environ, {"SPECIALIST_WALLET_ADDRESS": "0xSpecialist0000000000000000000000000000000"}):
                result = await propose(
                    guild_address="0xGuild000000000000000000000000000000000",
                    specialist_erc8004_id=1,
                )

        assert result == "42"

    @pytest.mark.asyncio
    async def test_propose_requires_specialist_wallet(self):
        """propose() raises if SPECIALIST_WALLET_ADDRESS not set."""
        from src.shared.agentfightclub import propose

        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SPECIALIST_WALLET_ADDRESS", None)
            with pytest.raises(RuntimeError, match="SPECIALIST_WALLET_ADDRESS"):
                await propose(guild_address="0x0", specialist_erc8004_id=1)


# ---------------------------------------------------------------------------
# agentfightclub.vote
# ---------------------------------------------------------------------------

class TestVote:
    """Test Specialist membership vote via moloch-agent + WalletProvider."""

    @pytest.mark.asyncio
    async def test_vote_sponsor_and_vote(self):
        """vote() builds sponsor + vote calldata, signs each via WalletProvider."""
        from src.shared.agentfightclub import vote

        fake_tx = {"to": "0x0", "data": "0x0", "value": "0", "chainId": 8453}
        with patch("src.shared.agentfightclub._build_calldata", return_value=fake_tx) as mock_build, \
             patch("src.shared.agentfightclub._sign_and_broadcast", side_effect=["0xsponsor_tx", "0xvote_tx"]) as mock_sign, \
             patch("src.shared.agentfightclub._get_wallet"):
            result = await vote(
                guild_address="0xGuild000000000000000000000000000000000",
                proposal_id="42",
                approve=True,
            )

        assert result == "0xvote_tx"
        assert mock_build.call_count == 2
        assert mock_sign.call_count == 2

    @pytest.mark.asyncio
    async def test_vote_continues_if_sponsor_fails(self):
        """vote() continues even if sponsor fails (already sponsored)."""
        from src.shared.agentfightclub import vote

        fake_tx = {"to": "0x0", "data": "0x0", "value": "0", "chainId": 8453}

        build_call_count = 0

        def build_side_effect(*args, **kwargs):
            nonlocal build_call_count
            build_call_count += 1
            if build_call_count == 1:
                raise RuntimeError("already sponsored")
            return fake_tx

        with patch("src.shared.agentfightclub._build_calldata", side_effect=build_side_effect), \
             patch("src.shared.agentfightclub._sign_and_broadcast", return_value="0xvote_tx"), \
             patch("src.shared.agentfightclub._get_wallet"):
            result = await vote(
                guild_address="0xGuild000000000000000000000000000000000",
                proposal_id="42",
            )

        assert result == "0xvote_tx"


# ---------------------------------------------------------------------------
# tools.membership_propose
# ---------------------------------------------------------------------------

class TestMembershipProposeTool:
    """Test membership_propose MCP tool end-to-end."""

    @pytest.mark.asyncio
    async def test_membership_propose_updates_context(self, tmp_path):
        """membership_propose calls propose and updates guild_context."""
        from src.orchestrator.tools import membership_propose
        from src.shared import guild_context

        original_path = guild_context.CONTEXT_PATH
        test_file = tmp_path / "guild_context.json"
        guild_context.CONTEXT_PATH = test_file

        try:
            # Initialize context
            guild_context.save({
                "guild_address": "0xGuild000000000000000000000000000000000",
                "mandate": "Test",
                "treasury_wei": "1000",
                "member_list": [],
                "task_state": "ACTIVE",
            })

            with patch("src.shared.agentfightclub.propose") as mock_propose, \
                  patch.dict(os.environ, {"SPECIALIST_WALLET_ADDRESS": "0xSpec00000000000000000000000000000000000"}):

                async def fake_propose(*args, **kwargs):
                    return "99"
                mock_propose.side_effect = fake_propose

                result = await membership_propose(
                    guild_address="0xGuild000000000000000000000000000000000",
                    specialist_erc8004_id=1,
                )

            assert result["proposal_id"] == "99"
            assert result["status"] == "proposed"

            # Verify guild context updated
            ctx = guild_context.load()
            assert ctx["proposal_id"] == "99"
        finally:
            guild_context.CONTEXT_PATH = original_path


# ---------------------------------------------------------------------------
# tools.membership_vote
# ---------------------------------------------------------------------------

class TestMembershipVoteTool:
    """Test membership_vote MCP tool end-to-end."""

    @pytest.mark.asyncio
    async def test_membership_vote_adds_to_member_list(self, tmp_path):
        """membership_vote adds Specialist to member_list on approval."""
        from src.orchestrator.tools import membership_vote
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
                "proposal_id": "99",
            })

            with patch("src.shared.agentfightclub.vote") as mock_vote, \
                 patch.dict(os.environ, {"SPECIALIST_WALLET_ADDRESS": "0xSpec00000000000000000000000000000000000"}):

                async def fake_vote(*args, **kwargs):
                    return "0xvote_tx"
                mock_vote.side_effect = fake_vote

                result = await membership_vote(
                    guild_address="0xGuild000000000000000000000000000000000",
                    proposal_id="99",
                    approve=True,
                )

            assert result["vote_tx"] == "0xvote_tx"
            assert result["approved"] is True
            assert "0xSpec00000000000000000000000000000000000" in result["member_list"]

            # Verify guild context updated
            ctx = guild_context.load()
            assert "0xSpec00000000000000000000000000000000000" in ctx["member_list"]
        finally:
            guild_context.CONTEXT_PATH = original_path

    @pytest.mark.asyncio
    async def test_membership_vote_rejection_no_member(self, tmp_path):
        """membership_vote does not add member on rejection."""
        from src.orchestrator.tools import membership_vote
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
                "proposal_id": "99",
            })

            with patch("src.shared.agentfightclub.vote") as mock_vote:

                async def fake_vote(*args, **kwargs):
                    return "0xvote_tx"
                mock_vote.side_effect = fake_vote

                result = await membership_vote(
                    guild_address="0xGuild000000000000000000000000000000000",
                    proposal_id="99",
                    approve=False,
                )

            assert result["approved"] is False
            assert "member_list" not in result

            # member_list should remain empty
            ctx = guild_context.load()
            assert ctx["member_list"] == []
        finally:
            guild_context.CONTEXT_PATH = original_path


# ---------------------------------------------------------------------------
# Gate 1 CLI behavior
# ---------------------------------------------------------------------------

class TestGate1:
    """Test Gate 1 — membership approval CLI gate."""

    def test_gate_1_displays_profile(self):
        """Gate 1 shows Specialist ERC-8004 profile."""
        from src.cli.gates import gate_1_membership

        profile = {
            "name": "Specialist Agent",
            "agent_id": "erc8004:1",
            "capabilities": ["code-generation", "audit"],
        }

        with patch("builtins.input", return_value="y"):
            result = gate_1_membership(profile)
            assert result is True

    def test_gate_1_rejection(self):
        """Gate 1 returns False on rejection."""
        from src.cli.gates import gate_1_membership

        profile = {"name": "Bad Agent", "capabilities": []}

        with patch("builtins.input", return_value="n"):
            result = gate_1_membership(profile)
            assert result is False

    def test_gate_1_empty_input_is_rejection(self):
        """Gate 1 treats empty input as rejection (never auto-proceeds)."""
        from src.cli.gates import gate_1_membership

        with patch("builtins.input", return_value=""):
            result = gate_1_membership({"name": "Test"})
            assert result is False
