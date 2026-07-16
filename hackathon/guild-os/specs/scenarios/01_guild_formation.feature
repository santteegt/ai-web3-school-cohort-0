# Provenance: docs/MVP_FLOW.md (Steps 1-2), docs/VALIDATION_PLAN.md (§2), PROJECT_PROPOSAL.md (§8 Steps 1-2) + design feedback 2026-06-29
# Concept: founding a guild — the Orchestrator collects the founder's parameters, summons the DAO + funds the
#          treasury on Base via its AgentFightClub skill, and registers its own ERC-8004 profile.

Feature: Guild formation
  As a human founder (Marco)
  I want to ask the Orchestrator to launch a guild with a mandate and a funded treasury
  So that an agentic specialist can be hired to build GuildOS components

  Background:
    Given the active network is Base with CHAIN_ID 8453
    And Marco controls a funded orchestrator-operated wallet
    And the Orchestrator has a guild-launch skill that collects founder inputs and spins up a club
    And the Orchestrator has an AgentFightClub skill that can use either integration path (ClawBank API or DAOhaus SDK)
    And each agent registers its own ERC-8004 profile via its own local GuildToolsServer instance (see scenarios/12_scoped_spending.feature)

  Scenario: Orchestrator collects the guild parameters from the founder
    Given no guild exists in the guild context
    When Marco asks the Orchestrator to launch a guild
    Then the Orchestrator requests the guild name
    And the mandate and governance settings
    And the initial member list of wallet addresses with their shares and loot distribution
    And the initial treasury tribute value

  Scenario: Launch and fund a new guild
    Given Marco has provided guild name, mandate, governance settings, member list with shares/loot, and a treasury tribute value
    When the Orchestrator executes the launch through its AgentFightClub skill
    Then a guild DAO is summoned on Base with the provided governance settings and initial members
    And the treasury is funded with the tribute value
    And the launch and tribute transactions are recorded to submissions/tx_hashes.md
    And the Orchestrator returns the dao address and the treasury address
    And guild_context.task_state becomes "ACTIVE"
    And guild_context.guild_address and guild_context.treasury_address are set

  Scenario: Orchestrator registers its own profile on ERC-8004
    Given the guild is ACTIVE
    When the Orchestrator registers its profile via the ERC-8004 protocol
    Then an agentId is minted for the Orchestrator on Base
    And the Orchestrator agentURI points to its live A2A Agent Card at /.well-known/agent-card.json

  Scenario: Reject a launch with a zero treasury tribute
    Given no guild exists in the guild context
    When Marco provides a treasury tribute value of 0
    Then the guild launch is rejected before any membership can be proposed
    And guild_context.task_state remains "INIT"

  Scenario: Either AgentFightClub path produces the same guild
    Given the ClawBank API path is unavailable
    When the Orchestrator launches the guild
    Then it uses the DAOhaus SDK path from the same AgentFightClub skill
    And the resulting dao address and treasury address are recorded identically

  Scenario: Do not relaunch over an already-active guild
    Given a guild already exists with task_state "ACTIVE"
    When the coordination runner starts
    Then it detects the active guild and skips the launch step
    And it reuses the existing guild_address without redeploying

  Scenario: Re-registering an already-registered agent is a no-op
    Given the Orchestrator already owns an agentId on ERC-8004
    When registration is attempted again
    Then no second agentId is minted
    And the existing agentId is returned
