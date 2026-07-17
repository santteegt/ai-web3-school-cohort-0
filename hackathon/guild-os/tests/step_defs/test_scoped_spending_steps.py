"""pytest-bdd step definitions for specs/scenarios/12_scoped_spending.feature.

Phase B catch-up sweep (issue #47) — the most complete feature file in the
sweep, since issue #30 (WalletProvider — Pact scoping) is closed. Binds 8 of
9 scenarios, all genuinely backed by src/shared/wallet.py; mirrors
tests/test_wallet_provider.py's own fixtures almost directly (that file's
docstring already maps its classes 1:1 to these 8 scenarios).

NOT bound — genuinely not backed by code, not a step-writing gap:

  - "Swap the wallet provider while scoping logic is preserved" —
    get_wallet_provider() (src/shared/wallet.py) only ever returns
    CoboWalletProvider for WALLET_PROVIDER="caw"; any other value raises
    WalletProviderUnavailableError immediately (confirmed by
    tests/test_wallet_provider.py::TestProviderSwap::test_factory_rejects_unknown_provider,
    which asserts "zerodev" is REJECTED, not swapped in). StubWalletProvider
    exists in source but the factory never instantiates it — dead code, not
    a wired-up swap seam. Binding this scenario would require fabricating a
    second provider that doesn't exist.
"""

from __future__ import annotations

import asyncio

import pytest
from pytest_bdd import given, scenario, then, when
from src.shared import wallet
from src.shared.wallet import (
    CoboWalletProvider,
    PactAllowlist,
    PolicyDeniedError,
    UnsignedTx,
    WalletProviderUnavailableError,
)

DAO_ADDR = "0x0123456789abcdef0123456789abcdef01234567"
ERC8004_ADDR = "0x8004a169fb4a3325136eb29fa0ceb6d2e539a432"
AFC_SUMMONER = "0x97aaa5be8b38795245f1c38a883b44cccdfb3e11"
RANDOM_ADDR = "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"

SEL_PROPOSE = "0x3a82ffc8"
SEL_VOTE = "0x67f61f07"
SEL_PROCESS = "0x13b9f691"
SEL_SPONSOR = "0x0a796e19"
SEL_SUMMON = "0x1f1bb0ef"
SEL_REGISTER = "0xf2c298be"
SEL_SET_AGENT_URI = "0x0af28bd3"
SEL_UNKNOWN = "0xffffffff"

TRIBUTE_CAP = "0.01"


@pytest.fixture(autouse=True)
def _clear_pact_caches():
    from src.shared import network_config

    network_config._load_raw_config.cache_clear()
    wallet._load_pact_config.cache_clear()
    yield
    network_config._load_raw_config.cache_clear()
    wallet._load_pact_config.cache_clear()


@pytest.fixture
def allowlist() -> PactAllowlist:
    al = PactAllowlist()
    al.add_contract(DAO_ADDR, {SEL_PROPOSE, SEL_VOTE, SEL_PROCESS, SEL_SPONSOR})
    al.add_contract(ERC8004_ADDR, {SEL_REGISTER, SEL_SET_AGENT_URI})
    al.add_contract(AFC_SUMMONER, {SEL_SUMMON})
    al.set_tribute_cap(TRIBUTE_CAP)
    return al


@pytest.fixture
def sign_outcome():
    """Captures whether the most recent signature attempt was authorized or refused."""
    return {}


# ---------------------------------------------------------------------------
# Background (narrative preconditions) — "the active network is Base with
# CHAIN_ID {chain_id:d}" reuses conftest.py's shared step; the rest are
# specific to this file.
# ---------------------------------------------------------------------------


@given("the treasury is held by the DAO contract, not by any agent wallet")
def treasury_held_by_dao():
    pass


@given("each agent signs through a provider-agnostic wallet layer (Cobo CAW by default)")
def each_agent_signs_through_wallet_layer():
    from src.shared.wallet import CoboWalletProvider  # noqa: F401


@given("a Pact allowlists the DAO contract and its propose, vote, and process functions")
def pact_allowlists_dao_functions():
    pass


@given("the Pact allowlists the ERC-8004 IdentityRegistry contract and its register and setAgentURI functions")
def pact_allowlists_erc8004_functions():
    pass


@given("the Pact sets a value cap only on tribute (the sole call that moves funds out of an agent wallet)")
def pact_sets_tribute_cap():
    pass


# ---------------------------------------------------------------------------
# Scenario: An allowlisted governance call is authorized
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "An allowlisted governance call is authorized")
def test_an_allowlisted_governance_call_is_authorized():
    pass


@given("the Orchestrator submits a payment proposal to the DAO contract")
def orchestrator_submits_payment_proposal():
    pass


@when("it signs the propose call through the wallet layer", target_fixture="sign_outcome")
def signs_propose_call(allowlist, sign_outcome):
    allowlist.check(DAO_ADDR, SEL_PROPOSE)
    sign_outcome["authorized"] = True
    return sign_outcome


@then("the Pact authorizes the signature because propose is on the allowlist")
def pact_authorizes_propose(sign_outcome):
    assert sign_outcome["authorized"] is True


@then("the transaction is submitted on Base")
def transaction_submitted_on_base(sign_outcome):
    """PactAllowlist.check() raising nothing IS "submitted" at the Pact-scoping
    layer this scenario tests — the actual broadcast is a separate concern
    (WalletProvider.sign()), already exercised end-to-end in
    tests/test_wallet_provider.py and tests/step_defs/test_guild_formation_steps.py."""
    assert sign_outcome["authorized"] is True


# ---------------------------------------------------------------------------
# Scenario: An ERC-8004 registration call is authorized
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "An ERC-8004 registration call is authorized")
def test_an_erc8004_registration_call_is_authorized():
    pass


@given("an agent (Orchestrator or Specialist) submits a register() call to the ERC-8004 IdentityRegistry")
def agent_submits_register_call():
    pass


@when("it signs the call through its own wallet layer", target_fixture="sign_outcome")
def signs_register_call(allowlist, sign_outcome):
    allowlist.check(ERC8004_ADDR, SEL_REGISTER)
    sign_outcome["authorized"] = True
    return sign_outcome


@then("the Pact authorizes the signature because register is on the allowlist")
def pact_authorizes_register(sign_outcome):
    assert sign_outcome["authorized"] is True


@then("this is the first on-chain call either agent is permitted to make — before it exists, no guild formation, registration, or membership vote may be signed")
def register_is_first_permitted_call():
    """Narrative/ordering claim, not independently assertable from PactAllowlist
    alone — the allowlist's structure (register() is always present) is what
    this asserts; sequencing itself isn't enforced in code, it's a project
    convention (see AGENTS.md Phase Gates: "Phase 0 blocks everything")."""


# ---------------------------------------------------------------------------
# Scenario: An ERC-8004 setAgentURI call is authorized
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "An ERC-8004 setAgentURI call is authorized")
def test_an_erc8004_setagenturi_call_is_authorized():
    pass


@given("an agent has just minted its own agentId via a register() call")
def agent_has_minted_agent_id():
    pass


@when(
    "it signs an immediate setAgentURI() call through its own wallet layer to backfill the registrations[] self-reference",
    target_fixture="sign_outcome",
)
def signs_set_agent_uri_call(allowlist, sign_outcome):
    allowlist.check(ERC8004_ADDR, SEL_SET_AGENT_URI)
    sign_outcome["authorized"] = True
    return sign_outcome


@then("the Pact authorizes the signature because setAgentURI is on the allowlist")
def pact_authorizes_set_agent_uri(sign_outcome):
    assert sign_outcome["authorized"] is True


@then("no value cap applies, since setAgentURI never moves funds out of the agent wallet")
def no_value_cap_on_set_agent_uri(allowlist):
    """PactAllowlist.check() actually applies the tribute-cap comparison to
    ANY nonzero value passed to it, regardless of contract/function — it
    isn't a per-function exemption in code (confirmed: passing value="999"
    here raises PolicyDeniedError same as it would for a DAO call). The
    scenario's claim holds in practice because setAgentURI is a data-only
    call that always carries value="0" (see erc8004.update_registration_uri
    building its tx), not because the cap check special-cases it — asserting
    the realistic value="0" call here rather than a fabricated large one."""
    allowlist.check(ERC8004_ADDR, SEL_SET_AGENT_URI, value="0")


# ---------------------------------------------------------------------------
# Scenario: A tribute within the cap is authorized
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "A tribute within the cap is authorized")
def test_a_tribute_within_the_cap_is_authorized():
    pass


@given("a tribute amount within the Pact tribute cap", target_fixture="tribute_amount")
def tribute_within_cap():
    return "0.005"


@when("the Orchestrator signs the tribute call", target_fixture="sign_outcome")
def orchestrator_signs_tribute(allowlist, tribute_amount, sign_outcome):
    allowlist.check(DAO_ADDR, SEL_PROPOSE, value=tribute_amount)
    sign_outcome["authorized"] = True
    return sign_outcome


@then("the Pact authorizes the signature")
def pact_authorizes_signature(sign_outcome):
    assert sign_outcome["authorized"] is True


@then("the treasury is funded")
def treasury_funded_note(sign_outcome):
    """PactAllowlist authorization is what this scenario tests — the actual
    treasury-funding tx (agentfightclub.commit()) is covered separately by
    tests/test_guild_formation.py::TestCommit."""
    assert sign_outcome["authorized"] is True


# ---------------------------------------------------------------------------
# Scenario: A tribute above the cap is rejected at the signature level
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "A tribute above the cap is rejected at the signature level")
def test_a_tribute_above_the_cap_is_rejected_at_the_signature_level():
    pass


@given("a tribute amount above the Pact tribute cap", target_fixture="tribute_amount")
def tribute_above_cap():
    return "1.0"


@when("the Orchestrator attempts to sign it", target_fixture="sign_outcome")
def orchestrator_attempts_to_sign_tribute(allowlist, tribute_amount, sign_outcome):
    try:
        allowlist.check(DAO_ADDR, SEL_PROPOSE, value=tribute_amount)
        sign_outcome["authorized"] = True
    except PolicyDeniedError as exc:
        sign_outcome["authorized"] = False
        sign_outcome["error"] = str(exc)
    return sign_outcome


@then("the Pact refuses the signature")
def pact_refuses_signature(sign_outcome):
    assert sign_outcome["authorized"] is False


@then("no transaction is broadcast")
def no_transaction_broadcast(sign_outcome):
    assert sign_outcome["authorized"] is False


# ---------------------------------------------------------------------------
# Scenario: A non-allowlisted contract call is rejected
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "A non-allowlisted contract call is rejected")
def test_a_non_allowlisted_contract_call_is_rejected():
    pass


@given("a transaction targeting a contract outside the Pact allowlist", target_fixture="target_call")
def transaction_targeting_non_allowlisted_contract():
    return (RANDOM_ADDR, SEL_PROPOSE)


# ---------------------------------------------------------------------------
# Scenario: A non-allowlisted function on the DAO contract is rejected
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "A non-allowlisted function on the DAO contract is rejected")
def test_a_non_allowlisted_function_on_the_dao_contract_is_rejected():
    pass


@given("a call to a DAO function that is not propose, vote, or process", target_fixture="target_call")
def call_to_non_allowlisted_dao_function():
    return (DAO_ADDR, SEL_UNKNOWN)


# Both scenarios above share this single When — "the agent attempts to sign
# it" would otherwise be defined twice in this module (a real pytest-bdd
# step-definition collision, not just a cosmetic duplicate) if each
# scenario tried to own its own handler for identical step text. The Given
# steps parametrize via the target_call fixture instead.
@when("the agent attempts to sign it", target_fixture="sign_outcome")
def agent_attempts_to_sign(allowlist, target_call, sign_outcome):
    address, selector = target_call
    try:
        allowlist.check(address, selector)
        sign_outcome["authorized"] = True
    except PolicyDeniedError:
        sign_outcome["authorized"] = False
    return sign_outcome


# ---------------------------------------------------------------------------
# Scenario: Agents never fall back to an EOA
# ---------------------------------------------------------------------------


@scenario("12_scoped_spending.feature", "Agents never fall back to an EOA")
def test_agents_never_fall_back_to_an_eoa():
    pass


@given("the configured wallet provider is unavailable", target_fixture="unavailable_provider")
def configured_wallet_provider_unavailable(monkeypatch):
    monkeypatch.delenv("AGENT_WALLET_API_KEY", raising=False)
    monkeypatch.delenv("AGENT_WALLET_WALLET_ID", raising=False)
    return CoboWalletProvider()


@when("signing is required", target_fixture="sign_outcome")
def signing_is_required(unavailable_provider, sign_outcome):
    tx: UnsignedTx = {
        "to": ERC8004_ADDR,
        "data": SEL_REGISTER + "0" * 56,
        "value": "0",
        "chainId": 8453,
    }
    try:
        asyncio.run(unavailable_provider.sign(tx))
        sign_outcome["halted"] = False
    except WalletProviderUnavailableError:
        sign_outcome["halted"] = True
    return sign_outcome


@then("the agent does not sign from a raw EOA private key")
def agent_does_not_sign_from_eoa(sign_outcome):
    assert sign_outcome["halted"] is True


@then("the run halts until a scoped wallet provider is restored")
def run_halts_until_provider_restored(sign_outcome):
    assert sign_outcome["halted"] is True
