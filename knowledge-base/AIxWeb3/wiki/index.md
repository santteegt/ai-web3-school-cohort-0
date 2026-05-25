# Wiki Index

_Last updated: 2026-05-24 — 75 pages (68 concept/topic + 11 source)_

---

## Topics (Overview Pages)

- [[ai-foundations-overview]] — Full map of AI Foundations concepts: LLM, Prompt, Context, RAG, Agent, Frameworks, MCP
- [[ai-frameworks-overview]] — Framework selection, LangChain/LangGraph/DSPy/Hermes comparison, three-layer responsibility model
- [[aixweb3-bridge-overview]] — The intersection layer: where AI agents meet on-chain systems
- [[frontier-exploration-overview]] — Hackathon tracks: Agentic Commerce, Wallet/Permission, AI Security, Governance, Dev Tooling

---

## Sources

- [[sources/ai-fundamentals-introduction]] — Module A bootcamp notes: LLM basics, control layers, agent components
- [[sources/llms]] — LLMs mental model: tokens, embeddings, transformers, hallucination
- [[sources/context]] — Context as information governance: five-layer model, context engineering
- [[sources/prompt]] — Prompt as communication protocol: four-segment structure, security principles
- [[sources/rag]] — RAG as evidence chain: chunking, vector DB, retrieval, citations
- [[sources/aixweb3-school]] — Handbook outline: four-layer learning map
- [[sources/program-structure]] — Four-week bootcamp structure and deliverables
- [[sources/agent]] — Agent as constrained execution loop: planning, state, reflection, AI × Web3 architecture
- [[sources/frameworks]] — Framework selection, LangChain/LangGraph/OpenAI SDK/DSPy/Hermes, learning agents
- [[sources/mcp]] — MCP architecture: client/server split, tool schemas, permission model
- [[sources/vibe-coding]] — AI coding as disciplined human-AI iteration; engineering discipline requirements

---

## Concepts — AI Foundations: LLM

- [[large-language-model]] — Probabilistic text generator; reasoning layer, not truth source
- [[tokens]] — Processing unit; affects context capacity, cost, and completeness
- [[embeddings]] — Semantic vector representations; good for retrieval, not correctness judgments
- [[transformer-architecture]] — Attention-based architecture; pattern composition without ground-truth authority
- [[hallucination]] — Confident fabrication; requires external verification, not just better prompts
- [[multimodal]] — Models processing text, images, audio, and video
- [[maas]] — API-based model access; per-token billing, no GPU required

---

## Concepts — AI Foundations: Context

- [[context-window]] — Token-bounded working memory; longer ≠ better focus
- [[context-engineering]] — Designing what information enters the model at the right layer
- [[five-layer-agent-context]] — Instruction / Task / Fact / Knowledge / Memory layers
- [[information-governance]] — Labeling context by source, freshness, permission, trust level
- [[agent-memory]] — Cross-session persistence; must be revocable; cannot replace authorization
- [[knowledge-base]] — External knowledge repository; requires source, version, deprecation tracking

---

## Concepts — AI Foundations: Prompt

- [[prompt-design]] — Interface between user and model; executable communication protocol
- [[instruction]] — Task rule for model: role, goal, prohibitions, uncertainty, format
- [[four-segment-prompt]] — Task Goal / Available Inputs / Prohibited Behaviors / Output Format
- [[four-control-layers]] — Context window, system instructions, prompt, tool calling
- [[few-shot-prompting]] — Example-based guidance; carries maintenance cost
- [[structured-output]] — Schema-constrained output; makes LLM output machine-processable
- [[prompt-injection]] — Adversarial content overriding system instructions; defense via zone isolation
- [[verification-chain]] — Six-layer defense: prompt → context → model → code → guard → human

---

## Concepts — AI Foundations: RAG

- [[retrieval-augmented-generation]] — Evidence chain: retrieve, filter, cite, bound answers to sources
- [[chunking]] — Document splitting; preserve source URL, heading path, version per chunk
- [[vector-database]] — Embedding storage + metadata; filter first, then rank
- [[retriever]] — Candidate selection; hybrid approaches outperform pure vector search
- [[re-ranking]] — Post-retrieval quality ordering; adds latency/cost tradeoff
- [[citations]] — Source traceability; user verification entry point

---

## Concepts — AI Foundations: Agent

- [[ai-agent]] — Constrained execution loop: goal, tools, state, permissions, stop conditions _(updated)_
- [[prompt-workflow-agent-boundary]] — Three architectures with different failure modes
- [[tool-calling]] — Model-to-world action mechanism; requires tool design discipline _(updated)_
- [[state-management]] — Externalized, queryable, recoverable, auditable agent state _(updated)_
- [[agent-planning]] — Candidate plan generation; step classification as read/write; not an authorization
- [[agent-reflection]] — Self-checking for intermediate correction; not a substitute for deterministic checks
- [[agent-stop-conditions]] — Explicit halting criteria: goal reached, budget exceeded, risk crossed
- [[multi-agent-systems]] — Coordination patterns; amplifies failures when roles are unclear
- [[mcp]] — Unified tool connectivity protocol; client/server architecture _(updated)_
- [[mcp-server]] — Exposes resources, tools, prompts; defines permission model
- [[mcp-client]] — Connects model to servers; handles discovery, confirmation, session isolation
- [[tool-schema]] — Machine-readable tool declaration; vague schemas cause wrong-parameter calls
- [[mcp-permission-model]] — Permission design per tool risk level; the most underestimated MCP issue
- [[guardrails]] — Hard execution constraints; code-enforced, not prompt-enforced
- [[agent-handoff]] — Control transfer after subtask completes
- [[ai-agent-tracing]] — Execution chain observability; debugging and audit
- [[maas]] — API-based model access; per-token billing, no GPU required
- [[vibe-coding]] — AI-assisted rapid prototyping; requires engineering discipline _(updated)_
- [[ai-coding]] — AI coding in the full engineering flow: issue → branch → commit → test → review → merge

---

## Concepts — AI Foundations: Frameworks

- [[ai-frameworks-overview]] — Selection criteria, three-layer responsibility model
- [[langchain]] — Component library for composing AI capabilities; good for prototyping
- [[langgraph]] — DAG-based stateful workflows; reference for explicit state management
- [[openai-agents-sdk]] — Agent engineering primitives: handoffs, guardrails, tracing, structured output
- [[dspy]] — Metric-driven prompt optimization; treats pipelines as optimizable programs
- [[hermes]] — Tool-calling and structured-output oriented model ecosystem
- [[learning-agents]] — Systems that improve via evaluation loop, not direct online behavior change

---

## Concepts — AI × Web3 Bridge

- [[chain-aware-context]] — Live on-chain state in agent context
- [[web3-tool-use]] — RPC, wallet, contract tools called by agents
- [[agent-workflow]] — Automation boundaries and human-in-the-loop design
- [[agent-wallet]] — Delegated permissions, spending limits, revocation
- [[machine-payment]] — Autonomous micro-payments and on-chain settlement
- [[agent-identity]] — Agent identification, authorization, accountability
- [[verifiable-ai]] — Proving model outputs and execution processes
- [[ai-security]] — Prompt injection defense, tool abuse prevention, permission isolation
- [[aixweb3-agent-architecture]] — 8-step reference pattern: goal → plan → read/write split → policy → simulation → confirmation → execution → log
