"""AgentFightClub — interface for Moloch v3 guild treasury and governance.

Calldata is built by ``moloch-agent --build-only --full`` (no PRIVATE_KEY
passed to the subprocess). Signing and broadcast go through WalletProvider
(CAW TSS by default). No raw EOA key is ever read or held by this module.

Network is resolved from CHAIN_ID via src/shared/network_config.py — never
hardcode an RPC URL or assume a fixed network here. AFC has no Base Sepolia
deployment; only CHAIN_ID=8453 (Base) is valid for AgentFightClub calls.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile

from src.shared import network_config, wallet
from src.shared.wallet import UnsignedTx, get_wallet_provider

logger = logging.getLogger(__name__)

_MCLI = "moloch-agent"

_SUMMON_BAAL_TOPIC0 = "0xcf2f09cd0dbc149b12a3630a11b7d73476660f3d08d3dc7dcc79c6dec555ee7a"

_wallet: wallet.WalletProviderProtocol | None = None


def _get_wallet() -> wallet.WalletProviderProtocol:
    global _wallet
    if _wallet is None:
        _wallet = get_wallet_provider()
    return _wallet


def _rpc_url() -> str:
    return network_config.get_rpc_url()


def _build_calldata(*args: str, timeout: int = 120) -> UnsignedTx:
    """Build unsigned calldata via moloch-agent --build-only --full.

    No PRIVATE_KEY is passed to the subprocess — the CLI only encodes the
    transaction data. Returns the unsigned tx dict {to, data, value, chainId}.
    """
    cmd = [_MCLI, *args, "--build-only", "--full"]
    env = {**os.environ, "PRIVATE_KEY": "", "RPC_URL": _rpc_url()}

    logger.info("Building calldata: %s", " ".join(cmd[:3]))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "moloch-agent not found — install with: npm install -g @raidguild/meta-clawtel"
        ) from exc

    if result.returncode != 0:
        stderr = result.stderr.strip()
        logger.error("moloch-agent error: %s", stderr)
        raise RuntimeError(
            f"moloch-agent failed (exit {result.returncode}): {stderr}"
        )

    stdout = result.stdout.strip()
    try:
        output = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"moloch-agent returned non-JSON: {stdout[:200]}"
        ) from exc

    tx = output.get("tx")
    if not tx or "to" not in tx or "data" not in tx:
        raise RuntimeError(
            f"moloch-agent output missing tx field: {list(output.keys())}"
        )
    return tx


async def _sign_and_broadcast(tx: UnsignedTx) -> str:
    """Sign via WalletProvider and return the confirmed tx hash."""
    result = await _get_wallet().sign(tx)
    if not result.tx_hash:
        raise RuntimeError(
            f"WalletProvider returned no tx_hash (status: {result.status})"
        )
    logger.info("Tx confirmed: %s", result.tx_hash)
    return result.tx_hash


def _parse_dao_from_receipt(tx_hash: str) -> str | None:
    """Parse the DAO address from the SummonBaal event in the tx receipt."""
    if not tx_hash or tx_hash.startswith("0xdead"):
        return None

    from web3 import Web3

    w3 = Web3(Web3.HTTPProvider(_rpc_url()))
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    for log in receipt["logs"]:
        topics = log.get("topics", [])
        if topics and topics[0].hex().lower() == _SUMMON_BAAL_TOPIC0.lower():
            raw = topics[1].hex()
            return "0x" + raw[-40:]
    return None


async def launch(mandate: str, treasury_address: str) -> dict:
    """Deploy guild contract (Moloch v3 DAO) with mandate string.

    Args:
        mandate: Guild mission statement / mandate string
        treasury_address: Address to receive initial treasury funding

    Returns:
        dict with guild_address and tx_hash.
    """
    account_addr = os.getenv("AGENT_WALLET_ADDRESS", "")
    if not account_addr:
        raise RuntimeError("AGENT_WALLET_ADDRESS env var not set")

    summon_params = {
        "daoName": "GuildOS-Genesys",
        "tokenName": "GUILD",
        "tokenSymbol": "GLD",
        "members": [
            {
                "address": account_addr,
                "shares": "1000000000000000000",
                "loot": "0",
            }
        ],
        "votingPeriod": "60",
        "gracePeriod": "60",
        "quorum": "0",
        "minRetention": "0",
        "sponsorThreshold": "0",
        "proposalOffering": "0",
        "metadata": {
            "name": "GuildOS Genesys",
            "description": mandate,
        },
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(summon_params, f, indent=2)
        params_path = f.name

    try:
        tx = _build_calldata("summon", "--params", params_path, timeout=180)
    finally:
        os.unlink(params_path)

    tx_hash = await _sign_and_broadcast(tx)

    dao_address = _parse_dao_from_receipt(tx_hash)
    if not dao_address:
        raise RuntimeError(
            f"Could not parse DAO address from receipt tx {tx_hash}"
        )

    _get_wallet().register_guild_contract(dao_address)
    logger.info("Guild deployed at: %s (tx: %s)", dao_address, tx_hash)

    return {
        "guild_address": dao_address,
        "tx_hash": tx_hash,
    }


async def commit(guild_address: str, amount_wei: int) -> str:
    """Fund treasury via wrap-eth -> approve-token -> tribute flow.

    Args:
        guild_address: Deployed guild contract address
        amount_wei: Amount in wei to fund

    Returns:
        Transaction hash of the tribute/funding tx.
    """
    amount_eth = amount_wei / 1e18
    weth_address = network_config.get_contract_address("weth")

    logger.info("Wrapping %s ETH to WETH", amount_eth)
    wrap_tx = _build_calldata("wrap-eth", "--amount", str(amount_eth))
    await _sign_and_broadcast(wrap_tx)

    logger.info("Approving WETH for guild %s", guild_address)
    approve_tx = _build_calldata(
        "approve-token",
        "--token", weth_address,
        "--amount", str(amount_eth),
    )
    await _sign_and_broadcast(approve_tx)

    logger.info("Submitting tribute to guild %s", guild_address)
    tribute_tx = _build_calldata(
        "tribute",
        "--dao", guild_address,
        "--token", weth_address,
        "--amount", str(amount_eth),
    )
    tribute_hash = await _sign_and_broadcast(tribute_tx)
    logger.info("Tribute tx: %s", tribute_hash)
    return tribute_hash


async def propose(guild_address: str, specialist_erc8004_id: int) -> str:
    """Submit Specialist membership proposal via mint-shares (no tribute).

    Returns proposal ID.
    """
    specialist_wallet = os.getenv("SPECIALIST_WALLET_ADDRESS", "")
    if not specialist_wallet:
        raise RuntimeError("SPECIALIST_WALLET_ADDRESS env var not set")

    tx = _build_calldata(
        "mint-shares",
        "--dao", guild_address,
        "--to", specialist_wallet,
        "--shares", "1000000000000000000",
    )
    await _sign_and_broadcast(tx)

    proposal_id = _read_latest_proposal_id(guild_address)
    logger.info("Membership proposal created: %s", proposal_id)
    return str(proposal_id)


async def vote(guild_address: str, proposal_id: str, approve: bool = True) -> str:
    """Cast membership vote. Returns tx hash."""
    try:
        sponsor_tx = _build_calldata(
            "sponsor", "--dao", guild_address, "--proposal", proposal_id
        )
        await _sign_and_broadcast(sponsor_tx)
    except RuntimeError as exc:
        logger.warning("Sponsor failed (may already be sponsored): %s", exc)

    vote_tx = _build_calldata(
        "vote",
        "--dao", guild_address,
        "--proposal", proposal_id,
        "--approved", str(approve).lower(),
    )
    tx_hash = await _sign_and_broadcast(vote_tx)
    logger.info("Vote tx: %s", tx_hash)
    return tx_hash


async def settle(guild_address: str, specialist_wallet: str) -> str:
    """Release treasury payment to Specialist wallet via proposal process.

    Returns tx hash (Basescan tx #2).
    """
    payment_tx = _build_calldata(
        "payment",
        "--dao", guild_address,
        "--recipient", specialist_wallet,
        "--amount", "0.001",
    )
    await _sign_and_broadcast(payment_tx)

    proposal_id = _read_latest_proposal_id(guild_address)
    logger.info("Payment proposal: %s", proposal_id)

    try:
        sponsor_tx = _build_calldata(
            "sponsor", "--dao", guild_address, "--proposal", proposal_id
        )
        await _sign_and_broadcast(sponsor_tx)
    except RuntimeError as exc:
        logger.warning("Sponsor failed: %s", exc)

    vote_tx = _build_calldata(
        "vote",
        "--dao", guild_address,
        "--proposal", proposal_id,
        "--approved", "true",
    )
    await _sign_and_broadcast(vote_tx)

    import asyncio

    logger.info("Waiting 65s for grace period...")
    await asyncio.sleep(65)

    process_tx = _build_calldata(
        "process", "--dao", guild_address, "--proposal", proposal_id
    )
    tx_hash = await _sign_and_broadcast(process_tx)
    logger.info("Settlement tx: %s", tx_hash)
    return tx_hash


def _read_latest_proposal_id(dao_address: str) -> str:
    """Read the current proposalCount from the DAO to get the latest proposal ID."""
    import urllib.request

    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{"to": dao_address, "data": "0xda35c664"}, "latest"],
            "id": 1,
        }
    ).encode()
    req = urllib.request.Request(
        _rpc_url(),
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
        hex_count = body.get("result", "0x0")
        return str(int(hex_count, 16))
    except Exception as exc:
        logger.warning("Could not read proposalCount: %s", exc)
        raise RuntimeError(
            f"Failed to read proposalCount from DAO {dao_address}: {exc}"
        ) from exc
