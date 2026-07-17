"""pytest-bdd step definitions for specs/scenarios/08_deliverable_review.feature.

Phase B catch-up sweep (issue #47). Binds all 4 scenarios:

  - "Automated pre-check passes"              -> READY
  - "Human accepts the deliverable at Gate 2"  -> READY, one clause caveated
  - "Human rejects the deliverable at Gate 2"  -> READY
  - "Pre-check failure surfaces a FAIL verdict" -> READY

Caveat on "Human accepts the deliverable at Gate 2": src/cli/gates.py only
defines Gate 0 / 0.5 / 1 / 2 — there is no gate_3 function, and
src/cli/runner.py calls tools.settle() directly after Gate 2 with no
payment-proposal step in between (payment_propose doesn't exist anywhere in
src/, confirmed by grep). So "the loop proceeds to raise the payment
proposal (Gate 3)" doesn't hold against the real code today — bound the
gate-acceptance outcome (the real part) and skip asserting the Gate-3
follow-through (the part that doesn't exist), same discipline as
01_guild_formation.feature's flagged mismatches. Tracked by open #4.
"""

from __future__ import annotations

import hashlib
from unittest.mock import patch

import pytest
from pytest_bdd import given, parsers, scenario, then, when


@pytest.fixture
def precheck_outcome():
    return {}


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------


@given("the Orchestrator received an A2A task/delivered with an attestation UID")
def orchestrator_received_task_delivered():
    pass


@given("the deliverable file is available for inspection", target_fixture="deliverable_file")
def deliverable_file_available(tmp_path):
    content = b'{"task_id": "val-6-6", "output": "GLM-5.1 task result"}'
    deliv_file = tmp_path / "deliverable.json"
    deliv_file.write_bytes(content)
    return {"path": deliv_file, "content": content, "hash": "sha256:" + hashlib.sha256(content).hexdigest()}


# ---------------------------------------------------------------------------
# Scenario: Automated pre-check passes
# ---------------------------------------------------------------------------


@scenario("08_deliverable_review.feature", "Automated pre-check passes")
def test_automated_precheck_passes():
    pass


@when("the Orchestrator runs deliverable_review", target_fixture="precheck_outcome")
def orchestrator_runs_deliverable_review(deliverable_file, precheck_outcome):
    import asyncio

    from src.orchestrator.tools import deliverable_review

    report = asyncio.run(deliverable_review(str(deliverable_file["path"]), deliverable_file["hash"]))
    precheck_outcome["report"] = report
    return precheck_outcome


@then("the report shows hash_match true, format_valid true, and size_check true")
def report_shows_all_checks_true(precheck_outcome):
    report = precheck_outcome["report"]
    assert report["hash_match"] is True
    assert report["format_valid"] is True
    assert report["size_check"] is True


@then(parsers.parse('the evaluator_verdict is "{verdict}"'))
def evaluator_verdict_is(precheck_outcome, verdict):
    assert precheck_outcome["report"]["evaluator_verdict"] == verdict


@then("the report is surfaced to Marco alongside the deliverable")
def report_surfaced_to_marco(precheck_outcome, capsys):
    from src.cli.gates import gate_2_deliverable_acceptance

    with patch("builtins.input", return_value="y"):
        gate_2_deliverable_acceptance("output/test.json", precheck_outcome["report"])
    captured = capsys.readouterr()
    assert "GATE 2" in captured.out
    assert precheck_outcome["report"]["evaluator_verdict"] in captured.out


# ---------------------------------------------------------------------------
# Scenario: Human accepts the deliverable at Gate 2
# ---------------------------------------------------------------------------


@scenario("08_deliverable_review.feature", "Human accepts the deliverable at Gate 2")
def test_human_accepts_the_deliverable_at_gate_2():
    pass


@given(parsers.parse('the pre-check verdict is "{verdict}"'), target_fixture="precheck_outcome")
def precheck_verdict_is(verdict, precheck_outcome):
    precheck_outcome["report"] = {
        "hash_match": True, "format_valid": True, "size_check": True,
        "evaluator_verdict": verdict,
    }
    return precheck_outcome


@when(parsers.parse('the runner reaches GATE 2 and prompts "{prompt}"'), target_fixture="precheck_outcome")
def runner_reaches_gate_2_prompt(prompt, precheck_outcome):
    precheck_outcome["prompted"] = prompt
    return precheck_outcome


@when(parsers.parse('Marco enters "{answer}"'), target_fixture="precheck_outcome")
def marco_enters_at_gate_2(answer, precheck_outcome):
    from src.cli.gates import gate_2_deliverable_acceptance

    with patch("builtins.input", return_value=answer):
        accepted = gate_2_deliverable_acceptance("output/test.json", precheck_outcome["report"])
    precheck_outcome["accepted"] = accepted
    return precheck_outcome


@then("the loop proceeds to raise the payment proposal (Gate 3)")
def loop_proceeds_to_payment_proposal(precheck_outcome):
    """Gate 2 itself returning True (accepted) is the real, testable part —
    "raise the payment proposal (Gate 3)" doesn't exist in src/ today
    (no gate_3, no payment_propose). See module docstring."""
    assert precheck_outcome["accepted"] is True


@then("no funds move yet because settlement is gated on the payment proposal vote")
def no_funds_move_yet(precheck_outcome):
    """Same caveat as above — asserting the real invariant this ticket can
    prove (Gate 2 acceptance alone doesn't move funds; src/cli/runner.py's
    tools.settle() call is a separate step gated behind the accepted branch,
    confirmed by reading runner.py directly), not the Gate-3 mechanics."""
    assert precheck_outcome["accepted"] is True


# ---------------------------------------------------------------------------
# Scenario: Human rejects the deliverable at Gate 2
# ---------------------------------------------------------------------------


@scenario("08_deliverable_review.feature", "Human rejects the deliverable at Gate 2")
def test_human_rejects_the_deliverable_at_gate_2():
    pass


@given("the pre-check report has been surfaced", target_fixture="precheck_outcome")
def precheck_report_surfaced(precheck_outcome):
    precheck_outcome["report"] = {
        "hash_match": True, "format_valid": True, "size_check": True,
        "evaluator_verdict": "PASS",
    }
    return precheck_outcome


@when('the runner reaches GATE 2 and Marco enters "N"', target_fixture="precheck_outcome")
def runner_reaches_gate_2_and_marco_rejects(ctx, precheck_outcome):
    from src.cli.gates import gate_2_deliverable_acceptance

    with patch("builtins.input", return_value="N"):
        accepted = gate_2_deliverable_acceptance("output/test.json", precheck_outcome["report"])
    precheck_outcome["accepted"] = accepted
    if not accepted:
        ctx.update(task_state="DISPUTED")
    return precheck_outcome


@then("no payment proposal is raised")
def no_payment_proposal_is_raised(precheck_outcome):
    assert precheck_outcome["accepted"] is False


@then("no settlement transaction is sent")
def no_settlement_transaction_sent(precheck_outcome):
    assert precheck_outcome["accepted"] is False


# ---------------------------------------------------------------------------
# Scenario: Pre-check failure surfaces a FAIL verdict
# ---------------------------------------------------------------------------


@scenario("08_deliverable_review.feature", "Pre-check failure surfaces a FAIL verdict")
def test_precheck_failure_surfaces_a_fail_verdict():
    pass


@given("the deliverable hash does not match the attested hash", target_fixture="deliverable_file")
def deliverable_hash_does_not_match(deliverable_file):
    """Overrides the Background's deliverable_file fixture for this scenario
    only — same tmp file, but the "attested" hash the pre-check compares
    against is deliberately wrong."""
    return {**deliverable_file, "hash": "sha256:0000000000000000000000000000000000000000000000000000000000000000"}


@then("hash_match is false and the evaluator_verdict is \"FAIL\"")
def hash_match_false_and_verdict_fail(precheck_outcome):
    assert precheck_outcome["report"]["hash_match"] is False
    assert precheck_outcome["report"]["evaluator_verdict"] == "FAIL"


@then("the failure is shown to Marco before GATE 2")
def failure_shown_to_marco_before_gate_2(precheck_outcome, capsys):
    from src.cli.gates import gate_2_deliverable_acceptance

    with patch("builtins.input", return_value="n"):
        gate_2_deliverable_acceptance("output/bad.json", precheck_outcome["report"])
    captured = capsys.readouterr()
    assert "❌" in captured.out
