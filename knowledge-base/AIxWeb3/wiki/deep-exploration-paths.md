---
title: "Deep Exploration Paths"
type: concept
tags: [aixweb3-bridge, framework, direction-selection]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

Deep Exploration Paths are structured decomposition templates for each AI × Web3 direction. Rather than starting with a technology, each path starts with the scenario, process, and verification layer before reaching protocol decisions. This prevents building solutions where either AI or Web3 is optional.

## Paths by Direction

### Payment → From Scenario to Protocol
- **Scenario layer**: clarify what the agent is buying — API calls, data, compute, human services, on-chain execution
- **Process layer**: draw the flow: service discovery → quote → budget authorization → task execution → result delivery → acceptance → payment/refund/dispute
- **Verification layer**: judge whether delivery can be automatically verified; specify who accepts, what criteria, how disputes are handled
- **Protocol layer**: determine if the problem needs checkout, invoice, receipt, escrow, reputation, evaluator, or marketplace/settlement

### Identity/Capability → From Agent Profile to Collaboration Network
- **Profile**: who is the agent, who maintains it, what can it do, what are inputs/outputs, how does it charge, who bears failure responsibility
- **Capability**: break "can do things" into concrete capabilities (read docs, call APIs, deploy contracts, explain transactions, execute payments)
- **Interoperability**: judge if it needs to work with tools (MCP), another agent (A2A), or on-chain registry (ERC-8004, MPP)
- **Reputation**: define as historical tasks, delivery records, reviews, stake, slashing, verifiable evidence, or third-party endorsements

### Wallet → From Authorization to Recoverable Execution
- **Authorization subject**: user wallet, team multisig, project treasury, test wallet, or read-only API?
- **Authorization scope**: callable contracts, functions, amounts, frequency, time windows, networks, tokens, counterparties, max loss
- **Execution strategy**: which actions can be automated vs. which must pause (signing, transfers, approvals, deployment, upgrades, governance voting, key handling)
- **Recovery mechanisms**: pause, revocation, rollback, alerts, logs, post-incident audits, human takeover

### Privacy/Security → From Threat Model to Security Boundaries
- **Asset inventory**: private keys, API keys, session tokens, user data, transaction permissions, budgets, sensitive documents, governance permissions
- **Attack surfaces**: prompt injection, malicious web pages/documents, polluted tool returns, forged transaction descriptions, phishing links, model hallucinations, provider failures
- **Controls**: least privilege, read-only first, human-in-the-loop, allowlists, budget limits, sandboxes, logs, simulated execution, anomaly alerts
- **Sovereignty questions**: can users export data, switch models, switch execution environments, revoke authorization, continue without a single provider?

### Governance → From Community Process to Verifiable Coordination
- **Information organization**: AI can summarize proposals, meetings, discussion threads, and task status — must preserve source links and uncertainties
- **Action conversion**: turn meeting notes into action items with owners, deadlines, dependencies, budget impact, and public records
- **Contribution records**: Web3 records contributions, funding, votes, execution status, and public accountability — quality still requires human judgment
- **Governance boundaries**: AI can assist with explanation and reminders, but cannot replace community in value judgments, budget approvals, penalties, or final governance decisions

## Related Concepts

- [[direction-evaluation-matrix]]
- [[unified-evaluation-framework]]
- [[payment-and-commerce]]
- [[identity-reputation-capability]]
- [[wallet-permission-safe-execution]]
- [[privacy-security-sovereignty]]
- [[governance-coordination-public-goods]]

## Sources

- [[sources/aixweb3-problem-space-direction-map]]
