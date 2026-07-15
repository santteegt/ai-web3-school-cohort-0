"""Tests for GuildTools — thin, agent-agnostic wrappers over ERC8004.

These confirm correct delegation only (identity_register() delegates to
erc8004.register_agent() with all fields passed through; identity_read_profile()
is a passthrough) — the underlying ERC8004 logic (schema building, the
setAgentURI backfill, idempotency) is covered in test_erc8004.py.
"""

from __future__ import annotations

import asyncio

from src.guild import tools as guild_tools


class TestIdentityRegister:
    def test_delegates_to_register_agent(self, monkeypatch):
        calls = []

        async def _fake_register_agent(**kwargs):
            calls.append(kwargs)
            return {
                "agent_id": 1,
                "agent_uri": "data:application/json;base64,ZmFrZQ==",
                "register_tx_hash": "0xabc",
                "update_tx_hash": "0xdef",
                "minted": True,
            }

        monkeypatch.setattr("src.shared.erc8004.register_agent", _fake_register_agent)

        result = asyncio.run(
            guild_tools.identity_register(
                name="Specialist Agent",
                description="desc",
                services=[{"name": "A2A", "endpoint": "http://localhost:10001/.well-known/agent-card.json"}],
                wallet_address="0x1234567890123456789012345678901234567890",
                image="https://example.com/logo.png",
                x402_support=True,
                active=True,
                registrations=None,
                supported_trust=["reputation"],
            )
        )

        assert calls == [
            {
                "name": "Specialist Agent",
                "description": "desc",
                "services": [
                    {"name": "A2A", "endpoint": "http://localhost:10001/.well-known/agent-card.json"}
                ],
                "wallet_address": "0x1234567890123456789012345678901234567890",
                "image": "https://example.com/logo.png",
                "x402_support": True,
                "active": True,
                "registrations": None,
                "supported_trust": ["reputation"],
            }
        ]
        assert result["agent_id"] == 1
        assert result["minted"] is True


class TestIdentityReadProfile:
    def test_passthrough_to_read_profile(self, monkeypatch):
        calls = []

        def _fake_read_profile(agent_id):
            calls.append(agent_id)
            return {"agent_id": agent_id, "name": "Specialist Agent"}

        monkeypatch.setattr("src.shared.erc8004.read_profile", _fake_read_profile)

        result = asyncio.run(guild_tools.identity_read_profile(agent_id=7))

        assert calls == [7]
        assert result == {"agent_id": 7, "name": "Specialist Agent"}
