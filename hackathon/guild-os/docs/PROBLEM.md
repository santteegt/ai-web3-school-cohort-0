# Problem — GuildOS

## Statement

The coordination infrastructure for AI-augmented knowledge work does not exist yet. Traditional freelance and agency structures are slow and opaque: finding a specialist takes weeks, reputation is locked in platforms you do not own, and every project restarts context from scratch.

AI agents can now execute real development work autonomously — writing code, running tests, generating analyses — but without structure they hallucinate, overreach, and leave no verifiable trail. The deeper problem is that neither side is using what the other offers: developers treat agents as tools rather than collaborators, and agents have no economic structure to join that rewards verified delivery with portable reputation.

The result is a coordination gap that no existing platform addresses: capable contributors, human and AI, cannot yet form credible, accountable, ephemeral work structures without a rent-extracting intermediary in the middle.

---

## Target Users

**Primary:** Independent developers and small dev shops (1–4 people) who regularly need short-duration specialized expertise — security review, contract audits, frontend work, data analysis, spec writing — and are tired of Upwork's fees, GitHub marketplace's rigidity, and Slack-based coordination that loses context after every project.

**Secondary:** AI agent developers who want their agents to participate in economic structures, accept work, deliver verifiably, and accumulate portable reputation across engagements — rather than being confined to one platform's tool ecosystem.

**Not this hackathon:** Enterprise procurement teams, non-technical clients, anyone who needs a polished consumer UI. The demo targets a technically fluent audience: developers and judges who can read a Basescan transaction.

---

## Real Scenario

Marco is an independent smart contract developer with a client project: build and audit a minimal ERC-20 staking contract in two weeks. He can write the contract himself but does not have a strong audit background. He opens GuildOS, defines a mandate, and commits capital to a shared guild treasury via AgentFightClub. The club is live: mandate on-chain, treasury open, governance rails active.

A security-specialist agent registered on ERC-8004 discovers the mandate through the Orchestrator Agent's A2A card. It submits a membership proposal through AgentFightClub. Marco reviews the agent's on-chain profile — twelve prior audit deliveries, 94% acceptance rate — and votes to approve. The agent is now a guild member.

The Orchestrator delegates the audit task via a structured A2A task message: contract source, scope boundaries, acceptance criteria, deadline, and budget. The Specialist decomposes the task using GLM-5.1's long-horizon planning, runs static analysis, writes the audit report, and creates an EAS attestation of the SHA-256 deliverable hash on Base mainnet — embedding the attestation UID in the A2A result message. The result arrives back to the Orchestrator via A2A. Marco reviews the report, accepts the deliverable, and AgentFightClub's `settle()` releases the treasury funds to the Specialist Agent's wallet. The agent's ERC-8004 profile gains a new delivery record: task type, deliverable hash, acceptance timestamp, payment amount, guild address. The reputation is on-chain and portable to the next engagement.

---

## Why Web3 Is Necessary

| Without Web3 | With Web3 (GuildOS) |
|-------------|---------------------|
| Reputation is a database row on a platform | Portable on-chain record (ERC-8004) — readable by any future guild or employer |
| Payment depends on the platform releasing funds | Contract-enforced treasury (Moloch v3) — payment releases only on acceptance, not on trust |
| Mandate is a Notion doc anyone can edit | EAS attestation — cryptographically signed by the Specialist, timestamped, verifiable on Basescan and queryable on easscan |

Web3 makes these three properties enforceable at the protocol level, not the platform level.

---

## Why AI Is Necessary

| Without AI | With AI (GuildOS) |
|-----------|-------------------|
| Specialists are humans — sourcing takes weeks | Orchestrator queries ERC-8004 registry and returns a shortlist in seconds |
| Work execution requires human availability | Specialist Agent executes tasks autonomously via GLM-5.1 long-horizon planning |
| Context is lost between projects | A2A message log + on-chain delivery record creates a verifiable work trail |

GuildOS is an intersection problem: neither pure Web3 (DAO for humans) nor pure AI (platform-locked agent tool) — it requires both to close the coordination gap.

---

## Intersection Test

| Machine execution | Economic exchange | Permission control | Verifiable records |
|-------------------|-------------------|--------------------|--------------------|
| GLM-5.1 executes tasks autonomously | Shared treasury; payment on acceptance | Scoped wallets; human gates; AgentFightClub governance | EAS delivery attestation; ERC-8004 reputation; settlement tx |

All four dimensions present.
