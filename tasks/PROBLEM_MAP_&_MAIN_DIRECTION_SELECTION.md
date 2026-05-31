
# AIxWeb3 - Problem Map and Main Direction Selection

Prior to deciding on the main direction I will choose to dive deep and build something, I asked my learning agent to help me draw a mental model around all the topics covered in the AIxWeb3 Bridge module of the handbook so I can fully understand how the 6 main modules interact with each other when an AI×Web3 agent acts on a user intent (See [report](/knowledge-base/AIxWeb3/concepts/aixweb3-bridge-mental-model.md)).

With this foundation and the help of the knowledge base I've been building during my learnind journey, I then asked the agent to map the AI×Web3 problem space by covers the core 5 foundational directions in this cross-domain scenario. That was useful to then describe the role that AI and Web3 mechanisms independently play in each direction and why both domains are required for building that direction. See the [HTML diagram](tasks/AIxWeb3-problem-map.html) and a [summary report](tasks/AIxWeb3-problem-map.md) for details.

with that in mind, I chose the following directions

## Identity / Reputation / Capability / Interoperability

I merged both directions into a **main track** as I see them very interrelated, not only in terms of standards and tooling but also as fields that need from each other in order to serve its purpose: capabilities cannot be discovered without identity, interoperability cannot be safely invoked without verifying reputation.

![main_direction](assets/direction_main.png)

### Identity / Reputation

#### AI Role

> Understands what agents can do and how well. Parses capability manifests, matches services to user goals via semantic search, evaluates task quality for reputation scoring, and detects behavioral anomalies across delivery records.

#### Web3 Mechanism

> Makes identity and reputation portable and tamper-proof. DIDs/Verifiable Credentials, ERC-8004 on-chain agent registry, EAS attestations, immutable task delivery records, and stake/slashing for reputation enforcement.

#### Why both are required

> **AI** \
> Web3 can store attestations on-chain, but cannot evaluate the semantic meaning of capability claims, judge task quality, or match an agent's profile to a user's intent. A registry without understanding is just a phone book.

> **Web3** \
> AI can infer reputation from behavior patterns, but those inferences aren't portable or verifiable across systems. Without Web3, reputation lives in one platform's database and disappears when the platform changes.

### Capability / Interoperability

#### AI Role

> Orchestrates across agents and tools. Translates between capability formats (MCP, A2A), composes multi-agent workflows, maps natural language goals to structured tool calls, and resolves which combination of capabilities satisfies a user intent.

#### Web3 Mechanism

> Provides open, trustless discovery and invocation. On-chain capability registries (ERC-8004), standardized agent-to-agent protocols (A2A), payment for capability access (MPP), and open provenance records for auditable cross-agent invocations.

#### Why both are required

> **AI** \
> Web3 can register capabilities in an open registry, but cannot plan which capabilities to combine for a given goal, resolve ambiguity, or handle errors gracefully across service calls. Composition requires reasoning, not just lookup.

> **Web3** \
> AI can orchestrate agents, but without open registries and payment primitives there's no trustless discovery or economic incentive for third-party agents to expose capabilities. Multi-agent systems collapse into closed ecosystems.

## Governance / Coordination

On user-agent and agent-agent systems, coordination is crucial, and requires proper interoperability and agent identity to makes things work. I want to dig deeper into multi-agent and user-agent scenarios during the course, so I chose this as the secondary direction.

![alt text](assets/direction_secondary.png)


### Governance / Coordination

#### AI Role

> Reduces information overload and surfaces actionable structure. Summarizes proposals, extracts meeting action items, models budget impact, synthesizes community sentiment, and tracks contribution records — but cannot make value judgments, approve budgets, or replace community deliberation.

#### Web3 Mechanism

> Makes governance binding, transparent, and auditable. On-chain voting (Snapshot, Governor), transparent treasury execution, verifiable contribution records, DAO coordination primitives, and immutable decision logs that prevent retroactive revision of who voted for what.

#### Why both are required

> **AI** \
> Web3 can record votes and execute treasury transfers on-chain, but cannot synthesize complex proposals into accessible summaries, reduce participation fatigue, or help communities understand the downstream implications of a governance decision.

> **Web3** \
> AI can summarize proposals and suggest actions, but without Web3 there is no way to make those decisions binding, tamper-proof, or trustlessly executable. AI governance without on-chain enforcement is just a well-organized Notion doc.

---

## Side-by-side comparison

| | Identity / Capability (Main) | Governance (Secondary) |
|---|---|---|
| Real user | Agent developer/user composing multi-agent systems | DAO contributor (user or agent) managing information overload |
| AI necessity | Semantic matching — registries can't infer meaning | Synthesis at scale — humans can't read every thread |
| Web3 necessity | Portable, tamper-proof reputation + open registries | Binding, verifiable decisions + transparent execution |
| Build form | Developer tooling → product demo | Product demo |
| Minimal proof | Query a registry, rank agents by capability + trust score | Ingest Snapshot + forum, output structured governance brief |
| Hardest risk | Stale or gamed reputation data | AI output being mistaken for authoritative decision |

---

## Direction Evaluation Matrix

> Applied from the AI × Web3 School Handbook — Problem Space & Direction Map framework.  
> Five criteria used to validate whether a direction is worth pursuing in depth and building toward a Hackathon proposal.

---

### Main Track — Identity / Reputation / Capability / Interoperability

#### Structural Demand

**Verdict: Strong — long-term, infrastructure-level demand.**

The problem is not tied to any single project cycle. Every multi-agent system — regardless of which LLM framework, chain, or deployment model is in use — faces the same underlying question: *how do I know which agent to call, whether it can actually do what it claims, and whether I should trust it based on past behavior?* As agent ecosystems grow more heterogeneous (MCP servers, A2A agents, on-chain execution environments, third-party capability providers), the discovery and trust problem compounds. The structural demand predates any specific hot project and will persist as long as agents are composed from heterogeneous, third-party sources — which is the architectural direction the industry is clearly moving toward.

**Countercheck:** Would this problem disappear if a dominant agent marketplace (e.g., an OpenAI agent store) wins? Partially — but only within that closed ecosystem. The open, cross-platform version of the problem (agents from different providers, chains, and frameworks composing trustlessly) would still exist and would be the more valuable infrastructure to address.

#### Verifiability

**Verdict: High — multiple validation paths available at different levels of effort.**

- **Flowchart / diagram**: A capability discovery and trust-scoring flow can be mapped in one session (already partially done via the mental model and problem map).
- **Reference implementation**: Query an existing ERC-8004-compatible registry (or mock one), apply semantic matching against a user goal, return a ranked shortlist with a trust score derived from on-chain delivery records. This is a self-contained demo that validates the core value proposition.
- **Transaction records**: On-chain attestations (EAS), registry reads, and delivery log references all produce verifiable artifacts.
- **User interviews**: An agent developer integrating third-party tools is the clearest user — asking them "how do you currently discover and evaluate agents?" would surface the pain quickly.

The direction passes the verifiability test at every level: paper, code, and on-chain evidence.

#### Minimal Entry Point

**Verdict: Clear — buildable within one week at proof-of-concept level.**

The interface layer above ERC-8004/A2A is the entry point, not the standards themselves. A minimal prototype can:
1. Read or mock an on-chain agent registry (ERC-8004 schema)
2. Accept a natural language user goal as input
3. Semantically match the goal against registered capability manifests
4. Return a ranked shortlist annotated with a trust score derived from available on-chain attestations (EAS) or mock delivery records

This does not require deploying a new standard or writing a new smart contract — the registry and attestation infrastructure exists. The week-one deliverable is the matching and scoring logic, which can be written in Python or TypeScript with an LLM call and a few JSON-RPC reads. A repo skeleton, flowchart, and one working query are sufficient to validate the concept before Hackathon week.

#### Risk Boundaries

**Verdict: Present but manageable — identity and reputation data are the primary risks, not funds or keys.**

This direction does involve sensitive system concerns:
- **Identity claims**: A malicious agent could publish false capability claims to a registry. The risk is misrouting tasks to unqualified or adversarial agents, not direct fund loss.
- **Reputation gaming**: Sybil attacks on reputation systems (fake delivery records, self-attestation loops) are a known hard problem. The mitigation is stake/slashing (economic cost to fake reputation) and third-party attestations — both of which the ERC-8004/EAS stack supports.
- **No private keys or funds in the minimal entry point**: The initial developer tooling layer (semantic matching + trust scoring) is read-only. It does not require wallet signing or asset transfers. This keeps the risk surface low for the prototype phase.

The direction does **not** require handling private keys, transaction signing, or funds at the layer being targeted for the Hackathon. Risk escalates only if the scope expands to include on-chain registration writes or payment-for-capability flows — both of which are extensions, not core requirements.

#### Follow-Through

**Verdict: Excellent — feeds directly into Week 3 proposal, Hackathon build, and long-term reference material.**

- **Week 3 proposal**: The problem breakdown (stakeholders, flow, AI role, Web3 mechanism, automation boundaries) is already partially scaffolded. A full proposal can be written from the existing direction selection document in one session.
- **Hackathon challenge**: The minimal prototype (agent discovery + trust scoring) is a standalone Hackathon deliverable. Extensions (on-chain registration, payment-for-capability, governance integration via the secondary track) are natural Week 4–5 additions.
- **Handbook / research backlog**: The capability matching and reputation scoring design questions are open enough to generate handbook feedback entries, a reference implementation writeup, and potentially a contribution to the ERC-8004 or A2A discussion. Long-term research value is high.
- **Secondary track integration**: The Governance direction connects naturally — agent identity and reputation are prerequisites for multi-agent coordination and on-chain governance participation. The main and secondary tracks reinforce rather than compete.

---

### Secondary Track — Governance / Coordination

#### Structural Demand

**Verdict: Solid — participation fatigue is a chronic, not cyclical, problem.**

DAO governance participation rates have been declining since 2021 across most major protocols, independent of market cycles. The root cause is persistent: governance proposals are long, technical, and numerous; participants lack the time and context to evaluate each one; and abstention is the path of least resistance. This is a structural information asymmetry problem, not a temporary one caused by a specific bull or bear market. AI-assisted synthesis directly addresses the root cause. The Web3 mechanism (binding on-chain votes, transparent treasury) provides the enforcement layer that makes AI-assisted summaries actionable rather than advisory.

**Countercheck:** Would better UX alone (e.g., Snapshot improvements) solve this? No — better UX reduces friction but does not reduce the cognitive load of evaluating complex proposals. The synthesis and summarization layer requires AI.

#### Verifiability

**Verdict: High — the demo output is self-evident.**

A governance brief agent produces an output (structured summary + action items + vote record links) that any DAO participant can immediately evaluate for accuracy against the source forum posts and Snapshot proposals. Validation requires no special tooling: a reader can compare the brief against the original thread and judge whether the summary is accurate, balanced, and actionable. Transaction records (on-chain vote history, treasury execution logs) provide ground truth for the Web3 side. A reference implementation can be tested against any live DAO with public Snapshot data.

#### Minimal Entry Point

**Verdict: Very low barrier — can prototype with existing public APIs in a few hours.**

- Snapshot has a public GraphQL API — no authentication required to read proposals, votes, and spaces.
- Governance forums (Commonwealth, Discourse) are publicly readable.
- The minimal prototype: ingest a Snapshot space → summarize the top active proposals → output a structured brief with summary, for/against arguments, vote deadline, and a link to the on-chain record.

No smart contract deployment required. No wallet integration at the prototype stage. The entire initial build runs on LLM + Snapshot API + a structured output template. This is the lowest barrier to a working demo of any direction in the problem map.

#### Risk Boundaries

**Verdict: Well-defined and bounded — the hard constraint is also the clearest design spec.**

The primary risk is explicit and well-understood: AI output being mistaken for an authoritative governance recommendation, leading participants to vote without reading the source material. This risk is addressed by design: every AI-generated brief must link to primary sources, include uncertainty markers, and carry a clear disclaimer that the summary is an input to deliberation, not a substitute for it.

Other risks:
- **Selective summarization**: AI may over- or under-represent certain arguments. Mitigation: structured output format that requires capturing both sides of every proposal.
- **Stale data**: Governance forums update continuously. Mitigation: timestamp every summary and link to the live source.

No private keys, funds, or irreversible actions are involved at any stage of this direction. The governance execution layer (treasury transfers, on-chain votes) is read-only from the agent's perspective — the agent surfaces and summarizes; humans vote and execute.

#### Follow-Through

**Verdict: Good as secondary — complements the main track without competing for scope.**

- **Week 3 / Hackathon**: A governance brief agent is a standalone demo with clear user value. It can be scoped to a single DAO and a single session's worth of proposals without losing the demonstration of both AI and Web3 roles.
- **Integration with main track**: Agent identity and reputation (main track) are natural prerequisites for multi-agent governance coordination. An agent participating in governance on behalf of a user needs a verifiable identity (ERC-8004) and a trust score that participants can inspect before accepting its summaries. This makes the secondary track a natural extension of the main track rather than a separate thread.
- **Long-term research value**: The governance direction raises open questions (where is the AI/human deliberation boundary? how should AI-generated governance briefs be attributed on-chain?) that feed into handbook feedback and research backlog entries.

---

### Evaluation Summary

| Criterion | Identity / Capability (Main) | Governance (Secondary) |
|---|---|---|
| **Structural demand** | ✅ Infrastructure-level, pre-dates hot projects | ✅ Chronic participation fatigue, not cyclical |
| **Verifiability** | ✅ Demo, flowchart, on-chain records, user interviews | ✅ Self-evident output, public Snapshot data |
| **Minimal entry point** | ✅ Read-only registry + LLM matching, week-one build | ✅ Snapshot API + LLM, few-hour prototype |
| **Risk boundaries** | ✅ Read-only prototype; no keys or funds at entry layer | ✅ No keys or funds; hard constraint writes the spec |
| **Follow-through** | ✅ Week 3 proposal, Hackathon build, standards backlog | ✅ Standalone demo + natural extension of main track |

Both directions pass all five criteria. The main track scores higher on follow-through depth and standards contribution potential; the secondary track scores higher on entry point speed and demo clarity. Together they form a coherent scope: **open agent discovery and trust** (main) + **AI-assisted governance coordination** (secondary, as an applied scenario that uses the main track's identity/reputation layer).

---