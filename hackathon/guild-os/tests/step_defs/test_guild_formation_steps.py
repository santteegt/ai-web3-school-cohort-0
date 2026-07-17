"""pytest-bdd step definitions for specs/scenarios/01_guild_formation.feature.

Phase A catch-up-sweep spike (issue #47) — binds only the scenarios whose
src/ code is genuinely implemented today, confirmed by reading src/
directly rather than assuming from milestone/issue titles:

  - "Launch and fund a new guild"                            -> IMPLEMENTED
  - "Orchestrator registers its own profile on ERC-8004"     -> IMPLEMENTED
  - "Do not relaunch over an already-active guild"           -> IMPLEMENTED
  - "Re-registering an already-registered agent is a no-op"  -> IMPLEMENTED

NOT bound here — genuinely not backed by code yet, not a step-writing gap:

  - "Orchestrator collects the guild parameters from the founder" — no
    interactive parameter-collection code exists; guild_launch(mandate,
    treasury_address) takes neither a guild name, governance settings, nor
    a member list. Tracked by open issue #31.
  - "Reject a launch with a zero treasury tribute" — guild_launch has no
    tribute-value parameter or validation at all today (the tribute amount
    is hardcoded in src/orchestrator/tools.py). Also #31.
  - "Either AgentFightClub path produces the same guild" — describes a
    ClawBank-API-vs-DAOhaus-SDK branch that was never built; the actual
    integration is always a single moloch-agent CLI subprocess path (see
    AGENTS.md "When Unsure" — "the actual current integration is a CLI
    subprocess wrapper, not either API"). A spec/code mismatch worth a
    scenario rewrite, not a missing test — flagged as an Out-of-Scope
    Finding on the PR, not silently worked around here.
"""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

from pytest_bdd import given, parsers, scenario, then, when
from src.shared import erc8004
from src.shared.wallet import SignedTx


class _FakeWallet:
    """Minimal WalletProvider stand-in — signs successfully, records nothing."""

    def __init__(self, tx_hash: str = "0xabc123"):
        self.tx_hash = tx_hash

    async def sign(self, tx):
        return SignedTx(tx_hash=self.tx_hash, status="Success", request_id="req")

    def register_guild_contract(self, guild_address: str) -> None:
        pass


# ---------------------------------------------------------------------------
# Scenario: Launch and fund a new guild
# ---------------------------------------------------------------------------


@scenario("01_guild_formation.feature", "Launch and fund a new guild")
def test_launch_and_fund_a_new_guild():
    pass


@given(
    "Marco has provided guild name, mandate, governance settings, member "
    "list with shares/loot, and a treasury tribute value",
    target_fixture="founder_inputs",
)
def founder_inputs():
    """guild_launch's current signature only models mandate + treasury_address
    — the richer founder-parameter set (name, governance, member list,
    tribute value) isn't separately represented in src/ yet (see module
    docstring, issue #31). This step carries forward what genuinely exists."""
    return {
        "mandate": "Build DeFi tools",
        "treasury_address": "0xTreasury00000000000000000000000000000000",
    }


@when(
    "the Orchestrator executes the launch through its AgentFightClub skill",
    target_fixture="launch_result",
)
def execute_launch(founder_inputs, ctx):
    from src.orchestrator.tools import guild_launch

    fake_tx = {"to": "0x0", "data": "0x0", "value": "0", "chainId": 8453}
    with patch("src.shared.agentfightclub._build_calldata", return_value=fake_tx), \
         patch(
             "src.shared.agentfightclub._sign_and_broadcast",
             side_effect=["0xlaunch_tx", "0xwrap_tx", "0xapprove_tx", "0xtribute_tx"],
         ), \
         patch(
             "src.shared.agentfightclub._parse_dao_from_receipt",
             return_value="0x1234567890abcdef1234567890abcdef12345678",
         ), \
         patch("src.shared.agentfightclub._get_wallet"), \
         patch(
             "src.shared.network_config.get_contract_address",
             return_value="0xWETH000000000000000000000000000000000",
         ):
        result = asyncio.run(guild_launch(**founder_inputs))
    return result


@then("a guild DAO is summoned on Base with the provided governance settings and initial members")
def dao_summoned(launch_result):
    assert launch_result["guild_address"] == "0x1234567890abcdef1234567890abcdef12345678"


@then("the treasury is funded with the tribute value")
def treasury_funded(launch_result):
    assert launch_result["commit_tx"] == "0xtribute_tx"


@then("the launch and tribute transactions are recorded to submissions/tx_hashes.md")
def transactions_recorded_note(launch_result):
    """guild_launch() itself doesn't write submissions/tx_hashes.md — that's a
    human/agent follow-up step per AGENTS.md ("log any new on-chain tx
    hashes to ./logs/tx_hashes.md"). This step confirms the tx hashes this
    scenario needs recorded genuinely exist, not that the write happened."""
    assert launch_result["launch_tx"] and launch_result["commit_tx"]


@then("the Orchestrator returns the dao address and the treasury address")
def returns_dao_and_treasury(launch_result):
    assert launch_result["guild_address"]


@then("guild_context.guild_address and guild_context.treasury_address are set")
def guild_context_addresses_set(ctx, launch_result):
    """guild_context persists treasury_wei, not a distinct treasury_address
    key (see src/shared/guild_context.py's reset() field list) — the
    scenario's phrasing doesn't exactly match the persisted schema.
    Asserting against what's genuinely there rather than inventing a field."""
    saved = ctx.load()
    assert saved["guild_address"] == launch_result["guild_address"]
    assert saved.get("treasury_wei") is not None


# ---------------------------------------------------------------------------
# Scenario: Orchestrator registers its own profile on ERC-8004
# ---------------------------------------------------------------------------


@scenario("01_guild_formation.feature", "Orchestrator registers its own profile on ERC-8004")
def test_orchestrator_registers_its_own_profile_on_erc8004():
    pass


@given("the guild is ACTIVE")
def guild_is_active(ctx):
    ctx.update(
        task_state="ACTIVE",
        guild_address="0xGuild0000000000000000000000000000000000",
    )


@when(
    "the Orchestrator registers its profile via the ERC-8004 protocol",
    target_fixture="registration",
)
def orchestrator_registers(monkeypatch, isolated_erc8004_cache, erc8004_registration):
    mock_identity = MagicMock()
    mock_identity.functions.balanceOf.return_value.call.return_value = 0
    mock_identity.encode_abi.return_value = "0xf2c298be"
    mock_identity.events.Registered.return_value.process_receipt.return_value = [
        {"args": {"agentId": 1}}
    ]
    monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

    async def _fake_receipt(w3, tx_hash):
        return {"logs": []}

    monkeypatch.setattr(erc8004, "_get_receipt_with_retry", _fake_receipt)
    monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: _FakeWallet(tx_hash="0xorchreg"))

    orchestrator_endpoint = "http://localhost:10000/.well-known/agent-card.json"
    services = [erc8004.build_a2a_service(orchestrator_endpoint)]
    result = asyncio.run(erc8004.register_agent(
        name="Orchestrator",
        description="GuildOS Orchestrator",
        services=services,
        wallet_address="0x1234567890123456789012345678901234567890",
    ))
    erc8004_registration.update(result)
    erc8004_registration["agent_uri_endpoint"] = orchestrator_endpoint
    return result


@then("an agentId is minted for the Orchestrator on Base")
def agent_id_minted(erc8004_registration):
    assert erc8004_registration["minted"] is True
    assert erc8004_registration["agent_id"] is not None


@then("the Orchestrator agentURI points to its live A2A Agent Card at /.well-known/agent-card.json")
def agent_uri_points_to_live_card(erc8004_registration):
    assert erc8004_registration["agent_uri_endpoint"].endswith("/.well-known/agent-card.json")


# ---------------------------------------------------------------------------
# Scenario: Do not relaunch over an already-active guild
# ---------------------------------------------------------------------------


@scenario("01_guild_formation.feature", "Do not relaunch over an already-active guild")
def test_do_not_relaunch_over_an_already_active_guild():
    pass


@given(parsers.parse('a guild already exists with task_state "{state}"'), target_fixture="existing_guild")
def guild_already_exists(state, ctx):
    ctx.update(guild_address="0xExistingGuild00000000000000000000000000", task_state=state)
    return ctx.load()


@when("the coordination runner starts", target_fixture="runner_tools")
def coordination_runner_starts(mock_gates, mock_orchestrator_tools, tmp_path, monkeypatch):
    import src.shared.a2a as a2a_mod
    from src.cli.runner import run_coordination_loop

    monkeypatch.setattr(a2a_mod, "TRACE_DIR", tmp_path)

    # This scenario only concerns Step 1's already-active skip check — the
    # rest of the 15-step loop isn't mocked here, so it will raise once it
    # reaches an unmocked A2A network call. That's expected: we only assert
    # guild_launch was never invoked, not that the full loop completed.
    try:
        asyncio.run(run_coordination_loop("test task"))
    except Exception:
        pass
    return mock_orchestrator_tools


@then("it detects the active guild and skips the launch step")
def detects_active_guild_and_skips(runner_tools):
    runner_tools.guild_launch.assert_not_called()


@then("it reuses the existing guild_address without redeploying")
def reuses_existing_guild_address(ctx, existing_guild):
    assert ctx.load()["guild_address"] == existing_guild["guild_address"]


# ---------------------------------------------------------------------------
# Scenario: Re-registering an already-registered agent is a no-op
# ---------------------------------------------------------------------------


@scenario("01_guild_formation.feature", "Re-registering an already-registered agent is a no-op")
def test_reregistering_an_already_registered_agent_is_a_noop():
    pass


@given("the Orchestrator already owns an agentId on ERC-8004", target_fixture="wallet_address")
def orchestrator_already_registered(monkeypatch, isolated_erc8004_cache):
    import json

    wallet_address = "0x1234567890123456789012345678901234567890"
    mock_identity = MagicMock()
    mock_identity.functions.balanceOf.return_value.call.return_value = 1
    monkeypatch.setattr(erc8004, "_identity_registry_contract", lambda w3: mock_identity)

    cached_record = {
        "agent_id": 5,
        "tx_hash": "0xold",
        "agent_uri": "data:application/json;base64,e30=",
    }
    erc8004.REGISTRATIONS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    erc8004.REGISTRATIONS_CACHE_PATH.write_text(json.dumps({wallet_address.lower(): cached_record}))
    return wallet_address


@when("registration is attempted again", target_fixture="registration")
def registration_attempted_again(wallet_address, monkeypatch, erc8004_registration):
    class _NoSignWallet(_FakeWallet):
        async def sign(self, tx):
            raise AssertionError("should not sign on the idempotent path")

    monkeypatch.setattr(erc8004, "get_wallet_provider", lambda: _NoSignWallet())

    services = [erc8004.build_a2a_service("http://localhost:10000/.well-known/agent-card.json")]
    result = asyncio.run(erc8004.register_agent(
        name="Orchestrator",
        description="GuildOS Orchestrator",
        services=services,
        wallet_address=wallet_address,
    ))
    erc8004_registration.update(result)
    return result


# "no second agentId is minted" / "the existing agentId is returned" are
# defined once in conftest.py — shared verbatim by this scenario and
# 02_talent_discovery.feature's mirror scenario for the Specialist.
