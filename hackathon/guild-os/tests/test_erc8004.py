"""Tests for ERC8004 — IdentityRegistry registration + profile reads.

Covers the negative/idempotency scenarios added to
specs/scenarios/01_guild_formation.feature and 02_talent_discovery.feature
("Re-registering an already-registered agent is a no-op"), the
service-entry-based schema (capabilities/skills live on services[], not
top-level — a2aSkills on A2A, capabilities on MCP, skills/domains on OASF),
and register_agent()'s immediate setAgentURI() follow-up that backfills the
registrations[] self-reference after a fresh mint.

web3.py Contract objects are mocked directly (MagicMock) rather than hitting
a live RPC — the contract-call *shape* (function names, args) is what's
under test, not network behavior.
"""

from __future__ import annotations

import asyncio
import base64
import json
from unittest.mock import MagicMock

import pytest
from src.shared import erc8004
from src.shared.wallet import SignedTx

WALLET_ADDRESS = "0x1234567890123456789012345678901234567890"
AGENT_URI = "data:application/json;base64,eyJuYW1lIjoidGVzdCJ9"


class _FakeWallet:
    def __init__(self, tx_hash: str = "0xabc123"):
        self.tx_hash = tx_hash
        self.calls: list[dict] = []

    async def sign(self, tx):
        self.calls.append(tx)
        return SignedTx(tx_hash=self.tx_hash, status="Success", request_id="req")

    def register_guild_contract(self, guild_address: str) -> None:
        pass


@pytest.fixture(autouse=True)
def _isolate_cache(tmp_path, monkeypatch):
    """Point the registration cache at a tmp file so tests don't touch ./logs."""
    monkeypatch.setattr(erc8004, "REGISTRATIONS_CACHE_PATH", tmp_path / "erc8004_registrations.json")
    monkeypatch.setattr(erc8004, "_web3", lambda: object())
    yield


class TestBuildRegistrationUri:
    def test_roundtrip_minimal(self):
        services = [erc8004.build_a2a_service("http://localhost:10001/.well-known/agent-card.json")]
        uri = erc8004.build_registration_uri(
            name="Specialist Agent", description="Agentic AI x Web3 engineer.", services=services,
        )
        assert uri.startswith("data:application/json;base64,")
        _, _, payload = uri.partition(",")
        decoded = json.loads(base64.b64decode(payload))
        assert decoded["name"] == "Specialist Agent"
        assert decoded["services"] == services
        assert decoded["active"] is True
        assert decoded["type"] == "https://eips.ethereum.org/EIPS/eip-8004#registration-v1"
        # No top-level capabilities/skills — those live on services[] entries.
        assert "capabilities" not in decoded
        assert "skills" not in decoded
        # Optional fields omitted entirely when not supplied.
        assert "image" not in decoded
        assert "x402Support" not in decoded
        assert "registrations" not in decoded
        assert "supportedTrust" not in decoded

    def test_optional_fields_included_when_supplied(self):
        services = [erc8004.build_a2a_service("http://localhost:10000/.well-known/agent-card.json")]
        uri = erc8004.build_registration_uri(
            name="Orchestrator",
            description="desc",
            services=services,
            image="https://example.com/logo.png",
            x402_support=True,
            active=False,
            registrations=[{"agentId": 1, "agentRegistry": "eip155:8453:0xabc"}],
            supported_trust=["reputation"],
        )
        _, _, payload = uri.partition(",")
        decoded = json.loads(base64.b64decode(payload))
        assert decoded["image"] == "https://example.com/logo.png"
        assert decoded["x402Support"] is True
        assert decoded["active"] is False
        assert decoded["registrations"] == [{"agentId": 1, "agentRegistry": "eip155:8453:0xabc"}]
        assert decoded["supportedTrust"] == ["reputation"]


class TestServiceBuilders:
    def test_build_a2a_service(self):
        service = erc8004.build_a2a_service(
            "http://localhost:10001/.well-known/agent-card.json", a2a_skills=["coding_skills/text_to_code"]
        )
        assert service == {
            "name": "A2A",
            "endpoint": "http://localhost:10001/.well-known/agent-card.json",
            "version": "0.3.0",
            "a2aSkills": ["coding_skills/text_to_code"],
        }

    def test_build_a2a_service_without_skills(self):
        service = erc8004.build_a2a_service("http://localhost:10001/.well-known/agent-card.json")
        assert "a2aSkills" not in service

    def test_build_mcp_service(self):
        service = erc8004.build_mcp_service(
            "https://mcp.agent.eth/", tools=["search"], capabilities=["streaming"]
        )
        assert service["name"] == "MCP"
        assert service["mcpTools"] == ["search"]
        assert service["capabilities"] == ["streaming"]
        assert "mcpPrompts" not in service
        assert "mcpResources" not in service

    def test_build_oasf_service(self):
        service = erc8004.build_oasf_service(skills=["code-generation", "audit"], domains=["technology"])
        assert service == {
            "name": "OASF",
            "endpoint": "",
            "version": "0.8",
            "skills": ["code-generation", "audit"],
            "domains": ["technology"],
        }


class TestRegisterHappyPath:
    def test_mints_and_decodes_agent_id(self, monkeypatch):
        mock_identity = MagicMock()
        mock_identity.functions.balanceOf.return_value.call.return_value = 0
        mock_identity.encode_abi.return_value = "0xf2c298be"
        mock_identity.events.Registered.return_value.process_receipt.return_value = [
            {"args": {"agentId": 42}}
        ]
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        async def _fake_receipt(w3, tx_hash):
            return {"logs": []}

        monkeypatch.setattr(erc8004, "_get_receipt_with_retry", _fake_receipt)

        fake_wallet = _FakeWallet(tx_hash="0xnewtx")
        monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: fake_wallet)

        result = asyncio.run(erc8004.register(AGENT_URI, wallet_address=WALLET_ADDRESS))

        assert result == {"agent_id": 42, "tx_hash": "0xnewtx", "agent_uri": AGENT_URI, "minted": True}
        assert len(fake_wallet.calls) == 1
        cache = json.loads(erc8004.REGISTRATIONS_CACHE_PATH.read_text())
        assert cache[WALLET_ADDRESS.lower()]["agent_id"] == 42
        assert "minted" not in cache[WALLET_ADDRESS.lower()]


class TestRegisterIdempotency:
    def test_cache_hit_no_new_transaction(self, monkeypatch):
        mock_identity = MagicMock()
        mock_identity.functions.balanceOf.return_value.call.return_value = 1
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        cached_record = {"agent_id": 7, "tx_hash": "0xold", "agent_uri": AGENT_URI}
        erc8004.REGISTRATIONS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        erc8004.REGISTRATIONS_CACHE_PATH.write_text(
            json.dumps({WALLET_ADDRESS.lower(): cached_record})
        )

        fake_wallet = _FakeWallet()
        monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: fake_wallet)

        result = asyncio.run(erc8004.register(AGENT_URI, wallet_address=WALLET_ADDRESS))

        assert result == {**cached_record, "minted": False}
        assert fake_wallet.calls == []

    def test_cache_miss_recovers_from_event_log(self, monkeypatch):
        mock_identity = MagicMock()
        mock_identity.functions.balanceOf.return_value.call.return_value = 1
        mock_tx_hash = MagicMock()
        mock_tx_hash.hex.return_value = "0xrecoveredtx"
        mock_identity.events.Registered.return_value.get_logs.return_value = [
            {
                "args": {"agentId": 99, "agentURI": AGENT_URI},
                "transactionHash": mock_tx_hash,
            }
        ]
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        fake_wallet = _FakeWallet()
        monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: fake_wallet)

        result = asyncio.run(erc8004.register(AGENT_URI, wallet_address=WALLET_ADDRESS))

        assert result == {
            "agent_id": 99, "tx_hash": "0xrecoveredtx", "agent_uri": AGENT_URI, "minted": False,
        }
        assert fake_wallet.calls == []
        cache = json.loads(erc8004.REGISTRATIONS_CACHE_PATH.read_text())
        assert cache[WALLET_ADDRESS.lower()]["agent_id"] == 99

    def test_balance_positive_no_events_raises(self, monkeypatch):
        mock_identity = MagicMock()
        mock_identity.functions.balanceOf.return_value.call.return_value = 1
        mock_identity.events.Registered.return_value.get_logs.return_value = []
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        fake_wallet = _FakeWallet()
        monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: fake_wallet)

        with pytest.raises(erc8004.RegistrationStateError):
            asyncio.run(erc8004.register(AGENT_URI, wallet_address=WALLET_ADDRESS))

        assert fake_wallet.calls == []


class TestUpdateRegistrationUri:
    def test_calls_set_agent_uri_through_wallet_provider(self, monkeypatch):
        mock_identity = MagicMock()
        mock_identity.encode_abi.return_value = "0x0af28bd3"
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        fake_wallet = _FakeWallet(tx_hash="0xupdatetx")
        monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: fake_wallet)

        tx_hash = asyncio.run(erc8004.update_registration_uri(42, "data:application/json;base64,e30="))

        assert tx_hash == "0xupdatetx"
        mock_identity.encode_abi.assert_called_once_with(
            abi_element_identifier="setAgentURI", args=[42, "data:application/json;base64,e30="]
        )


class TestBuildRegistrationsEntry:
    def test_shape(self, monkeypatch):
        monkeypatch.setenv("CHAIN_ID", "8453")
        entry = erc8004.build_registrations_entry(42)
        assert entry["agentId"] == 42
        assert entry["agentRegistry"].startswith("eip155:8453:0x")


class TestRegisterAgent:
    def test_happy_path_backfills_registrations_via_set_agent_uri(self, monkeypatch):
        monkeypatch.setenv("CHAIN_ID", "8453")

        mock_identity = MagicMock()
        mock_identity.functions.balanceOf.return_value.call.return_value = 0
        mock_identity.encode_abi.return_value = "0xf2c298be"
        mock_identity.events.Registered.return_value.process_receipt.return_value = [
            {"args": {"agentId": 42}}
        ]
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        async def _fake_receipt(w3, tx_hash):
            return {"logs": []}

        monkeypatch.setattr(erc8004, "_get_receipt_with_retry", _fake_receipt)

        fake_wallet = _FakeWallet(tx_hash="0xregtx")
        monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: fake_wallet)

        update_calls = []

        async def _fake_update(agent_id, new_uri):
            update_calls.append((agent_id, new_uri))
            return "0xupdatetx"

        monkeypatch.setattr(erc8004, "update_registration_uri", _fake_update)

        services = [erc8004.build_a2a_service("http://localhost:10001/.well-known/agent-card.json")]
        result = asyncio.run(
            erc8004.register_agent(
                name="Specialist Agent", description="desc", services=services,
                wallet_address=WALLET_ADDRESS,
            )
        )

        assert result["agent_id"] == 42
        assert result["register_tx_hash"] == "0xregtx"
        assert result["update_tx_hash"] == "0xupdatetx"
        assert result["minted"] is True

        # The setAgentURI follow-up fired exactly once, with the self-reference merged in.
        assert len(update_calls) == 1
        updated_agent_id, updated_uri = update_calls[0]
        assert updated_agent_id == 42
        _, _, payload = updated_uri.partition(",")
        decoded = json.loads(base64.b64decode(payload))
        assert decoded["registrations"] == [erc8004.build_registrations_entry(42)]
        assert result["agent_uri"] == updated_uri

        # Cache ends up holding the FINAL uri, not the initial one.
        cache = json.loads(erc8004.REGISTRATIONS_CACHE_PATH.read_text())
        assert cache[WALLET_ADDRESS.lower()]["agent_uri"] == updated_uri

    def test_idempotent_path_skips_set_agent_uri(self, monkeypatch):
        mock_identity = MagicMock()
        mock_identity.functions.balanceOf.return_value.call.return_value = 1
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        cached_record = {"agent_id": 7, "tx_hash": "0xold", "agent_uri": AGENT_URI}
        erc8004.REGISTRATIONS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        erc8004.REGISTRATIONS_CACHE_PATH.write_text(
            json.dumps({WALLET_ADDRESS.lower(): cached_record})
        )

        update_calls = []

        async def _fake_update(agent_id, new_uri):
            update_calls.append((agent_id, new_uri))
            return "0xshouldnothappen"

        monkeypatch.setattr(erc8004, "update_registration_uri", _fake_update)

        services = [erc8004.build_a2a_service("http://localhost:10001/.well-known/agent-card.json")]
        result = asyncio.run(
            erc8004.register_agent(
                name="Specialist Agent", description="desc", services=services,
                wallet_address=WALLET_ADDRESS,
            )
        )

        assert result["agent_id"] == 7
        assert result["update_tx_hash"] is None
        assert result["minted"] is False
        assert update_calls == []


class TestReadProfile:
    def _mock_contracts(self, monkeypatch, registration: dict, delivery_count: int = 0):
        raw = json.dumps(registration).encode()
        data_uri = "data:application/json;base64," + base64.b64encode(raw).decode()

        mock_identity = MagicMock()
        mock_identity.functions.tokenURI.return_value.call.return_value = data_uri
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        mock_reputation = MagicMock()
        mock_reputation.functions.getSummary.return_value.call.return_value = (delivery_count, 0, 0)
        monkeypatch.setattr(erc8004, "_reputation_registry_contract", lambda w3: mock_reputation)

    def test_a2a_only(self, monkeypatch):
        registration = {
            "name": "Specialist Agent",
            "services": [
                erc8004.build_a2a_service(
                    "http://localhost:10001/.well-known/agent-card.json",
                    a2a_skills=["coding_skills/text_to_code"],
                )
            ],
        }
        self._mock_contracts(monkeypatch, registration)

        profile = erc8004.read_profile(1)

        assert profile["name"] == "Specialist Agent"
        assert profile["capabilities"] == ["coding_skills/text_to_code"]
        assert profile["domains"] == []
        assert profile["a2a_endpoint"] == "http://localhost:10001/.well-known/agent-card.json"
        assert profile["delivery_count"] == 0

    def test_oasf_only(self, monkeypatch):
        registration = {
            "name": "Specialist Agent",
            "services": [erc8004.build_oasf_service(skills=["code-generation", "audit"], domains=["technology"])],
        }
        self._mock_contracts(monkeypatch, registration)

        profile = erc8004.read_profile(1)

        assert profile["capabilities"] == ["code-generation", "audit"]
        assert profile["domains"] == ["technology"]
        assert profile["a2a_endpoint"] is None

    def test_combined_a2a_and_oasf_deduped(self, monkeypatch):
        registration = {
            "name": "Specialist Agent",
            "services": [
                erc8004.build_a2a_service(
                    "http://localhost:10001/.well-known/agent-card.json", a2a_skills=["audit"]
                ),
                erc8004.build_oasf_service(skills=["audit", "code-generation"], domains=["technology"]),
            ],
        }
        self._mock_contracts(monkeypatch, registration)

        profile = erc8004.read_profile(1)

        # "audit" appears in both A2A and OASF — deduped, order-preserving.
        assert profile["capabilities"] == ["audit", "code-generation"]
        assert profile["domains"] == ["technology"]
        assert profile["a2a_endpoint"] == "http://localhost:10001/.well-known/agent-card.json"

    def test_unresolvable_https_uri_returns_partial_profile(self, monkeypatch):
        import httpx

        mock_identity = MagicMock()
        mock_identity.functions.tokenURI.return_value.call.return_value = "https://example.invalid/card.json"
        monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

        mock_reputation = MagicMock()
        mock_reputation.functions.getSummary.return_value.call.return_value = (0, 0, 0)
        monkeypatch.setattr(erc8004, "_reputation_registry_contract", lambda w3: mock_reputation)

        def _raise_connect_error(*args, **kwargs):
            raise httpx.ConnectError("simulated failure")

        monkeypatch.setattr(httpx, "get", _raise_connect_error)

        profile = erc8004.read_profile(1)

        assert profile["name"] is None
        assert profile["capabilities"] == []
        assert profile["domains"] == []
        assert profile["a2a_endpoint"] is None
        assert profile["agent_uri"] == "https://example.invalid/card.json"


class TestNotesDirPath:
    def test_notes_dir_resolves_to_guild_os_root_logs(self):
        from src.shared import guild_context

        assert erc8004.NOTES_DIR.name == "logs"
        # Mirrors guild_context.CONTEXT_PATH's 3-parent convention — both
        # should resolve to the guild-os/ project root's sibling paths.
        assert erc8004.NOTES_DIR.parent == guild_context.CONTEXT_PATH.parent
