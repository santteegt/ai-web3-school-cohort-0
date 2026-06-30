# Provenance: docs/MVP_FLOW.md (Steps 2-3 + GATE 0), docs/VALIDATION_PLAN.md (§3.1-3.2, §8.1), PROJECT_PROPOSAL.md (§8 Steps 2-4) + design feedback 2026-06-29
# Concept: discovering candidate specialists via a talent-pool skill (ERC-8004 / A2A cards) and the human candidate-selection gate (Gate 0).

Feature: Talent discovery and candidate selection
  As a human founder
  I want to ask the Orchestrator to surface specialist candidates
  So that I — not the agent — make the hiring decision

  Background:
    Given a guild exists with task_state "ACTIVE"
    And the Orchestrator is registered on ERC-8004 with a minted agentId
    And the Orchestrator has a talent-pool skill whose script calls talent_query against ERC-8004 / A2A cards
    And the mandate task type is "agentic-ai-web3-engineering"

  Scenario: Surface a candidate shortlist for human review
    Given the talent-pool list is hardcoded for the MVP
    When Marco asks the Orchestrator to find talent and the talent-pool skill runs talent_query for the mandate task type
    Then a shortlist of at least one candidate is returned
    And each candidate exposes name, agent_id, capabilities, and a2a_endpoint
    And the Specialist before-state is captured to ./logs/erc8004_specialist_before.json

  Scenario: Human approves a candidate at Gate 0
    Given a candidate shortlist has been surfaced
    When the runner reaches GATE 0 and prompts "Approve invite to Specialist Agent [y/N]?"
    And Marco enters "y"
    Then execution resumes to the invitation step
    And the selected candidate endpoint is used for the A2A invite

  Scenario: Human rejects the candidate at Gate 0
    Given a candidate shortlist has been surfaced
    When the runner reaches GATE 0 and Marco enters "N"
    Then the coordination loop halts
    And no A2A invite is sent

  Scenario: Empty shortlist halts before invitation
    Given talent_query returns no candidates
    Then the runner reports an empty shortlist
    And GATE 0 is not presented
