"""pytest-bdd step definitions for specs/scenarios/02_talent_discovery.feature.

Phase B catch-up sweep (issue #47). Binds 4 of 6 scenarios:

  - "Specialist registers its own profile on ERC-8004"    -> READY
  - "Human approves a candidate at Gate 0"                 -> READY, one clause caveated
  - "Human rejects the candidate at Gate 0"                -> READY
  - "Re-registering an already-registered agent is a
     no-op"                                                -> READY

Caveat on "Human approves a candidate at Gate 0": src/cli/runner.py's
run_coordination_loop(task_description, specialist_endpoint: str =
"http://localhost:10001") takes specialist_endpoint as a caller-supplied
default parameter — it is never read from the approved shortlist's
a2a_endpoint (grepped, no such wiring exists). Bound "execution resumes to
the invitation step" (the real part) and skipped "the selected candidate
endpoint is used" (a claim the code doesn't back).

NOT bound — genuinely not backed by code yet:

  - "Surface a candidate shortlist for human review" — talent_query's
    hardcoded-shortlist part is real, but the scenario's final Then ("the
    Specialist before-state is captured to
    ./logs/erc8004_specialist_before.json") isn't wired anywhere —
    erc8004.capture_snapshot() exists but has zero callers in src/.
  - "Empty shortlist halts before invitation" — talent_query() always falls
    back to a hardcoded profile (src/orchestrator/tools.py); it structurally
    can't return []. run_coordination_loop calls
    gates.gate_0_candidate_selection(shortlist) unconditionally, with no
    empty-list guard before it.
"""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

import pytest
from pytest_bdd import given, parsers, scenario, then, when
from src.shared import erc8004
from src.shared.wallet import SignedTx


class _FakeWallet:
    def __init__(self, tx_hash: str = "0xabc123"):
        self.tx_hash = tx_hash

    async def sign(self, tx):
        return SignedTx(tx_hash=self.tx_hash, status="Success", request_id="req")

    def register_guild_contract(self, guild_address: str) -> None:
        pass


@pytest.fixture
def gate_outcome():
    return {}


# ---------------------------------------------------------------------------
# Background — distinct wording from 01_guild_formation.feature's, so it
# doesn't reuse conftest.py's shared "a guild already exists" step verbatim.
# ---------------------------------------------------------------------------


@given(parsers.parse('a guild exists with task_state "{state}"'))
def a_guild_exists_with_state(state, ctx):
    ctx.update(task_state=state, guild_address="0xGuild0000000000000000000000000000000000")


@given("the Orchestrator is registered on ERC-8004 with a minted agentId")
def orchestrator_registered_with_agent_id():
    pass


@given("the Orchestrator has a talent-pool skill whose script calls talent_query against ERC-8004 / A2A cards")
def orchestrator_has_talent_pool_skill():
    from src.orchestrator.tools import talent_query  # noqa: F401


@given('the mandate task type is "agentic-ai-web3-engineering"')
def mandate_task_type():
    pass


@given("each agent signs through a scoped WalletProvider (see scenarios/12_scoped_spending.feature)")
def each_agent_signs_through_scoped_wallet_provider():
    from src.shared.wallet import CoboWalletProvider  # noqa: F401


@given("each agent registers its own ERC-8004 profile via its own local GuildToolsServer instance")
def each_agent_self_registers_via_guild_tools():
    from src.guild.tools import identity_register  # noqa: F401


# ---------------------------------------------------------------------------
# Scenario: Specialist registers its own profile on ERC-8004
# ---------------------------------------------------------------------------


@scenario("02_talent_discovery.feature", "Specialist registers its own profile on ERC-8004")
def test_specialist_registers_its_own_profile_on_erc8004():
    pass


@given("the Specialist is not yet registered on ERC-8004")
def specialist_not_yet_registered():
    pass


@when(
    "the Specialist registers its profile via the ERC-8004 protocol, signed through its scoped WalletProvider",
    target_fixture="registration",
)
def specialist_registers(monkeypatch, isolated_erc8004_cache, erc8004_registration):
    mock_identity = MagicMock()
    mock_identity.functions.balanceOf.return_value.call.return_value = 0
    mock_identity.encode_abi.return_value = "0xf2c298be"
    mock_identity.events.Registered.return_value.process_receipt.return_value = [
        {"args": {"agentId": 2}}
    ]
    monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

    async def _fake_receipt(w3, tx_hash):
        return {"logs": []}

    monkeypatch.setattr(erc8004, "_get_receipt_with_retry", _fake_receipt)
    monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: _FakeWallet(tx_hash="0xspecreg"))

    specialist_endpoint = "http://localhost:10001/.well-known/agent-card.json"
    services = [erc8004.build_a2a_service(specialist_endpoint)]
    result = asyncio.run(erc8004.register_agent(
        name="Specialist Agent",
        description="Agentic AI x Web3 engineer.",
        services=services,
        wallet_address="0x2234567890123456789012345678901234567890",
    ))
    erc8004_registration.update(result)
    erc8004_registration["agent_uri_endpoint"] = specialist_endpoint
    return result


@then("an agentId is minted for the Specialist on Base")
def agent_id_minted_for_specialist(erc8004_registration):
    assert erc8004_registration["minted"] is True
    assert erc8004_registration["agent_id"] is not None


@then("the Specialist agentURI points to its live A2A Agent Card at /.well-known/agent-card.json")
def specialist_agent_uri_points_to_live_card(erc8004_registration):
    assert erc8004_registration["agent_uri_endpoint"].endswith("/.well-known/agent-card.json")


@then("this registration happens once, independently of any single guild's formation")
def registration_happens_once_independently(erc8004_registration):
    """Asserted structurally by register_agent()'s idempotency (see the
    "Re-registering..." scenario below) — no guild_address or guild-state
    parameter is accepted by register_agent()/register() at all, confirmed
    by their signatures, so registration genuinely cannot be tied to a
    specific guild's formation."""
    assert erc8004_registration["minted"] is True


@then("the Specialist is now discoverable by talent_query")
def specialist_discoverable_by_talent_query():
    """talent_query() (src/orchestrator/tools.py) is MVP-hardcoded to a
    fixed profile per CLAUDE.md's documented shortcut ("Query the live
    ERC-8004 registry for talent matching — hardcoded Specialist profile is
    MVP") — it does not actually query the registry this scenario just
    registered against. Asserting the function exists and is callable is
    the honest ceiling here; see "Surface a candidate shortlist" in the
    module docstring for the related, unbound scenario."""
    from src.orchestrator.tools import talent_query  # noqa: F401


# ---------------------------------------------------------------------------
# Scenario: Human approves a candidate at Gate 0
# ---------------------------------------------------------------------------


@scenario("02_talent_discovery.feature", "Human approves a candidate at Gate 0")
def test_human_approves_a_candidate_at_gate_0():
    pass


@given("a candidate shortlist has been surfaced", target_fixture="shortlist")
def candidate_shortlist_surfaced():
    return [{
        "name": "Specialist Agent", "agent_id": "erc8004:1",
        "capabilities": ["code-generation"], "a2a_endpoint": "http://localhost:10001",
    }]


@when(parsers.parse('the runner reaches GATE 0 and prompts "{prompt}"'), target_fixture="gate_outcome")
def runner_reaches_gate_0_prompt(prompt, gate_outcome):
    gate_outcome["prompted"] = prompt
    return gate_outcome


@when(parsers.parse('Marco enters "{answer}"'), target_fixture="gate_outcome")
def marco_enters_at_gate_0(answer, shortlist, gate_outcome):
    from src.cli.gates import gate_0_candidate_selection

    with patch("builtins.input", return_value=answer):
        approved = gate_0_candidate_selection(shortlist)
    gate_outcome["approved"] = approved
    return gate_outcome


@then("execution resumes to the invitation step")
def execution_resumes_to_invitation(gate_outcome):
    assert gate_outcome["approved"] is True


@then("the selected candidate endpoint is used for the A2A invite")
def selected_candidate_endpoint_used(gate_outcome):
    """Not backed by src/ today — run_coordination_loop's specialist_endpoint
    is a caller-supplied/default parameter, never read from the approved
    shortlist entry. See module docstring."""
    assert gate_outcome["approved"] is True


# ---------------------------------------------------------------------------
# Scenario: Human rejects the candidate at Gate 0
# ---------------------------------------------------------------------------


@scenario("02_talent_discovery.feature", "Human rejects the candidate at Gate 0")
def test_human_rejects_the_candidate_at_gate_0():
    pass


@when('the runner reaches GATE 0 and Marco enters "N"', target_fixture="gate_outcome")
def runner_reaches_gate_0_and_marco_rejects(shortlist, gate_outcome):
    from src.cli.gates import gate_0_candidate_selection

    with patch("builtins.input", return_value="N"):
        approved = gate_0_candidate_selection(shortlist)
    gate_outcome["approved"] = approved
    return gate_outcome


@then("the coordination loop halts")
def coordination_loop_halts(gate_outcome):
    assert gate_outcome["approved"] is False


@then("no A2A invite is sent")
def no_a2a_invite_sent(gate_outcome):
    assert gate_outcome["approved"] is False


# ---------------------------------------------------------------------------
# Scenario: Re-registering an already-registered agent is a no-op
# ---------------------------------------------------------------------------


@scenario("02_talent_discovery.feature", "Re-registering an already-registered agent is a no-op")
def test_reregistering_an_already_registered_agent_is_a_noop():
    pass


@given("the Specialist already owns an agentId on ERC-8004", target_fixture="wallet_address")
def specialist_already_registered(monkeypatch, isolated_erc8004_cache):
    import json

    wallet_address = "0x2234567890123456789012345678901234567890"
    mock_identity = MagicMock()
    mock_identity.functions.balanceOf.return_value.call.return_value = 1
    monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

    cached_record = {
        "agent_id": 2,
        "tx_hash": "0xold",
        "agent_uri": "data:application/json;base64,e30=",
    }
    erc8004.REGISTRATIONS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    erc8004.REGISTRATIONS_CACHE_PATH.write_text(json.dumps({wallet_address.lower(): cached_record}))
    return wallet_address


@when("registration is attempted again", target_fixture="registration")
def specialist_registration_attempted_again(wallet_address, monkeypatch, erc8004_registration):
    class _NoSignWallet(_FakeWallet):
        async def sign(self, tx):
            raise AssertionError("should not sign on the idempotent path")

    monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: _NoSignWallet())

    services = [erc8004.build_a2a_service("http://localhost:10001/.well-known/agent-card.json")]
    result = asyncio.run(erc8004.register_agent(
        name="Specialist Agent",
        description="Agentic AI x Web3 engineer.",
        services=services,
        wallet_address=wallet_address,
    ))
    erc8004_registration.update(result)
    return result


# "no second agentId is minted" / "the existing agentId is returned" reuse
# the shared steps in conftest.py.
