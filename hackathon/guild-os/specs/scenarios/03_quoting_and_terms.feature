# Provenance: docs/MVP_FLOW.md (Step 4 + GATE 0.5), docs/VALIDATION_PLAN.md (§4.3-4.4, §8.2), PROJECT_PROPOSAL.md (§8 Step 5)
# Concept: the A2A invite/quote exchange and the lightweight economic-terms gate (Gate 0.5).

Feature: Quoting and economic terms
  As a human founder
  I want the Specialist to quote scope, cost, and timeline before work begins
  So that the economic terms are locked before any execution

  Background:
    Given a candidate was approved at GATE 0
    And the Orchestrator holds the Specialist A2A endpoint
    And the ticket to delegate is "Implement the EAS attestation module (EASClient)"

  Scenario: Specialist returns a quote for the ticket
    When the Orchestrator sends an A2A task/invite with the task spec
    Then the Specialist responds with an A2A task/quote
    And the quote contains scope, estimated_cost_wei, and deadline_iso
    And the quote is logged to hackathon/notes/a2a_trace_{date}.json

  Scenario: Human accepts the quote at Gate 0.5
    Given a task/quote has been received
    When the runner reaches GATE 0.5 and prompts "Accept quote? [y/N]"
    And Marco enters "y"
    Then the economic terms are locked
    And execution resumes to the membership-proposal step

  Scenario: Human rejects the quote at Gate 0.5
    Given a task/quote has been received
    When the runner reaches GATE 0.5 and Marco enters "N"
    Then the coordination loop halts
    And no membership proposal is submitted

  Scenario: Quote exceeding the mandate budget is surfaced for rejection
    Given the mandate budget is 0.001 ETH
    When the Specialist returns a quote with estimated_cost_wei above the budget
    Then the Orchestrator flags the over-budget quote at GATE 0.5
    And Marco can reject it to halt the loop
