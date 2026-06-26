#!/usr/bin/env python3
"""
Agent Fight Club — ClawBank Convenience Path PoC
=================================================
Exercises the ClawBank REST API (POST /api/v1/moloch/read|write/:command)
without any CLI dependency.  All operations map 1:1 to the MCP fightclub_*
tool names from https://agentfightclub.xyz/skill.md.

Required env vars:
  CLAWBANK_BASE_URL  e.g. https://clawbank.yourdomain.com
  CLAWBANK_TOKEN     Bearer token from ClawBank profile page

Optional:
  AFC_DAO            0x address of the guild/DAO to operate on
  AFC_SPECIALIST     0x address to grant shares to (mint-shares demo)
  AFC_PAYMENT_TO     0x recipient for payment demo (defaults to AFC_SPECIALIST)

Usage:
  uv run afc_clawbank.py               # run full demo (reads only)
  uv run afc_clawbank.py --write       # include write operations (needs funded DAO)
  uv run afc_clawbank.py --test health # single section
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# ClawBank client
# ---------------------------------------------------------------------------

class ClawBankClient:
    """Thin wrapper around the ClawBank Fight Club REST API.

    Skill reference: https://agentfightclub.xyz/skill.md  §§ 2–4
    """

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _request(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=120)
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        except requests.HTTPError as exc:
            raise RuntimeError(f"HTTP {exc.response.status_code} from {url}: {exc.response.text}") from exc
        except requests.ConnectionError as exc:
            raise RuntimeError(f"Network error calling {url}: {exc}") from exc

    # -- Read helpers --------------------------------------------------------

    def read(self, command: str, flags: dict | None = None) -> dict:
        """POST /api/v1/moloch/read/:command  (fightclub_<command> MCP equivalent)."""
        return self._request(f"/api/v1/moloch/read/{command}", {"flags": flags or {}})

    def health(self) -> dict:
        return self.read("health")

    def capabilities(self) -> dict:
        return self.read("capabilities")

    def list_daos(self) -> dict:
        """fightclub_list_daos — all DAOs visible to this ClawBank instance."""
        return self.read("list-daos")

    def my_daos(self) -> dict:
        """fightclub_my_daos — DAOs the authenticated wallet belongs to."""
        return self.read("my-daos")

    def dao(self, dao_address: str) -> dict:
        return self.read("dao", {"dao": dao_address})

    def proposals(self, dao_address: str, first: int = 10) -> dict:
        return self.read("proposals", {"dao": dao_address, "first": first})

    def members(self, dao_address: str) -> dict:
        return self.read("members", {"dao": dao_address})

    def balances(self, dao_address: str) -> dict:
        return self.read("balances", {"dao": dao_address})

    def process_queue(self, dao_address: str) -> dict:
        return self.read("process-queue", {"dao": dao_address})

    def inspect_payload_schema(self, command: str) -> dict:
        """fightclub_inspect_fightclub_payload_schema — get required flags before writes."""
        return self.read("inspect-fightclub-payload-schema", {"command": command})

    # -- Write helpers -------------------------------------------------------

    def write(self, command: str, flags: dict, wait: bool = True) -> dict:
        """POST /api/v1/moloch/write/:command  (fightclub_<command> MCP equivalent).

        Pass wait=False to return immediately with tx hash (no confirmation wait).
        Skill reference: §2 optional query param ?wait=false
        """
        path = f"/api/v1/moloch/write/{command}"
        if not wait:
            path += "?wait=false"
        return self._request(path, {"flags": flags})

    def mint_shares(self, dao: str, to: str, amount: str,
                    title: str = "", description: str = "") -> dict:
        """fightclub_mint_shares — no-tribute membership (tribute == 0, shares > 0).

        Membership rule: use mint-shares when tribute is zero and shares > 0.
        Skill reference: §8
        """
        return self.write("mint-shares", {
            "dao": dao,
            "to": to,
            "amount": amount,
            "title": title or f"Grant {amount} shares to {to[:10]}...",
            "description": description or "No-tribute membership request via ClawBank PoC",
        })

    def payment(self, dao: str, recipient: str, amount: str,
                title: str = "", description: str = "") -> dict:
        """fightclub_payment — payment proposal from treasury."""
        return self.write("payment", {
            "dao": dao,
            "recipient": recipient,
            "amount": amount,
            "title": title or f"Payment to {recipient[:10]}...",
            "description": description or "Payment via ClawBank PoC",
        })

    def vote(self, dao: str, proposal: str, approved: bool = True,
             wait_for_confirmation: bool = True) -> dict:
        """fightclub_vote — cast a vote on a proposal."""
        return self.write("vote", {
            "dao": dao,
            "proposal": proposal,
            "approved": approved,
            "wait_for_confirmation": wait_for_confirmation,
        })

    def sponsor(self, dao: str, proposal: str) -> dict:
        """fightclub_sponsor — sponsor a proposal to enter voting period."""
        return self.write("sponsor", {"dao": dao, "proposal": proposal})

    def process(self, dao: str, proposal: str) -> dict:
        """fightclub_process — execute a passed proposal after grace period."""
        return self.write("process", {"dao": dao, "proposal": proposal})

    def signal(self, dao: str, title: str, description: str) -> dict:
        """fightclub_signal — on-chain signal/memo proposal (no treasury action)."""
        return self.write("signal", {"dao": dao, "title": title, "description": description})

    def summon(
        self,
        dao_name: str,
        token_name: str,
        token_symbol: str,
        member_addresses: list[str],
        member_shares: list[str],       # raw base units (18 decimals), e.g. "1000000000000000000" = 1 share
        member_loot: list[str] | None = None,
        voting_period: int = 60,
        grace_period: int = 60,
        quorum: int = 0,
        min_retention: int = 66,
        sponsor_threshold: int = 0,
        description: str = "",
        # no_workspace: bool = False,
    ) -> dict:
        """fightclub_summon — deploy a new Moloch v3 DAO.

        Schema: params (required) wraps all Baal/Moloch summon fields.
        no_workspace is a top-level flag (not inside params).
        memberShares/memberLoot must be raw base-unit strings (18 decimals).
        """
        params: dict = {
            "daoName": dao_name,
            "tokenName": token_name,
            "tokenSymbol": token_symbol,
            "lootTokenName": f"{token_name} Loot",
            "lootTokenSymbol": f"L{token_symbol}",
            "memberAddresses": member_addresses,
            "memberShares": member_shares,
            "memberLoot": member_loot or ["0"] * len(member_addresses),
            "votingPeriodInSeconds": voting_period,
            "gracePeriodInSeconds": grace_period,
            "quorum": quorum,
            "minRetention": min_retention,
            "sponsorThreshold": sponsor_threshold,
        }
        if description:
            params["description"] = description
        # return self.write("summon", {"params": params, "no_workspace": no_workspace})
        return self.write("summon", { "params": params })


# ---------------------------------------------------------------------------
# Demo helpers
# ---------------------------------------------------------------------------

def _ok(label: str, value: Any = None) -> bool:
    print(f"  OK  {label}" + (f": {value}" if value is not None else ""))
    return True


def _fail(label: str, detail: str = "") -> bool:
    print(f"  FAIL {label}" + (f": {detail}" if detail else ""))
    return False


def _section(title: str) -> None:
    print(f"\n{'='*60}")
    print(f"  {title}")
    print("=" * 60)


def _pp(data: dict, max_chars: int = 400) -> None:
    text = json.dumps(data, indent=2)
    if max_chars > 0 and len(text) > max_chars:
        text = text[:max_chars] + "\n  ...(truncated)"
    for line in text.splitlines():
        print(f"    {line}")


# ---------------------------------------------------------------------------
# Demo sections
# ---------------------------------------------------------------------------

def demo_health(client: ClawBankClient) -> bool:
    _section("1. Health + Capabilities (fightclub_capabilities)")
    try:
        h = client.health()
        _ok("health", h.get("data", {}).get('ok', False))
    except RuntimeError as exc:
        return _fail("health", str(exc))

    try:
        caps = client.capabilities()
        _pp(caps, -1)
        _ok("capabilities fetched")
    except RuntimeError as exc:
        return _fail("capabilities", str(exc))

    return True


def demo_discover(client: ClawBankClient) -> tuple[bool, str]:
    """Returns (success, first_dao_address)."""
    _section("2. Discover DAOs (fightclub_list_daos + fightclub_my_daos)")

    dao_addr = os.getenv("AFC_DAO", "")

    ok = True

    try:
        result = client.list_daos()
        daos = result.get("data", {}).get("daos", [])
        print(f"  list-daos returned {len(daos)} DAO(s)")
        for dao in daos:
            _pp(dao)
            # if not dao_addr:
            #     first = dao
            #     dao_addr = first.get("address", "")
    except RuntimeError as exc:
        ok = False
        _fail("list-daos", str(exc))

    try:
        result = client.my_daos()
        mine = result.get("data", {}).get("daos", [])
        print(f"  my-daos returned {len(mine)} DAO(s) for this wallet")
        if len(mine) > 0:
            first = mine[0]
            _pp(first),
            dao_addr = first.get("address", "")
    except RuntimeError as exc:
        ok = False
        _fail("my-daos", str(exc))

    if dao_addr:
        _ok("active DAO", dao_addr)
    else:
        print("  No DAO found — set AFC_DAO env var to use a specific address")

    return ok, dao_addr


def demo_read_dao(client: ClawBankClient, dao_addr: str) -> bool:
    _section("3. Read DAO State (dao / proposals / members / balances)")
    print(f"  DAO: {dao_addr}")

    try:
        dao_info = client.dao(dao_addr)
        data = dao_info.get("data", {}).get('dao', {})
        summary = {
            "data": {
                "safeAddress": data.get("safeAddress", ""),
                "activeMemberCount": data.get("activeMemberCount", data.get("totalMembers")),
                "proposalCount": data.get("proposalCount", data.get("totalProposals")),
                "name": data.get("name", ""),
            }
        }
        print("  DAO summary:")
        _pp(summary, -1)
    except RuntimeError as exc:
        _fail("dao", str(exc))

    # try:
    #     props = client.proposals(dao_addr, first=5)
    #     items = props.get("data", {}).get("proposals", [])
    #     print(f"  proposals (last 5): {len(items)} returned")
    #     if len(items) > 0:
    #         _pp(items[0], -1)
    # except RuntimeError as exc:
    #     _fail("proposals", str(exc))

    # try:
    #     m = client.members(dao_addr)
    #     members = m.get("data", {}).get("members", [])
    #     print(f"  members: {len(members)}")
    #     if members:
    #         _pp(members[0], -1)
    # except RuntimeError as exc:
    #     _fail("members", str(exc))

    try:
        bal = client.balances(dao_addr)
        print("  balances:")
        _pp(bal, -1)
    except RuntimeError as exc:
        _fail("balances", str(exc))

    return True


def demo_inspect_schema(client: ClawBankClient) -> bool:
    _section("4. Inspect Payload Schema (before any write)")
    print("  Best practice: call inspect before complex writes (skill §11)")
    for cmd in ("mint-shares", "payment", "signal"):
        try:
            schema = client.inspect_payload_schema(cmd)
            print(f"\n  Schema for '{cmd}':")
            _pp(schema)
        except RuntimeError as exc:
            _fail(f"inspect {cmd}", str(exc))
    return True


def demo_signal(client: ClawBankClient, dao_addr: str) -> bool:
    _section("5. Signal Proposal Write (fightclub_signal — no treasury action)")
    print(f"  DAO: {dao_addr}")
    print("  A signal proposal is the lowest-risk write — no funds move.")
    try:
        result = client.signal(
            dao=dao_addr,
            title="[PoC #4] ClawBank convenience-path test",
            description="Proof that the ClawBank REST write path works end-to-end. "
                        "Emitted from experiments/afc-simple/afc_clawbank.py",
        )
        tx = result.get("data", {}).get("tx_hash", "")
        _ok("signal proposal submitted", tx or "(no tx hash in response)")
        _pp(result)
        return True
    except RuntimeError as exc:
        return _fail("signal", str(exc))


def demo_mint_shares(client: ClawBankClient, dao_addr: str, specialist: str) -> bool:
    _section("6. Mint Shares (fightclub_mint_shares — no-tribute membership)")
    print(f"  DAO: {dao_addr}")
    print(f"  Recipient: {specialist}")
    print("  Skill §8: tribute == 0, shares > 0 → use mint-shares (not join-dao)")
    try:
        result = client.mint_shares(
            dao=dao_addr,
            to=specialist,
            amount="10",
            title=f"[PoC] Membership — {specialist[:12]}...",
            description="No-tribute share grant via ClawBank convenience path",
        )
        tx = result.get("txHash", result.get("transactionHash", ""))
        proposal_id = result.get("proposalId", result.get("proposal", ""))
        _ok("mint-shares proposal submitted")
        _ok("tx hash", tx or "(check result)")
        _ok("proposal id", proposal_id or "(check result)")
        _pp(result)
        return True
    except RuntimeError as exc:
        return _fail("mint-shares", str(exc))


def demo_payment(client: ClawBankClient, dao_addr: str, recipient: str) -> bool:
    _section("7. Payment Proposal (fightclub_payment)")
    print(f"  DAO: {dao_addr}")
    print(f"  Recipient: {recipient}")
    print("  Note: treasury must have WETH balance for this to succeed.")
    try:
        result = client.payment(
            dao=dao_addr,
            recipient=recipient,
            amount="0.001",
            title="[PoC] Payment test",
            description="Minimal payment proposal via ClawBank REST write path",
        )
        tx = result.get("txHash", result.get("transactionHash", ""))
        _ok("payment proposal submitted", tx or "(check result)")
        _pp(result)
        return True
    except RuntimeError as exc:
        return _fail("payment", str(exc))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def demo_vote_latest(client: ClawBankClient, dao_addr: str) -> bool:
    _section("Vote — Most Recent Proposal (fightclub_vote)")
    print(f"  DAO: {dao_addr}")

    try:
        result = client.proposals(dao_addr, first=1)
        proposals = result.get("data", {}).get("proposals", [])
    except RuntimeError as exc:
        return _fail("proposals fetch", str(exc))

    if not proposals:
        return _fail("proposals", "no proposals found in this DAO")

    proposal_id = proposals[0].get("proposalId")
    if proposal_id is None:
        return _fail("proposalId", f"missing in proposals[0]: {proposals[0]}")

    print(f"  Most recent proposal id: {proposal_id}")

    try:
        result = client.vote(
            dao=dao_addr,
            proposal=str(proposal_id),
            approved=True,
            wait_for_confirmation=False,
        )
        tx = tx = result.get("data", {}).get("tx_hash", "")
        _ok("vote submitted", tx or "(no tx hash in response)")
        if tx:
            print(f"  Basescan: https://basescan.org/tx/{tx}")
        _pp(result)
        return True
    except RuntimeError as exc:
        return _fail("vote", str(exc))


_SUMMON_PARAMS_FILE = Path(__file__).parent / "summon_params.json"


def demo_summon(client: ClawBankClient) -> tuple[bool, str]:
    """Deploy a new Moloch v3 DAO via ClawBank summon. Returns (success, dao_address)."""
    _section("Summon — Deploy New Moloch v3 DAO (fightclub_summon)")

    if not _SUMMON_PARAMS_FILE.exists():
        return _fail("config", f"{_SUMMON_PARAMS_FILE} not found"), ""
    cfg = json.loads(_SUMMON_PARAMS_FILE.read_text())
    print(f"  Loaded params from {_SUMMON_PARAMS_FILE.name}")

    # Resolve founding member address from env or fightclub_account read
    member = os.getenv("AFC_MEMBER", "")
    if not member:
        try:
            result = client.read("account")
            member = result.get("data", {}).get("address", "")
            if member:
                print(f"  Signer address (auto): {member}")
        except RuntimeError as exc:
            return _fail("account lookup", str(exc)), ""
    if not member:
        return _fail("member address", "Set AFC_MEMBER=0x... or ensure fightclub_account returns an address"), ""

    member_shares = cfg.get("memberSharesRaw", "100000000000000000000")

    print(f"  DAO name    : {cfg.get('daoName')}")
    print(f"  Token       : {cfg.get('tokenName')} ({cfg.get('tokenSymbol')})")
    print(f"  Member      : {member}")
    print(f"  Shares (raw): {member_shares}")
    print(f"  Voting/grace: {cfg.get('votingPeriodInSeconds')}s / {cfg.get('gracePeriodInSeconds')}s")

    try:
        result = client.summon(
            dao_name=cfg["daoName"],
            token_name=cfg["tokenName"],
            token_symbol=cfg["tokenSymbol"],
            member_addresses=[member],
            member_shares=[member_shares],
            voting_period=cfg.get("votingPeriodInSeconds", 60),
            grace_period=cfg.get("gracePeriodInSeconds", 60),
            quorum=cfg.get("quorum", 0),
            min_retention=cfg.get("minRetention", 66),
            sponsor_threshold=cfg.get("sponsorThreshold", 0),
            description=cfg.get("description", ""),
        )

        out_file = Path(__file__).parent / "summon_output.json"
        out_file.write_text(json.dumps(result, indent=2))

        ok = result.get("ok", True)
        dao_addr = (
            result.get("daoAddress")
            or result.get("contractAddress")
            or result.get("data", {}).get("daoAddress", "")
        )
        tx_hash = (
            result.get("txHash")
            or result.get("transactionHash")
            or result.get("data", {}).get("txHash", "")
        )

        _ok("summon call succeeded")
        if tx_hash:
            _ok("tx hash", tx_hash)
            print(f"  Basescan: https://basescan.org/tx/{tx_hash}")
        if dao_addr:
            _ok("DAO address", dao_addr)
            print(f"  Basescan: https://basescan.org/address/{dao_addr}")
        else:
            print("  DAO address not in response — check tx on Basescan or poll my-daos")
        _pp(result, -1)
        print(f"  Full response saved to {out_file.name}")

        return bool(ok), dao_addr or ""
    except RuntimeError as exc:
        return _fail("summon", str(exc)), ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Fight Club — ClawBank convenience path PoC")
    parser.add_argument(
        "--write", action="store_true",
        help="Run write sections (signal, mint-shares, payment). Requires funded DAO.",
    )
    parser.add_argument(
        "--vote", action="store_true",
        help="Vote yes on the most recent proposal in the active DAO.",
    )
    parser.add_argument(
        "--test",
        choices=["health", "discover", "read", "schema", "signal", "mint", "payment", "summon", "vote"],
        help="Run a single section only.",
    )
    args = parser.parse_args()

    base_url = os.getenv("CLAWBANK_BASE_URL", "")
    token = os.getenv("CLAWBANK_TOKEN", "")
    dao_addr = os.getenv("AFC_DAO", "")
    specialist = os.getenv("AFC_SPECIALIST", "")
    payment_to = os.getenv("AFC_PAYMENT_TO", specialist)

    if not base_url or not token:
        print("ERROR: set CLAWBANK_BASE_URL and CLAWBANK_TOKEN before running.")
        print("  See .env.example for setup instructions.")
        sys.exit(1)

    client = ClawBankClient(base_url, token)

    print(f"\n Agent Fight Club — ClawBank Convenience Path PoC")
    print(f"  Base URL : {base_url}")
    print(f"  DAO      : {dao_addr or '(auto-discover)'}")
    print(f"  Write    : {'yes' if args.write else 'no (reads only)'}")

    results: dict[str, bool] = {}
    only = args.test

    def run(key: str, fn) -> bool:
        if only and only != key:
            return True
        r = fn()
        results[key] = r
        return r

    run("health", lambda: demo_health(client))

    ok_disc, discovered_dao = demo_discover(client)
    results["discover"] = ok_disc

    active_dao = dao_addr or discovered_dao
    if only == "summon":
        ok_summon, summoned_addr = demo_summon(client)
        results["summon"] = ok_summon
        if ok_summon and summoned_addr:
            active_dao = summoned_addr
    elif not active_dao:
        print("\n  No DAOs associated to this wallet")
        print("  Set AFC_DAO=0x... to test against a specific guild.")
    else:
        run("read", lambda: demo_read_dao(client, active_dao))
        # run("schema", lambda: demo_inspect_schema(client)) # TODO: endpoint not available

        if args.write:
            run("signal", lambda: demo_signal(client, active_dao))

            if args.vote:
                run("vote", lambda: demo_vote_latest(client, active_dao))

            if specialist:
                run("mint", lambda: demo_mint_shares(client, active_dao, specialist))
            else:
                print("\n  Skipping mint-shares: set AFC_SPECIALIST=0x... to enable.")

            if payment_to:
                run("payment", lambda: demo_payment(client, active_dao, payment_to))
            else:
                print("\n  Skipping payment: set AFC_PAYMENT_TO=0x... to enable.")

    # Summary
    print(f"\n{'='*60}")
    print("  RESULTS")
    print("=" * 60)
    for k, v in results.items():
        icon = "OK  " if v else "FAIL"
        print(f"  {icon}  {k}")
    fails = [k for k, v in results.items() if not v]
    if fails:
        print(f"\n  {len(fails)} section(s) failed.")
        sys.exit(1)
    else:
        print("\n  All sections passed.")


if __name__ == "__main__":
    main()
