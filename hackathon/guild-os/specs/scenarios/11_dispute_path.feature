# Provenance: docs/MVP_FLOW.md (Step 15), docs/RISKS.md (Scope Creep — ragequit documented only), PROJECT_PROPOSAL.md (§8 Step 13 rejection branch) + design feedback 2026-06-29
# Concept: the rejection/dispute branch — DISPUTED state reached at either Gate 2 (deliverable) or Gate 3 (payment), locked funds, documented ragequit (not executed).

Feature: Dispute and rejection path
  As a human founder
  I want a clean rejection path that locks funds
  So that disputed work never triggers payment and funds remain recoverable

  Background:
    Given the Orchestrator received a deliverable and surfaced the pre-check report

  Scenario: Gate 2 rejection records a DISPUTED state
    When the runner reaches GATE 2 and Marco rejects the deliverable
    Then guild_context.task_state becomes "DISPUTED"
    And no payment proposal is raised
    And no task/accepted message is sent
    And no settlement transaction is created

  Scenario: Gate 3 payment rejection records a DISPUTED state
    Given the deliverable was accepted at GATE 2 and a payment proposal was raised
    When the runner reaches GATE 3 and Marco votes the payment proposal down
    Then guild_context.task_state becomes "DISPUTED"
    And the payment proposal is not processed
    And no settlement transaction is created

  Scenario: Funds remain locked in the treasury on dispute
    Given guild_context.task_state is "DISPUTED"
    Then the treasury balance is unchanged
    And the Specialist wallet receives no payment

  Scenario: Ragequit exit is documented, not executed
    Given guild_context.task_state is "DISPUTED"
    When the founder reviews the recovery options
    Then the Moloch v3 ragequit() exit path is documented in the README
    And no ragequit transaction is executed in the demo
