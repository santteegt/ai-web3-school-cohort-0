"""AgentFightClub — interface for Moloch v3 guild treasury and governance.

Primary: Direct integration via moloch-agent CLI (@raidguild/meta-clawtel)
Fallback: web3.py direct contract calls if CLI fails (see docs/RISKS.md §F1)

Decision recorded in docs/TECH_STACK.md Decision Log on Day 8.
Network: Base mainnet (chain_id 8453)
"""

from __future__ import annotations

import json
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

# Config from environment
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
RPC_URL = os.getenv("RPC_URL", "https://mainnet.base.org")

# moloch-agent CLI
_MCLI = "moloch-agent"


def _run_cli(*args: str, timeout: int = 120) -> dict:
    """Run moloch-agent CLI command and return parsed JSON output.

    Raises RuntimeError on non-zero exit or parse failure.
    """
    cmd = [_MCLI] + list(args)
    env = {**os.environ, "PRIVATE_KEY": PRIVATE_KEY, "RPC_URL": RPC_URL}

    logger.info("CLI: %s", " ".join(cmd[:3]) + ("..." if len(cmd) > 3 else ""))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip()
        logger.error("CLI error: %s", stderr)
        raise RuntimeError(f"moloch-agent failed (exit {result.returncode}): {stderr}")

    # Try to parse JSON output
    stdout = result.stdout.strip()
    if not stdout:
        return {"raw": ""}

    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        # Some commands return plain text
        return {"raw": stdout}


# ---------------------------------------------------------------------------
# Guild operations
# ---------------------------------------------------------------------------


async def launch(mandate: str, treasury_address: str) -> dict:
    """Deploy guild contract (Moloch v3 DAO) with mandate string.

    Uses moloch-agent summon with minimal params:
    - Short voting/grace periods for demo (60s each)
    - Founder as initial member with 1 share
    - Mandate stored in DAO metadata

    Args:
        mandate: Guild mission statement / mandate string
        treasury_address: Address to receive initial treasury funding

    Returns:
        dict with guild_address and tx_hash.
    """
    if not PRIVATE_KEY:
        raise RuntimeError("PRIVATE_KEY env var not set — cannot sign transactions")

    # Get signer address first
    account_info = _run_cli("account")
    signer_address = account_info.get("address", "")
    if not signer_address:
        raise RuntimeError(f"Could not get signer address from 'account': {account_info}")

    logger.info("Signer address: %s", signer_address)

    # Build summon params
    summon_params = {
        "daoName": "GuildOS-Guild",
        "tokenName": "GUILD",
        "tokenSymbol": "GLD",
        "members": [
            {
                "address": signer_address,
                "shares": "1000000000000000000",  # 1 share (18 decimals)
                "loot": "0",
            }
        ],
        "votingPeriod": "60",     # 60 seconds for demo
        "gracePeriod": "60",      # 60 seconds for demo
        "quorum": "0",
        "minRetention": "0",
        "sponsorThreshold": "0",
        "proposalOffering": "0",
        "metadata": {
            "name": "GuildOS Guild",
            "description": mandate,
        },
    }

    # Write params to temp file for moloch-agent
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(summon_params, f, indent=2)
        params_path = f.name

    try:
        result = _run_cli("summon", "--params", params_path, timeout=180)
    finally:
        os.unlink(params_path)

    # Parse result — moloch-agent returns tx hash and DAO address
    tx_hash = result.get("txHash", result.get("transactionHash", ""))
    dao_address = result.get("daoAddress", result.get("contractAddress", ""))

    if not dao_address:
        # Try to extract from raw output
        raw = result.get("raw", "")
        if "0x" in raw:
            # Look for 0x address pattern
            import re
            addresses = re.findall(r"0x[a-fA-F0-9]{40}", raw)
            if addresses:
                dao_address = addresses[-1]  # Last address is usually the DAO

    if not dao_address:
        raise RuntimeError(f"Could not extract DAO address from summon result: {result}")

    logger.info("Guild deployed at: %s (tx: %s)", dao_address, tx_hash)

    return {
        "guild_address": dao_address,
        "tx_hash": tx_hash,
    }


async def commit(guild_address: str, amount_wei: int) -> str:
    """Fund treasury via wrap-eth → approve-token → tribute flow.

    Moloch v3 requires WETH, so we:
    1. Wrap ETH to WETH
    2. Approve WETH for the DAO
    3. Submit tribute to fund the treasury

    Args:
        guild_address: Deployed guild contract address
        amount_wei: Amount in wei to fund (e.g. 1_000_000_000_000_000 = 0.001 ETH)

    Returns:
        Transaction hash of the tribute/funding tx.
    """
    if not PRIVATE_KEY:
        raise RuntimeError("PRIVATE_KEY env var not set — cannot sign transactions")

    # Convert wei to ETH for CLI
    amount_eth = amount_wei / 1e18

    # Step 1: Wrap ETH → WETH
    logger.info("Wrapping %s ETH to WETH", amount_eth)
    wrap_result = _run_cli("wrap-eth", "--amount", str(amount_eth))
    wrap_tx = wrap_result.get("txHash", wrap_result.get("transactionHash", ""))
    logger.info("Wrap tx: %s", wrap_tx)

    # Step 2: Approve WETH for the guild (use WETH address on Base)
    weth_base = "0x4200000000000000000000000000000000000006"
    logger.info("Approving WETH for guild %s", guild_address)
    approve_result = _run_cli(
        "approve-token",
        "--token", weth_base,
        "--amount", str(amount_eth),
    )
    approve_tx = approve_result.get("txHash", approve_result.get("transactionHash", ""))
    logger.info("Approve tx: %s", approve_tx)

    # Step 3: Submit tribute to fund treasury
    logger.info("Submitting tribute to guild %s", guild_address)
    tribute_result = _run_cli(
        "tribute",
        "--dao", guild_address,
        "--token", weth_base,
        "--amount", str(amount_eth),
    )
    tribute_tx = tribute_result.get("txHash", tribute_result.get("transactionHash", ""))

    if not tribute_tx:
        raw = tribute_result.get("raw", "")
        if "0x" in raw:
            import re
            txs = re.findall(r"0x[a-fA-F0-9]{64}", raw)
            if txs:
                tribute_tx = txs[-1]

    logger.info("Tribute tx: %s", tribute_tx)
    return tribute_tx


# ---------------------------------------------------------------------------
# Membership operations (Issue #2)
# ---------------------------------------------------------------------------


async def propose(guild_address: str, specialist_erc8004_id: int) -> str:
    """Submit Specialist membership proposal via mint-shares (no tribute).

    Creates a proposal to grant the Specialist shares (voting membership).
    Returns proposal ID.
    """
    if not PRIVATE_KEY:
        raise RuntimeError("PRIVATE_KEY env var not set")

    # Get specialist wallet address from ERC-8004 or use provided address
    specialist_wallet = os.getenv("SPECIALIST_WALLET_ADDRESS", "")
    if not specialist_wallet:
        raise RuntimeError("SPECIALIST_WALLET_ADDRESS env var not set")

    result = _run_cli(
        "mint-shares",
        "--dao", guild_address,
        "--to", specialist_wallet,
        "--shares", "1000000000000000000",  # 1 share
    )

    proposal_id = result.get("proposalId", result.get("proposal", ""))
    if not proposal_id:
        raw = result.get("raw", "")
        if raw:
            proposal_id = raw.strip()

    logger.info("Membership proposal created: %s", proposal_id)
    return str(proposal_id)


async def vote(guild_address: str, proposal_id: str, approve: bool = True) -> str:
    """Cast membership vote. Returns tx hash.

    For demo: auto-approve (single human operator).
    """
    if not PRIVATE_KEY:
        raise RuntimeError("PRIVATE_KEY env var not set")

    # Sponsor first (required before voting)
    try:
        sponsor_result = _run_cli(
            "sponsor",
            "--dao", guild_address,
            "--proposal", proposal_id,
        )
        sponsor_tx = sponsor_result.get("txHash", "")
        logger.info("Sponsor tx: %s", sponsor_tx)
    except RuntimeError as e:
        logger.warning("Sponsor failed (may already be sponsored): %s", e)

    # Vote
    result = _run_cli(
        "vote",
        "--dao", guild_address,
        "--proposal", proposal_id,
        "--approved", str(approve).lower(),
    )

    tx_hash = result.get("txHash", result.get("transactionHash", ""))
    if not tx_hash:
        raw = result.get("raw", "")
        if "0x" in raw:
            import re
            txs = re.findall(r"0x[a-fA-F0-9]{64}", raw)
            if txs:
                tx_hash = txs[-1]

    logger.info("Vote tx: %s", tx_hash)
    return tx_hash


# ---------------------------------------------------------------------------
# Settlement (Day 11)
# ---------------------------------------------------------------------------


async def settle(guild_address: str, specialist_wallet: str) -> str:
    """Release treasury payment to Specialist wallet.

    Uses payment proposal: payment → sponsor → vote → grace → process.
    For demo with short periods: sponsor + vote + process in sequence.

    Returns tx hash (Basescan tx #2).
    """
    if not PRIVATE_KEY:
        raise RuntimeError("PRIVATE_KEY env var not set")

    # Create payment proposal
    payment_result = _run_cli(
        "payment",
        "--dao", guild_address,
        "--recipient", specialist_wallet,
        "--amount", "0.001",  # Match commit amount
    )

    proposal_id = payment_result.get("proposalId", "")
    if not proposal_id:
        raw = payment_result.get("raw", "")
        if raw:
            proposal_id = raw.strip()

    logger.info("Payment proposal: %s", proposal_id)

    # Sponsor
    try:
        _run_cli("sponsor", "--dao", guild_address, "--proposal", proposal_id)
    except RuntimeError as e:
        logger.warning("Sponsor failed: %s", e)

    # Vote approve
    _run_cli("vote", "--dao", guild_address, "--proposal", proposal_id, "--approved", "true")

    # Wait for grace period (60s) then process
    import asyncio
    logger.info("Waiting 65s for grace period...")
    await asyncio.sleep(65)

    # Process
    process_result = _run_cli("process", "--dao", guild_address, "--proposal", proposal_id)
    tx_hash = process_result.get("txHash", process_result.get("transactionHash", ""))

    if not tx_hash:
        raw = process_result.get("raw", "")
        if "0x" in raw:
            import re
            txs = re.findall(r"0x[a-fA-F0-9]{64}", raw)
            if txs:
                tx_hash = txs[-1]

    logger.info("Settlement tx: %s", tx_hash)
    return tx_hash
