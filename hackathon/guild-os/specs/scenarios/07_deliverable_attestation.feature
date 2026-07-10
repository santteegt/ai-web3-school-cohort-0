# Provenance: docs/MVP_FLOW.md (Steps 8-9), docs/VALIDATION_PLAN.md (§5), docs/RISKS.md (F7), PROJECT_PROPOSAL.md (§8 Step 10)
# Concept: hashing the deliverable, creating an EAS attestation, and returning the UID over A2A.
#
# Complementary flow:
# ```mermaid
# sequenceDiagram
#     participant S as Specialist
#     participant EAS as EAS (Base mainnet)
#     participant O as Orchestrator
#     S->>S: SHA-256(deliverable)
#     S->>EAS: attest(hash, taskType, guildContract, paymentAmount)
#     EAS-->>S: attestation UID
#     S->>O: A2A task/delivered { hash, attestation_uid, attestation_url }
# ```

Feature: Deliverable EAS attestation
  As the Specialist Agent
  I want to attest my deliverable's hash via EAS and return the UID
  So that the delivery claim is cryptographically signed and judge-verifiable

  Background:
    Given the Specialist produced a code deliverable
    And DELIVERY_SCHEMA_UID is registered on Base mainnet
    And the active network is Base mainnet with CHAIN_ID 8453

  Scenario: Attest the deliverable hash and return the UID
    When the Specialist computes the SHA-256 of the deliverable
    And calls EASClient.attest with the hash, task type, guild contract, and payment amount
    Then a non-zero attestation UID is returned
    And the attestation is queryable at https://base.easscan.org/attestation/{uid}
    And guild_context.attestation_uid and attestation_url are set
    And the easscan link is saved to ./submissions/tx_hashes.md

  Scenario: Embed the attestation UID in the A2A result
    Given an attestation UID was returned
    When the Specialist sends A2A task/delivered
    Then the message carries deliverable_hash, attestation_uid, and attestation_url
    And the message carries no on_chain_tx field

  Scenario: Read back the attestation and confirm the hash matches
    Given an attestation UID was returned
    When the Orchestrator calls EASClient.get_attestation with the UID
    Then the returned deliverableHash equals the SHA-256 of the deliverable

  Scenario: Fall back to a raw event when the schema is missing (F7)
    Given DELIVERY_SCHEMA_UID is not present in the environment
    When the Specialist attempts to attest
    Then it falls back to a raw eth_sendTransaction emitting DeliverableCommitted(bytes32 hash)
    And the fallback tx hash is saved to submissions/tx_hashes.md

  Scenario: Orchestrator's A2A server receives the proactive task/delivered
    Given an attestation UID was returned
    When SpecialistA2AClient sends a proactive task/delivered to the orchestrator_endpoint
    Then OrchestratorA2AServer receives it as an inbound message/send on port 10000
    And its executor triggers the deliverable pre-check for Gate 2
    And the message is logged to hackathon/notes/a2a_trace_{date}.json

  Scenario: Proactive push to an unreachable orchestrator_endpoint fails closed
    Given the orchestrator_endpoint in the task carries an unreachable or malformed URL
    When SpecialistA2AClient attempts to send the proactive task/delivered
    Then the send fails with a logged, surfaced error
    And the task is not silently treated as delivered
    And the Specialist does not silently drop the deliverable
