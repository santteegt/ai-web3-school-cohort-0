# Provenance: docs/VALIDATION_PLAN.md (§1 Agent Wallets / CAW), docs/TRACK.md (Cobo — controllable fund operations), PROJECT_PROPOSAL.md (§9 Track Alignment) + design feedback 2026-06-29
# Concept: scoped agent authority via a provider-agnostic wallet layer. Treasury funds are DAO-held, so the only
#          value cap is on tribute; what is scoped in detail is the set of allowed DAO contract calls (propose, vote, process).

Feature: Scoped agent authority (CAW Pacts over DAO calls)
  As a guild operator
  I want agent authority bounded by a Pact at the signature level
  So that an agent can only call the DAO's governance functions and only tribute within a cap — never arbitrary spending

  Background:
    Given the active network is Base with CHAIN_ID 8453
    And the treasury is held by the DAO contract, not by any agent wallet
    And each agent signs through a provider-agnostic wallet layer (Cobo CAW by default)
    And a Pact allowlists the DAO contract and its propose, vote, and process functions
    And the Pact sets a value cap only on tribute (the sole call that moves funds out of an agent wallet)

  Scenario: An allowlisted governance call is authorized
    Given the Orchestrator submits a payment proposal to the DAO contract
    When it signs the propose call through the wallet layer
    Then the Pact authorizes the signature because propose is on the allowlist
    And the transaction is submitted on Base

  Scenario: A tribute within the cap is authorized
    Given a tribute amount within the Pact tribute cap
    When the Orchestrator signs the tribute call
    Then the Pact authorizes the signature
    And the treasury is funded

  Scenario: A tribute above the cap is rejected at the signature level
    Given a tribute amount above the Pact tribute cap
    When the Orchestrator attempts to sign it
    Then the Pact refuses the signature
    And no transaction is broadcast

  Scenario: A non-allowlisted contract call is rejected
    Given a transaction targeting a contract outside the Pact allowlist
    When the agent attempts to sign it
    Then the Pact refuses the signature

  Scenario: A non-allowlisted function on the DAO contract is rejected
    Given a call to a DAO function that is not propose, vote, or process
    When the agent attempts to sign it
    Then the Pact refuses the signature

  Scenario: Agents never fall back to an EOA
    Given the configured wallet provider is unavailable
    When signing is required
    Then the agent does not sign from a raw EOA private key
    And the run halts until a scoped wallet provider is restored

  Scenario: Swap the wallet provider while scoping logic is preserved
    Given the wallet layer is reconfigured from Cobo CAW to another provider such as ZeroDev or Turnkey
    When the same governance calls are signed
    Then the same allowlist and tribute cap are enforced through the new provider
    And no scenario above changes its outcome
