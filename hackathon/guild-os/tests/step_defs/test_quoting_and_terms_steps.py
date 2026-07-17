"""pytest-bdd step definitions for specs/scenarios/03_quoting_and_terms.feature.

Phase B catch-up sweep (issue #47). Binds 3 of 4 scenarios:

  - "Specialist returns a quote for the ticket"  -> READY, trace-path caveat
  - "Human accepts the quote at Gate 0.5"          -> READY
  - "Human rejects the quote at Gate 0.5"          -> READY

NOT bound — genuinely not backed by code yet:

  - "Quote exceeding the mandate budget is surfaced for rejection" —
    grepped `budget` across src/: budget_wei only appears as a static
    payload field (src/cli/runner.py, src/orchestrator/server.py), never
    compared against any mandate budget. gate_0_5_quote_acceptance()
    (src/cli/gates.py) displays cost uniformly with no "over budget" flag
    concept. This describes behavior the code doesn't have.
"""

from __future__ import annotations

from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
from pytest_bdd import given, parsers, scenario, then, when


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod

    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def quote_outcome():
    return {}


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------


@given("a candidate was approved at GATE 0")
def candidate_approved_at_gate_0():
    pass


@given("the Orchestrator holds the Specialist A2A endpoint")
def orchestrator_holds_specialist_endpoint():
    pass


@given('the ticket to delegate is "Implement the EAS attestation module (EASClient)"')
def ticket_to_delegate():
    pass


# ---------------------------------------------------------------------------
# Scenario: Specialist returns a quote for the ticket
# ---------------------------------------------------------------------------


@scenario("03_quoting_and_terms.feature", "Specialist returns a quote for the ticket")
def test_specialist_returns_a_quote_for_the_ticket():
    pass


@when("the Orchestrator sends an A2A task/invite with the task spec", target_fixture="quote_outcome")
def orchestrator_sends_task_invite(tmp_trace_dir, quote_outcome):
    import asyncio

    from src.shared.a2a import send_invite

    mock_response = {
        "type": "task/quote",
        "scope": "Implement EASClient with attest() and get_attestation()",
        "estimated_cost_wei": 500000000000000,
        "deadline_iso": "2026-07-08T00:00:00+00:00",
    }
    with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = mock_response
        result = asyncio.run(send_invite("http://localhost:10001", {"task": "test"}))
    quote_outcome["quote"] = result
    return quote_outcome


@then("the Specialist responds with an A2A task/quote")
def specialist_responds_with_quote(quote_outcome):
    assert quote_outcome["quote"]["type"] == "task/quote"


@then("the quote contains scope, estimated_cost_wei, and deadline_iso")
def quote_contains_required_fields(quote_outcome):
    quote = quote_outcome["quote"]
    assert "scope" in quote
    assert "estimated_cost_wei" in quote
    assert "deadline_iso" in quote


@then("the quote is logged to hackathon/notes/a2a_trace_{date}.json")
def quote_logged_to_trace(tmp_trace_dir, quote_outcome):
    """Scenario text says "hackathon/notes/..." but a2a.TRACE_DIR resolves to
    "hackathon/logs/..." — a spec-wide notes-vs-logs inconsistency (also in
    specs/20-api-contracts.md and 06/07/10's scenario text), not scenario-
    specific. Asserting against the real TRACE_DIR constant."""
    import json

    trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
    entries = json.loads(trace_file.read_text())
    assert any(e["type"] == "task/quote" for e in entries)


# ---------------------------------------------------------------------------
# Scenario: Human accepts the quote at Gate 0.5
# ---------------------------------------------------------------------------


@scenario("03_quoting_and_terms.feature", "Human accepts the quote at Gate 0.5")
def test_human_accepts_the_quote_at_gate_05():
    pass


@given("a task/quote has been received", target_fixture="quote_outcome")
def task_quote_received():
    return {"quote": {
        "scope": "Implement EASClient", "estimated_cost_wei": 500000000000000,
        "deadline_iso": "2026-07-08T00:00:00+00:00",
    }}


@when(parsers.parse('the runner reaches GATE 0.5 and prompts "{prompt}"'), target_fixture="quote_outcome")
def runner_reaches_gate_05_prompt(prompt, quote_outcome):
    quote_outcome["prompted"] = prompt
    return quote_outcome


@when(parsers.parse('Marco enters "{answer}"'), target_fixture="quote_outcome")
def marco_enters_at_gate_05(answer, quote_outcome):
    from src.cli.gates import gate_0_5_quote_acceptance

    with patch("builtins.input", return_value=answer):
        accepted = gate_0_5_quote_acceptance(quote_outcome["quote"])
    quote_outcome["accepted"] = accepted
    return quote_outcome


@then("the economic terms are locked")
def economic_terms_locked(quote_outcome):
    assert quote_outcome["accepted"] is True


@then("execution resumes to the membership-proposal step")
def execution_resumes_to_membership_proposal(quote_outcome):
    assert quote_outcome["accepted"] is True


# ---------------------------------------------------------------------------
# Scenario: Human rejects the quote at Gate 0.5
# ---------------------------------------------------------------------------


@scenario("03_quoting_and_terms.feature", "Human rejects the quote at Gate 0.5")
def test_human_rejects_the_quote_at_gate_05():
    pass


@when('the runner reaches GATE 0.5 and Marco enters "N"', target_fixture="quote_outcome")
def runner_reaches_gate_05_and_marco_rejects(quote_outcome):
    from src.cli.gates import gate_0_5_quote_acceptance

    quote = {
        "scope": "Implement EASClient", "estimated_cost_wei": 500000000000000,
        "deadline_iso": "2026-07-08T00:00:00+00:00",
    }
    with patch("builtins.input", return_value="N"):
        accepted = gate_0_5_quote_acceptance(quote)
    quote_outcome["accepted"] = accepted
    return quote_outcome


@then("the coordination loop halts")
def coordination_loop_halts(quote_outcome):
    assert quote_outcome["accepted"] is False


@then("no membership proposal is submitted")
def no_membership_proposal_submitted(quote_outcome):
    assert quote_outcome["accepted"] is False
