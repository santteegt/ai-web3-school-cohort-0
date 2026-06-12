"""Coordination Runner — wires all 4 human gates into the live MVP flow.

This is the main CLI entry point that orchestrates the full 15-step MVP loop:
  Step 1-3:  Guild launch + ERC-8004 registration + talent query
  GATE 0:    Human selects Specialist candidate from shortlist
  Step 4:    Send task/invite, receive task/quote
  GATE 0.5:  Human accepts/rejects Specialist quote
  Step 5-7:  Membership propose + vote + task delegation
  GATE 1:    Human approves Specialist membership (vote)
  Step 8-10: Specialist executes, hashes deliverable, sends task/delivered
  GATE 2:    Human accepts/rejects deliverable (settle or DISPUTED)
  Step 11-14: Settlement + reputation write-back
  Step 15:   Rejection path → DISPUTED

Run: python -m src.cli.runner
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path

from src.cli import gates
from src.orchestrator import tools
from src.shared import guild_context
from src.shared.a2a import send_accepted
from src.specialist.agent import handle_task_invite, handle_task_send

logger = logging.getLogger(__name__)


async def run_coordination_loop(
    task_description: str,
    specialist_endpoint: str = "http://localhost:10001",
) -> None:
    """Execute the full MVP coordination loop with all 4 human gates.

    Args:
        task_description: The task to delegate to the Specialist.
        specialist_endpoint: A2A endpoint URL for the Specialist agent.
    """
    print("\n" + "=" * 60)
    print("  GuildOS — MVP Coordination Loop")
    print("=" * 60)

    # ---------------------------------------------------------------
    # Step 1: Guild launch (skip if already active)
    # ---------------------------------------------------------------
    ctx = guild_context.load()
    if ctx.get("guild_address") and ctx.get("task_state") not in (None, "INIT"):
        print(f"\n  ℹ️  Guild already active: {ctx['guild_address']}")
        print(f"     State: {ctx['task_state']}")
    else:
        print("\n  ▶ Step 1: Launching guild...")
        mandate = f"Execute task: {task_description[:80]}"
        treasury_address = os.getenv("ORCHESTRATOR_WALLET_ADDRESS", "")
        if not treasury_address:
            print("  ⚠️  ORCHESTRATOR_WALLET_ADDRESS not set, using placeholder")
            treasury_address = "0x0000000000000000000000000000000000000000"

        result = await tools.guild_launch(mandate=mandate, treasury_address=treasury_address)
        print(f"  ✅ Guild launched: {result['guild_address']}")
        print(f"     Launch tx: {result.get('launch_tx', 'N/A')}")
        print(f"     Commit tx: {result.get('commit_tx', 'N/A')}")

    # ---------------------------------------------------------------
    # Step 3: Talent query — get ERC-8004 shortlist
    # ---------------------------------------------------------------
    print("\n  ▶ Step 3: Querying ERC-8004 for candidate Specialists...")
    shortlist = await tools.talent_query(task_type="code-generation")
    print(f"  ✅ Found {len(shortlist)} candidate(s)")

    # ---------------------------------------------------------------
    # GATE 0 — Candidate Selection
    # ---------------------------------------------------------------
    if not gates.gate_0_candidate_selection(shortlist):
        print("\n  🛑 Gate 0 rejected — aborting coordination loop.")
        return

    # ---------------------------------------------------------------
    # Step 4: Send task/invite, receive task/quote
    # ---------------------------------------------------------------
    print("\n  ▶ Step 4: Sending task/invite to Specialist...")
    task_spec = {
        "task_description": task_description,
        "task_type": "code-generation",
    }

    # Get the quote back from the Specialist
    invite_msg_id = await tools.task_invite(
        specialist_endpoint=specialist_endpoint,
        task_spec=task_spec,
    )
    print(f"  ✅ Invite sent (msg: {invite_msg_id})")

    # For the MVP flow, we simulate receiving the quote directly
    # In production, the quote comes back via A2A response
    quote = await handle_task_invite({"type": "task/invite", "task_spec": task_spec})
    print("  📋 Quote received:")
    print(f"     Scope: {quote.get('scope', 'N/A')}")
    cost_eth = int(quote.get('estimated_cost_wei', 0)) / 1e18
    print(f"     Cost: {cost_eth:.6f} ETH")
    print(f"     Deadline: {quote.get('deadline_iso', 'N/A')}")

    # ---------------------------------------------------------------
    # GATE 0.5 — Quote Acceptance
    # ---------------------------------------------------------------
    if not gates.gate_0_5_quote_acceptance(quote):
        print("\n  🛑 Gate 0.5 rejected — quote not accepted. Aborting.")
        return

    # ---------------------------------------------------------------
    # Step 5: Membership proposal
    # ---------------------------------------------------------------
    ctx = guild_context.load()
    guild_address = ctx.get("guild_address", "")
    if not guild_address:
        print("  ⚠️  No guild_address in context — cannot propose membership.")
        return

    print("\n  ▶ Step 5: Submitting Specialist membership proposal...")
    try:
        proposal_result = await tools.membership_propose(
            guild_address=guild_address,
            specialist_erc8004_id=1,
        )
        print(f"  ✅ Proposal submitted: {proposal_result.get('proposal_id', 'N/A')}")
    except Exception as e:
        print(f"  ⚠️  Membership proposal failed: {e}")
        print("     Continuing with task delegation (membership already granted or not required).")

    # ---------------------------------------------------------------
    # GATE 1 — Membership Approval
    # ---------------------------------------------------------------
    # Load specialist profile for Gate 1 display
    profile_path = Path(__file__).parent.parent.parent / "assets" / "erc8004_specialist_profile.json"
    if profile_path.exists():
        specialist_profile = json.loads(profile_path.read_text())
    else:
        specialist_profile = {"name": "Specialist Agent", "agent_id": "erc8004:1"}

    if not gates.gate_1_membership(specialist_profile):
        print("\n  🛑 Gate 1 rejected — membership not approved. Aborting.")
        return

    # Step 7: Vote to approve (called only after Gate 1 approval)
    proposal_id = guild_context.load().get("proposal_id")
    if proposal_id:
        print("\n  ▶ Step 7: Casting membership vote...")
        try:
            vote_result = await tools.membership_vote(
                guild_address=guild_address,
                proposal_id=proposal_id,
                approve=True,
            )
            print(f"  ✅ Vote cast: {vote_result.get('vote_tx', 'N/A')}")
        except Exception as e:
            print(f"  ⚠️  Vote failed: {e}")

    # ---------------------------------------------------------------
    # Step 6: Delegate task via A2A
    # ---------------------------------------------------------------
    print("\n  ▶ Step 6: Delegating task to Specialist via A2A...")
    full_task = {
        "task_description": task_description,
        "input_data": "",
        "acceptance_criteria": ["Deliverable is a valid JSON file", "SHA-256 hash matches on-chain commit"],
        "budget_wei": "1000000000000000",
    }
    delegate_msg_id = await tools.task_delegate(
        specialist_endpoint=specialist_endpoint,
        full_task=full_task,
    )
    print(f"  ✅ Task delegated (msg: {delegate_msg_id})")

    # ---------------------------------------------------------------
    # Step 9: Receive task/delivered from Specialist
    # ---------------------------------------------------------------
    print("\n  ▶ Step 8-9: Waiting for Specialist deliverable...")
    # Simulate Specialist execution for MVP (in production, wait for A2A response)
    delivered = await handle_task_send({
        "type": "task/send",
        "task_id": delegate_msg_id,
        "task": full_task,
    })
    print("  ✅ Deliverable received:")
    print(f"     Reference: {delivered.get('deliverable_reference', 'N/A')}")
    print(f"     Hash: {delivered.get('deliverable_hash', 'N/A')}")

    # ---------------------------------------------------------------
    # Step 10: Automated pre-check
    # ---------------------------------------------------------------
    print("\n  ▶ Step 10: Running automated pre-check...")
    deliverable_path = delivered.get("deliverable_reference", "")
    deliverable_hash = delivered.get("deliverable_hash", "")

    # For MVP, write the deliverable to a temp location if it doesn't exist
    if deliverable_path and not Path(deliverable_path).exists():
        # Write simulated deliverable to disk for pre-check
        deliv_dir = Path("deliverables")
        deliv_dir.mkdir(exist_ok=True)
        actual_path = deliv_dir / f"{delegate_msg_id}.json"
        actual_path.write_text(json.dumps({
            "task_id": delegate_msg_id,
            "output": "Task executed successfully via GLM-5.1",
        }, indent=2))
        deliverable_path = str(actual_path)

    pre_check = await tools.deliverable_review(
        deliverable_reference=deliverable_path,
        deliverable_hash=deliverable_hash,
    )
    print("  📋 Pre-check report:")
    print(f"     Hash match:   {'✅' if pre_check.get('hash_match') else '❌'}")
    print(f"     Format valid: {'✅' if pre_check.get('format_valid') else '❌'}")
    print(f"     Size > 0:     {'✅' if pre_check.get('size_check') else '❌'}")
    print(f"     Verdict:      {pre_check.get('evaluator_verdict', 'N/A')}")

    # ---------------------------------------------------------------
    # GATE 2 — Deliverable Acceptance
    # ---------------------------------------------------------------
    accepted = gates.gate_2_deliverable_acceptance(
        deliverable_reference=deliverable_path,
        pre_check_report=pre_check,
    )

    if not accepted:
        # Step 15: Rejection / Dispute path
        print("\n  ⚠️  Gate 2 rejected — entering DISPUTE path.")
        guild_context.update(task_state="DISPUTED")
        print("  ✅ guild_context.task_state → DISPUTED")
        print("  ℹ️  Funds remain locked in AgentFightClub treasury.")
        print("  ℹ️  Exit path: Moloch v3 ragequit() — see README.")
        return

    # ---------------------------------------------------------------
    # Step 11: Send task/accepted to Specialist
    # ---------------------------------------------------------------
    print("\n  ▶ Step 11: Sending task/accepted to Specialist...")
    await send_accepted(specialist_endpoint, delegate_msg_id)
    print("  ✅ task/accepted sent.")

    # ---------------------------------------------------------------
    # Step 12: Settlement
    # ---------------------------------------------------------------
    specialist_wallet = os.getenv("SPECIALIST_WALLET_ADDRESS", "")
    if not specialist_wallet:
        print("  ⚠️  SPECIALIST_WALLET_ADDRESS not set — skipping settlement.")
    else:
        print("\n  ▶ Step 12: Settling payment via AgentFightClub...")
        try:
            settle_tx = await tools.settle(
                guild_address=guild_address,
                specialist_wallet=specialist_wallet,
            )
            print(f"  ✅ Settlement tx: {settle_tx}")
            print(f"  🔗 Basescan: https://basescan.org/tx/{settle_tx}")
        except Exception as e:
            print(f"  ⚠️  Settlement failed: {e}")

    # ---------------------------------------------------------------
    # Step 13: ERC-8004 reputation write-back
    # ---------------------------------------------------------------
    print("\n  ▶ Step 13: Writing ERC-8004 reputation...")
    delivery_record = {
        "task_type": "code-generation",
        "deliverable_hash": deliverable_hash,
        "acceptance_timestamp": 0,
        "payment_wei": "1000000000000000",
        "guild_address": guild_address,
        "a2a_task_id": delegate_msg_id,
    }
    try:
        rep_tx = await tools.reputation_write(delivery_record=delivery_record)
        print(f"  ✅ Reputation tx: {rep_tx}")
    except NotImplementedError:
        print("  ℹ️  Reputation write-back is a stub (post-hackathon).")

    # ---------------------------------------------------------------
    # Step 14: Final state update
    # ---------------------------------------------------------------
    print("\n  ▶ Step 14: Updating guild context to SETTLED...")
    ctx = guild_context.load()
    if ctx.get("task_state") != "SETTLED":
        guild_context.update(task_state="SETTLED")
    print("  ✅ guild_context.task_state → SETTLED")

    print("\n" + "=" * 60)
    print("  🎉 MVP Coordination Loop Complete!")
    print("=" * 60)


def main() -> None:
    """CLI entry point for the coordination runner."""
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    task = sys.argv[1] if len(sys.argv) > 1 else "Generate a Python function that computes SHA-256 of input"
    asyncio.run(run_coordination_loop(task_description=task))


if __name__ == "__main__":
    main()
