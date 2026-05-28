## AIxWeb3 Foundational Directions

- payment / commerce
- identity / reputation
- capability / interoperability
- wallet / permission
- privacy / security
- governance / coordination

## Problem space and Direction Map

- Cross-domain directions can be understood through problem domains such as payment / commerce, identity / reputation, capability / interoperability, wallet / permission, privacy / security, governance / coordination, and related areas.
- Whether a direction is valid depends not on how many new terms it uses, but on whether AI capabilities and Web3 mechanisms are both indispensable.
- Truly valuable problems usually sit at the intersection of “machine execution + economic exchange + permission control + verifiable records.”

## How to Choose a Main Direction

1. First choose 2 directions of interest from the 6 directions, and write one sentence for each: who is the real user in this direction?
2. Then write one sentence: why is this problem hard to solve without AI, and what is missing without Web3?
3. Then judge whether it is more suitable as a product demo, developer tooling, protocol / standard, risk model, or research memo.
4. Finally, choose only 1 main direction as the object of deeper Week 2 exploration. Put the other directions into the backlog; do not open too many threads at once.

### Direction Evaluation Matrix

- **Structural demand**: does this problem exist over the long term, or only because a hot project appeared?
- **Verifiability**: can it be validated through a demo, flowchart, transaction records, logs, user interviews, or a reference implementation?
- **Minimal entry point**: can you produce a problem breakdown, flowchart, mock, repo skeleton, or minimal prototype within one week?
- **Risk boundaries**: does it involve private keys, signatures, funds, identity, sensitive data, governance power, or irreversible actions?
- **Follow-through**: can it naturally feed into the Week 3 proposal, a Hackathon challenge, or a long-term handbook / research backlog?

### Deep Exploration Paths

#### Payment - From Scenario to Protocol

- Scenario layer: first clarify what the agent is actually buying—API calls, data queries, compute tasks, human services, content generation, or on-chain execution. Different services require different acceptance methods.
- Process layer: draw the flow “service discovery → quote → budget authorization → task execution → result delivery → acceptance → payment / refund / dispute.”
- Verification layer: judge whether delivery can be automatically verified. If not, specify who accepts the result, what the acceptance criteria are, and how disputes are handled.
- Protocol layer: then judge whether the problem needs checkout, invoice, receipt, escrow, reputation, evaluator, or a more complete marketplace / settlement layer.
- Counterexample: if an agent merely helps a user click a traditional payment button, without budget control, proof of delivery, verifiable records, or dispute handling, it is closer to ordinary automation and may not be a strong AI × Web3 direction.

#### Identity / Capability - From Agent Profile to Collaboration Network

- Profile: describe who the agent is, who maintains it, what it can do, what its inputs and outputs are, how it charges, and who bears responsibility for failures.
- Capability: break “can do things” into concrete capabilities, such as reading documents, calling APIs, deploying contracts, explaining transactions, generating reports, and executing payments.
- Interoperability: judge whether it needs to work with tools, another agent, or an on-chain contract / registry / payment layer. Different layers correspond to different interfaces such as MCP, A2A, ERC-8004, and MPP.
- Reputation: reputation is not an avatar or a name; it is historical tasks, delivery records, reviews, stake, slashing, verifiable evidence, or third-party endorsements.
- Counterexample: if a system only issues an NFT business card to an agent, without capability claims, invocation interfaces, delivery records, or verification methods, it usually does not form a complete identity / reputation direction.

#### Wallet - From Authorization to Recoverable Execution

- Authorization subject: on whose behalf is the agent allowed to act? A user wallet, team multisig, project treasury, test wallet, or read-only API?
- Authorization scope: limit callable contracts, functions, amounts, frequency, time windows, networks, tokens, counterparties, and maximum loss.
- Execution strategy: low-risk actions can be automated, while high-risk actions must pause. High-risk actions include signing, transfers, approvals, deployment, upgrades, governance voting, and key handling. 
- Recovery mechanisms: design pause, revocation, rollback, alerts, logs, post-incident audits, and human takeover. Automation without recovery mechanisms should not enter real-asset scenarios.
- Counterexample: if an AI wallet can only show “send transactions in natural language,” but cannot explain permission limits, failure handling, and audit methods, it is closer to a dangerous demo than a reliable product direction.

#### Privacy / Security - From Threat Model to Security Boundaries

- Asset inventory: list what the system holds—private keys, API keys, session tokens, user data, transaction permissions, budgets, sensitive documents, or governance permissions.
- Attack surfaces: prompt injection, malicious web pages / documents, polluted tool returns, forged transaction descriptions, phishing links, model hallucinations, and provider failures.
- Controls: least privilege, read-only first, human-in-the-loop, allowlists, budget limits, sandboxes, logs, simulated execution, and anomaly alerts.
- Sovereignty questions: can users export data, switch models, switch execution environments, revoke authorization, and continue using core assets without relying on a single provider?
- Counterexample: if a system requires users to entrust private keys, full transaction permissions, and complete context to a black-box agent, it must be marked high-risk and should not be the default learning path.

#### Governance - From Community Process to Verifiable Coordination

- Information organization: AI can summarize proposals, meetings, discussion threads, and task status, but it must preserve source links and uncertainties.
- Action conversion: turn meeting notes into action items, owners, deadlines, dependencies, budget impact, and public records.
- Contribution records: Web3 can help record contributions, funding, votes, execution status, and public accountability, but contribution quality still requires human judgment.
- Governance boundaries: AI can assist with explanation and reminders, but cannot replace the community in making value judgments, approving budgets, imposing penalties, or making final governance decisions.
- Counterexample: if a governance assistant automatically generates and passes budget proposals without human confirmation, public discussion, and accountability mechanisms, it is not an efficiency improvement; it is a governance risk.