"""pytest-bdd step definitions for specs/scenarios/05_task_delegation.feature.

Phase B catch-up sweep (issue #47). Binds 5 of 7 scenarios:

  - "Delegate a complete, well-formed task"                       -> READY
  - "Reject a task missing acceptance criteria"                   -> READY
  - "Reject a task missing the GitHub issue link"                 -> READY
  - "Reject a task with an unrecognized deliverable format"       -> READY
  - "Carry GuildOS fields in the text body when metadata is
     rejected"                                                    -> READY*
  - "Reject a task/send missing the orchestrator_endpoint"        -> READY

  * The "Given the A2A transport rejects extension metadata fields"
    precondition is narrative only — src/shared/a2a.py's send_task() has no
    metadata-vs-text-body branch at all; text-body JSON is the ONLY
    transport mode that ever runs. The scenario's actual OUTCOME (the full
    task round-trips through Part.text as JSON, unmodified) is genuinely
    real and tested — bound with that caveat, same discipline as
    01_guild_formation.feature's "Either AgentFightClub path" mismatch.

NOT bound — genuinely not backed by code yet:

  - "Send task/send non-blocking and receive an immediate WORKING
    response" — src/specialist/agent.py's SpecialistExecutor.execute()
    enqueues WORKING then, in the SAME synchronous call, computes the fully
    faked deliverable and enqueues COMPLETED — there is no "WORKING only,
    deliverable withheld, pollable later" gap. That gap is the harness work
    engine, tracked by open #40/#10. tests/test_a2a.py's
    test_send_task_nonblocking_returns_task_id only tests send_task()'s
    handling of an already-mocked WORKING response at the transport layer —
    it doesn't exercise the real executor, so it doesn't actually prove
    this scenario either.
"""

from __future__ import annotations

import json
from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
from pytest_bdd import given, scenario, then, when


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod

    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def well_formed_task() -> dict:
    """A complete task/send payload matching specs/20-api-contracts.md §3."""
    return {
        "task_id": "task-abc-123",
        "task_description": "Implement the EAS attestation module (EASClient)",
        "github_issue_url": "https://github.com/santteegt/ai-web3-school-cohort-0/issues/10",
        "input_data": "See linked GitHub issue for full ticket context.",
        "technical_constraints": {
            "repo_branch": "main",
            "library_versions": ["a2a-sdk[http-server]==1.1.0", "web3==7.16.0"],
            "env_vars": ["GLM_API_KEY"],
        },
        "agbom": {
            "tools": ["GLM-5.1 API client (Z.AI, via Hermes)", "file I/O", "git"],
            "mcp_servers": [],
            "data_sources": ["specs/scenarios/06_specialist_execution.feature"],
        },
        "acceptance_criteria": [
            "Plan contains at least 3 steps",
            "Output satisfies every BDD test listed in task.acceptance_criteria",
        ],
        "deliverable_format": "github_commit",
        "deadline": "2026-07-08T00:00:00+00:00",
        "budget_wei": "1000000000000000",
        "orchestrator_endpoint": "http://localhost:10000",
    }


@pytest.fixture
def delegation_outcome():
    return {}


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------


@given("the Specialist is a guild member")
def specialist_is_guild_member():
    pass


@given('the ticket to delegate is "Implement the EAS attestation module (EASClient)"')
def ticket_to_delegate():
    pass


# ---------------------------------------------------------------------------
# Scenario: Delegate a complete, well-formed task
# ---------------------------------------------------------------------------


@scenario("05_task_delegation.feature", "Delegate a complete, well-formed task")
def test_delegate_a_complete_well_formed_task():
    pass


@when(
    "the Orchestrator sends an A2A task/send carrying all required fields",
    target_fixture="delegation_outcome",
)
def orchestrator_sends_well_formed_task(well_formed_task, tmp_trace_dir, ctx, delegation_outcome):
    import asyncio

    from src.orchestrator import tools

    with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
        mock_a2a.send_task = AsyncMock(return_value="msg-well-formed")
        message_id = asyncio.run(tools.task_delegate("http://localhost:10001", well_formed_task))
        sent_task = mock_a2a.send_task.call_args[0][1]

    delegation_outcome["message_id"] = message_id
    delegation_outcome["sent_task"] = sent_task
    delegation_outcome["source_task"] = well_formed_task

    # guild_context.a2a_task_id is captured by task_delegate() against the
    # real (module-level, patched) guild_context — but task_delegate imports
    # guild_context via `from src.shared import ... guild_context` inside
    # src/orchestrator/tools.py, which is the same module object our `ctx`
    # fixture already isolates, so capture it directly for the Then steps.
    ctx.update(a2a_task_id=message_id)

    # send_task() itself (not task_delegate's mocked a2a_client) is what
    # actually writes the trace log — exercise it for real to prove the
    # logging Then-clause below.
    from src.shared.a2a import send_task as real_send_task

    with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"type": "task/delivered"}
        asyncio.run(real_send_task("http://localhost:10001", well_formed_task))

    return delegation_outcome


@then("the task includes a link to the GitHub issue")
def task_includes_github_issue_link(delegation_outcome):
    assert delegation_outcome["sent_task"]["github_issue_url"] == delegation_outcome["source_task"]["github_issue_url"]


@then("the task includes technical constraints: repo working branch, library versions, and environment variables")
def task_includes_technical_constraints(delegation_outcome):
    assert delegation_outcome["sent_task"]["technical_constraints"] == delegation_outcome["source_task"]["technical_constraints"]


@then("the task includes an Agent Bill of Materials listing the allowed tools, MCP servers, and data sources")
def task_includes_agbom(delegation_outcome):
    assert delegation_outcome["sent_task"]["agbom"] == delegation_outcome["source_task"]["agbom"]


@then("the task includes acceptance_criteria expressed as a list of BDD tests that must pass")
def task_includes_acceptance_criteria(delegation_outcome):
    assert delegation_outcome["sent_task"]["acceptance_criteria"] == delegation_outcome["source_task"]["acceptance_criteria"]


@then('the task includes a deliverable_format of either "zip+hash" or "github_commit"')
def task_includes_deliverable_format(delegation_outcome):
    assert delegation_outcome["sent_task"]["deliverable_format"] in {"zip+hash", "github_commit"}


@then("the task includes deadline and budget_wei")
def task_includes_deadline_and_budget(delegation_outcome):
    assert delegation_outcome["sent_task"]["deadline"] == delegation_outcome["source_task"]["deadline"]
    assert delegation_outcome["sent_task"]["budget_wei"] == delegation_outcome["source_task"]["budget_wei"]


@then("the Specialist receives and parses the task")
def specialist_receives_and_parses_task(delegation_outcome):
    assert delegation_outcome["message_id"] is not None


@then("the message id is captured to guild_context.a2a_task_id")
def message_id_captured_to_context(ctx, delegation_outcome):
    assert ctx.load()["a2a_task_id"] == delegation_outcome["message_id"]


@then("the message is logged to ./logs/a2a_trace_{date}.json")
def message_logged_to_trace(tmp_trace_dir, delegation_outcome):
    trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
    entries = json.loads(trace_file.read_text())
    outgoing = next(e for e in entries if e["type"] == "task/send")
    assert outgoing["payload"]["task"]["github_issue_url"] == delegation_outcome["source_task"]["github_issue_url"]


# ---------------------------------------------------------------------------
# Negative scenarios — under-specified payloads must never reach the Specialist
# ---------------------------------------------------------------------------


@scenario("05_task_delegation.feature", "Reject a task missing acceptance criteria")
def test_reject_a_task_missing_acceptance_criteria():
    pass


@when(
    "the Orchestrator attempts an A2A task/send with an empty acceptance_criteria list",
    target_fixture="delegation_outcome",
)
def attempts_task_send_empty_acceptance_criteria(well_formed_task, delegation_outcome):
    return _attempt_rejected_task_delegate({**well_formed_task, "acceptance_criteria": []}, delegation_outcome)


@scenario("05_task_delegation.feature", "Reject a task missing the GitHub issue link")
def test_reject_a_task_missing_the_github_issue_link():
    pass


@when(
    "the Orchestrator attempts an A2A task/send without a github_issue_url",
    target_fixture="delegation_outcome",
)
def attempts_task_send_missing_github_url(well_formed_task, delegation_outcome):
    bad_task = dict(well_formed_task)
    del bad_task["github_issue_url"]
    return _attempt_rejected_task_delegate(bad_task, delegation_outcome)


@scenario("05_task_delegation.feature", "Reject a task with an unrecognized deliverable format")
def test_reject_a_task_with_an_unrecognized_deliverable_format():
    pass


@when(
    'the Orchestrator attempts an A2A task/send with a deliverable_format that is neither "zip+hash" nor "github_commit"',
    target_fixture="delegation_outcome",
)
def attempts_task_send_bad_deliverable_format(well_formed_task, delegation_outcome):
    return _attempt_rejected_task_delegate({**well_formed_task, "deliverable_format": "pdf"}, delegation_outcome)


@scenario("05_task_delegation.feature", "Reject a task/send missing the orchestrator_endpoint")
def test_reject_a_task_send_missing_the_orchestrator_endpoint():
    pass


@when(
    "the Orchestrator attempts an A2A task/send without an orchestrator_endpoint field",
    target_fixture="delegation_outcome",
)
def attempts_task_send_missing_orchestrator_endpoint(well_formed_task, delegation_outcome):
    """This validation lives in src.shared.a2a.send_task() itself (raises
    ValueError), NOT in tools.task_delegate() (which raises
    UnderspecifiedTaskError for the other three reject scenarios) — going
    through the mocked-a2a_client task_delegate() path, as the other three
    scenarios do, would bypass the real check entirely and this scenario
    would falsely pass. Call send_task() directly instead, matching
    tests/test_a2a.py::test_send_task_rejects_missing_orchestrator_endpoint."""
    import asyncio

    from src.shared.a2a import send_task

    bad_task = dict(well_formed_task)
    del bad_task["orchestrator_endpoint"]

    with patch("src.shared.a2a._send_to_agent", new_callable=AsyncMock) as mock_send:
        try:
            asyncio.run(send_task("http://localhost:10001", bad_task))
            delegation_outcome["rejected"] = False
        except ValueError:
            delegation_outcome["rejected"] = True
        delegation_outcome["send_task_mock"] = mock_send
    return delegation_outcome


def _attempt_rejected_task_delegate(bad_task: dict, delegation_outcome: dict) -> dict:
    import asyncio

    from src.orchestrator import tools

    with patch("src.orchestrator.tools.a2a_client") as mock_a2a:
        mock_a2a.send_task = AsyncMock()
        try:
            asyncio.run(tools.task_delegate("http://localhost:10001", bad_task))
            delegation_outcome["rejected"] = False
        except tools.UnderspecifiedTaskError:
            delegation_outcome["rejected"] = True
        delegation_outcome["send_task_mock"] = mock_a2a.send_task
    return delegation_outcome


@then("the task is rejected as under-specified")
def task_rejected_as_underspecified(delegation_outcome):
    assert delegation_outcome["rejected"] is True


@then("no execution is started by the Specialist")
def no_execution_started(delegation_outcome):
    delegation_outcome["send_task_mock"].assert_not_called()


# ---------------------------------------------------------------------------
# Scenario: Carry GuildOS fields in the text body when metadata is rejected
# ---------------------------------------------------------------------------


@scenario("05_task_delegation.feature", "Carry GuildOS fields in the text body when metadata is rejected")
def test_carry_guildos_fields_in_the_text_body_when_metadata_is_rejected():
    pass


@given("the A2A transport rejects extension metadata fields")
def a2a_transport_rejects_metadata():
    """Narrative-only precondition — src/shared/a2a.py's send_task() has no
    metadata-vs-text-body branch to reject from; text-body JSON is the only
    transport mode that ever runs. See module docstring."""


@when("the Orchestrator sends the task", target_fixture="delegation_outcome")
def orchestrator_sends_task_text_body(well_formed_task, delegation_outcome):
    import asyncio

    from src.shared.a2a import send_task

    captured_messages = []

    async def fake_send_to_agent(agent_url, message, configuration=None):
        captured_messages.append(message)
        return {"type": "task/delivered"}

    with patch("src.shared.a2a._send_to_agent", side_effect=fake_send_to_agent):
        asyncio.run(send_task("http://localhost:10001", well_formed_task))

    delegation_outcome["captured_messages"] = captured_messages
    delegation_outcome["source_task"] = well_formed_task
    return delegation_outcome


@then("the GuildOS task fields are carried as a JSON string in the message text body")
def guildos_fields_carried_as_json(delegation_outcome):
    assert len(delegation_outcome["captured_messages"]) == 1
    text_part = delegation_outcome["captured_messages"][0].parts[0].text
    parsed = json.loads(text_part)
    assert parsed["type"] == "task/send"
    delegation_outcome["parsed_text_body"] = parsed


@then("the Specialist parses them successfully")
def specialist_parses_them_successfully(delegation_outcome):
    assert delegation_outcome["parsed_text_body"]["task"] == delegation_outcome["source_task"]
