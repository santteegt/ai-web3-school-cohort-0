"""WalletProvider — provider-agnostic signing with Pact-scoped authority.

Every on-chain call an agent makes goes through this layer. The Pact
allowlist scopes exactly:
  - DAO contract: sponsor, propose, vote, process (Moloch v3 governance)
  - ERC-8004 IdentityRegistry: register, setAgentURI (agent identity)
  - Tribute: the only call with a value cap

The default implementation wraps Cobo Agentic Wallet (CAW). The CAW
server-side Pact enforces the allowlist via target_in + function_id
selectors with default-deny semantics — an operation not explicitly
covered by a policy is automatically denied. This class mirrors that
check locally for fast, clear rejection before hitting the network.

No raw EOA fallback exists. If the configured provider is unavailable,
the run halts (specs/10-technical-design.md §8 F4). ZeroDev/Turnkey are
swappable via WALLET_PROVIDER, preserving the same allowlist + cap
behavior with no other code changes.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Protocol, TypedDict, runtime_checkable
from uuid import uuid4

from src.shared import network_config

logger = logging.getLogger(__name__)

PACT_CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "pact.json"

POLL_INTERVAL = 3.0
PACT_ACTIVE = "active"
PACT_TERMINAL = {"rejected", "expired", "revoked", "completed"}
TX_SUCCESS = {"Success", "Completed"}
TX_TERMINAL = {"Failed", "Rejected", "Cancelled"}


class WalletProviderError(RuntimeError):
    """Base error for all wallet provider failures."""


class PolicyDeniedError(WalletProviderError):
    """A transaction was rejected by the Pact allowlist or tribute cap.

    Raised locally before the transaction reaches CAW, or wrapped from a
    CAW server-side policy denial.
    """


class WalletProviderUnavailableError(WalletProviderError):
    """The configured wallet provider cannot be initialized or reached.

    No raw EOA fallback — the caller must halt until a scoped provider
    is restored (specs/10-technical-design.md §8 F4).
    """


class UnsignedTx(TypedDict):
    """Unsigned transaction from moloch-agent --build-only --full."""

    to: str
    data: str
    value: str
    chainId: int


@dataclass
class SignedTx:
    """Result of a signed and broadcast transaction."""

    tx_hash: str | None = None
    status: str = "Initiated"
    request_id: str = ""


class PactAllowlist:
    """Local representation of the Pact policy.

    Defines which (contract_address, function_selector) pairs the agent
    may call, plus the tribute value cap. CAW's server-side Pact mirrors
    this exactly via target_in entries — this local copy provides fast
    rejection with clear error messages before hitting the network.
    """

    def __init__(self) -> None:
        self._contracts: dict[str, set[str]] = {}
        self._tribute_cap: str | None = None

    def add_contract(self, address: str, selectors: set[str]) -> None:
        addr = address.lower()
        if addr not in self._contracts:
            self._contracts[addr] = set()
        self._contracts[addr] |= selectors

    def set_tribute_cap(self, cap: str) -> None:
        self._tribute_cap = cap

    def check(self, to: str, selector: str, value: str = "0") -> None:
        """Raise PolicyDeniedError if the call is outside the allowlist."""
        addr = to.lower()
        allowed = self._contracts.get(addr)
        if allowed is None:
            raise PolicyDeniedError(
                f"Contract {addr} is not on the Pact allowlist"
            )
        if selector not in allowed:
            raise PolicyDeniedError(
                f"Function selector {selector} is not allowlisted on {addr}"
            )
        if self._tribute_cap and _value_exceeds_cap(value, self._tribute_cap):
            raise PolicyDeniedError(
                f"Tribute value {value} exceeds cap {self._tribute_cap}"
            )

    def build_pact_spec(
        self,
        caw_chain_id: str,
        completion_conditions: list[dict[str, str]],
        always_review: bool,
    ) -> dict[str, Any]:
        target_in: list[dict[str, str]] = []
        for addr, selectors in sorted(self._contracts.items()):
            for sel in sorted(selectors):
                target_in.append(
                    {
                        "chain_id": caw_chain_id,
                        "contract_addr": addr,
                        "function_id": sel,
                    }
                )
        rules: dict[str, Any] = {
            "effect": "allow",
            "when": {
                "chain_in": [caw_chain_id],
                "target_in": target_in,
            },
        }
        if always_review:
            rules["always_review"] = True
        if self._tribute_cap:
            rules["deny_if"] = {"amount_gt": self._tribute_cap}
        return {
            "policies": [
                {
                    "name": "guildos-scoped-authority",
                    "type": "contract_call",
                    "rules": rules,
                }
            ],
            "completion_conditions": completion_conditions,
        }


@runtime_checkable
class WalletProviderProtocol(Protocol):
    """The swappable seam — all agents sign through this interface."""

    async def sign(self, tx: UnsignedTx) -> SignedTx: ...

    def register_guild_contract(self, guild_address: str) -> None: ...


class CoboWalletProvider:
    """Cobo Agentic Wallet (CAW) implementation of WalletProviderProtocol.

    Submits a per-session Pact covering all allowlisted contracts, then
    signs each transaction through the pact-scoped CAW API key. The CAW
    server-side Pact enforces target_in + function_id with default-deny;
    this class mirrors that check locally for fast, clear errors.

    Requires AGENT_WALLET_API_KEY, AGENT_WALLET_WALLET_ID, and
    AGENT_WALLET_ADDRESS in the environment. Run
    ``caw wallet current --show-api-key`` to obtain them.
    """

    def __init__(self) -> None:
        self._api_url = os.getenv(
            "AGENT_WALLET_API_URL", "https://api.agenticwallet.cobo.com"
        )
        self._api_key = os.getenv("AGENT_WALLET_API_KEY", "")
        self._wallet_id = os.getenv("AGENT_WALLET_WALLET_ID", "")
        self._wallet_addr = os.getenv("AGENT_WALLET_ADDRESS", "")
        self._pact: dict[str, Any] | None = None
        self._allowlist = _build_default_allowlist()

    def register_guild_contract(self, guild_address: str) -> None:
        """Add the dynamic guild/DAO contract to the allowlist.

        Called after guild_launch() returns the DAO address. The guild's
        sponsor/propose/vote/process selectors are added to the Pact scope.
        If a Pact was already submitted, the next sign() submits a fresh
        one with the expanded allowlist.
        """
        self._allowlist.add_contract(guild_address, _load_moloch_selectors())
        self._pact = None
        logger.info("Guild %s registered in Pact allowlist", guild_address)

    async def sign(self, tx: UnsignedTx) -> SignedTx:
        """Sign and broadcast a transaction through the CAW Pact.

        Raises PolicyDeniedError if the call is outside the local allowlist
        or rejected by the CAW server-side Pact. Raises
        WalletProviderUnavailableError if CAW credentials are missing.
        """
        selector = _extract_selector(tx["data"])
        self._allowlist.check(tx["to"], selector, tx.get("value", "0"))

        if not self._api_key or not self._wallet_id:
            raise WalletProviderUnavailableError(
                "AGENT_WALLET_API_KEY and AGENT_WALLET_WALLET_ID must be set — "
                "run `caw wallet current --show-api-key` to obtain them"
            )

        from cobo_agentic_wallet import WalletAPIClient

        async with WalletAPIClient(
            base_url=self._api_url, api_key=self._api_key
        ) as client:
            pact = await self._ensure_pact(client)

            pact_client = WalletAPIClient(
                base_url=self._api_url, api_key=pact["api_key"]
            )
            try:
                request_id = f"guildos-{uuid4().hex[:12]}"
                await pact_client.contract_call(
                    self._wallet_id,
                    src_addr=self._wallet_addr,
                    chain_id=self._caw_chain_id(),
                    contract_addr=tx["to"],
                    calldata=tx["data"],
                    value=tx.get("value", "0"),
                    request_id=request_id,
                )
                logger.info("Tx submitted via CAW (request_id: %s)", request_id)
                return await self._wait_for_tx(client, request_id)
            finally:
                await pact_client.close()

    async def _ensure_pact(self, client: Any) -> dict[str, Any]:
        """Submit and wait for Pact approval if not already active."""
        if self._pact and self._pact.get("status") == PACT_ACTIVE:
            return self._pact

        spec = self._allowlist.build_pact_spec(
            self._caw_chain_id(),
            _load_pact_config()["completion_conditions"],
            _load_pact_config()["always_review"],
        )
        pact = await client.submit_pact(
            wallet_id=self._wallet_id,
            intent="GuildOS scoped signing authority",
            spec=spec,
            name="guildos-wallet-provider",
        )
        pact_id = pact["pact_id"]
        logger.info("Pact %s submitted — approve in CAW app", pact_id)

        while True:
            pact = await client.get_pact(pact_id)
            status = pact.get("status", "")
            if status == PACT_ACTIVE:
                logger.info("Pact %s active", pact_id)
                self._pact = pact
                return pact
            if status in PACT_TERMINAL:
                raise WalletProviderUnavailableError(
                    f"Pact {pact_id} ended with status: {status}"
                )
            await asyncio.sleep(POLL_INTERVAL)

    async def _wait_for_tx(
        self, client: Any, request_id: str, timeout: int = 120
    ) -> SignedTx:
        elapsed = 0.0
        while elapsed < timeout:
            record = await client.get_user_transaction_by_request_id(
                self._wallet_id, request_id
            )
            status = record.get("status_display", record.get("status", ""))
            tx_hash = record.get("transaction_hash")
            if status in TX_SUCCESS:
                logger.info("Tx confirmed: %s", tx_hash)
                return SignedTx(
                    tx_hash=tx_hash, status=status, request_id=request_id
                )
            if status in TX_TERMINAL:
                raise WalletProviderError(
                    f"Transaction {request_id} failed: {status}"
                )
            await asyncio.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL
        raise WalletProviderError(
            f"Transaction {request_id} not confirmed within {timeout}s"
        )

    def _caw_chain_id(self) -> str:
        return _load_pact_config()["caw_chain_id"]


class StubWalletProvider:
    """Placeholder for unimplemented providers (ZeroDev, Turnkey).

    Preserves the swappable seam — selecting these via WALLET_PROVIDER
    fails fast with a clear message instead of silently using CAW.
    """

    _name: str

    def __init__(self, name: str) -> None:
        self._name = name

    async def sign(self, tx: UnsignedTx) -> SignedTx:
        raise NotImplementedError(
            f"WALLET_PROVIDER={self._name} is declared swappable but not yet "
            f"implemented — use 'caw' for now"
        )

    def register_guild_contract(self, guild_address: str) -> None:
        raise NotImplementedError(
            f"WALLET_PROVIDER={self._name} is declared swappable but not yet "
            f"implemented — use 'caw' for now"
        )


def get_wallet_provider() -> WalletProviderProtocol:
    """Return the configured WalletProvider implementation.

    Selected by WALLET_PROVIDER env var (default: caw). ZeroDev/Turnkey
    are swappable via the StubWalletProvider seam — they raise
    NotImplementedError, preserving the interface without a partial impl.
    """
    name = os.getenv("WALLET_PROVIDER", "caw").lower()
    if name == "caw":
        return CoboWalletProvider()
    raise WalletProviderUnavailableError(
        f"WALLET_PROVIDER={name} is not supported. Known: caw"
    )


def _value_exceeds_cap(value: str, cap: str) -> bool:
    try:
        return float(value) > float(cap)
    except (ValueError, TypeError):
        return False


def _extract_selector(data: str) -> str:
    """Extract the 4-byte function selector (0x + 8 hex chars) from calldata."""
    if not data or len(data) < 10:
        return ""
    return data[:10]


@lru_cache(maxsize=1)
def _load_pact_config() -> dict[str, Any]:
    chain_id = network_config.get_chain_id()
    with open(PACT_CONFIG_PATH) as f:
        data = json.load(f)
    if chain_id not in data:
        raise WalletProviderError(
            f"CHAIN_ID={chain_id} has no entry in config/pact.json"
        )
    return data[chain_id]


def _load_moloch_selectors() -> set[str]:
    moloch = _load_pact_config()["selectors"]["moloch"]
    return {
        moloch["sponsor"],
        moloch["propose"],
        moloch["vote"],
        moloch["process"],
    }


def _load_erc8004_selectors() -> set[str]:
    erc8004 = _load_pact_config()["selectors"]["erc8004"]
    return {erc8004["register"], erc8004["setAgentURI"]}


def _build_default_allowlist() -> PactAllowlist:
    """Build the initial allowlist from static contract addresses + pact.json."""
    allowlist = PactAllowlist()
    cfg = _load_pact_config()

    erc8004_addr = network_config.get_contract_address("erc8004_identity_registry")
    allowlist.add_contract(erc8004_addr, _load_erc8004_selectors())

    afc_addr = network_config.get_contract_address("afc_summoner")
    summon_sel = {cfg["selectors"]["moloch"]["summon"]}
    allowlist.add_contract(afc_addr, summon_sel)

    allowlist.set_tribute_cap(cfg["tribute_cap"])
    return allowlist
