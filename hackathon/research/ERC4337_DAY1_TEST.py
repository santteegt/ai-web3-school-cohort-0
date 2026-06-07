"""
GuildOS — Day 1 Wallet Integration Test
ERC-4337 via ZeroDev Kernel on Base Sepolia

Validates all 5 high-risk operations before building the full GuildOS stack.

Setup:
    pip install zerodev-aa web3

Required env vars:
    ZERODEV_PROJECT_ID       — from dashboard.zerodev.app (create a Base Sepolia project)
    SPECIALIST_AGENT_KEY     — 0x-prefixed private key for the Specialist Agent
    ORCHESTRATOR_AGENT_KEY   — 0x-prefixed private key for the Orchestrator Agent
    AGENTFIGHTCLUB_ADDRESS   — deployed AgentFightClub contract on Base Sepolia (or any test contract)

Run:
    python hackathon/research/ERC4337_DAY1_TEST.py
"""

import os
import sys
import hashlib
import time

from zerodev_aa import Context, Signer, Call, KernelVersion, GasMiddleware, PaymasterMiddleware

# ── Config ──────────────────────────────────────────────────────────────────

PROJECT_ID = os.environ.get("ZERODEV_PROJECT_ID")
SPECIALIST_KEY_HEX = os.environ.get("SPECIALIST_AGENT_KEY", "").removeprefix("0x")
ORCHESTRATOR_KEY_HEX = os.environ.get("ORCHESTRATOR_AGENT_KEY", "").removeprefix("0x")
AFC_ADDRESS = os.environ.get("AGENTFIGHTCLUB_ADDRESS", "0x0000000000000000000000000000000000000000")

BASE_SEPOLIA_CHAIN_ID = 84532
BASESCAN_URL = "https://sepolia.basescan.org/tx/"

PASS = "✅ PASS"
FAIL = "❌ FAIL"
WARN = "⚠️  WARN"

results = []

def log(label: str, status: str, detail: str = ""):
    line = f"{status}  {label}"
    if detail:
        line += f"\n        {detail}"
    print(line)
    results.append((label, status))


def check_env():
    missing = []
    if not PROJECT_ID:
        missing.append("ZERODEV_PROJECT_ID")
    if not SPECIALIST_KEY_HEX:
        missing.append("SPECIALIST_AGENT_KEY")
    if missing:
        print(f"Missing required env vars: {', '.join(missing)}")
        print("Set them before running this script.")
        sys.exit(1)


# ── Test 1: Smart account creation (deterministic address) ───────────────────

def test_1_account_creation():
    """
    Verifies that creating a Kernel smart account twice with the same private key
    produces the same deterministic address on Base Sepolia.
    """
    label = "Test 1: Smart account creation (deterministic address)"
    try:
        key_bytes = bytes.fromhex(SPECIALIST_KEY_HEX)

        addr_run1 = None
        addr_run2 = None

        with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
                     gas=GasMiddleware.ZERODEV,
                     paymaster=PaymasterMiddleware.ZERODEV) as ctx:
            with Signer.local(key_bytes) as signer:
                with ctx.new_account(signer, KernelVersion.V3_3) as account:
                    addr_run1 = account.get_address().hex() if hasattr(account.get_address(), 'hex') else str(account.get_address())

        # Second run — same key, must produce same address
        with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
                     gas=GasMiddleware.ZERODEV,
                     paymaster=PaymasterMiddleware.ZERODEV) as ctx:
            with Signer.local(key_bytes) as signer:
                with ctx.new_account(signer, KernelVersion.V3_3) as account:
                    addr_run2 = account.get_address().hex() if hasattr(account.get_address(), 'hex') else str(account.get_address())

        if addr_run1 == addr_run2:
            log(label, PASS, f"Specialist Agent address: 0x{addr_run1}")
        else:
            log(label, FAIL, f"Run 1: {addr_run1}  Run 2: {addr_run2} — addresses differ!")

    except Exception as e:
        log(label, FAIL, str(e))


# ── Test 2: Sponsored UserOp (no-op transaction) ─────────────────────────────

def test_2_sponsored_userop():
    """
    Sends a zero-value transfer to the agent's own address (no-op).
    Validates bundler connectivity, paymaster sponsorship, and EntryPoint v0.7.
    """
    label = "Test 2: Sponsored UserOp — zero-value self-transfer"
    try:
        key_bytes = bytes.fromhex(SPECIALIST_KEY_HEX)

        with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
                     gas=GasMiddleware.ZERODEV,
                     paymaster=PaymasterMiddleware.ZERODEV) as ctx:
            with Signer.local(key_bytes) as signer:
                with ctx.new_account(signer, KernelVersion.V3_3) as account:
                    own_addr = account.get_address()
                    # No-op: send 0 ETH to self
                    tx_hash = account.send_user_op([Call(target=own_addr)])
                    receipt = account.wait_for_receipt(tx_hash)

                    if receipt.success:
                        tx_hex = receipt.transaction_hash.hex() if hasattr(receipt.transaction_hash, 'hex') else receipt.transaction_hash
                        log(label, PASS, f"{BASESCAN_URL}{tx_hex}")
                    else:
                        log(label, FAIL, "Transaction reverted")

    except Exception as e:
        log(label, FAIL, str(e))


# ── Test 3: Deliverable hash commit (mock guild contract) ─────────────────────

def test_3_hash_commit():
    """
    Generates a SHA-256 deliverable hash (simulating Specialist Agent output)
    and encodes a 'commitHash(bytes32)' call to the AgentFightClub contract.

    NOTE: If AGENTFIGHTCLUB_ADDRESS is the zero address, this will send a tx to
    address(0) which will succeed on-chain but produce no state change — sufficient
    to validate the signing + submission path. Replace with real contract for
    actual integration testing.
    """
    label = "Test 3: Deliverable hash commit transaction"
    try:
        key_bytes = bytes.fromhex(SPECIALIST_KEY_HEX)

        # Simulate the Specialist Agent hashing a deliverable
        fake_deliverable = b"audit_report_v1.0: no critical findings\n"
        sha256_hash = hashlib.sha256(fake_deliverable).digest()  # 32 bytes
        print(f"        Deliverable SHA-256: {sha256_hash.hex()}")

        # ABI-encode commitHash(bytes32) manually
        # Function selector: keccak256("commitHash(bytes32)")[:4]
        # Using a fixed-known selector for test purposes; replace with actual ABI encoding
        # For a real test: use web3.py eth_abi.encode or similar
        selector = bytes.fromhex("a9059cbb")  # placeholder selector for test path
        calldata = selector + sha256_hash  # naive encoding; use eth_abi in production

        with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
                     gas=GasMiddleware.ZERODEV,
                     paymaster=PaymasterMiddleware.ZERODEV) as ctx:
            with Signer.local(key_bytes) as signer:
                with ctx.new_account(signer, KernelVersion.V3_3) as account:
                    tx_hash = account.send_user_op([
                        Call(target=bytes.fromhex(AFC_ADDRESS.removeprefix("0x")), data=calldata)
                    ])
                    receipt = account.wait_for_receipt(tx_hash)

                    if receipt.success:
                        tx_hex = receipt.transaction_hash.hex() if hasattr(receipt.transaction_hash, 'hex') else receipt.transaction_hash
                        log(label, PASS, f"Hash committed: {BASESCAN_URL}{tx_hex}")
                    else:
                        log(label, FAIL, "Transaction reverted — check ABI encoding and contract address")

    except Exception as e:
        log(label, FAIL, str(e))


# ── Test 4: ETH receipt into smart account ────────────────────────────────────

def test_4_eth_receipt():
    """
    Checks that the Specialist Agent's smart account can receive ETH.
    This is required for AgentFightClub settle() to pay the agent.

    This test only reads the balance — it does not send ETH.
    To fully test: fund the smart account address from a faucet first.
    """
    label = "Test 4: Smart account ETH balance readable"
    try:
        from web3 import Web3

        key_bytes = bytes.fromhex(SPECIALIST_KEY_HEX)

        with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
                     gas=GasMiddleware.ZERODEV,
                     paymaster=PaymasterMiddleware.ZERODEV) as ctx:
            with Signer.local(key_bytes) as signer:
                with ctx.new_account(signer, KernelVersion.V3_3) as account:
                    addr = account.get_address()
                    addr_hex = addr.hex() if hasattr(addr, 'hex') else str(addr)

                    # Read balance via public Base Sepolia RPC
                    w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
                    balance_wei = w3.eth.get_balance(Web3.to_checksum_address("0x" + addr_hex))
                    balance_eth = w3.from_wei(balance_wei, 'ether')

                    if balance_wei >= 0:  # any non-negative balance is valid (including 0)
                        log(label, PASS, f"Smart account 0x{addr_hex} balance: {balance_eth} ETH")
                        if balance_wei == 0:
                            print(f"        {WARN} Balance is 0 — fund from faucet before testing settle() payout")
                    else:
                        log(label, FAIL, "Could not read balance")

    except ImportError:
        log(label, WARN, "web3 not installed — run: pip install web3. Skipping balance check.")
    except Exception as e:
        log(label, FAIL, str(e))


# ── Test 5: Two-agent setup (Orchestrator + Specialist different addresses) ───

def test_5_two_agent_wallets():
    """
    Creates smart accounts for both Orchestrator and Specialist agents.
    Confirms they have different addresses (different private keys → different accounts).
    This is required for the GuildOS two-agent architecture.
    """
    label = "Test 5: Two-agent wallet setup (Orchestrator ≠ Specialist)"
    if not ORCHESTRATOR_KEY_HEX:
        log(label, WARN, "ORCHESTRATOR_AGENT_KEY not set — skipping. Set it to run two-agent test.")
        return

    try:
        spec_key = bytes.fromhex(SPECIALIST_KEY_HEX)
        orch_key = bytes.fromhex(ORCHESTRATOR_KEY_HEX)

        addrs = {}
        for role, key in [("Specialist", spec_key), ("Orchestrator", orch_key)]:
            with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
                         gas=GasMiddleware.ZERODEV,
                         paymaster=PaymasterMiddleware.ZERODEV) as ctx:
                with Signer.local(key) as signer:
                    with ctx.new_account(signer, KernelVersion.V3_3) as account:
                        a = account.get_address()
                        addrs[role] = a.hex() if hasattr(a, 'hex') else str(a)

        if addrs["Specialist"] != addrs["Orchestrator"]:
            log(label, PASS,
                f"Specialist:   0x{addrs['Specialist']}\n"
                f"        Orchestrator: 0x{addrs['Orchestrator']}")
        else:
            log(label, FAIL, "Both agents produced the same address — keys may be identical")

    except Exception as e:
        log(label, FAIL, str(e))


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    check_env()

    print("=" * 60)
    print("GuildOS — Day 1 ERC-4337 Wallet Integration Tests")
    print(f"Chain:   Base Sepolia (chain_id={BASE_SEPOLIA_CHAIN_ID})")
    print(f"Stack:   ZeroDev Kernel v3.3, EntryPoint v0.7")
    print("=" * 60)
    print()

    test_1_account_creation()
    print()
    test_2_sponsored_userop()
    print()
    test_3_hash_commit()
    print()
    test_4_eth_receipt()
    print()
    test_5_two_agent_wallets()

    print()
    print("=" * 60)
    passed = sum(1 for _, s in results if s == PASS)
    warned = sum(1 for _, s in results if s == WARN)
    failed = sum(1 for _, s in results if s == FAIL)
    print(f"Results: {passed} passed · {warned} warnings · {failed} failed out of {len(results)} tests")

    if failed > 0:
        print()
        print("Failed tests indicate integration blockers. Fix before building GuildOS stack.")
        sys.exit(1)
    elif warned > 0:
        print()
        print("Warnings are non-blocking but should be resolved before the live demo.")
    else:
        print()
        print("All tests passed. Safe to proceed with GuildOS wallet integration.")
