# Provenance: docs/MVP_FLOW.md (Steps 13a-14 + GATE 4), docs/VALIDATION_PLAN.md (§3.3-3.7), docs/RISKS.md (F2), 10-technical-design.md (§3) + design feedback 2026-06-29
# Concept: DAO-governed reputation write-back, triggered by the Specialist — an executable submitFeedback proposal whose passing vote (Gate 4) triggers giveFeedback().
#
# Complementary flow:
# ```mermaid
# sequenceDiagram
#     participant S as Specialist
#     participant O as Orchestrator
#     participant AFC as AgentFightClub
#     actor H as Human
#     participant R as ERC-8004
#     S->>O: A2A feedback/request (completed work)
#     O->>AFC: reputation_propose (submitFeedback, 6 fields)
#     H->>AFC: GATE 4 vote approve -> process
#     AFC->>R: giveFeedback() (guild contract = msg.sender)
#     R-->>AFC: DeliveryRecorded event
# ```

Feature: DAO-governed reputation feedback
  As a guild
  I want reputation feedback to be requested by the Specialist and require a passing DAO vote
  So that no single party can unilaterally write to a Specialist's on-chain profile

  Background:
    Given settlement completed and the settlement tx is recorded
    And the Specialist sent an A2A feedback/request asking the Orchestrator for feedback on the completed work
    And the 6 delivery fields are available: task_type, deliverable_hash, acceptance_timestamp, payment_wei, guild_address, a2a_task_id

  Scenario: Submit the executable submitFeedback proposal on the Specialist's request
    Given the Orchestrator received the feedback/request
    When the Orchestrator calls reputation_propose with the delivery record
    Then an executable submitFeedback proposal is recorded on Base
    And the proposal encodes the giveFeedback call with the 6 fields
    And guild_context.reputation_proposal_id holds the proposal id

  Scenario: Passing vote executes giveFeedback on-chain
    Given a submitFeedback proposal exists
    When the runner reaches GATE 4 and prompts "Approve reputation feedback for Specialist? [y/N]"
    And Marco enters "y" and the proposal is processed
    Then giveFeedback executes with the guild contract as the caller
    And a DeliveryRecorded event is emitted with all 6 fields
    And the reputation tx is saved as Basescan tx #3
    And guild_context.task_state becomes "SETTLED"

  Scenario: Voted-down proposal writes no reputation
    Given a submitFeedback proposal exists
    When the runner reaches GATE 4 and Marco enters "N"
    Then giveFeedback is not executed
    And the Specialist profile gains no delivery record

  Scenario: Caller constraint is enforced (F2)
    Given a submitFeedback proposal is being executed
    Then the caller of giveFeedback is the guild contract
    And the Specialist Agent's own wallet is never the caller

  Scenario: Reputation delta is visible before and after
    Given the Specialist before-state was captured
    When giveFeedback has executed
    Then the after-state is captured to ./logs/erc8004_specialist_after.json
    And the before and after delivery counts differ by one
