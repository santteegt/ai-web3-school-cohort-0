# Provenance: docs/MVP_FLOW.md (Step 6), docs/VALIDATION_PLAN.md (§4.5), PROJECT_PROPOSAL.md (§8 Step 8), 20-api-contracts.md (§3 task/send) + design feedback 2026-06-29
# Concept: delegating a GuildOS ticket to the Specialist via a structured, fully-specified A2A task/send message.

Feature: Task delegation over A2A
  As the Orchestrator
  I want to delegate a GuildOS ticket as a structured A2A task
  So that the Specialist has an unambiguous, guess-proof work order

  Background:
    Given the Specialist is a guild member
    And the ticket to delegate is "Implement the EAS attestation module (EASClient)"

  Scenario: Delegate a complete, well-formed task
    When the Orchestrator sends an A2A task/send carrying all required fields
    Then the task includes a link to the GitHub issue
    And the task includes technical constraints: repo working branch, library versions, and environment variables
    And the task includes an Agent Bill of Materials listing the allowed tools, MCP servers, and data sources
    And the task includes acceptance_criteria expressed as a list of BDD tests that must pass
    And the task includes a deliverable_format of either "zip+hash" or "github_commit"
    And the task includes deadline and budget_wei
    Then the Specialist receives and parses the task
    And the message id is captured to guild_context.a2a_task_id
    And the message is logged to ./logs/a2a_trace_{date}.json

  Scenario: Reject a task missing acceptance criteria
    When the Orchestrator attempts an A2A task/send with an empty acceptance_criteria list
    Then the task is rejected as under-specified
    And no execution is started by the Specialist

  Scenario: Reject a task missing the GitHub issue link
    When the Orchestrator attempts an A2A task/send without a github_issue_url
    Then the task is rejected as under-specified
    And no execution is started by the Specialist

  Scenario: Reject a task with an unrecognized deliverable format
    When the Orchestrator attempts an A2A task/send with a deliverable_format that is neither "zip+hash" nor "github_commit"
    Then the task is rejected as under-specified

  Scenario: Carry GuildOS fields in the text body when metadata is rejected
    Given the A2A transport rejects extension metadata fields
    When the Orchestrator sends the task
    Then the GuildOS task fields are carried as a JSON string in the message text body
    And the Specialist parses them successfully
