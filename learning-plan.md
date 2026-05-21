# Personalized Learning Plan — Santiago

> Generated: 2026-05-20 | Cohort 0 | AI × Web3 School  
> Based on: [Handbook](https://aiweb3.school/en/handbook/) + program structure + learner profile  
> Updated: 2026-05-20 (v3 — corrected to official 5-week structure: 3-week bootcamp + 2-week hackathon)

---

## Overview

Santiago is strong on Web3 and an independent developer. This plan follows the official program structure: 3-week bootcamp (May 17 – June 7) + 2-week hackathon sprint (June 7 – June 14+). The emphasis is on filling AI/Agent gaps first, then applying them at the AI × Web3 intersection, then shipping a demo.

Estimated pace: **2–4 hours/day** · Total: ~5 weeks · Program: May 17 – June 14, 2026

---

## Week 1 — Bootcamp: AI and Web3 Foundations

*Goal: Build shared language across LLMs, prompts, agents, tool use, wallets, transactions, and smart contracts — connecting everything into one execution chain.*

| Day | Topic | Handbook Chapter(s) | Deliverable |
|---|---|---|---|
| Day 0 (today) | Setup | — | Repo, AGENTS.md, learning-plan, Sensei agent ✅ |
| Day 1 | LLM + Prompt | [LLM](https://aiweb3.school/en/handbook/llm.html), [Prompt](https://aiweb3.school/en/handbook/prompt.html) | Daily note + first experiment |
| Day 2 | Context + RAG | [Context](https://aiweb3.school/en/handbook/context.html), [RAG](https://aiweb3.school/en/handbook/rag.html) | Experiment: retrieval over on-chain data |
| Day 3 | Agent + Frameworks | [Agent](https://aiweb3.school/en/handbook/agent.html), [Frameworks](https://aiweb3.school/en/handbook/frameworks.html) | Vibe-code or Hermes agent practice run |
| Day 4 | MCP + Tool Use | [MCP](https://aiweb3.school/en/handbook/mcp.html) | Wire up a simple MCP tool call |
| Day 5 | Wallet + Transaction | [Wallet](https://aiweb3.school/en/handbook/wallet.html) (ref) | Create test wallet, make testnet transaction |
| Day 6 | Smart Contract basics | [Smart Contract](https://aiweb3.school/en/handbook/smart-contract.html) (ref) | Deploy or call a minimal contract on testnet |
| Day 7 | Week 1 wrap-up | — | Document successes, failures, human corrections; push to GitHub |

**Week 1 milestone:** One end-to-end chain — LLM prompt → agent tool call → wallet sign → testnet transaction → receipt

---

## Week 2 — Bootcamp: AI × Web3 Intersection Areas

*Goal: Enter the real problem space. Choose one track, map the full execution flow, produce a proposal.*

### Tracks (choose one by end of Day 8)

| Track | Core Question | Relevant Handbook Chapters |
|---|---|---|
| **Agentic Commerce / Payment** | Who initiates, executes, pays, verifies, and carries risk? | Machine Payment, Agent Wallet, Settlement & Escrow |
| **Dev Tooling** | How does AI accelerate on-chain dev workflows? | Agent Workflow, MCP, Evaluation |
| **AI Security / Privacy** | What breaks when an agent handles assets and private data? | AI Security, AI Privacy, Verifiable AI |
| **AI × Governance / Coordination** | Can agents propose, vote, and execute governance actions? | Agent Identity, Agent Trust, Verifiable AI |
| **Open Track** | Your own intersection | Mix as needed |

| Day | Topic | Handbook Chapter(s) | Deliverable |
|---|---|---|---|
| Day 8 | Chain-aware Context | [Chain-aware Context](https://aiweb3.school/en/handbook/chain-aware-context.html) | On-chain state injected into agent context |
| Day 9 | Web3 Tool Use | [Web3 Tool Use](https://aiweb3.school/en/handbook/web3-tool-use.html) | RPC / wallet / contract called by an agent |
| Day 10 | Agent Workflow | [Agent Workflow](https://aiweb3.school/en/handbook/agent-workflow.html) | Map automation vs. human-in-the-loop steps |
| Day 11 | Agent Wallet + Payment | [Agent Wallet](https://aiweb3.school/en/handbook/agent-wallet.html), [Machine Payment](https://aiweb3.school/en/handbook/machine-payment.html) | Spending limit or session key prototype |
| Day 12 | Agent Identity + Trust | [Agent Identity](https://aiweb3.school/en/handbook/agent-identity.html), [Agent Trust](https://aiweb3.school/en/handbook/agent-trust.html) | Authorization / responsibility tracking note |
| Day 13 | Track deep dive | Track-specific chapters | Draft project proposal (problem + flow + risk) |
| Day 14 | Proposal finalization | — | Written proposal ready for Week 3 → push to `hackathon/proposal.md` |

**Week 2 milestone:** One written proposal — who initiates, who executes, who pays, who verifies, who carries the risk

---

## Week 3 — Practice Deepening + Hackathon Kickoff

*Goal: Fill remaining gaps with targeted exercises, finalize hackathon team + direction, define demo plan.*

| Day | Focus | Exercises / Deliverables |
|---|---|---|
| Day 15 | Verifiable AI + AI Security | Verifiable execution record; prompt-injection isolation note |
| Day 16 | AI Privacy + Evaluation | User data / on-chain identity exercise; testable agent behavior |
| Day 17 | Gap fill (from Week 1–2 blockers) | Revisit anything unclear; file `handbook-feedback/` entries |
| Day 18 | Smaller exercises | Agent workflow + wallet confirmation, on-chain receipt, testnet payment, or governance proposal summary |
| Day 19 | Risk-control strategies | Risk-control write-up for your chosen track |
| Day 20 | Hackathon prep | Finalize: track, project topic, target users, technical path, roles, demo plan → `hackathon/kickoff.md` |
| Day 21 | Week 3 wrap-up | All gaps documented, hackathon plan committed and pushed |

**Week 3 milestone:** Hackathon plan committed: track + project topic + target users + technical path + roles + demo outline

---

## Weeks 4–5 — Hackathon Sprint + Demo Showcase

*Goal: Build the core implementation, test it, document it, and present it. Two full weeks to ship.*

### Week 4 — Build

| Day | Focus | Deliverable |
|---|---|---|
| Day 22 | Hackathon kickoff | Repo structure, task breakdown, team alignment (if applicable) |
| Day 23–24 | Core implementation | Working prototype in `experiments/` or dedicated folder |
| Day 25 | On-chain / tool-call integration | Contract calls, testnet txs, MCP tool logs wired into demo |
| Day 26 | Basic testing + README | README written, demo flow end-to-end working |
| Day 27 | Mentor / office-hour feedback | Incorporate feedback, adjust scope |
| Day 28 | Week 4 checkpoint | Mid-hackathon push — what's working, what's cut |

### Week 5 — Polish + Submit

| Day | Focus | Deliverable |
|---|---|---|
| Day 29–30 | Polish + edge cases | Stable demo, handle failure cases |
| Day 31 | Demo video recording | Short walkthrough video |
| Day 32 | Final submission prep | Project name, track, target user, problem def, demo link, repo, video |
| Day 33 | Buffer / overflow | Fix last blockers, finalize docs |
| Day 34 | Submit | Final submission on WCB before deadline |
| Day 35 | Demo showcase | Present — celebrate — collect feedback |

**Final submission checklist:**
- [ ] Project name + track
- [ ] Target user + problem definition
- [ ] Demo link
- [ ] GitHub repository + README
- [ ] Demo video
- [ ] Contract addresses / testnet addresses / transaction hashes (if applicable)

---

## Handbook Reference Chapters (use as needed)

Already strong on Web3 — return to these when intersection topics reference them:

Network · Cryptography · Wallet · Smart Contract · Account Abstraction · DeFi · Oracle · Indexing · Security

---

## Daily Minimum Path

Even on a short day (< 1 hour):

1. Skim one Handbook chapter
2. Write 3 bullets in `daily/YYYY-MM-DD.md`: what I read, what I didn't understand, what I want to try
3. Submit WCB check-in

## Recommended Path (2 hours)

1. Read one full chapter + take notes
2. Write `daily/YYYY-MM-DD.md` with check-in draft
3. Run one experiment or code snippet in `experiments/`
4. File one feedback item in `handbook-feedback/` if anything was unclear

## Challenge Path (4 hours)

1. Read + annotate chapter(s)
2. Complete a WCB task
3. Build an experiment touching real RPC / contract / agent
4. Push everything to GitHub
