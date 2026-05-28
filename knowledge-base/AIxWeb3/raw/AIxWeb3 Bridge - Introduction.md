
## Cross-domain Landscape

- **Payment / Commerce / Settlement**: focuses on how machines or agents buy APIs, data, compute, and services, and how quoting, acceptance, escrow, dispute handling, and settlement form a closed loop. Suitable for learners interested in commercial loops, payments, standards, and protocols.
    
- **Identity / Reputation / Capability / Interoperability**: focuses on how agents are discovered, described, invoked, verified, and coordinated. Suitable for learners interested in MCP, A2A, ERC-8004, registry, agent profiles, and capability claims.
    
- **Wallet / Permission / Safe Execution**: focuses on permission layering, automation boundaries, human confirmation, revocation, and auditing when agents interact with wallets, signatures, budgets, and on-chain actions. Suitable for learners interested in account abstraction, Safe, policy, guard, and session keys.
    
- **Privacy / Security / Sovereignty**: focuses on prompt injection, tool abuse, sensitive data, dependency on model providers, private key / API key exposure, local execution, and user sovereignty. Suitable for learners interested in security, privacy, trusted execution, auditing, and risk control.
    
- **Dev Tooling / Agent Workflow**: focuses on whether AI can genuinely improve Web3 builder workflows, such as docs-to-agent, contract reading, transaction explanation, deployment assistants, test scripts, and automated repo maintenance. Suitable for learners who want to build tools, developer experience, or workflows.
    
- **Governance / Coordination / Public Goods**: focuses on how AI can help DAOs, communities, and public goods projects with proposal summaries, meeting action items, contribution records, budget checklists, and transparent execution. Suitable for learners interested in community collaboration, public goods, and organizational processes.

### Payment / Commerce / Settlement

Agent economic activity is not a simple extension of ordinary payments. The real difficulty is not “whether money can be transferred,” but how quoting, budgeting, authorization, delivery, verification, escrow, dispute handling, receipts, and settlement connect into a controllable flow.

- When an AI agent acts as a consumer or service provider, the budget, payment conditions, delivery standards, and failure remedies must be clear.
- Payment is only one segment of the flow; commerce also includes service discovery, price negotiation, task execution, result acceptance, dispute handling, and settlement.
- On-chain records can provide receipts, state, and a basis for settlement, but they cannot automatically solve service quality, arbitration, and trust issues.

Recommended Learning Material:
- [x402 Docs](https://docs.x402.org/introduction): open payment entry points and machine payment framing.
- [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) / [ERC-8183](https://eips.ethereum.org/EIPS/eip-8183): references for protocol directions such as agent trust, jobs, escrow, and evaluators.
- [Olas](https://olas.network/): reference for the agent economy / autonomous services direction.
- [MPP Official Documentation](https://docs.stripe.com/payments/machine/mpp): documentation entry point for Machine Payments Protocol (MPP).

### Identity / Reputation / Capability / Interoperability

An agent is not just “a program that can execute.” It also needs a capability layer for being discovered, described, verified, and coordinated. This module separates what identity, capability claims, communication protocols, task collaboration, and reputation accumulation each solve.

- Identity answers “who are you,” capability answers “what can you do,” and reputation answers “why should others trust you.”
- Interoperability focuses on how different agents, tools, services, and systems exchange context, tasks, and results.
- MCP, A2A, ERC-8004, and MPP are not the same kind of thing: they sit at different layers and address different problems and constraints.
- The truly valuable direction is not giving an agent a DID name, but forming a complete flow of discovery, collaboration, invocation, and verification.

Recommended Learning Materials

- [MCP Official Documentation](https://modelcontextprotocol.io/docs/getting-started/intro): tool context and agent-tool interfaces. 
- [A2A Official Repository](https://github.com/a2aproject/A2A): reference for agent-to-agent collaboration protocols.

### Wallet / Permission / Safe Execution

When an agent participates in on-chain actions, the most important question is not “how to call a signing API,” but how permissions are granted, limited, revoked, audited, and recovered.

- When an agent participates in on-chain actions, distinguish between steps that can be automated and steps that require human confirmation.
- Authorization is not a one-time action; it is a combination of budget, scope, time, operation type, and failure handling.
- Account abstraction, smart accounts, multisigs, and guard / policy mechanisms can provide finer-grained control for agent execution, but they also increase system complexity.

On this basis, task-level authorization can also be introduced: instead of giving an agent a long-term permission, generate a temporary authorization around one concrete task. For example, Cobo CAW’s Pact lets the user first confirm the agent’s task intent, budget, operation scope, time window, and failure-handling strategy. The agent can only execute within the boundaries defined by that Pact, and the permission expires when the task ends.

Recommended Learning Materials

- [ERC-4337 Documentation](https://docs.erc4337.io/): foundations of account abstraction and smart accounts.
- [Ethereum Account Abstraction](https://ethereum.org/roadmap/account-abstraction/): background on the account abstraction roadmap.
- [What Is Safe](https://docs.safe.global/home/what-is-safe) / [Safe Smart Account Guards](https://docs.safe.global/advanced/smart-account-guards): references for multisigs, smart accounts, and guard / policy mechanisms.
- [ERC-4337 Official EIP](https://eips.ethereum.org/EIPS/eip-4337): the base protocol for account abstraction.
- [ERC-7702 Official EIP](https://eips.ethereum.org/EIPS/eip-7702): understand how standard externally owned accounts can temporarily gain smart-account-like capabilities.
- [Coinbase Policy Engine](https://help.coinbase.com/en/prime/onchain-wallet/onchain-policy-engine): an example of configurable transaction policies.
- [Cobo Agentic Wallet Developer Assistant](https://www.cobo.com/products/agentic-wallet/manual/developer/quickstart-overview): how to integrate a native agent wallet.
- [MetaMask — Design Server Wallets for AI Agents with ERC-8004](https://docs.metamask.io/tutorials/design-server-wallets/): understand a production architecture combining agent identity, backend signer, and wallet execution.
- [LI.FI Agents Overview](https://docs.li.fi/agents/overview): understand how agents can query chains, tokens, transaction status, and execute cross-chain actions.

### Privacy / Security / Sovereignty

Once an agent holds context, credentials, API keys, private keys, or a budget, security is no longer a side issue; it is a system prerequisite.

- Common risks include at least five categories: prompt injection, tool abuse, unauthorized execution, sensitive data leakage, and dependency on model providers. In concrete systems, these may further expand into attack surfaces such as unauditable operations, forged tool returns, phishing links, and model hallucinations.
- Security design must answer: what can the agent see, what can it call, how much can it spend, on whose behalf can it make decisions, and who is responsible when something goes wrong?
- Privacy / sovereignty is not just the four words “local model”; it also involves data boundaries, provider dependency, portability, auditing, and user control.

Recommended Learning Materials

- [Understanding Prompt Injection Attacks](https://openai.com/index/prompt-injections/): OpenAI’s introduction to prompt injection attacks.
- [Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/): basic knowledge of sensitive information disclosure risks.
- [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/): basic knowledge of excessive-agency risks when agents can take actions.
- [Fileverse documentation](https://docs.fileverse.io/d/0200015f0008#k=xSLRzkvhNF0YVBb8CpGH0X1qJtd6_obOC5odV0dcWzU): reference for privacy, data ownership, and user-controlled collaboration contexts.

### Governance / Coordination / Public Goods

AI can help DAOs, communities, and public goods projects organize information, track contributions, generate action items, and support transparent execution, but governance power, budget actions, and final judgment must have clear boundaries.

- Parts suitable for AI assistance: proposal summaries, organizing discussion threads, turning meetings into action items, contribution records, budget execution checklists, and community Q&A.
- Parts not suitable for direct delegation to AI: value judgments, budget approvals, punishment / incentive decisions, and initiating irreversible actions on behalf of the community.
- What Web3 provides is not “a livelier community tool,” but mechanisms for public records, verifiable contributions, transparent budgets, and open collaboration.

Recommended Learning Materials

- [Ethereum Governance Basics](https://ethereum.org/governance/): basic knowledge of Ethereum governance.
- [Decentralized Autonomous Organizations (DAOs)](https://ethereum.org/dao/): basic knowledge of DAOs.
- [Snapshot Documentation](https://docs.snapshot.box/): offchain voting, proposals, spaces, strategies, and common DAO governance tooling.
- [OpenZeppelin Governor Documentation](https://docs.openzeppelin.com/contracts/5.x/api/governance): onchain execution-oriented governance contracts and patterns.
- [Gitcoin Funding Mechanisms](https://gitcoin.co/mechanisms): public-goods funding mechanisms.

## Must- read

- [Ethereum Developer Documentation Overview](https://ethereum.org/developers/docs/): a foundational entry point for understanding Web3 mechanisms.
- [x402 Official Homepage](https://www.x402.org/): understand the entry point for machine / agent payments.
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) / [A2A](https://github.com/a2aproject/A2A): understand collaboration interfaces between agents and tools / agents.
- [MPP introduction](https://stripe.com/blog/machine-payments-protocol): understand the problem background of Machine Payments Protocol (MPP).
- [GLM 5.1 Agentic Coding Guide](https://docs.z.ai/guides/llm/glm-5.1#agentic-coding): gives you a sense of where GLM 5.1 lands on planning, tool use, and coding, which is exactly what you need to answer the Week 2 question of what the AI is actually doing in a given agent workflow
- [Chat Completion API](https://docs.z.ai/api-reference/llm/chat-completion): the core GLM 5.1 endpoint, OpenAI compatible with messages, tools, and tool_choice; you can fire off your first function calling request in five minutes and use it as the skeleton for capability manifests, agent profiles, or payment flows
- [Web Search Tool](https://docs.z.ai/api-reference/tools/web-search): built in web search so you don't have to wire up your own search API, perfect for spinning up agent demos that need external context, such as reading docs, looking up contracts, or explaining transactions