> ## Documentation Index
> Fetch the complete documentation index at: https://cobo.com/products/agentic-wallet/manual/llms.txt
> Use this file to discover all available pages before exploring further.

# Pacts

> The technical reference for pact enforcement: operating modes, PactSpec schema, state machine, and pact-scoped credentials.

For the conceptual overview and the end-to-end flow, see [What is a pact](/products/agentic-wallet/manual/start-here/what-is-a-pact) and [Pact flow](/products/agentic-wallet/manual/start-here/pact-flow). This page covers the technical details: operating modes, the PactSpec schema, the state machine, and how pact-scoped credentials work.

## Two modes: owner and delegate

The pact mechanism behaves differently depending on whether your agent is the wallet owner or a delegate. Before pairing, pacts are automatically processed. After pairing, the agent is a delegate and every pact requires explicit owner approval in the Cobo Agentic Wallet app.

When you pair the wallet with the Cobo Agentic Wallet app, your agent transitions from owner to delegate. From that point on, the owner uses pacts to define the terms the agent operates under: what it is trying to do, under which policies, and when that authority ends.

## The PactSpec: what the agent declares

When your agent needs a new scoped delegation, it submits a **PactSpec** — a machine-readable declaration of its intent, plan, and policy boundaries:

| Field                   | Type   | Description                                                                                                                                                                 |
| ----------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `intent`                | string | Natural language description of the task. Shown to the owner during approval review.                                                                                        |
| `execution_plan`        | string | Free-form markdown description of how the agent plans to carry out the task.                                                                                                |
| `policies`              | list   | Inline policy rules constraining the agent's actions — spend limits, address restrictions, review thresholds, and so on. Evaluated by the policy engine on every operation. |
| `completion_conditions` | list   | Conditions that automatically complete the pact when reached — such as a transaction count, spend cap, or time limit.                                                       |

## Pact state machine

| State              | Meaning                                                                                                                 |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `pending_approval` | Submitted by the agent, awaiting owner review. No access has been granted.                                              |
| `active`           | Approved by the owner. The delegation and API key are live. The agent can submit operations.                            |
| `rejected`         | Rejected by the owner during approval review. No access was ever granted.                                               |
| `completed`        | A completion condition was met. The pact has ended naturally.                                                           |
| `expired`          | The pact was active and its `expires_at` timestamp was reached without a `time_elapsed` completion condition in effect. |
| `revoked`          | The owner explicitly revoked the pact. Access was terminated immediately.                                               |
| `withdrawn`        | The agent withdrew the pact before it was acted on by the owner.                                                        |

```
PENDING_APPROVAL
    ├─ approved ──→ ACTIVE
    │                 ├─ completion condition met ──→ COMPLETED
    │                 ├─ expires_at reached ──→ EXPIRED
    │                 └─ owner revokes ──→ REVOKED
    ├─ rejected ──→ REJECTED
    └─ agent withdraws ──→ WITHDRAWN
```

## The pact-scoped API key

When a pact is approved, the agent receives an API key scoped to that pact's policies. This key:

* Can only authorize operations within the delegation scope derived from the pact's policy set
* Is subject to all policies defined in the pact's `policies` field on every call
* Is bound to the specific wallet identified by `wallet_id`
* Becomes invalid immediately when the pact exits `ACTIVE` for any reason — no grace period

## Policy controls

A pact's `policies` field is where you set the guardrails the agent must operate within. The following pages cover each control in detail:

* [Policy engine](/products/agentic-wallet/manual/security/policy-engine) — how every agent operation is evaluated before execution
* [Spend limits](/products/agentic-wallet/manual/security/spend-limits) — per-transaction and rolling spend caps
* [Address allowlists](/products/agentic-wallet/manual/security/address-allowlists) — restricting which addresses the agent can send to
