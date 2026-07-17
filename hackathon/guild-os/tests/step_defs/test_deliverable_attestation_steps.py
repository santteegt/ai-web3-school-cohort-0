"""pytest-bdd step definitions for specs/scenarios/07_deliverable_attestation.feature.

Phase B catch-up sweep (issue #47). Binds 2 of 6 scenarios — the A2A
transport-layer ones (backed by closed #36/#37), NOT the EAS attestation
scenarios themselves (blocked on open #28):

  - "Orchestrator's A2A server receives the proactive task/delivered" -> READY
  - "Proactive push to an unreachable orchestrator_endpoint fails
     closed"                                                          -> READY

NOT bound — genuinely not backed by code yet:

  - "Attest the deliverable hash and return the UID" — src/shared/eas.py
    does not exist; no EASClient/attest() anywhere in src/.
  - "Embed the attestation UID in the A2A result" — the transport plumbing
    genuinely carries attestation_uid/attestation_url fields (see
    tests/test_specialist_a2a_client.py), but nothing in src/ ever produces
    a real attestation_uid to embed — src/specialist/agent.py's
    handle_task_send still calls the old onchain_hash.commit_hash path.
    Binding this would require fabricating an attestation_uid the real
    harness never produces.
  - "Read back the attestation and confirm the hash matches" — no
    get_attestation() anywhere; no eas.py.
  - "Fall back to a raw event when the schema is missing (F7)" —
    src/shared/onchain_hash.py is unconditionally used by handle_task_send,
    not as a conditional fallback from a failed EAS attempt (there is no
    EAS attempt to fall back from), and it doesn't emit the described
    DeliverableCommitted(bytes32 hash) event.

Also worth noting: this file's own Background ("DELIVERY_SCHEMA_UID is
registered on Base mainnet") is false today — config/networks.json's
delivery_schema_uid is null for both networks — but that precondition
isn't load-bearing for the 2 transport scenarios bound here, which don't
depend on EAS having actually run.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest
from pytest_bdd import given, parsers, scenario, then, when


@pytest.fixture
def tmp_trace_dir(tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod

    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def delivered_outcome():
    return {}


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------


@given("the Specialist produced a code deliverable")
def specialist_produced_deliverable():
    pass


@given("DELIVERY_SCHEMA_UID is registered on Base mainnet")
def delivery_schema_uid_registered():
    """Narrative only — false in config/networks.json today (null for both
    networks); not load-bearing for the transport scenarios bound here.
    See module docstring."""


@given(parsers.parse("the active network is Base mainnet with CHAIN_ID {chain_id:d}"))
def active_network_base_mainnet(chain_id, monkeypatch):
    monkeypatch.setenv("CHAIN_ID", str(chain_id))


@given("an attestation UID was returned", target_fixture="attestation")
def an_attestation_uid_was_returned():
    """Narrative fixture for the two bound scenarios below — a synthetic
    UID, since nothing in src/ produces a real one yet (see module
    docstring's EAS-related skips)."""
    return {
        "attestation_uid": "0xabc",
        "attestation_url": "https://base.easscan.org/attestation/0xabc",
    }


# ---------------------------------------------------------------------------
# Scenario: Orchestrator's A2A server receives the proactive task/delivered
# ---------------------------------------------------------------------------


@scenario("07_deliverable_attestation.feature", "Orchestrator's A2A server receives the proactive task/delivered")
def test_orchestrators_a2a_server_receives_the_proactive_task_delivered():
    pass


@when(
    "SpecialistA2AClient sends a proactive task/delivered to the orchestrator_endpoint",
    target_fixture="delivered_outcome",
)
def specialist_client_sends_proactive_delivered(tmp_trace_dir, tmp_path, attestation, delivered_outcome):
    import asyncio
    import hashlib

    from a2a.server.agent_execution.context import RequestContext
    from a2a.server.context import ServerCallContext
    from a2a.server.events.event_queue import EventQueueLegacy
    from a2a.types.a2a_pb2 import ROLE_USER, Message, Part, SendMessageRequest
    from src.orchestrator.a2a_server import OrchestratorExecutor
    from src.specialist.a2a_client import send_delivered

    content = b'{"output": "test deliverable"}'
    deliv_file = tmp_path / "deliverable.json"
    deliv_file.write_bytes(content)
    expected_hash = "sha256:" + hashlib.sha256(content).hexdigest()

    # Send side — SpecialistA2AClient — confirmed real, per
    # tests/test_specialist_a2a_client.py::TestSendDelivered.
    with patch("src.specialist.a2a_client._send_to_agent", new_callable=AsyncMock) as mock_send:
        mock_send.return_value = {"type": "deliverable_review"}
        asyncio.run(send_delivered(
            orchestrator_endpoint="http://localhost:10000",
            task_id="task-delivered-1",
            deliverable_hash=expected_hash,
            attestation_uid=attestation["attestation_uid"],
            attestation_url=attestation["attestation_url"],
        ))
    delivered_outcome["send_call"] = mock_send.call_args

    # Receive side — OrchestratorExecutor — confirmed real, per
    # tests/test_orchestrator_a2a_server.py::TestOrchestratorExecutorTransport.
    message = Message(
        message_id="test-msg-id",
        role=ROLE_USER,
        parts=[Part(text=json.dumps({
            "type": "task/delivered",
            "task_id": "task-delivered-1",
            "deliverable_reference": str(deliv_file),
            "deliverable_hash": expected_hash,
            "attestation_uid": attestation["attestation_uid"],
            "attestation_url": attestation["attestation_url"],
        }))],
    )
    context = RequestContext(
        call_context=ServerCallContext(),
        request=SendMessageRequest(message=message),
        task_id="task-delivered-1",
        context_id="test-context-id",
    )
    queue = EventQueueLegacy()
    executor = OrchestratorExecutor()
    asyncio.run(executor.execute(context, queue))

    events = []
    for _ in range(2):
        try:
            event = asyncio.run(asyncio.wait_for(queue.dequeue_event(), timeout=2.0))
            events.append(event)
            queue.task_done()
        except TimeoutError:
            break
    asyncio.run(queue.close(immediate=True))
    delivered_outcome["events"] = events
    return delivered_outcome


@then("OrchestratorA2AServer receives it as an inbound message/send on port 10000")
def orchestrator_receives_inbound_message(delivered_outcome):
    """Port 10000 itself is a deployment-time constant (ORCHESTRATOR_A2A_PORT
    default, see README.md), not something this in-process executor test
    binds to — asserting the executor actually processed and emitted events
    is the meaningful part of "received" at this test layer."""
    assert len(delivered_outcome["events"]) == 2


@then("its executor triggers the deliverable pre-check for Gate 2")
def executor_triggers_precheck(delivered_outcome):
    from a2a.types.a2a_pb2 import TASK_STATE_COMPLETED, TASK_STATE_WORKING

    events = delivered_outcome["events"]
    assert events[0].status.state == TASK_STATE_WORKING
    assert events[1].status.state == TASK_STATE_COMPLETED
    payload = json.loads(events[1].status.message.parts[0].text)
    assert payload["type"] == "deliverable_review"
    assert payload["pre_check"]["evaluator_verdict"] == "PASS"


@then("the message is logged to hackathon/notes/a2a_trace_{date}.json")
def message_logged_to_notes_trace(tmp_trace_dir, delivered_outcome):
    """The scenario text says "hackathon/notes/..." but a2a.TRACE_DIR
    resolves to "hackathon/logs/..." — this exact notes-vs-logs mismatch
    also appears in specs/20-api-contracts.md and 03/06/10's scenario text
    (a spec-wide inconsistency, not scenario-specific). Asserting against
    the real TRACE_DIR constant, not the literal path string."""
    from datetime import date

    trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
    entries = json.loads(trace_file.read_text())
    assert any(e["type"] == "task/delivered" and e["direction"] == "outgoing" for e in entries)


# ---------------------------------------------------------------------------
# Scenario: Proactive push to an unreachable orchestrator_endpoint fails closed
# ---------------------------------------------------------------------------


@scenario("07_deliverable_attestation.feature", "Proactive push to an unreachable orchestrator_endpoint fails closed")
def test_proactive_push_to_an_unreachable_orchestrator_endpoint_fails_closed():
    pass


@given("the orchestrator_endpoint in the task carries an unreachable or malformed URL")
def orchestrator_endpoint_unreachable():
    pass


@when(
    "SpecialistA2AClient attempts to send the proactive task/delivered",
    target_fixture="delivered_outcome",
)
def specialist_client_attempts_send_to_unreachable(tmp_trace_dir, delivered_outcome):
    """This scenario's own Given doesn't produce an "an attestation UID was
    returned" fixture (only the first scenario's Given does) — use inline
    placeholder values, matching tests/test_specialist_a2a_client.py's own
    test_unreachable_endpoint_raises."""
    import asyncio

    from src.specialist.a2a_client import send_delivered

    with patch(
        "src.specialist.a2a_client._send_to_agent",
        new_callable=AsyncMock,
        side_effect=ConnectionError("Connection refused"),
    ):
        try:
            asyncio.run(send_delivered(
                orchestrator_endpoint="http://unreachable:9999",
                task_id="task-fail",
                deliverable_hash="sha256:fail",
                attestation_uid="0xfail",
                attestation_url="https://base.easscan.org/attestation/0xfail",
            ))
            delivered_outcome["raised"] = False
        except ConnectionError as exc:
            delivered_outcome["raised"] = True
            delivered_outcome["error"] = str(exc)
    return delivered_outcome


@then("the send fails with a logged, surfaced error")
def send_fails_with_logged_error(tmp_trace_dir, delivered_outcome):
    from datetime import date

    assert delivered_outcome["raised"] is True
    trace_file = tmp_trace_dir / f"a2a_trace_{date.today().isoformat()}.json"
    entries = json.loads(trace_file.read_text())
    assert any(e["type"] == "task/delivered" and e["direction"] == "outgoing" for e in entries)


@then("the task is not silently treated as delivered")
def task_not_silently_treated_as_delivered(delivered_outcome):
    assert delivered_outcome["raised"] is True


@then("the Specialist does not silently drop the deliverable")
def specialist_does_not_silently_drop_deliverable(delivered_outcome):
    """send_delivered() re-raises the ConnectionError rather than swallowing
    it — the caller (the harness work engine, #40/open) is what would be
    responsible for a retry/persist strategy; this scenario's guarantee at
    this layer is "the error surfaces," which the raise satisfies."""
    assert delivered_outcome["raised"] is True
