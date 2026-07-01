"""NetworkConfig — loads per-network on-chain settings from config/networks.json.

Components must never hardcode a contract address, RPC URL, or explorer link.
Read CHAIN_ID from the environment, then call into this module to resolve
everything network-specific. Secrets (ALCHEMY_API_KEY, private keys) stay in
the environment and are substituted into the RPC URL template here — they are
never written into config/networks.json.

See docs/RISKS.md §F6 and AGENTS.md "Don't: Hardcode chain_id" for why this
exists — CHAIN_ID must be the single switch between Base (canonical,
submission-evidence) and Base Sepolia (isolated component testing only).
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "networks.json"

DEFAULT_CHAIN_ID = "8453"


class UnknownChainIdError(RuntimeError):
    """Raised when CHAIN_ID has no entry in config/networks.json."""


@lru_cache(maxsize=1)
def _load_raw_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_chain_id() -> str:
    """Return the active CHAIN_ID from the environment (default: Base, 8453)."""
    return os.getenv("CHAIN_ID", DEFAULT_CHAIN_ID)


def get_network_config(chain_id: str | None = None) -> dict:
    """Return the full network config block for the given (or active) chain_id.

    Raises:
        UnknownChainIdError: if chain_id has no entry in config/networks.json.
    """
    cid = chain_id or get_chain_id()
    raw = _load_raw_config()
    if cid not in raw:
        known = [k for k in raw if not k.startswith("_")]
        raise UnknownChainIdError(
            f"CHAIN_ID={cid} has no entry in config/networks.json. Known: {known}"
        )
    return raw[cid]


def get_contract_address(name: str, chain_id: str | None = None) -> str:
    """Return a contract address by logical name for the given (or active) network.

    Args:
        name: one of "erc8004_identity_registry", "erc8004_reputation_registry",
              "eas", "eas_schema_registry", "weth".
    """
    network = get_network_config(chain_id)
    try:
        return network["contracts"][name]
    except KeyError:
        raise UnknownChainIdError(
            f"Contract '{name}' not defined for CHAIN_ID={chain_id or get_chain_id()}"
        ) from None


def get_rpc_url(chain_id: str | None = None) -> str:
    """Build the RPC URL for the given (or active) network, injecting ALCHEMY_API_KEY.

    Raises:
        RuntimeError: if ALCHEMY_API_KEY is not set.
    """
    network = get_network_config(chain_id)
    api_key = os.getenv("ALCHEMY_API_KEY", "")
    if not api_key:
        raise RuntimeError("ALCHEMY_API_KEY env var not set — cannot build RPC URL")
    return network["rpc_url_template"].format(ALCHEMY_API_KEY=api_key)


def get_explorer_tx_url(tx_hash: str, chain_id: str | None = None) -> str:
    """Build the full Basescan (or network-equivalent) tx URL."""
    network = get_network_config(chain_id)
    return network["explorer_tx_url"] + tx_hash


def get_easscan_attestation_url(uid: str, chain_id: str | None = None) -> str:
    """Build the full easscan attestation URL."""
    network = get_network_config(chain_id)
    return network["easscan_attestation_url"] + uid


def get_delivery_schema_uid(chain_id: str | None = None) -> str | None:
    """Return the registered DELIVERY_SCHEMA_UID for the given (or active) network.

    Falls back to the DELIVERY_SCHEMA_UID env var if config/networks.json has
    not been updated with the registered UID yet (e.g. immediately after a
    fresh schema registration before the config file is committed).
    """
    network = get_network_config(chain_id)
    return network.get("delivery_schema_uid") or os.getenv("DELIVERY_SCHEMA_UID") or None


def is_canonical(chain_id: str | None = None) -> bool:
    """True if the given (or active) network is the canonical evidence network."""
    return get_network_config(chain_id).get("role") == "canonical"
