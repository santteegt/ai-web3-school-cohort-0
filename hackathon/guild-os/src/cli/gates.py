"""HumanGates — CLI prompts for the four human confirmation gates.

Every gate MUST halt execution and wait for explicit y/N input.
Never auto-proceed or default to approval.

Gates:
  Gate 0   — Candidate selection (Step 4): review ERC-8004 shortlist
  Gate 0.5 — Quote acceptance (Step 4): review Specialist quote
  Gate 1   — Membership (Step 5–7): review profile + approve via AgentFightClub vote
  Gate 2   — Deliverable acceptance (Step 13): review work + pre-check report
"""

from __future__ import annotations

import json


def _prompt(label: str, details: str) -> bool:
    print(f"\n{'━' * 60}")
    print(f"  {label}")
    print(f"{'━' * 60}")
    print(details)
    print(f"{'━' * 60}")
    while True:
        answer = input("\n  Proceed? [y/N]: ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no", ""):
            return False
        print("  Please enter y or n.")


def gate_0_candidate_selection(shortlist: list[dict]) -> bool:
    """Gate 0 — Human approves invite to selected Specialist candidate."""
    details = json.dumps(shortlist, indent=4)
    return _prompt(
        "GATE 0 — Candidate Selection",
        f"ERC-8004 Shortlist:\n{details}\n\n  Approve invite to top candidate?",
    )


def gate_0_5_quote_acceptance(quote: dict) -> bool:
    """Gate 0.5 — Human accepts Specialist's quoted scope, cost, and timeline."""
    details = (
        f"  Scope:    {quote.get('scope', 'N/A')}\n"
        f"  Cost:     {int(quote.get('estimated_cost_wei', 0)) / 1e18:.6f} ETH\n"
        f"  Deadline: {quote.get('deadline_iso', 'N/A')}"
    )
    return _prompt("GATE 0.5 — Quote Acceptance", details)


def gate_1_membership(specialist_profile: dict) -> bool:
    """Gate 1 — Human votes to approve Specialist membership via AgentFightClub."""
    details = json.dumps(specialist_profile, indent=4)
    return _prompt(
        "GATE 1 — Membership Approval",
        f"Specialist ERC-8004 Profile:\n{details}\n\n  Call AgentFightClub vote(approve=True)?",
    )


def gate_2_deliverable_acceptance(deliverable_reference: str, pre_check_report: dict) -> bool:
    """Gate 2 — Human accepts deliverable (triggers settle) or rejects (DISPUTED)."""
    check_summary = (
        f"  Hash present:  {'✅' if pre_check_report.get('hash_match') else '❌'}\n"
        f"  Format valid:  {'✅' if pre_check_report.get('format_valid') else '❌'}\n"
        f"  Size > 0:      {'✅' if pre_check_report.get('size_check') else '❌'}\n"
        f"  Verdict:       {pre_check_report.get('evaluator_verdict', 'N/A')}"
    )
    details = f"  Deliverable: {deliverable_reference}\n\n{check_summary}"
    accepted = _prompt("GATE 2 — Deliverable Acceptance", details)
    if not accepted:
        print("\n  ⚠️  Rejection recorded — guild_context.task_state → DISPUTED")
        print("  Funds remain locked in AgentFightClub treasury.")
        print("  Exit path: Moloch v3 ragequit() — see README for instructions.\n")
    return accepted
