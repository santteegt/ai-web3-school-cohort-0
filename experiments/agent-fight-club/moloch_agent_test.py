#!/usr/bin/env python3
"""
GuildOS — AgentFightClub Day 1 Integration Test
================================================
Run this script on Day 1 of the hackathon to validate the highest-risk
AgentFightClub/Moloch v3 operations before building the full stack.

Prerequisites:
  npm install -g @raidguild/meta-clawtel
  export PRIVATE_KEY=0x...
  export RPC_URL=https://sepolia.base.org  # or https://mainnet.base.org
  export MOLOCH_SERVICE_URL=https://moloch-service-production.up.railway.app

Usage:
  python AGENTFIGHTCLUB_DAY1_TEST.py           # run all tests
  python AGENTFIGHTCLUB_DAY1_TEST.py --test 1  # run specific test
  python AGENTFIGHTCLUB_DAY1_TEST.py --dry-run # print commands without executing

Tests:
  1. Hosted service health check
  2. DAO summon on target network (highest risk)
  3. Membership proposal full lifecycle (mint-shares → sponsor → vote → process)
  4. Payment proposal full lifecycle (payment → sponsor → vote → process)
  5. Signal proposal with deliverable hash
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
def load_dotenv(env_file: Path = Path(".env")) -> None:
    """Load key=value pairs from a .env file into os.environ (no-op if file absent)."""
    if not env_file.exists():
        return
    with env_file.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

load_dotenv()
DRY_RUN = False
GUILD_ADDR = os.environ.get("TEST_GUILD_ADDR", "")  # Set after summon, or pre-stage
SPECIALIST_ADDR = os.environ.get("SPECIALIST_ADDR", "0x0000000000000000000000000000000000000001")
MOLOCH_CLI = "moloch-agent"

# Short periods for demo/testing — override if DAO was summoned differently
VOTING_PERIOD_SEC = 65   # slightly over 60s summon param
GRACE_PERIOD_SEC = 65

SUMMON_PARAMS = {
    "daoName": "GuildOS-Test-Guild",
    "tokenName": "GUILDTEST",
    "tokenSymbol": "GT",
    "lootTokenName": "GUILDTEST-LOOT",
    "lootTokenSymbol": "GTL",
    "votingPeriodInSeconds": 60,
    "gracePeriodInSeconds": 60,
    "quorum": 1,
    "minRetention": 66,
    "sponsorThreshold": 0,
    "newOffering": 0,
    # memberAddresses and memberShares populated at runtime from 'moloch-agent account'
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: str, capture: bool = True) -> tuple[int, str, str]:
    """Run a shell command. Returns (returncode, stdout, stderr)."""
    print(f"\n  $ {cmd}")
    if DRY_RUN:
        print("  [DRY RUN — not executed]")
        return 0, "", ""
    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    if result.stdout.strip():
        print(f"  → {result.stdout.strip()[:500]}")
    if result.stderr.strip():
        print(f"  ✗ stderr: {result.stderr.strip()[:300]}")
    return result.returncode, result.stdout, result.stderr


def cli(args: str, capture: bool = True) -> tuple[int, str, str]:
    return run(f"{MOLOCH_CLI} {args}", capture=capture)


def check(condition: bool, label: str):
    if condition:
        print(f"  ✅ PASS: {label}")
    else:
        print(f"  ❌ FAIL: {label}")
    return condition


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  TEST: {title}")
    print(f"{'='*60}")


def wait(seconds: int, reason: str = ""):
    msg = f"  ⏳ Waiting {seconds}s{' — ' + reason if reason else ''}..."
    print(msg)
    if not DRY_RUN:
        time.sleep(seconds)


def get_proposal_count(guild: str) -> int:
    """Read proposalCount directly from the Baal contract via RPC (no graph)."""
    _, out, _ = cli(f"read-dao --dao {guild}")
    try:
        return int(json.loads(out).get("proposalCount", 0))
    except (json.JSONDecodeError, AttributeError, TypeError, ValueError):
        return 0


def wait_for_new_proposal(guild: str, prev_count: int, max_wait: int = 60, poll_interval: int = 5) -> str | None:
    """Poll read-dao until proposalCount exceeds prev_count, then return the new proposal ID.

    Handles RPC propagation lag and MOLOCH_WAIT_DEFAULT=false by retrying on-chain reads
    until the submitted proposal is confirmed visible.
    """
    deadline = time.time() + max_wait
    while time.time() < deadline:
        count = get_proposal_count(guild)
        if count > prev_count:
            return str(count)
        remaining = int(deadline - time.time())
        print(f"  ⏳ Proposal not yet on-chain (count={count}, prev={prev_count}, {remaining}s left)...")
        if not DRY_RUN:
            time.sleep(poll_interval)
    return None


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_state(path: Path, state: dict):
    path.write_text(json.dumps(state, indent=2))
    print(f"  💾 State saved to {path}")


# ---------------------------------------------------------------------------
# Test 1 — Hosted service health check
# ---------------------------------------------------------------------------

def test_health() -> bool:
    section("1. Hosted Service Health Check")
    print("  Verifying moloch-agent CLI is installed and hosted service is reachable.")

    # rc, out, _ = cli("--version")
    # if not check(rc == 0, "moloch-agent CLI installed"):
    #     print("  Fix: npm install -g @raidguild/meta-clawtel")
    #     return False

    rc, out, _ = cli("health")
    ok_health = check(rc == 0, "health endpoint responds")

    rc, out, _ = cli("capabilities")
    try:
        caps = json.loads(out)
    except json.JSONDecodeError:
        caps = {}
    ok_graph = check(caps.get("graph", {}).get("configured") is True, "graph.configured: true")
    ok_pinning = check(caps.get("pinning", {}).get("configured") is True, "pinning.configured visible")
    ok_signing = check("handledByService" in caps.get("signing", {}), "signing.handledByService reported")

    rc, out, _ = cli("account")
    try:
        acct = json.loads(out)
    except json.JSONDecodeError:
        acct = {}
    ok_account = check(acct.get("available") is True, "signer account readable")
    if ok_account:
        addr = acct.get("address", "")
        if addr:
            print(f"  → Signer address: {addr}")
            os.environ["FOUNDER_ADDR"] = addr

    return all([ok_health, ok_graph, ok_account])


# ---------------------------------------------------------------------------
# Test 2 — DAO Summon (highest risk: network support)
# ---------------------------------------------------------------------------

def test_summon(state_path: Path) -> bool:
    section("2. DAO Summon on Target Network (HIGHEST RISK)")
    print(f"  Network: {os.environ.get('RPC_URL', 'default (Base mainnet)')}")
    print("  Risk: Baal Summoner factory may not be deployed on Base Sepolia.")
    print("  If this fails, switch to Base mainnet (https://mainnet.base.org).")

    founder = os.environ.get("FOUNDER_ADDR", "")
    if not founder:
        print("  ⚠️  FOUNDER_ADDR not set — run test 1 first")
        return False

    params = dict(SUMMON_PARAMS)
    params["memberAddresses"] = [founder]
    params["memberShares"] = ["1000000000000000000"]  # 1 share in base units
    params["memberLoot"] = ["0"]

    params_file = Path("guildos-test-summon.tmp.json")
    params_file.write_text(json.dumps(params, indent=2))
    print(f"  Summon params written to {params_file}")
    print(f"  votingPeriodInSeconds: {params['votingPeriodInSeconds']}s | gracePeriodInSeconds: {params['gracePeriodInSeconds']}s")

    # --full includes receipt.logs so we can parse the deployed DAO address from the BaalSummoned event
    rc, out, err = cli(f"summon --params {params_file} --full")

    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        data = {}

    # The SUMMONER factory emits BaalSummoned(address indexed baal, ...).
    # topics[1] is the 32-byte zero-padded baal address; last 40 chars = the 20-byte address.
    SUMMONER = "0x97aaa5be8b38795245f1c38a883b44cccdfb3e11"
    dao_addr = ""
    for log in data.get("receipt", {}).get("logs", []):
        if log.get("address", "").lower() == SUMMONER:
            topics = log.get("topics", [])
            if len(topics) >= 2 and len(topics[1]) == 66:
                dao_addr = "0x" + topics[1][-40:]
                break

    ok_summon = check(rc == 0, "summon command succeeded")
    ok_addr = check(bool(dao_addr), f"DAO address returned: {dao_addr or '(none)'}")

    if ok_summon and ok_addr:
        state = load_state(state_path)
        state["guild_addr"] = dao_addr
        state["network"] = os.environ.get("RPC_URL", "mainnet")
        save_state(state_path, state)
        print(f"\n  → DAO deployed at: {dao_addr}")
        print(f"  → Basescan: https://sepolia.basescan.org/address/{dao_addr}")
        global GUILD_ADDR
        GUILD_ADDR = dao_addr

    if not ok_summon:
        print("\n  ⚠️  FALLBACK OPTIONS:")
        print("  Option A: Set RPC_URL=https://mainnet.base.org and retry")
        print("  Option B: Deploy Baal Summoner factory to Base Sepolia via HausDAO/Baal repo")
        print("  Option C: Use a pre-deployed DAO address (set TEST_GUILD_ADDR env var)")

    return ok_summon and ok_addr


# ---------------------------------------------------------------------------
# Test 3 — Membership proposal full lifecycle
# ---------------------------------------------------------------------------

def test_membership(state_path: Path) -> bool:
    section("3. Membership Proposal Full Lifecycle")
    print("  Flow: mint-shares → sponsor → vote → wait → process-ready")

    state = load_state(state_path)
    guild = GUILD_ADDR or state.get("guild_addr", "")
    if not guild:
        print("  ⚠️  No guild address. Run test 2 first, or set TEST_GUILD_ADDR env var.")
        return False

    specialist = SPECIALIST_ADDR
    print(f"  Guild:      {guild}")
    print(f"  Specialist: {specialist}")

    # Snapshot proposalCount before submitting so we can detect when the new proposal lands
    prev_count = get_proposal_count(guild)

    # Create membership proposal — --wait forces the CLI to block until the receipt is confirmed
    rc, out, _ = cli(
        f'mint-shares --dao {guild} --to {specialist} --amount 10 '
        f'--title "Specialist Agent Membership Test" '
        f'--description "Day1 test | ERC-8004: placeholder | capabilities: security-audit" '
        f'--wait'
    )
    ok_propose = check(rc == 0, "mint-shares proposal submitted")
    if not ok_propose:
        return False

    # Poll until proposalCount > prev_count (guards against RPC propagation lag)
    proposal_id = wait_for_new_proposal(guild, prev_count)
    if not proposal_id:
        print(f"  ⚠️  Timed out waiting for proposal to appear on-chain (prev count={prev_count}).")
        return False
    print(f"  → Proposal ID: {proposal_id}")

    # Sponsor — skip if already sponsored
    _, prop_out, _ = cli(f"proposal --dao {guild} --proposal {proposal_id}")
    try:
        already_sponsored = json.loads(prop_out).get("proposal", {}).get("sponsored", False)
    except (json.JSONDecodeError, AttributeError):
        already_sponsored = False

    if already_sponsored:
        ok_sponsor = check(True, "proposal already sponsored — skipping")
    else:
        rc, out, _ = cli(f"sponsor --dao {guild} --proposal {proposal_id}")
        ok_sponsor = check(rc == 0, "sponsor succeeded")

    # Vote
    rc, _, _ = cli(f"vote --dao {guild} --proposal {proposal_id} --approved true")
    ok_vote = check(rc == 0, "vote submitted")

    # Wait for voting + grace period
    wait(VOTING_PERIOD_SEC + GRACE_PERIOD_SEC, "voting + grace periods")

    # Check: verify our proposal is in the processable queue
    _, pq_out, _ = cli(f"process-queue --dao {guild}")
    try:
        pq_data = json.loads(pq_out)
        queue = pq_data.get("queue", [])
        in_queue = any(
            str(item.get("proposalId")) == str(proposal_id)
            for item in queue
            if isinstance(item, dict)
        )
    except (json.JSONDecodeError, AttributeError):
        in_queue = False
    ok_ready = check(in_queue, f"proposal {proposal_id} in process queue")
    if not ok_ready:
        return False

    # Process: submit tx to execute the oldest ready proposal
    rc, out, _ = cli(f"process-ready --dao {guild}")
    ok_process = check(rc == 0, "process-ready succeeded")

    # Verify membership
    rc, out, _ = cli(f"members --dao {guild}")
    try:
        members_data = json.loads(out)
    except json.JSONDecodeError:
        members_data = {}
    # DAOhaus graph returns { members: [...] } or a flat list; each member has memberAddress
    member_list = (
        members_data if isinstance(members_data, list)
        else members_data.get("members", members_data.get("data", []))
    )
    member_addrs = [m.get("memberAddress", "").lower() for m in member_list if isinstance(m, dict)]
    ok_member = check(
        specialist.lower() in member_addrs or specialist.lower() in out.lower(),
        "Specialist appears in members list",
    )

    if ok_member:
        print(f"  ✅ Full membership lifecycle works end-to-end")
        state["membership_proposal_id"] = proposal_id
        save_state(state_path, state)
    else:
        print("  ⚠️  Membership not confirmed in members list — check graph indexing lag")

    return all([ok_propose, ok_sponsor, ok_vote, ok_ready, ok_process])


# ---------------------------------------------------------------------------
# Test 4 — Payment proposal full lifecycle
# ---------------------------------------------------------------------------

def test_payment(state_path: Path) -> bool:
    section("4. Payment Proposal Full Lifecycle")
    print("  Flow: payment → sponsor → vote → wait → process-ready")
    print("  NOTE: Requires funded treasury. Funding with 0.01 ETH for test.")

    state = load_state(state_path)
    guild = GUILD_ADDR or state.get("guild_addr", "")
    if not guild:
        print("  ⚠️  No guild address. Run test 2 first.")
        return False

    # Fund treasury with minimal test amount
    print("  Funding treasury with 0.01 WETH...")
    rc, _, _ = cli("wrap-eth --amount 0.01")
    check(rc == 0, "wrap-eth succeeded")

    # Approve WETH (Base Sepolia WETH address — verify before use)
    weth_base_sepolia = "0x4200000000000000000000000000000000000006"
    rc, _, _ = cli(f"approve-token --token {weth_base_sepolia} --amount 0.01")
    check(rc == 0, "approve-token succeeded")

    # Tribute (fund treasury)
    rc, _, _ = cli(
        f"tribute --dao {guild} --token {weth_base_sepolia} "
        f"--amount 10000000000000000 --shares 0"
    )
    check(rc == 0, "tribute (fund treasury) succeeded")

    prev_count = get_proposal_count(guild)

    # Payment proposal — --wait forces the CLI to block until the receipt is confirmed
    rc, out, _ = cli(
        f'payment --dao {guild} --recipient {SPECIALIST_ADDR} '
        f'--amount 0.005 '
        f'--title "Test payment: T001 accepted" '
        f'--description "sha256:PLACEHOLDER_HASH | task:TEST-T001" '
        f'--wait'
    )
    ok_payment = check(rc == 0, "payment proposal submitted")
    if not ok_payment:
        return False

    proposal_id = wait_for_new_proposal(guild, prev_count)
    if not proposal_id:
        print(f"  ⚠️  Timed out waiting for payment proposal on-chain (prev count={prev_count}).")
        return False

    print(f"  → Payment proposal ID: {proposal_id}")

    # Sponsor — skip if already sponsored
    _, prop_out, _ = cli(f"proposal --dao {guild} --proposal {proposal_id}")
    try:
        already_sponsored = json.loads(prop_out).get("sponsored", False)
    except (json.JSONDecodeError, AttributeError):
        already_sponsored = False

    if already_sponsored:
        ok_sponsor = check(True, "proposal already sponsored — skipping")
    else:
        rc, _, _ = cli(f"sponsor --dao {guild} --proposal {proposal_id}")
        ok_sponsor = check(rc == 0, "sponsor succeeded")
        if rc != 0:
            return False

    rc, _, _ = cli(f"vote --dao {guild} --proposal {proposal_id} --approved true")
    ok_vote = check(rc == 0, "vote submitted")

    wait(VOTING_PERIOD_SEC + GRACE_PERIOD_SEC, "voting + grace periods")

    # Check: verify our payment proposal is in the processable queue
    _, pq_out, _ = cli(f"process-queue --dao {guild}")
    try:
        pq_data = json.loads(pq_out)
        queue = pq_data.get("queue", [])
        in_queue = any(
            str(item.get("proposalId")) == str(proposal_id)
            for item in queue
            if isinstance(item, dict)
        )
    except (json.JSONDecodeError, AttributeError):
        in_queue = False
    ok_ready = check(in_queue, f"payment proposal {proposal_id} in process queue")
    if not ok_ready:
        return False

    # Process: submit tx to settle the payment
    rc, out, _ = cli(f"process-ready --dao {guild}")
    ok_process = check(rc == 0, "process-ready (settlement) succeeded")

    if ok_process:
        print("  ✅ Payment settlement works end-to-end")
        print("  → Find the process tx on Basescan — this is proof point #2 for judges")

    return all([ok_payment, ok_sponsor, ok_vote, ok_ready, ok_process])


# ---------------------------------------------------------------------------
# Test 5 — Signal proposal with deliverable hash
# ---------------------------------------------------------------------------

def test_hash_signal(state_path: Path) -> bool:
    section("5. Deliverable Hash Commitment via Signal Proposal")
    print("  This is the simplest on-chain proof path for the deliverable hash.")
    print("  Hash goes into proposal description — permanent on-chain record.")

    state = load_state(state_path)
    guild = GUILD_ADDR or state.get("guild_addr", "")
    if not guild:
        print("  ⚠️  No guild address. Run test 2 first.")
        return False

    test_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    rc, out, _ = cli(
        f'signal --dao {guild} '
        f'--title "Deliverable hash TEST-T001" '
        f'--description "sha256:{test_hash} | task:TEST-T001 | deliverable:ipfs://QmTest"'
    )
    ok_signal = check(rc == 0, "signal proposal submitted")

    if ok_signal:
        print("  ✅ Signal proposal works — hash is permanently on-chain")
        print("  → Find the signal tx on Basescan — this is proof point #1 for judges")
        print(f"  → Verify: the hash {test_hash[:16]}... appears in tx calldata")

    return ok_signal


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def main():
    global DRY_RUN, GUILD_ADDR

    parser = argparse.ArgumentParser(description="GuildOS AFC Day 1 Integration Tests")
    parser.add_argument("--test", type=int, help="Run specific test number (1-5)")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    parser.add_argument("--guild", help="Use existing guild address (skip summon)")
    args = parser.parse_args()

    if args.dry_run:
        DRY_RUN = True
        print("  [DRY RUN MODE — commands will be printed but not executed]")

    if args.guild:
        GUILD_ADDR = args.guild
        os.environ["TEST_GUILD_ADDR"] = args.guild
        print(f"  Using existing guild: {GUILD_ADDR}")

    state_path = Path("guildos-day1-state.tmp.json")
    if state_path.exists():
        saved = json.loads(state_path.read_text())
        if saved.get("guild_addr") and not GUILD_ADDR:
            GUILD_ADDR = saved["guild_addr"]
            print(f"  Loaded guild from previous run: {GUILD_ADDR}")

    print("\n🏟️  GuildOS — AgentFightClub Day 1 Integration Tests")
    print(f"   Network: {os.environ.get('RPC_URL', 'default (Base mainnet)')}")
    print(f"   Service: {os.environ.get('MOLOCH_SERVICE_URL', 'default')}")
    print(f"   Specialist: {SPECIALIST_ADDR}")

    results: dict[int, bool] = {}

    tests = {
        1: ("Hosted service health", lambda: test_health()),
        2: ("DAO summon", lambda: test_summon(state_path)),
        3: ("Membership lifecycle", lambda: test_membership(state_path)),
        4: ("Payment lifecycle", lambda: test_payment(state_path)),
        5: ("Hash signal", lambda: test_hash_signal(state_path)),
    }

    target = args.test
    for num, (name, fn) in tests.items():
        if target is not None and num != target:
            continue
        try:
            results[num] = fn()
            if not results[num]:
                break
        except Exception as e:
            print(f"\n  💥 Test {num} raised exception: {e}")
            results[num] = False

    # Summary
    print(f"\n{'='*60}")
    print("  RESULTS SUMMARY")
    print(f"{'='*60}")
    all_pass = True
    for num, (name, _) in tests.items():
        if num in results:
            icon = "✅" if results[num] else "❌"
            print(f"  {icon} Test {num}: {name}")
            if not results[num]:
                all_pass = False

    if all_pass and results:
        print("\n  🟢 All tests passed. Integration path is validated. Start building.")
    elif results:
        print("\n  🔴 Some tests failed. Review failures before building on top of AFC.")
        print("     See AGENTFIGHTCLUB_ANALYSIS.md for gap analysis and alternatives.")
        sys.exit(1)


if __name__ == "__main__":
    main()
