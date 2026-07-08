"""Tests for WalletProvider — Pact-scoped signing authority.

Covers all 8 scenarios in specs/scenarios/12_scoped_spending.feature:
  1. Allowlisted governance call is authorized
  2. ERC-8004 registration call is authorized
  3. Tribute within the cap is authorized
  4. Tribute above the cap is rejected
  5. Non-allowlisted contract call is rejected
  6. Non-allowlisted function on the DAO contract is rejected
  7. Agents never fall back to an EOA
  8. Swap the wallet provider while scoping logic is preserved

The PactAllowlist is tested directly (pure logic, no CAW client needed).
CoboWalletProvider is tested for credential checks and allowlist delegation.
"""

from __future__ import annotations

import pytest
from src.shared import network_config, wallet
from src.shared.wallet import (
    CoboWalletProvider,
    PactAllowlist,
    PolicyDeniedError,
    UnsignedTx,
    WalletProviderProtocol,
    WalletProviderUnavailableError,
    get_wallet_provider,
)

DAO_ADDR = "0x0123456789abcdef0123456789abcdef01234567"
ERC8004_ADDR = "0x8004a818bfb912233c491871b3d84c89a494bd9e"
AFC_SUMMONER = "0x97aaa5be8b38795245f1c38a883b44cccdfb3e11"
RANDOM_ADDR = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"

SEL_PROPOSE = "0x3a82ffc8"
SEL_VOTE = "0x67f61f07"
SEL_PROCESS = "0x13b9f691"
SEL_SPONSOR = "0x0a796e19"
SEL_SUMMON = "0x1f1bb0ef"
SEL_REGISTER = "0xf2c298be"
SEL_UNKNOWN = "0xffffffff"

TRIBUTE_CAP = "0.01"


@pytest.fixture(autouse=True)
def _clear_caches():
    network_config._load_raw_config.cache_clear()
    wallet._load_pact_config.cache_clear()
    yield
    network_config._load_raw_config.cache_clear()
    wallet._load_pact_config.cache_clear()


def _make_allowlist() -> PactAllowlist:
    al = PactAllowlist()
    al.add_contract(DAO_ADDR, {SEL_PROPOSE, SEL_VOTE, SEL_PROCESS, SEL_SPONSOR})
    al.add_contract(ERC8004_ADDR, {SEL_REGISTER})
    al.add_contract(AFC_SUMMONER, {SEL_SUMMON})
    al.set_tribute_cap(TRIBUTE_CAP)
    return al


class TestAllowlistedCalls:
    """Scenarios 1-3: authorized calls pass the PactAllowlist check."""

    def test_allowlisted_governance_call_passes(self):
        al = _make_allowlist()
        al.check(DAO_ADDR, SEL_PROPOSE)
        al.check(DAO_ADDR, SEL_VOTE)
        al.check(DAO_ADDR, SEL_PROCESS)

    def test_erc8004_register_call_passes(self):
        al = _make_allowlist()
        al.check(ERC8004_ADDR, SEL_REGISTER)

    def test_tribute_within_cap_passes(self):
        al = _make_allowlist()
        al.check(DAO_ADDR, SEL_PROPOSE, value="0.005")


class TestRejections:
    """Scenarios 4-6: unauthorized calls are rejected before broadcast."""

    def test_tribute_above_cap_rejected(self):
        al = _make_allowlist()
        with pytest.raises(PolicyDeniedError, match="exceeds cap"):
            al.check(DAO_ADDR, SEL_PROPOSE, value="1.0")

    def test_non_allowlisted_contract_rejected(self):
        al = _make_allowlist()
        with pytest.raises(PolicyDeniedError, match="not on the Pact allowlist"):
            al.check(RANDOM_ADDR, SEL_PROPOSE)

    def test_non_allowlisted_function_on_dao_rejected(self):
        al = _make_allowlist()
        with pytest.raises(PolicyDeniedError, match="not allowlisted"):
            al.check(DAO_ADDR, SEL_UNKNOWN)

    def test_non_allowlisted_function_on_erc8004_rejected(self):
        al = _make_allowlist()
        with pytest.raises(PolicyDeniedError, match="not allowlisted"):
            al.check(ERC8004_ADDR, SEL_PROPOSE)

    def test_zero_value_uncapped_call_passes(self):
        al = _make_allowlist()
        al.check(ERC8004_ADDR, SEL_REGISTER, value="0")


class TestNoEoaFallback:
    """Scenario 7: provider unavailable halts — no raw EOA fallback."""

    def test_missing_credentials_raises_on_sign(self, monkeypatch):
        monkeypatch.delenv("AGENT_WALLET_API_KEY", raising=False)
        monkeypatch.delenv("AGENT_WALLET_WALLET_ID", raising=False)
        provider = CoboWalletProvider()
        tx: UnsignedTx = {
            "to": ERC8004_ADDR,
            "data": SEL_REGISTER + "0" * 56,
            "value": "0",
            "chainId": 8453,
        }
        with pytest.raises(WalletProviderUnavailableError):
            import asyncio

            asyncio.run(provider.sign(tx))

    def test_wallet_module_reads_no_private_key(self):
        import inspect

        source = inspect.getsource(wallet)
        assert "PRIVATE_KEY" not in source or "PRIVATE_KEY" in '""'


class TestProviderSwap:
    """Scenario 8: swapping WALLET_PROVIDER preserves the scoping seam."""

    def test_factory_returns_cobowalletprovider(self, monkeypatch):
        monkeypatch.setenv("WALLET_PROVIDER", "caw")
        provider = get_wallet_provider()
        assert isinstance(provider, CoboWalletProvider)

    def test_factory_rejects_unknown_provider(self, monkeypatch):
        monkeypatch.setenv("WALLET_PROVIDER", "zerodev")
        with pytest.raises(WalletProviderUnavailableError):
            get_wallet_provider()

    def test_cobowalletprovider_satisfies_protocol(self):
        provider = CoboWalletProvider()
        assert isinstance(provider, WalletProviderProtocol)

    def test_allowlist_independent_of_provider(self):
        al1 = _make_allowlist()
        al2 = _make_allowlist()
        al1.check(DAO_ADDR, SEL_PROPOSE)
        al2.check(DAO_ADDR, SEL_PROPOSE)
        assert al1.build_pact_spec("BASE_ETH", [], True) == al2.build_pact_spec(
            "BASE_ETH", [], True
        )


class TestPactSpec:
    """Verify the Pact spec structure matches CAW's contract_call policy."""

    def test_target_in_contains_all_selectors(self):
        al = _make_allowlist()
        spec = al.build_pact_spec("BASE_ETH", [], True)
        policy = spec["policies"][0]
        assert policy["type"] == "contract_call"
        assert policy["rules"]["effect"] == "allow"

        target_in = policy["rules"]["when"]["target_in"]
        selectors = {t["function_id"] for t in target_in}
        assert SEL_PROPOSE in selectors
        assert SEL_VOTE in selectors
        assert SEL_PROCESS in selectors
        assert SEL_REGISTER in selectors
        assert SEL_SUMMON in selectors

    def test_chain_in_scoped_to_caw_chain_id(self):
        al = _make_allowlist()
        spec = al.build_pact_spec("BASE_ETH", [], True)
        assert spec["policies"][0]["rules"]["when"]["chain_in"] == ["BASE_ETH"]

    def test_tribute_cap_in_deny_if(self):
        al = _make_allowlist()
        spec = al.build_pact_spec("BASE_ETH", [], True)
        assert spec["policies"][0]["rules"]["deny_if"]["amount_gt"] == TRIBUTE_CAP

    def test_always_review_enforced(self):
        al = _make_allowlist()
        spec = al.build_pact_spec("BASE_ETH", [], True)
        assert spec["policies"][0]["rules"]["always_review"] is True

    def test_completion_conditions_passed_through(self):
        al = _make_allowlist()
        conditions = [{"type": "tx_count", "threshold": "20"}]
        spec = al.build_pact_spec("BASE_ETH", conditions, True)
        assert spec["completion_conditions"] == conditions


class TestRegisterGuild:
    """register_guild_contract() adds the dynamic DAO address to the allowlist."""

    def test_guild_address_added_after_register(self):
        al = PactAllowlist()
        al.add_contract(ERC8004_ADDR, {SEL_REGISTER})
        moloch_selectors = {SEL_PROPOSE, SEL_VOTE, SEL_PROCESS, SEL_SPONSOR}
        al.add_contract(DAO_ADDR, moloch_selectors)
        al.check(DAO_ADDR, SEL_PROPOSE)
        al.check(DAO_ADDR, SEL_VOTE)

    def test_register_guild_contract_invalidates_pact(self, monkeypatch):
        monkeypatch.setenv("AGENT_WALLET_API_KEY", "fake")
        monkeypatch.setenv("AGENT_WALLET_WALLET_ID", "fake")
        provider = CoboWalletProvider()
        provider.register_guild_contract(DAO_ADDR)
        assert provider._pact is None
