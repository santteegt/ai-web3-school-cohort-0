# Provenance: docs/MVP_FLOW.md (Step 7), docs/VALIDATION_PLAN.md (§6), docs/RISKS.md (F3), PROJECT_PROPOSAL.md (§8 Step 9) + design feedback 2026-06-29
# Concept: GLM-5.1 long-horizon execution of a delegated GuildOS ticket (dogfooding) — read the issue, plan, execute, produce a hashable deliverable.
#
# Complementary flow:
# ```mermaid
# sequenceDiagram
#     participant S as Specialist
#     participant GH as GitHub issue
#     participant G as GLM-5.1
#     S->>GH: read issue + load ticket prompt instructions
#     S->>G: decompose ticket into >=3-step plan
#     loop each step
#         G->>G: plan -> tool call -> result -> next
#     end
#     G-->>S: structured code deliverable
#     S->>S: produce deliverable hash (zip file hash OR github commit hash)
#     S->>S: log plan + tool calls + output to glm_trace
# ```

Feature: Specialist long-horizon execution
  As the Specialist Agent
  I want to read the GitHub issue, plan, and execute a GuildOS ticket with GLM-5.1
  So that I produce a real, verifiable code deliverable with a hash ready for attestation

  Background:
    Given the Specialist received an A2A task/send for "Implement the EAS attestation module (EASClient)"
    And the task carries a GitHub issue link, technical constraints, an Agent Bill of Materials, acceptance_criteria, and a deliverable_format
    And the GLM-5.1 API is reachable

  Scenario: Read the issue then decompose and execute a multi-step plan
    When the Specialist reads the GitHub issue and loads the ticket prompt instructions
    And the Specialist runs GLM-5.1 long-horizon planning within the declared technical constraints
    Then the ticket is decomposed into a plan of at least 3 steps
    And each step runs a plan to tool-call to result loop using only tools in the Agent Bill of Materials
    And a structured code deliverable is produced
    And the full trace is logged to hackathon/notes/glm_trace_{date}.json

  Scenario: Deliverable satisfies the declared acceptance criteria
    Given GLM-5.1 produced a code deliverable
    When the Specialist runs the acceptance_criteria BDD tests against the output
    Then the declared BDD tests pass
    And the deliverable file is non-empty

  Scenario: Produce a hash for the zip deliverable format
    Given the task deliverable_format is "zip+hash"
    When the Specialist packages the deliverable
    Then it produces a zip artifact and computes its SHA-256 hash
    And that hash is carried forward for EAS attestation in the next stage

  Scenario: Produce a hash for the GitHub commit deliverable format
    Given the task deliverable_format is "github_commit"
    When the Specialist pushes the work to the repo working branch
    Then it records the resulting commit hash
    And that commit hash is carried forward for EAS attestation in the next stage

  Scenario: Fall back to a deterministic task after repeated unusable output
    Given GLM-5.1 produces 3 consecutive unusable outputs
    When the Specialist applies the F3 fallback
    Then it switches to the deterministic fallback prompt
    And it still produces a hashable, structured deliverable
