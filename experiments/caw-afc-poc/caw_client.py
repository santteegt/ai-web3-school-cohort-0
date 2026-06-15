"""
CAW client for Moloch-Agent PoC.

Wraps the Cobo Agentic Wallet SDK to:
  1. Submit a pact (scoped to specific contracts) and wait for human approval.
  2. Execute a contract call using the calldata returned by moloch-agent --build-only.
  3. Wait for on-chain confirmation and return the tx hash.

No private key is ever held by this process — signing lives in the CAW TSS node.
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from uuid import uuid4

logger = logging.getLogger(__name__)

POLL_INTERVAL = 3.0
PACT_TERMINAL = {"rejected", "expired", "revoked", "completed"}
TX_SUCCESS = {"Success"}
TX_TERMINAL = {"Failed", "Rejected", "Cancelled"}

PACT_CONFIG_PATH = Path(__file__).parent / "pact-config.json"


def _save_pact_config(pact: dict, intent: str, allowed_contracts: list[str]) -> None:
    """Append active pact metadata to pact-config.json as a list of records."""
    records = json.loads(PACT_CONFIG_PATH.read_text()) if PACT_CONFIG_PATH.exists() else []
    records.append({
        "pact_id": pact.get("pact_id"),
        "status": pact.get("status"),
        "intent": intent,
        "allowed_contracts": allowed_contracts,
    })
    PACT_CONFIG_PATH.write_text(json.dumps(records, indent=2))
    logger.info(f"  💾 Pact config saved to {PACT_CONFIG_PATH.name}")


@dataclass
class TxResult:
    request_id: str
    tx_hash: Optional[str] = None
    status: str = "Initiated"


class CawClient:
    """
    Async Cobo Agentic Wallet client.

    Usage:
        async with CawClient() as caw:
            pact = await caw.submit_and_wait_pact(intent, contracts)
            result = await caw.execute_calldata(pact, moloch_tx, description)
            print(result.tx_hash)
    """

    def __init__(self):
        self.api_url = os.getenv("AGENT_WALLET_API_URL", "https://api.agenticwallet.cobo.com")
        self.api_key = os.getenv("AGENT_WALLET_API_KEY")
        self.wallet_id = os.getenv("AGENT_WALLET_WALLET_ID")
        if not self.api_key or not self.wallet_id:
            raise ValueError(
                "AGENT_WALLET_API_KEY and AGENT_WALLET_WALLET_ID must be set. "
                "Run `caw wallet current --show-api-key` to get them."
            )
        self._client = None

    async def __aenter__(self):
        from cobo_agentic_wallet import WalletAPIClient
        self._client = WalletAPIClient(base_url=self.api_url, api_key=self.api_key)
        return self

    async def __aexit__(self, *_):
        if self._client:
            await self._client.close()

    async def submit_and_wait_pact(
        self,
        intent: str,
        allowed_contracts: list[str],
        tx_count: int = 1,
        timeout: int = 300,
    ) -> dict:
        """
        Submit a contract_call pact and block until the owner approves it
        in the Cobo Agentic Wallet app.

        Returns the active pact dict — use pact["api_key"] for transactions.
        """
        from pact import make_pact_spec
        spec = make_pact_spec(allowed_contracts, tx_count=tx_count)
        pact = await self._client.submit_pact(
            wallet_id=self.wallet_id,
            intent=intent,
            spec=spec,
            name=f"caw-afc-{intent[:40]}",
        )
        pact_id = pact["pact_id"]
        logger.info(f"📱 Pact {pact_id} submitted — approve in the Cobo app")
        print(f"  📱 Approval required: {intent}")
        print(f"     Pact ID: {pact_id}")
        print(f"     Allowed contracts: {allowed_contracts}")
        print(f"  ⏳ Waiting for human approval (timeout: {timeout}s)...")

        elapsed = 0.0
        while elapsed < timeout:
            pact = await self._client.get_pact(pact_id)
            logger.info(f"Pact status: {pact}")
            status = pact.get("status", "")
            if status == "active":
                logger.info(f"  ✓ Pact {pact_id} active")
                _save_pact_config(pact, intent, allowed_contracts)
                return pact
            if status in PACT_TERMINAL:
                raise RuntimeError(f"❌ Pact {pact_id} ended with status: {status}")
            await asyncio.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL

        raise TimeoutError(f"Pact {pact_id} not approved within {timeout}s")

    async def execute_calldata(
        self,
        src_addr:  str,
        pact: dict,
        tx: dict,
        
        description: str = "",
        tx_timeout: int = 120,
    ) -> TxResult:
        """
        Submit a contract call using the pact-scoped API key, then wait for
        on-chain confirmation.

        Args:
            pact: Active pact dict (must contain "api_key").
            tx: Unsigned tx dict from moloch-agent --build-only --full:
                { "to": "0x...", "data": "0x...", "value": "0", "chainId": 8453 }
            description: Human-readable label for the tx.
            tx_timeout: Seconds to wait for on-chain confirmation.

        Returns:
            TxResult with tx_hash once confirmed.
        """
        logger.info("> Calling execute_calldata...")
        from cobo_agentic_wallet import WalletAPIClient
        pact_client = WalletAPIClient(base_url=self.api_url, api_key=pact["api_key"])
        request_id = f"caw-afc-{uuid4().hex[:12]}"
        try:
            await pact_client.contract_call(
                self.wallet_id,
                src_addr=src_addr,
                chain_id="BASE_ETH",
                contract_addr=tx["to"],
                calldata=tx["data"],
                value=tx.get("value", "0"),
                request_id=request_id,
                description=description or None,
            )
            print(f"  📤 Tx submitted (request_id: {request_id})")
            return await self._wait_for_tx(request_id, tx_timeout)
        finally:
            await pact_client.close()

    async def _wait_for_tx(
        self,
        request_id: str,
        timeout: int,
    ) -> TxResult:
        elapsed = 0.0
        from cobo_agentic_wallet import WalletAPIClient
        while elapsed < timeout:
            record = await self._client.get_user_transaction_by_request_id(self.wallet_id, request_id)
            status = record.get("status_display", "")
            status_code = record.get("status")
            tx_hash = record.get("transaction_hash")
            if status in TX_SUCCESS:
                print(f"  ✓ Tx confirmed: (Code: {status_code}) {tx_hash}")
                return TxResult(request_id=request_id, tx_hash=tx_hash, status=status)
            if status in TX_TERMINAL:
                raise RuntimeError(f"❌ Tx {request_id} failed with status: {status}")
            await asyncio.sleep(POLL_INTERVAL)
            elapsed += POLL_INTERVAL
        raise TimeoutError(f"Tx {request_id} not on-chain within {timeout}s")


class MockCawClient:
    """
    Mock CAW client for offline testing without live credentials.

    Simulates pact approval and tx confirmation without any network calls.
    """

    def __init__(self, auto_approve: bool = True):
        self.auto_approve = auto_approve
        self._pact_counter = 0
        self._tx_counter = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass

    async def submit_and_wait_pact(
        self,
        intent: str,
        allowed_contracts: list[str],
        tx_count: int = 1,
        timeout: int = 300,
    ) -> dict:
        self._pact_counter += 1
        pact_id = f"mock-pact-{self._pact_counter:04d}"
        print(f"  [mock] Pact submitted: {pact_id} — {intent}")
        if not self.auto_approve:
            confirm = input(f"  Approve pact for '{intent}'? (y/n): ").strip().lower()
            if confirm != "y":
                raise RuntimeError(f"❌ Pact {pact_id} rejected by user")
        print(f"  [mock] Pact {pact_id} approved")
        pact = {"pact_id": pact_id, "api_key": "mock-pact-api-key", "status": "active"}
        _save_pact_config(pact, intent, allowed_contracts)
        return pact

    async def execute_calldata(
        self,
        pact: dict,
        tx: dict,
        description: str = "",
        tx_timeout: int = 120,
    ) -> TxResult:
        self._tx_counter += 1
        request_id = f"mock-req-{self._tx_counter:04d}"
        # mock_hash = f"0x{'dead' * 8}{self._tx_counter:04x}"
        mock_hash = "0x15286c10368004283383fed5b0cbc361ffe4b384601c5a92607c1cbe90d2eedb"
        print(f"  [mock] Tx executed: {description or 'contract call'}")
        print(f"         to={tx['to']}  value={tx.get('value','0')}")
        print(f"         data={tx['data'][:42]}...{tx['data'][-8:]}")
        print(f"  [mock] Tx hash: {mock_hash}")
        return TxResult(request_id=request_id, tx_hash=mock_hash, status="Success")
