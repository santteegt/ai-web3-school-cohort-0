"""Tests for NetworkConfig — config/networks.json loader.

Covers: CHAIN_ID resolution, contract address lookup, RPC URL construction
(with secret injection), explorer/easscan URL construction, unknown-chain-id
failure, and canonical-network detection.
"""

from __future__ import annotations

import pytest

from src.shared import network_config


@pytest.fixture(autouse=True)
def _clear_config_cache():
    """Each test gets a fresh load of config/networks.json."""
    network_config._load_raw_config.cache_clear()
    yield
    network_config._load_raw_config.cache_clear()


class TestChainIdResolution:
    def test_defaults_to_base_when_unset(self, monkeypatch):
        monkeypatch.delenv("CHAIN_ID", raising=False)
        assert network_config.get_chain_id() == "8453"

    def test_reads_chain_id_from_env(self, monkeypatch):
        monkeypatch.setenv("CHAIN_ID", "84532")
        assert network_config.get_chain_id() == "84532"


class TestNetworkConfigLookup:
    def test_known_chain_id_returns_config(self):
        cfg = network_config.get_network_config("8453")
        assert cfg["label"] == "Base"
        assert cfg["role"] == "canonical"

    def test_unknown_chain_id_raises(self):
        with pytest.raises(network_config.UnknownChainIdError):
            network_config.get_network_config("999999")

    def test_uses_active_chain_id_when_not_passed(self, monkeypatch):
        monkeypatch.setenv("CHAIN_ID", "84532")
        cfg = network_config.get_network_config()
        assert cfg["role"] == "isolated-test"


class TestContractAddress:
    def test_returns_known_contract(self):
        addr = network_config.get_contract_address("eas", chain_id="8453")
        assert addr == "0x4200000000000000000000000000000000000021"

    def test_same_address_on_both_networks_for_predeploys(self):
        base = network_config.get_contract_address("weth", chain_id="8453")
        sepolia = network_config.get_contract_address("weth", chain_id="84532")
        assert base == sepolia

    def test_unknown_contract_name_raises(self):
        with pytest.raises(network_config.UnknownChainIdError):
            network_config.get_contract_address("not_a_real_contract", chain_id="8453")


class TestRpcUrl:
    def test_injects_alchemy_api_key(self, monkeypatch):
        monkeypatch.setenv("ALCHEMY_API_KEY", "test-key-123")
        url = network_config.get_rpc_url(chain_id="8453")
        assert url == "https://base-mainnet.g.alchemy.com/v2/test-key-123"

    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.delenv("ALCHEMY_API_KEY", raising=False)
        with pytest.raises(RuntimeError):
            network_config.get_rpc_url(chain_id="8453")

    def test_different_subdomain_per_network(self, monkeypatch):
        monkeypatch.setenv("ALCHEMY_API_KEY", "k")
        base_url = network_config.get_rpc_url(chain_id="8453")
        sepolia_url = network_config.get_rpc_url(chain_id="84532")
        assert "base-mainnet" in base_url
        assert "base-sepolia" in sepolia_url


class TestExplorerUrls:
    def test_explorer_tx_url(self):
        url = network_config.get_explorer_tx_url("0xabc", chain_id="8453")
        assert url == "https://basescan.org/tx/0xabc"

    def test_sepolia_explorer_tx_url(self):
        url = network_config.get_explorer_tx_url("0xabc", chain_id="84532")
        assert url == "https://sepolia.basescan.org/tx/0xabc"

    def test_easscan_attestation_url(self):
        url = network_config.get_easscan_attestation_url("0xuid", chain_id="8453")
        assert url == "https://base.easscan.org/attestation/0xuid"


class TestDeliverySchemaUid:
    def test_falls_back_to_env_when_config_value_is_null(self, monkeypatch):
        monkeypatch.setenv("DELIVERY_SCHEMA_UID", "0xfromenv")
        assert network_config.get_delivery_schema_uid(chain_id="8453") == "0xfromenv"

    def test_returns_none_when_neither_set(self, monkeypatch):
        monkeypatch.delenv("DELIVERY_SCHEMA_UID", raising=False)
        assert network_config.get_delivery_schema_uid(chain_id="8453") is None


class TestIsCanonical:
    def test_base_is_canonical(self):
        assert network_config.is_canonical(chain_id="8453") is True

    def test_sepolia_is_not_canonical(self):
        assert network_config.is_canonical(chain_id="84532") is False
