# Week 1 Proof-of-Work Pack

> **AI × Web3 School — Cohort 0**
> [GitHub Repo](https://github.com/santteegt/ai-web3-school-cohort-0)
> Covering: Days 1–7 (May 20–26, 2026)

---

## 1. Learning Repository

**Repository:** https://github.com/santteegt/ai-web3-school-cohort-0

The repo is the single source of truth for all Week 1 learning work: daily notes, raw chapter notes, the structured wiki, concept card decks, experiments, workflow diagrams, and the custom learning agent setup.

---

## 2. Handbook Coverage — AI Foundations

All 8 AI Foundations chapters read and summarised in the wiki knowledge base.

| Chapter | Raw Notes | Wiki Concept Page(s) |
|---|---|---|
| LLM | `knowledge-base/AIxWeb3/raw/LLM.md` | `wiki/llm.md`, `wiki/token-prediction.md`, `wiki/temperature.md` |
| Prompt Engineering | `knowledge-base/AIxWeb3/raw/Prompt Engineering.md` | `wiki/prompt-engineering.md`, `wiki/chain-of-thought.md`, `wiki/few-shot-learning.md` |
| Context | `knowledge-base/AIxWeb3/raw/Context.md` | `wiki/context-window.md`, `wiki/context-injection.md`, `wiki/retrieval-augmented-generation.md` |
| RAG | `knowledge-base/AIxWeb3/raw/RAG.md` | `wiki/retrieval-augmented-generation.md`, `wiki/vector-database.md`, `wiki/embedding.md` |
| Agent | `knowledge-base/AIxWeb3/raw/Agent.md` | `wiki/agent-loop.md`, `wiki/tool-calling.md`, `wiki/multi-agent-systems.md` |
| Frameworks | `knowledge-base/AIxWeb3/raw/Frameworks.md` | `wiki/langchain.md`, `wiki/langgraph.md`, `wiki/hermes.md` |
| MCP | `knowledge-base/AIxWeb3/raw/MCP.md` | `wiki/mcp-permission-model.md`, `wiki/mcp-server.md`, `wiki/tool-calling.md` |
| Evaluation | `knowledge-base/AIxWeb3/raw/Evaluation.md` | `wiki/evaluation-harness.md`, `wiki/golden-set.md`, `wiki/llm-as-judge.md` |
| Fine-tuning | `knowledge-base/AIxWeb3/raw/Fine Tuning.md` | |
| Inference | `knowledge-base/AIxWeb3/raw/Inference.md` | |

---

## 3. Handbook Coverage — Web3 Foundations

All 9 Web3 Foundations chapters skimmed and wiki updated with concept pages on May 25.

Chapters: Cryptography · Wallet · Smart Contract · Dev Stack · Network · Account Abstraction · DeFi · Oracle · Indexing · Security

Raw notes: `knowledge-base/AIxWeb3/raw/Web3 Foundations.md` (skimmed, May 25)

---

## 4. Concept Card Decks

Built and maintained using the `/concept-cards` [skill](/.claude/skills/concept-cards/SKILL.md).

### AI Foundations Deck
- **Marp source:** `knowledge-base/AIxWeb3/concepts/concepts-ai-fundamentals.md`
- **HTML export:** [concept-cards-ai-fundamentals.html](/submissions/concept-cards-ai-fundamentals.html)
- **Coverage:** 37+ concept cards across LLM, Prompt, Context, RAG, Agent, Frameworks, MCP, Evaluation, Fine-tuning, Inference chapters
- Each card: one-sentence explanation · concrete example · boundary / misconception

### Web3 Foundations Deck
- **Marp source:** `knowledge-base/AIxWeb3/concepts/concepts-web3-fundamentals.md`
- **HTML export:** [concept-cards-web3-fundamentals.html](/submissions/concept-cards-web3-fundamentals.html)
- **Coverage:** 55 concept cards across all 9 Web3 Foundations chapters

---

## 5. Wiki Knowledge Base

Built and maintained using the `/wiki-build` [skill](/.claude/skills/wiki-builder/SKILL.md).

- **Wiki index:** `knowledge-base/AIxWeb3/wiki/index.md`
- **Total pages:** ~150 (134 concept + 16 source summary pages)
- **Build log:** `knowledge-base/AIxWeb3/wiki/log.md`
- **Hash tracking:** `knowledge-base/AIxWeb3/wiki/.hashes.json` (incremental — only reprocesses changed sources)

Concepts are interlinked via `[[wikilinks]]`. Each concept page contains: definition, key properties, concrete example, boundary, related concepts, and source references.

---

## 6. Learning Agent Setup (Sensei / Claude via Cowork)

Evidence of AI tool usage throughout the learning journey.

| Artifact | Description |
|---|---|
| `AGENTS.md` | Agent rulebook: role, learner profile, daily flow, git conventions, WCB API usage, memory sync rules |
| `CLAUDE.md` | Symlink → AGENTS.md (auto-read by Claude Code and Cowork) |
| `tools/wcb_client.py` | WCB Agent API CLI — stdlib only, fetches tasks/events/check-in status |
| `skills/quiz/SKILL.md` | Interactive quiz skill: wiki-based, spaced-repetition cache, 5 questions per session with widget UI |
| `.claude/skills/wiki-builder/SKILL.md` | Incremental wiki builder skill |
| `.claude/skills/concept-cards/SKILL.md` | Marp concept card generator skill |
| `logs/quiz-cache.json` | Spaced-repetition cache — 9 topics covered, resets May 29 |
| `prompts/INTERACTIVE_LEARNING_ARTIFACT.md` | Full design log for the quiz artifact build |
| `submissions/LEARNING_AGENT_SETUP_EVIDENCE.md` | Screenshots of agent setup, successful outputs, manual review |

**Cowork scheduled task:**

- Everyday a morning kickoff, evening review and night warning prograss check-in tasks are scheduled.
- Quiz runs automatically every 2 hours (10am–10pm daily) via cron `0 10,12,14,16,18,20,22 * * *`.

---

## 7. Web3 On-Chain Exercises

### 7.1 Testnet Transaction (Sepolia)
- **Task file:** [TESTNET_TX.md](/tasks/TESTNET_TX.md)
- **Action:** Called `deposit()` on WETH contract — wrapping 0.0001 ETH via Uniswap on Sepolia testnet
- **TX Hash:** `0x72282192c26231258ff6cb438868f1c66276ca452f3475e4cc69a0dd3d6382b0`
- **Etherscan:** https://sepolia.etherscan.io/tx/0x72282192c26231258ff6cb438868f1c66276ca452f3475e4cc69a0dd3d6382b0
- **Wallet tool:** MetaMask

### 7.2 Smart Contract Deployment & Execution (Sepolia)
- **Task file:** [SMART_CONTRACT.md](/tasks/SMART_CONTRACT.md)
- **Contract:** `CheckInManager.sol` — stores learning commit hashes on-chain (mapping: address → block number → commit hash)
- **Source:** `experiments/CheckInManager.sol`
- **Contract Address:** `0x4D76e3f498324Da200694b0865f5545E678475b5`
- **Sourcify Verification:** https://repo.sourcify.dev/11155111/0x4D76e3f498324Da200694b0865f5545E678475b5
- **Deployment TX:** `0xedb9e134cf6865c044169b1deccece705c1d2932b8bdbc5b3113261da8e234fd`
- **Write TX (submitCommit):** `0xb44a06975ac79ab1079b9bbc1f1d0b63228f1455374b0a1627faee8c49b91492`

---

## 8. AI × Web3 Crossover Work

### 8.1 Agentic Commerce Workflow Diagram
- **Diagram (SVG):** [agentic-commerce-workflow.svg](/tasks/agentic-commerce-workflow.svg)
- **Report file:** [AIxWeb3_WORKFLOW.md](/tasks/AIxWeb3_WORKFLOW.md)
- **What it shows:** Full agentic commerce swimlane — 4 actors (Human Operator, Requester Agent, Data Provider Agent, On-chain/L2), 9 sequential steps, risk annotations at payment and settlement stages, verification chain (simulation → receipt → post-execution state check)

### 8.2 Restricted Web3 Assistant Workflow
- **Diagram (SVG):** [restricted-web3-assistant-workflow.svg](/tasks/restricted-web3-assistant-workflow.svg)
- **Report:** [RESTRICTED_WEB3_ASSISTANT_WORKFLOW.md](/tasks/RESTRICTED_WEB3_ASSISTANT_WORKFLOW.md)
- **What it shows:** A scoped AI assistant that can read on-chain state and explain transactions but requires human confirmation before any write action — 6-layer verification model (prompt → context → model → code → guard → human)

---

## 9. Daily Learning Notes

| Day | Date | File | Focus |
|---|---|---|---|
| Day 1 | May 20 | `daily/2026-05-20.md` | LLM chapter + repo setup |
| Day 2 | May 21 | `daily/2026-05-21.md` | Prompt Engineering + Context |
| Day 3 | May 22 | `daily/2026-05-22.md` | RAG + Agent chapters |
| Day 4 | May 23 | `daily/2026-05-23.md` | Frameworks + Vibe Coding (session replay) |
| Day 5 | May 24 | `daily/2026-05-24.md` | MCP + wiki build + concept cards |
| Day 6–7 | May 25 | `daily/2026-05-25.md` | Evaluation + Fine-tuning + Inference + Web3 skim |
| Day 8 prep | May 26 | `daily/2026-05-26.md` | Long-term Memory session + quiz artifact build |
| Day 9 wrap-up | May 27 | `daily/2026-05-27.md` | AixWeb3 Workflow diagrams + final reports |

---

## 10. Open Questions & Blockers

1. **Memory benchmarking** — Are third-party graph-based memory plugins (e.g., Mem0, Zep) meaningfully better than plain-text memory engines for agent continuity? What benchmark frameworks exist for evaluating a custom memory layer?

2. **ERC-4337 session key scope** — How tightly can session key permissions be scoped in practice? Is there a standard ABI for permission predicates, or is it wallet-implementation-specific?

3. **On-chain audit trail for inference** — The Inference chapter states that AI × Web3 systems should leave auditable records. What is the minimal viable pattern for this — log hash to a contract, use a ZK proof, or rely on a trusted execution environment?

4. **MCP permission granularity** — The MCP permission model chapter describes scoped tool access, but how does revocation work in practice for long-running agent sessions? Is there a session-level revocation primitive?

5. **LLM-as-judge bias in Web3 contexts** — Standard LLM-as-judge evaluation can miss domain-specific failure modes (e.g., a model that correctly explains a transaction but gets the risk level wrong). What evaluation patterns are specific to Web3 agent outputs?

---
