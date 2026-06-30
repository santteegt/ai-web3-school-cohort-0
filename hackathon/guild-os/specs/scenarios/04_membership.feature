# Provenance: docs/MVP_FLOW.md (Step 5 + GATE 1), docs/VALIDATION_PLAN.md (§2.3-2.4, §8.3), PROJECT_PROPOSAL.md (§8 Steps 6-7)
# Concept: Specialist membership via an AgentFightClub proposal and the human membership vote (Gate 1).

Feature: Specialist membership
  As a human founder
  I want to vote on the Specialist's membership using its on-chain reputation
  So that only a trusted agent gains access to the guild treasury

  Background:
    Given the quote was accepted at GATE 0.5
    And a guild exists with task_state "ACTIVE"
    And the Specialist has an ERC-8004 profile readable via 8004scan

  Scenario: Specialist submits a membership proposal
    When the Specialist calls AgentFightClub propose with its ERC-8004 id, task quote, and free-form description
    Then a membership proposal is recorded on Base mainnet
    And guild_context.membership_proposal_id holds the proposal id

  Scenario: Human approves membership at Gate 1
    Given a membership proposal exists
    And Marco has reviewed the Specialist's delivery history and acceptance rate
    When the runner reaches GATE 1 and prompts "Approve Specialist membership? [y/N]"
    And Marco enters "y"
    Then AgentFightClub vote is cast to approve and the proposal is processed
    And the Specialist wallet is added to guild_context.member_list

  Scenario: Human rejects membership at Gate 1
    Given a membership proposal exists
    When the runner reaches GATE 1 and Marco enters "N"
    Then the coordination loop halts
    And the Specialist is not added to the member_list

  Scenario: Skip proposal when the Specialist is already a member
    Given the Specialist wallet is already in guild_context.member_list
    When the membership step runs
    Then proposal submission is skipped
    And the loop continues to task delegation
