# Week 1 Learning Summary

> **AI × Web3 School — Cohort 0**
> Days 1–7, May 20–27, 2026
> Estimated read time: ~5 minutes

---

## One AI Concept I Understood Differently

**Evaluation is a first-class engineering concern, not a post-hoc check.**

Before Week 1, I thought of model evaluation as something you do once — run a benchmark, pick the best model, move on. What the Evaluation chapter reframed for me is that evaluation is a continuous loop that has to be designed *before* building the system, not retrofitted afterward.

The key shift: a **golden set** of real tasks plus **regression tests** that re-run on every change turns evaluation into the same kind of discipline as a test suite in traditional software. Without it you're flying blind — a prompt change might improve one failure mode and silently introduce three others.

In an AI × Web3 context this matters even more: mistakes can affect on-chain assets, governance votes, and permission grants. There is no "undo" for a bad transaction submitted by an agent with a broken prompt. That stakes difference justifies treating evaluation as infrastructure from day one, not an afterthought.

The practical takeaway for my own work: before building any agent that touches a wallet or contract call, define the golden set first. What are the 10 cases it must get right? What are the 3 failure modes it must never trigger? Only then design the agent.

---

## One Web3 Concept I Understood Differently

**Account abstraction (ERC-4337) makes agents first-class signers.**

I was already familiar with account abstraction as a UX improvement — gasless transactions, social recovery, session keys. What I hadn't thought through carefully was what it means for *agents specifically*.

A standard EOA signer is binary: it either holds the private key or it doesn't. There's no way to say "this agent can call `swap()` on Uniswap with up to 0.1 ETH but cannot transfer ERC-20 tokens to external addresses." ERC-4337 session keys change this. An agent can be issued a scoped key with a validity window, a contract allowlist, and a value cap. The account abstraction layer enforces those constraints at the smart contract level — not just at the application level where they could be bypassed.

This is the real unlock for AI × Web3 systems: you can give an agent *real on-chain authority* without giving it *unlimited authority*. The trust boundary becomes programmable and auditable rather than informal and unenforceable.

The open question this raised for me: how tightly can session key permission predicates be scoped in practice, and is there a standard ABI for defining them — or is each smart account wallet doing something different?

---

## One AI × Web3 Crossover Finding

**The verification chain for an AI agent in a Web3 context has a clear six-layer structure — and most systems implement only the first two.**

While building the workflow diagrams (Agentic Commerce and Restricted Web3 Assistant), I tried to map every place where something could go wrong when an agent acts on-chain. The result was a six-layer model:

1. **Prompt layer** — is the intent correctly expressed to the model?
2. **Context layer** — is the state the agent sees accurate and current?
3. **Model layer** — does the model output the right action/parameters?
4. **Code layer** — does the transaction the code constructs match the model's intent?
5. **Guard layer** — does a pre-execution simulation catch failures before broadcast?
6. **Human layer** — for high-stakes actions, does a human confirm before submission?

Most demos and tutorials I've seen handle layers 1 and 3 (prompt + model), maybe add a guard (layer 5), and call it done. Layers 2, 4, and 6 are where real production failures happen: stale on-chain state fed into context, a correct intent turned into a malformed calldata, or an autonomous agent executing a governance vote without any human sanity check.

The insight is that building an AI × Web3 system is really about making all six layers explicit and deciding *which ones* require automation, which require human confirmation, and which need on-chain enforcement. That framing is more useful than any specific framework or tool.

---

## Proof-of-Work Highlights

**Knowledge base built from scratch.** Starting from the raw Handbook chapters, I built a wiki of ~150 interlinked concept pages (`knowledge-base/AIxWeb3/wiki/`) using an incremental builder skill that processes only changed sources. The wiki became the reference layer for everything else — concept cards, quiz questions, and chapter reviews all draw from it.

**Two concept card decks.** Generated using the `/concept-cards` skill: 37+ cards for AI Foundations and 55 cards for Web3 Foundations. Each card has a one-sentence definition, a concrete example, and a boundary that captures the most common misconception. These are the fastest way to review a concept before a quiz or WCB check-in.

**On-chain exercises completed.** Interacted with a Sepolia testnet (WETH wrap via Uniswap, TX `0x72282...382b0`) and deployed a custom smart contract (`CheckInManager.sol` at `0x4D76e3...475b5` on Sepolia) that stores learning commit hashes on-chain. Both verified on Etherscan and Sourcify.

**Interactive quiz artifact.** Built a full quiz skill (`skills/quiz/SKILL.md`) that reads the wiki, selects a random uncovered concept, generates 5 factual multi-choice questions, runs an interactive session via in-chat widgets, and maintains a 72-hour spaced-repetition cache. Running on a Cowork scheduled task every 2 hours (10am–10pm). As of this writing: 9 concepts covered, cache resets May 29.

**Workflow diagrams.** Designed and built two swimlane diagrams: an Agentic Commerce workflow (Human Operator → Requester Agent → Data Provider Agent → On-chain/L2, 9 steps) and a Restricted Web3 Assistant workflow (read-only chain access + human confirmation gate for writes). Both are exported as SVG and available in `tasks/`.

---

## One Unresolved Question / Next Direction

**How do you build a memory layer for an AI × Web3 agent that is both persistent and auditable?**

The Long-term Memory session (watched May 26) made the case for agents that build continuity across sessions — remembering user preferences, past decisions, and context that would otherwise have to be re-established every conversation. That's the standard application-layer answer.

But in a Web3 context, there's an extra requirement: the memory layer should be auditable. If an agent made a governance vote or approved a transaction based on its "memory" of a past decision or user preference, that reasoning should be inspectable — not just by the user, but potentially by other parties (co-signers, a DAO, a compliance layer).

This topic feels like is going to be touched in more detail in the `chain-aware context` chapter in Week 2 and is something I want to explore in more detail.

---

## Looking Ahead

Week 2 focus: AIxWeb3 bridge and how things connect around Chain-aware Context, Web3 Tool Use, and the Agentic Commerce / AI Security tracks. This week should me more a hands-on session learning so I'm really looking forward to it.

Full proof-of-work evidence: [submissions/Week1-PoW.md](./Week1-PoW.md)

---
