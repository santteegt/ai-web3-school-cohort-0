# Provenance: docs/VALIDATION_PLAN.md (§1 Agent Wallets / CAW), docs/TRACK.md (Cobo — controllable fund operations), PROJECT_PROPOSAL.md (§9 Track Alignment) + design feedback 2026-06-29, 2026-06-30
# Concept: scoped agent authority via a provider-agnostic wallet layer. Treasury funds are DAO-held, so the only
#          value cap is on tribute; what is scoped in detail is the set of allowed contract calls — both the DAO's
#          governance functions (propose, vote, process) and the ERC-8004 IdentityRegistry's register() function.
#          This wallet layer must exist and be validated BEFORE any agent signs an on-chain coordination call —
#          registration, guild formation, and membership voting all depend on it, not just fund movement.

Feature: Scoped agent authority (CAW Pacts over DAO and identity-registry calls)
  As a guild operator
  I want agent authority bounded by a Pact at the signature level
  So that an agent can only call the DAO's governance functions, register its own ERC-8004 identity,
     and only tribute within a cap — never arbitrary spending or an arbitrary contract call

  Background:
    Given the active network is Base with CHAIN_ID 8453
    And the treasury is held by the DAO contract, not by any agent wallet
    And each agent signs through a provider-agnostic wallet layer (Cobo CAW by default)
    And a Pact allowlists the DAO contract and its propose, vote, and process functions
    And the Pact allowlists the ERC-8004 IdentityRegistry contract and its register and setAgentURI functions
    And the Pact sets a value cap only on tribute (the sole call that moves funds out of an agent wallet)

  Scenario: An allowlisted governance call is authorized
    Given the Orchestrator submits a payment proposal to the DAO contract
    When it signs the propose call through the wallet layer
    Then the Pact authorizes the signature because propose is on the allowlist
    And the transaction is submitted on Base

  Scenario: An ERC-8004 registration call is authorized
    Given an agent (Orchestrator or Specialist) submits a register() call to the ERC-8004 IdentityRegistry
    When it signs the call through its own wallet layer
    Then the Pact authorizes the signature because register is on the allowlist
    And the transaction is submitted on Base
    And this is the first on-chain call either agent is permitted to make — before it exists, no guild
      formation, registration, or membership vote may be signed

  Scenario: An ERC-8004 setAgentURI call is authorized
    Given an agent has just minted its own agentId via a register() call
    When it signs an immediate setAgentURI() call through its own wallet layer to backfill the
      registrations[] self-reference
    Then the Pact authorizes the signature because setAgentURI is on the allowlist
    And the transaction is submitted on Base
    And no value cap applies, since setAgentURI never moves funds out of the agent wallet

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
