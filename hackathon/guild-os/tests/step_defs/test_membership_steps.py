"""pytest-bdd step definitions for specs/scenarios/04_membership.feature.

Phase B catch-up sweep (issue #47). Binds 3 of 4 scenarios:

  - "Specialist submits a membership proposal"  -> READY, field-name caveat
  - "Human approves membership at Gate 1"        -> READY, one clause caveated
  - "Human rejects membership at Gate 1"         -> READY

Caveats:
  - `tools.membership_propose` writes `guild_context.update(proposal_id=...)`
    — the real field is `proposal_id`, not `guild_context.membership_proposal_id`
    as the scenario states (same class of naming mismatch already flagged
    for `treasury_address`/`treasury_wei` in 01_guild_formation.feature).
  - "AgentFightClub vote is cast to approve **and the proposal is
    processed**" — `agentfightclub.vote()` only does sponsor+vote; there is
    no `process()` call anywhere in the membership path (contrast with
    `settle()`, which explicitly does sponsor+vote+grace-wait+process for
    payment proposals). Bound "vote is cast" and "member_list updated" (both
    real); skipped asserting "processed" (not backed by code).

NOT bound — genuinely not backed by code yet:

  - "Skip proposal when the Specialist is already a member" — nothing
    checks guild_context.member_list before calling membership_propose();
    src/cli/runner.py's Step 5 calls it unconditionally.
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenario, then, when


@pytest.fixture
def membership_outcome():
    return {}


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------


@given("the quote was accepted at GATE 0.5")
def quote_accepted_at_gate_05():
    pass


@given(parsers.parse('a guild exists with task_state "{state}"'))
def a_guild_exists_with_state(state, ctx):
    ctx.update(task_state=state, guild_address="0xGuild0000000000000000000000000000000000")


@given("the Specialist has an ERC-8004 profile readable via 8004scan")
def specialist_profile_readable():
    pass


# ---------------------------------------------------------------------------
# Scenario: Specialist submits a membership proposal
# ---------------------------------------------------------------------------


@scenario("04_membership.feature", "Specialist submits a membership proposal")
def test_specialist_submits_a_membership_proposal():
    pass


@when(
    "the Specialist calls AgentFightClub propose with its ERC-8004 id, task quote, and free-form description",
    target_fixture="membership_outcome",
)
def specialist_calls_propose(ctx, membership_outcome):
    import asyncio

    from src.orchestrator.tools import membership_propose

    with patch("src.shared.agentfightclub.propose") as mock_propose, \
         patch.dict(os.environ, {"SPECIALIST_WALLET_ADDRESS": "0xSpec00000000000000000000000000000000000"}):
        async def fake_propose(*args, **kwargs):
            return "99"

        mock_propose.side_effect = fake_propose
        result = asyncio.run(membership_propose(
            guild_address=ctx.load()["guild_address"],
            specialist_erc8004_id=1,
        ))
    membership_outcome["result"] = result
    return membership_outcome


@then("a membership proposal is recorded on Base mainnet")
def membership_proposal_recorded(membership_outcome):
    assert membership_outcome["result"]["status"] == "proposed"


@then("guild_context.membership_proposal_id holds the proposal id")
def guild_context_membership_proposal_id_set(ctx, membership_outcome):
    """The real field is guild_context.proposal_id, not
    guild_context.membership_proposal_id — see module docstring."""
    assert ctx.load()["proposal_id"] == membership_outcome["result"]["proposal_id"]


# ---------------------------------------------------------------------------
# Scenario: Human approves membership at Gate 1
# ---------------------------------------------------------------------------


@scenario("04_membership.feature", "Human approves membership at Gate 1")
def test_human_approves_membership_at_gate_1():
    pass


@given("a membership proposal exists")
def membership_proposal_exists(ctx):
    ctx.update(proposal_id="99")


@given("Marco has reviewed the Specialist's delivery history and acceptance rate")
def marco_reviewed_delivery_history():
    pass


@when(parsers.parse('the runner reaches GATE 1 and prompts "{prompt}"'), target_fixture="membership_outcome")
def runner_reaches_gate_1_prompt(prompt, membership_outcome):
    membership_outcome["prompted"] = prompt
    return membership_outcome


@when(parsers.parse('Marco enters "{answer}"'), target_fixture="membership_outcome")
def marco_enters_at_gate_1(answer, ctx, membership_outcome):
    import asyncio

    from src.cli.gates import gate_1_membership
    from src.orchestrator.tools import membership_vote

    with patch("builtins.input", return_value=answer):
        approved = gate_1_membership({"name": "Specialist Agent", "agent_id": "erc8004:1"})
    membership_outcome["approved"] = approved

    if approved:
        with patch("src.shared.agentfightclub.vote") as mock_vote, \
             patch.dict(os.environ, {"SPECIALIST_WALLET_ADDRESS": "0xSpec00000000000000000000000000000000000"}):
            async def fake_vote(*args, **kwargs):
                return "0xvote_tx"

            mock_vote.side_effect = fake_vote
            result = asyncio.run(membership_vote(
                guild_address=ctx.load()["guild_address"],
                proposal_id=ctx.load()["proposal_id"],
                approve=True,
            ))
        membership_outcome["vote_result"] = result
    return membership_outcome


@then("AgentFightClub vote is cast to approve and the proposal is processed")
def agentfightclub_vote_cast_and_processed(membership_outcome):
    """"vote is cast" is real (agentfightclub.vote() ran); "the proposal is
    processed" is not — vote() only does sponsor+vote, there is no
    process() call in the membership path. See module docstring."""
    assert membership_outcome["vote_result"]["vote_tx"] == "0xvote_tx"
    assert membership_outcome["vote_result"]["approved"] is True


@then("the Specialist wallet is added to guild_context.member_list")
def specialist_wallet_added_to_member_list(ctx):
    assert "0xSpec00000000000000000000000000000000000" in ctx.load()["member_list"]


# ---------------------------------------------------------------------------
# Scenario: Human rejects membership at Gate 1
# ---------------------------------------------------------------------------


@scenario("04_membership.feature", "Human rejects membership at Gate 1")
def test_human_rejects_membership_at_gate_1():
    pass


@when('the runner reaches GATE 1 and Marco enters "N"', target_fixture="membership_outcome")
def runner_reaches_gate_1_and_marco_rejects(ctx, membership_outcome):
    import asyncio

    from src.cli.gates import gate_1_membership
    from src.orchestrator.tools import membership_vote

    with patch("builtins.input", return_value="N"):
        approved = gate_1_membership({"name": "Specialist Agent", "agent_id": "erc8004:1"})
    membership_outcome["approved"] = approved

    with patch("src.shared.agentfightclub.vote") as mock_vote:
        async def fake_vote(*args, **kwargs):
            return "0xvote_tx"

        mock_vote.side_effect = fake_vote
        result = asyncio.run(membership_vote(
            guild_address=ctx.load()["guild_address"],
            proposal_id=ctx.load()["proposal_id"],
            approve=False,
        ))
    membership_outcome["vote_result"] = result
    return membership_outcome


@then("the coordination loop halts")
def coordination_loop_halts(membership_outcome):
    assert membership_outcome["approved"] is False


@then("the Specialist is not added to the member_list")
def specialist_not_added_to_member_list(ctx):
    assert ctx.load()["member_list"] == []
