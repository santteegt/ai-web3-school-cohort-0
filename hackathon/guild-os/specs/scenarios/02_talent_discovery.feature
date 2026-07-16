# Provenance: docs/MVP_FLOW.md (Steps 2-3 + GATE 0), docs/VALIDATION_PLAN.md (§3.1-3.2, §8.1), PROJECT_PROPOSAL.md (§8 Steps 2-4) + design feedback 2026-06-29, 2026-06-30
# Concept: discovering candidate specialists via a talent-pool skill (ERC-8004 / A2A cards) and the human candidate-selection gate (Gate 0).
# The Specialist's own ERC-8004 registration is treated as first-class, tracked work here — not
# assumed fixture data — because the Specialist is the identity that accrues reputation over every
# future dogfooding run. It must register once, independently of any single guild, before it is
# discoverable at all.

Feature: Talent discovery and candidate selection
  As a human founder
  I want to ask the Orchestrator to surface specialist candidates
  So that I — not the agent — make the hiring decision

  Background:
    Given a guild exists with task_state "ACTIVE"
    And the Orchestrator is registered on ERC-8004 with a minted agentId
    And the Orchestrator has a talent-pool skill whose script calls talent_query against ERC-8004 / A2A cards
    And the mandate task type is "agentic-ai-web3-engineering"
    And each agent signs through a scoped WalletProvider (see scenarios/12_scoped_spending.feature)
    And each agent registers its own ERC-8004 profile via its own local GuildToolsServer instance

  Scenario: Specialist registers its own profile on ERC-8004
    Given the Specialist is not yet registered on ERC-8004
    When the Specialist registers its profile via the ERC-8004 protocol, signed through its scoped WalletProvider
    Then an agentId is minted for the Specialist on Base
    And the Specialist agentURI points to its live A2A Agent Card at /.well-known/agent-card.json
    And this registration happens once, independently of any single guild's formation
    And the Specialist is now discoverable by talent_query

  Scenario: Surface a candidate shortlist for human review
    Given the talent-pool list is hardcoded for the MVP
    And the Specialist is already registered on ERC-8004
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

  Scenario: Re-registering an already-registered agent is a no-op
    Given the Specialist already owns an agentId on ERC-8004
    When registration is attempted again
    Then no second agentId is minted
    And the existing agentId is returned
