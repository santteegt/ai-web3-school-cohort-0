"""
Orchestrator Agent — CAW × Moloch-Agent PoC.

Flow:
  1. moloch-agent --build-only --full  →  unsigned tx calldata (no PRIVATE_KEY needed)
  2. CawClient.submit_and_wait_pact()  →  human approves action scope in Cobo app
  3. CawClient.execute_calldata()      →  CAW signs and broadcasts the tx on Base mainnet
  4. Parse DAO address from tx receipt (summon only) or read from state

No private key is stored or used in this process.
"""

import asyncio
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from caw_client import CawClient, MockCawClient, TxResult
from pact import AFC_SUMMONER, get_pact_summary

# ──────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────

# Locate the moloch-agent binary — check PATH first, then the nvm global install
_NVM_BIN = Path.home() / ".nvm/versions/node/v24.13.0/bin/moloch-agent"
MOLOCH_CLI = str(_NVM_BIN) if _NVM_BIN.exists() else "moloch-agent"

RPC_URL = os.getenv("MOLOCH_RPC_URL", "https://mainnet.base.org")
CHAIN_ID = int(os.getenv("MOLOCH_CHAIN_ID", "8453"))

DAO_NAME = os.getenv("DAO_NAME", "GuildOS-POC")
TOKEN_NAME = os.getenv("TOKEN_NAME", "GUILDPOC")
TOKEN_SYMBOL = os.getenv("TOKEN_SYMBOL", "GUILDPOC")
VOTING_PERIOD = int(os.getenv("VOTING_PERIOD_SECONDS", "60"))
GRACE_PERIOD = int(os.getenv("GRACE_PERIOD_SECONDS", "30"))

ORCHESTRATOR_ADDRESS = os.getenv("ORCHESTRATOR_CAW_ADDRESS")

USE_MOCK_CAW = os.getenv("USE_MOCK_CAW", "true").lower() == "true"

# keccak256("SummonBaal(address,address,address,address,address,uint256)")
# computed via viem: keccak256(toHex(toBytes(sig)))
_SUMMON_BAAL_TOPIC0 = "0xcf2f09cd0dbc149b12a3630a11b7d73476660f3d08d3dc7dcc79c6dec555ee7a"


# ──────────────────────────────────────────────────────────────
# OrchestratorAgent
# ──────────────────────────────────────────────────────────────

class OrchestratorAgent:
    """
    Orchestrator agent that drives Moloch DAO operations via CAW.

    All on-chain actions go through:
      build calldata (moloch-agent) → pact approval (CAW) → broadcast (CAW TSS)
    """

    def __init__(self, use_mock: bool = USE_MOCK_CAW):
        self.use_mock = use_mock
        self.state_file = Path(__file__).parent / "state.json"
        self.state = self._load_state()

        summary = get_pact_summary()
        print(f"📋 CAW pact type: {summary['policy_type']}  chain: {summary['chain']}")
        if use_mock:
            print("⚠️  Running in MOCK mode — no real txs will be sent")

    # ── State ──────────────────────────────────────────────────

    def _load_state(self) -> dict:
        if self.state_file.exists():
            data = json.loads(self.state_file.read_text())
            print(f"📂 Loaded state from {self.state_file.name}")
            return data
        return {}

    def _save_state(self):
        self.state_file.write_text(json.dumps(self.state, indent=2))

    # ── moloch-agent calldata builder ──────────────────────────

    def _run_moloch(self, *args: str) -> dict:
        """
        Run moloch-agent with --build-only --full and return the unsigned tx dict.

        Returns:
            { "to": "0x...", "data": "0x...", "value": "0", "chainId": 8453 }

        No PRIVATE_KEY is passed — moloch-agent only encodes calldata.
        """
        cmd = [MOLOCH_CLI, *args, "--build-only", "--full"]
        env = {
            **os.environ,
            "RPC_URL": RPC_URL,
            # Explicitly unset PRIVATE_KEY so moloch-agent cannot accidentally sign
            "PRIVATE_KEY": "",
        }
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=60,
            )
        except FileNotFoundError:
            raise RuntimeError(
                f"moloch-agent not found at '{MOLOCH_CLI}'. "
                "Install with: npm install -g @raidguild/meta-clawtel"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("moloch-agent timed out")

        if result.returncode != 0:
            raise RuntimeError(f"moloch-agent error:\n{result.stderr.strip()}")

        try:
            output = json.loads(result.stdout.strip())
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"moloch-agent returned non-JSON: {result.stdout[:200]}") from exc

        tx = output.get("tx")
        if not tx or "to" not in tx or "data" not in tx:
            raise RuntimeError(f"moloch-agent output missing tx field: {list(output.keys())}")

        return tx  # { to, data, value, chainId, gas? }

    # ── CAW execution helper ───────────────────────────────────

    async def _execute_via_caw(
        self,
        description: str,
        allowed_contracts: list[str],
        tx: dict,
    ) -> TxResult:
        """Submit pact → human approves → execute calldata → return TxResult."""
        client_cls = MockCawClient if self.use_mock else CawClient
        async with client_cls() as caw:
            pact = await caw.submit_and_wait_pact(
                intent=description,
                allowed_contracts=allowed_contracts,
                tx_count=1,
            )
            return await caw.execute_calldata(
                self.state.get("orchestrator_address") or ORCHESTRATOR_ADDRESS,
                pact,
                tx,
                description=description
            )

    # ── DAO actions ────────────────────────────────────────────

    def summon_dao(self) -> str:
        """
        Summon a new Moloch DAO via the AgentFightClub SUMMONER.

        Returns:
            DAO contract address on Base mainnet.
        """
        print(f"\n🏛️  Summoning {DAO_NAME}...")

        # Build the summon params file
        params_file = Path(__file__).parent / "_summon_params.json"
        orchestrator_addr = self.state.get("orchestrator_address") or os.getenv(
            "ORCHESTRATOR_CAW_ADDRESS", "0x0000000000000000000000000000000000000001"
        )
        params = {
            "daoName": DAO_NAME,
            "tokenName": f"{TOKEN_NAME} Shares",
            "tokenSymbol": TOKEN_SYMBOL,
            "lootTokenName": f"{TOKEN_NAME} Loot",
            "lootTokenSymbol": f"{TOKEN_SYMBOL}L",
            "memberAddresses": [orchestrator_addr],
            "memberShares": ["1"],
            "votingPeriodInSeconds": VOTING_PERIOD,
            "gracePeriodInSeconds": GRACE_PERIOD,
            "quorum": "0",
            "sponsorThreshold": "0",
            "minRetention": "66",
        }
        params_file.write_text(json.dumps(params, indent=2))

        try:
            tx = self._run_moloch("summon", "--no-workspace", "--params", str(params_file))
        finally:
            params_file.unlink(missing_ok=True)

        result = asyncio.run(self._execute_via_caw(
            description=f"Summon DAO: {DAO_NAME}",
            allowed_contracts=[AFC_SUMMONER],
            tx=tx,
        ))

        # Parse the DAO address from the tx receipt
        dao_address = self._parse_dao_from_receipt(result.tx_hash)
        if not dao_address:
            # Fallback: ask the human (tx hash is shown — they can look up on Basescan)
            print(f"\n  ⚠️  Could not auto-parse DAO address from receipt.")
            print(f"     Tx: https://basescan.org/tx/{result.tx_hash}")
            dao_address = input("  Enter DAO address from Basescan: ").strip()

        print(f"  ✓ DAO summoned: {dao_address}")
        print(f"     Basescan: https://basescan.org/tx/{result.tx_hash}")

        self.state["dao_address"] = dao_address
        self.state["summon_tx"] = result.tx_hash
        self._save_state()
        return dao_address

    def propose_membership(self, specialist: str) -> str:
        """
        Submit a mint-shares governance proposal for the specialist address.

        Returns:
            Proposal ID as a string (from on-chain state or receipt).
        """
        dao = self.state.get("dao_address")
        if not dao:
            raise RuntimeError("DAO not summoned yet. Run summon_dao() first.")

        print(f"\n📋 Proposing membership for {specialist}...")

        tx = self._run_moloch(
            "mint-shares",
            "--no-workspace",
            "--dao", dao,
            "--to", specialist,
            "--amount", "1",
            "--title", f"Specialist Membership: {specialist[:10]}...",
        )

        result = asyncio.run(self._execute_via_caw(
            description=f"Propose membership for {specialist}",
            allowed_contracts=[dao],
            tx=tx,
        ))

        # Get the proposal ID from on-chain state via moloch-agent read
        proposal_id = self._read_latest_proposal_id(dao, result.tx_hash)
        print(f"  ✓ Proposal submitted: #{proposal_id}")
        print(f"     Basescan: https://basescan.org/tx/{result.tx_hash}")

        self.state["membership_proposal"] = proposal_id
        self.state["specialist_address"] = specialist
        self.state["propose_tx"] = result.tx_hash
        self._save_state()
        return str(proposal_id)

    def vote_on_proposal(self, proposal_id: str, approved: bool = True) -> TxResult:
        """
        Cast a vote on a governance proposal.

        Args:
            proposal_id: The proposal ID (integer as string).
            approved: True to vote YES, False to vote NO.

        Returns:
            TxResult with tx_hash.
        """
        dao = self.state.get("dao_address")
        if not dao:
            raise RuntimeError("DAO not summoned yet.")

        vote_str = "true" if approved else "false"
        label = "YES" if approved else "NO"
        print(f"\n🗳️  Voting {label} on proposal #{proposal_id}...")

        tx = self._run_moloch(
            "vote",
            "--dao", dao,
            "--proposal", str(proposal_id),
            "--approved", vote_str,
        )

        result = asyncio.run(self._execute_via_caw(
            description=f"Vote {label} on proposal #{proposal_id}",
            allowed_contracts=[dao],
            tx=tx,
        ))

        print(f"  ✓ Vote cast: {label}")
        print(f"     Basescan: https://basescan.org/tx/{result.tx_hash}")

        self.state["vote_cast"] = approved
        self.state["vote_tx"] = result.tx_hash
        self._save_state()
        return result

    # ── Receipt helpers ────────────────────────────────────────

    def _parse_dao_from_receipt(self, tx_hash: Optional[str]) -> Optional[str]:
        """
        Parse the new Baal DAO address from the SummonBaal event in the tx receipt.

        The SummonBaal event has:
          topic[0] = event signature hash
          topic[1] = baal address (indexed, padded to 32 bytes)
        """
        if not tx_hash or tx_hash.startswith("0xdead"):
            return None  # mock tx hash — skip RPC call

        try:
            payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "eth_getTransactionReceipt",
                "params": [tx_hash],
                "id": 1,
            }).encode()
            req = urllib.request.Request(
                RPC_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = json.loads(resp.read())

            receipt = body.get("result") or {}
            for log in receipt.get("logs", []):
                topics = log.get("topics", [])
                if topics and topics[0].lower() == _SUMMON_BAAL_TOPIC0.lower():
                    # topic[1] is the baal address, padded: "0x000...000<addr_20bytes>"
                    raw = topics[1]
                    return "0x" + raw[-40:]  # last 20 bytes = address
        except Exception as exc:
            print(f"  ⚠️  Receipt parse error: {exc}")

        return None

    def _read_latest_proposal_id(self, dao: str, tx_hash: Optional[str]) -> str:
        """
        Read the current proposalCount from the DAO to get the latest proposal ID.
        Falls back to manual input if the RPC call fails.
        """
        try:
            # eth_call to proposalCount() — selector: keccak256("proposalCount()")[0:4] = 0xb7ab4db5
            payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "eth_call",
                # "params": [{"to": dao, "data": "0xb7ab4db5"}, "latest"], # wrong function id generated by AI
                "params": [{"to": dao, "data": "0xda35c664"}, "latest"],
                "id": 1,
            }).encode()
            req = urllib.request.Request(
                RPC_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = json.loads(resp.read())
            hex_count = body.get("result", "0x0")
            count = int(hex_count, 16)
            return str(count)  # proposalCount is the ID of the just-submitted proposal
        except Exception as exc:
            print(f"  ⚠️  Could not read proposalCount: {exc}")
            print(f"     Tx: https://basescan.org/tx/{tx_hash}")
            return input("  Enter proposal ID from Basescan: ").strip()

    # ── Full PoC flow ──────────────────────────────────────────

    def run_poc(self, specialist_address: Optional[str] = None):
        """Run the complete PoC flow: summon → propose → vote."""
        specialist = specialist_address or os.getenv("SPECIALIST_WALLET_ADDRESS")
        if not specialist:
            raise ValueError(
                "Specialist address required. Pass as argument or set "
                "SPECIALIST_WALLET_ADDRESS env var."
            )

        print("=" * 55)
        print("  CAW × Moloch-Agent PoC")
        print("=" * 55)

        try:
            dao = os.getenv("DAO_ADDRESS")
            if dao:
                print(f"Skipping DAO deployment: {dao}")
                self.state["dao_address"] = dao
            else:
                # Step 1: Summon DAO
                dao = self.summon_dao()

            # TODO: submit a single Pact for dao interactions            
            # Step 2: Submit membership proposal
            proposal_id = self.propose_membership(specialist)
            # NOTE: proposal immediately goes to voting period if sponsorThreshold=0
            # Step 3: Vote on proposal
            self.vote_on_proposal(proposal_id, approved=True)

            print("\n" + "=" * 55)
            print("  Summary")
            print("=" * 55)
            print(f"  DAO:        {dao}")
            print(f"  Proposal:   #{proposal_id}")
            print(f"  Vote:       YES")
            print(f"  Specialist: {specialist}")
            print(f"\n  Summon tx:  {self.state.get('summon_tx', 'n/a')}")
            print(f"  Propose tx: {self.state.get('propose_tx', 'n/a')}")
            print(f"  Vote tx:    {self.state.get('vote_tx', 'n/a')}")
            print("=" * 55)

        except Exception as exc:
            print(f"\n❌ PoC failed: {exc}")
            raise


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1:
        specialist = sys.argv[1]
    else:
        specialist = os.getenv("SPECIALIST_WALLET_ADDRESS")
    if not specialist:
        print("Usage: python orchestrator.py <specialist_address>")
        print("Or set SPECIALIST_WALLET_ADDRESS in .env")
        sys.exit(1)

    agent = OrchestratorAgent()
    agent.run_poc(specialist)


if __name__ == "__main__":
    main()
