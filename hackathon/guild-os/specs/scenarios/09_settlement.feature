# Provenance: docs/MVP_FLOW.md (Steps 11-12), docs/VALIDATION_PLAN.md (§2.5), docs/RISKS.md (F1, F6), PROJECT_PROPOSAL.md (§8 Step 14) + design feedback 2026-06-29
# Concept: settlement is DAO-governed — the Orchestrator raises a payment proposal through AgentFightClub; the human votes and processes it (Gate 3); processing releases treasury funds.
#
# Complementary flow:
# ```mermaid
# sequenceDiagram
#     participant O as Orchestrator
#     participant AFC as AgentFightClub
#     participant S as Specialist
#     actor H as Human
#     O->>AFC: payment_propose (deliverable details, specialist address, amount)
#     O->>S: A2A task/accepted (payment_proposal_id + url)
#     H->>AFC: GATE 3 vote approve -> process
#     AFC->>S: treasury releases funds to Specialist wallet
# ```

Feature: Payment proposal and treasury settlement
  As the Orchestrator
  I want payment to flow through a DAO payment proposal voted by the founder
  So that treasury funds move on a passing governance vote, not on agent trust

  Background:
    Given Marco accepted the deliverable at GATE 2
    And the Specialist wallet address is known
    And the treasury is held by the DAO, not by any agent wallet

  Scenario: Raise the payment proposal and close the A2A loop
    When the Orchestrator submits a payment proposal through AgentFightClub with the deliverable details and the Specialist address
    Then guild_context.payment_proposal_id holds the proposal id
    And the Orchestrator sends A2A task/accepted carrying the payment proposal id and url
    And no funds have left the treasury yet

  Scenario: Passing vote processes the payment and settles
    Given a payment proposal exists
    When the runner reaches GATE 3 and prompts "Approve and process payment to Specialist? [y/N]"
    And Marco enters "y" and the payment proposal is processed
    Then the DAO treasury releases funds to the Specialist wallet
    And the settlement tx is saved as Basescan tx #2 in ./submissions/tx_hashes.md
    And guild_context.settlement_tx is set
    And the Specialist wallet balance increases

  Scenario: Voted-down payment proposal releases no funds
    Given a payment proposal exists
    When the runner reaches GATE 3 and Marco enters "N"
    Then the payment proposal is not processed
    And no funds leave the treasury
    And guild_context.task_state becomes "DISPUTED"

  Scenario: Block settlement before deliverable acceptance
    Given the deliverable has not been accepted at GATE 2
    When settlement is attempted
    Then no payment proposal is raised
    And no funds leave the treasury

  Scenario: Use the DAOhaus fallback when ClawBank is unavailable (F1)
    Given the AgentFightClub ClawBank API is unavailable
    When the payment proposal is raised and processed
    Then the Moloch v3 DAOhaus SDK path is used for the same proposal lifecycle
    And the same settlement evidence is recorded

  Scenario: Show pre-recorded evidence under network congestion (F6)
    Given a live settlement tx takes more than 30 seconds to confirm
    When the demo continues
    Then the pre-recorded Basescan screenshot is shown as a fallback
    And the loop is not blocked
