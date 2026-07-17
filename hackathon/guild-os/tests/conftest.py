"""Shared pytest-bdd fixtures and step definitions for specs/scenarios/*.feature.

.feature files are NOT copied into tests/ — they load directly from
specs/scenarios/ via pyproject.toml's bdd_features_base_dir, so specs/
stays the single canonical copy (see specs/README.md).

Steps defined here are shared across every step_defs/ module (pytest-bdd
collects conftest.py steps automatically). Only steps genuinely reused by
more than one feature file — or established Background preconditions —
belong here; scenario-specific steps live in their own step_defs/ module.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from pytest_bdd import given, parsers, then
from src.shared import erc8004, guild_context


@pytest.fixture
def ctx(tmp_path, monkeypatch):
    """Isolated guild_context.json for one scenario.

    guild_context.CONTEXT_PATH is a hardcoded module-level constant (no
    constructor injection seam) — tests/test_guild_formation.py already
    isolates it the same way; this fixture just makes that reusable and
    auto-restoring via monkeypatch instead of a manual try/finally.
    """
    test_file = tmp_path / "guild_context.json"
    monkeypatch.setattr(guild_context, "CONTEXT_PATH", test_file)
    guild_context.reset()
    return guild_context


# ---------------------------------------------------------------------------
# specs/scenarios/01_guild_formation.feature — Background (narrative
# preconditions; no on-chain call happens at Background time, only at the
# scenario's own When step)
# ---------------------------------------------------------------------------


@given(parsers.parse("the active network is Base with CHAIN_ID {chain_id:d}"))
def active_network(chain_id, monkeypatch):
    monkeypatch.setenv("CHAIN_ID", str(chain_id))


@given("Marco controls a funded orchestrator-operated wallet")
def marco_funded_wallet(monkeypatch):
    monkeypatch.setenv("AGENT_WALLET_ADDRESS", "0xMarco0000000000000000000000000000000000")


@given("the Orchestrator has a guild-launch skill that collects founder inputs and spins up a club")
def orchestrator_has_guild_launch_skill():
    """Narrative precondition — src.orchestrator.tools.guild_launch exists; asserted by import."""
    from src.orchestrator.tools import guild_launch  # noqa: F401


@given("the Orchestrator has an AgentFightClub skill that can use either integration path (ClawBank API or DAOhaus SDK)")
def orchestrator_has_agentfightclub_skill():
    """Narrative precondition — src.shared.agentfightclub exists; asserted by import.

    The "either integration path" framing describes a future ClawBank-API-
    vs-DAOhaus-SDK branch; today src/shared/agentfightclub.py always drives
    a single moloch-agent CLI subprocess path (see AGENTS.md "When Unsure").
    That gap is why scenarios/05 ("Either AgentFightClub path produces the
    same guild") is not automated by this Background — see step_defs/
    test_guild_formation_steps.py's module docstring.
    """
    from src.shared import agentfightclub  # noqa: F401


@given("each agent registers its own ERC-8004 profile via its own local GuildToolsServer instance (see scenarios/12_scoped_spending.feature)")
def each_agent_self_registers():
    """Narrative precondition — src.guild.tools.identity_register exists; asserted by import."""
    from src.guild.tools import identity_register  # noqa: F401


# ---------------------------------------------------------------------------
# guild_context.task_state assertions — reused across 01/02/04/08/09/10/11
# per the reuse map found during planning (parametrized, one step for both
# phrasings the specs use)
# ---------------------------------------------------------------------------


@then(parsers.parse('guild_context.task_state becomes "{state}"'))
@then(parsers.parse('guild_context.task_state remains "{state}"'))
def guild_context_task_state_is(ctx, state):
    assert ctx.load()["task_state"] == state


# ---------------------------------------------------------------------------
# ERC-8004 registration idempotency — shared verbatim by 01 (Orchestrator)
# and 02 (Specialist); same phrasing, different subject agent
# ---------------------------------------------------------------------------


@pytest.fixture
def erc8004_registration():
    """Captures the result of the most recent register_agent()-family call."""
    return {}


@pytest.fixture
def isolated_erc8004_cache(tmp_path, monkeypatch):
    """Point erc8004.REGISTRATIONS_CACHE_PATH (module-level constant, same
    seam as guild_context.CONTEXT_PATH) at a tmp file, mirroring
    test_erc8004.py's own _isolate_cache fixture — not made autouse here so
    it doesn't affect the existing hand-written test_erc8004.py suite."""
    monkeypatch.setattr(erc8004, "REGISTRATIONS_CACHE_PATH", tmp_path / "erc8004_registrations.json")
    monkeypatch.setattr(erc8004, "_web3", lambda: object())


@then("no second agentId is minted")
def no_second_agent_id_minted(erc8004_registration):
    assert erc8004_registration.get("minted") is False


@then("the existing agentId is returned")
def existing_agent_id_returned(erc8004_registration):
    assert erc8004_registration.get("agent_id") is not None


# ---------------------------------------------------------------------------
# Shared mocks for the coordination-runner idempotency check (scenario 6) —
# same pattern tests/test_runner.py already uses for the full-loop tests.
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_gates():
    with patch("src.cli.runner.gates") as mock_g:
        mock_g.gate_0_candidate_selection.return_value = True
        mock_g.gate_0_5_quote_acceptance.return_value = True
        mock_g.gate_1_membership.return_value = True
        mock_g.gate_2_deliverable_acceptance.return_value = True
        yield mock_g


@pytest.fixture
def mock_orchestrator_tools():
    with patch("src.cli.runner.tools") as mock_tools:
        mock_tools.guild_launch = AsyncMock(return_value={
            "guild_address": "0xguild123",
            "launch_tx": "0xlaunch",
            "commit_tx": "0xcommit",
        })
        mock_tools.talent_query = AsyncMock(return_value=[
            {"name": "Specialist", "agent_id": "erc8004:1", "capabilities": ["code-generation"]}
        ])
        mock_tools.membership_propose = AsyncMock(return_value={"proposal_id": "prop-1"})
        mock_tools.membership_vote = AsyncMock(return_value={"vote_tx": "0xvote"})
        mock_tools.deliverable_review = AsyncMock(return_value={
            "hash_match": True, "format_valid": True, "size_check": True,
            "evaluator_verdict": "PASS",
        })
        mock_tools.settle = AsyncMock(return_value="0xsettle")
        mock_tools.reputation_write = AsyncMock(side_effect=NotImplementedError("Phase 3"))
        yield mock_tools
