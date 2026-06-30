# Provenance: docs/MVP_FLOW.md (Step 10 + GATE 2), docs/VALIDATION_PLAN.md (§7.5, §8.4), PROJECT_PROPOSAL.md (§8 Steps 11-13) + design feedback 2026-06-29
# Concept: the Orchestrator automated pre-check and the human deliverable-acceptance gate (Gate 2). Acceptance leads to the payment proposal (Gate 3), not directly to settlement.

Feature: Deliverable review and acceptance
  As a human founder
  I want an automated pre-check plus a deliverable-acceptance gate
  So that the payment proposal is only raised for a verified, accepted deliverable

  Background:
    Given the Orchestrator received an A2A task/delivered with an attestation UID
    And the deliverable file is available for inspection

  Scenario: Automated pre-check passes
    When the Orchestrator runs deliverable_review
    Then the report shows hash_match true, format_valid true, and size_check true
    And the evaluator_verdict is "PASS"
    And the report is surfaced to Marco alongside the deliverable

  Scenario: Human accepts the deliverable at Gate 2
    Given the pre-check verdict is "PASS"
    When the runner reaches GATE 2 and prompts "Accept deliverable? [y/N]"
    And Marco enters "y"
    Then the loop proceeds to raise the payment proposal (Gate 3)
    And no funds move yet because settlement is gated on the payment proposal vote

  Scenario: Human rejects the deliverable at Gate 2
    Given the pre-check report has been surfaced
    When the runner reaches GATE 2 and Marco enters "N"
    Then guild_context.task_state becomes "DISPUTED"
    And no payment proposal is raised
    And no settlement transaction is sent

  Scenario: Pre-check failure surfaces a FAIL verdict
    Given the deliverable hash does not match the attested hash
    When the Orchestrator runs deliverable_review
    Then hash_match is false and the evaluator_verdict is "FAIL"
    And the failure is shown to Marco before GATE 2
