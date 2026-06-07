# Week 3 Proof-of-Work Pack

> **AI × Web3 School — Cohort 0**
> [GitHub Repo](https://github.com/santteegt/ai-web3-school-cohort-0)
> Covering: Days 15–21 (June 1–7, 2026)
> Track: Hackathon Pre-Sprint — Deep Explorations + Week 4 Ready Pack

---

## Part 1 — Week 3 Deep Explorations

Week 3 was focused entirely on pre-hackathon technical due diligence. Every component in the GuildOS stack was researched in depth: API availability, version mismatches, integration risks, and fallback plans were mapped before writing a single line of build code. The synthesis lives in [`hackathon/research/DEEP_RESEARCH.md`](../hackathon/research/DEEP_RESEARCH.md).

---

### 1. Component Research — Stack Validation

Eight individual deep-dive analyses were produced, one per component. Each analysis covers: what problem the component solves, what it does and does not cover, known gotchas, integration risks, and Day 1 validation steps.

| Component | Risk rating | Analysis document | Key finding |
|---|---|---|---|
| **AgentFightClub (Moloch v3)** | 🟡 MEDIUM | [`AGENTFIGHTCLUB_ANALYSIS.md`](../hackathon/research/AGENTFIGHTCLUB_ANALYSIS.md) | Command names differ from proposal (`launch` → `summon`, `settle()` → `process-ready`); Baal Summoner deployment on Base Sepolia unconfirmed — must validate Day 1 |
| **ERC-8004** | 🟢 LOW | [`ERC8004_ERC8183_ANALYSIS.md`](../hackathon/research/ERC8004_ERC8183_ANALYSIS.md) | Deployed and live on Base Sepolia; critical gotcha: `giveFeedback()` caller must NOT be the agent's own wallet — guild contract or human EOA required; ERC-8183 formally deferred (no Base Sepolia deploy, alpha spec) |
| **A2A Protocol v1.0.0** | 🟢 LOW | [`A2A_ANALYSIS.md`](../hackathon/research/A2A_ANALYSIS.md) | Spec is v1.0.0 (stable, Linux Foundation) — proposal was targeting "0.3.0"; lowest-risk component; payment/hash fields carried via `Message.metadata` and `Artifact.parts[0]` by convention |
| **EAS (Ethereum Attestation Service)** | 🟢 LOW | [`EAS_ANALYSIS.md`](../hackathon/research/EAS_ANALYSIS.md) | Additive improvement over raw `eth_sendTransaction` for deliverable hash commitment; signed proof of authorship, stable UID, easscan explorer link; schema to register Day 1 |
| **ZeroDev Kernel v3.3 (agent wallet)** | 🟡 MEDIUM | [`ERC4337_CAW_ANALYSIS.md`](../hackathon/research/ERC4337_CAW_ANALYSIS.md) | Cobo CAW confirmed broken (empty GitHub repo, non-functional x402, broken signing API) — replaced with ZeroDev Kernel; implements identical controllable-fund-operations pattern via ERC-4337 session keys; Python SDK alpha, session key policies require TypeScript bridge |
| **x402 (HTTP micropayments)** | 🟢 LOW | [`X402_ANALYSIS.md`](../hackathon/research/X402_ANALYSIS.md) | Additive fit: Specialist Agent auto-pays API endpoints with USDC during GLM-5.1 execution; does NOT replace AgentFightClub (wrong payment direction for treasury) |
| **Architecture decision** | 🟡 MEDIUM | [`ARCHITECTURE_DECISION_ANALYSIS.md`](../hackathon/research/ARCHITECTURE_DECISION_ANALYSIS.md) | Decision: hybrid custom Python workflow + MCP tool-manifest pack; Orchestrator on Claude Code (MCP server), Specialist as Python service running GLM-5.1; A2A provides harness independence |
| **Security controls** | 🔴 HIGH (residual) | [`SECURITY_ANALYSIS.md`](../hackathon/research/SECURITY_ANALYSIS.md) | Secret detection pre-filter, tool allowlist as Python set, zone-separation envelopes on A2A messages; Web3 hard floor (session key policies, AgentFightClub governance) is the only reliable financial backstop |

---

### 2. Key Research Findings

**Wallet provider change:** Cobo CAW was the planned agent wallet provider. Pre-research confirmed the GitHub repo is empty, the x402 integration is broken, and the signing API is non-functional. Replaced with ZeroDev Kernel v3.3 — the same controllable-fund-operations pattern implemented via ERC-4337 session keys. Decision logged in `hackathon/research/ERC4337_CAW_ANALYSIS.md` and `hackathon/guild-os/docs/TECH_STACK.md`.

**A2A version correction:** The proposal targeted A2A "0.3.0". The actual stable spec is v1.0.0 (Linux Foundation). All build code targets `a2a-sdk` v1.0.0 via `pip install "a2a-sdk[http-server]"`.

**ERC-8183 deferred:** Per-task escrow lifecycle is the architecturally correct post-hackathon upgrade to AgentFightClub settle. Too risky for MVP: no deployed Base Sepolia contracts, ERC-20 only, 5 stars/2 commits. Formally deferred.

**Integration diagram** (from `DEEP_RESEARCH.md`):

```
Human Founder
  │  sets mandate, votes, accepts deliverable
  ▼
AgentFightClub (Moloch v3)
  │  treasury escrow · membership governance · payment settlement
  │                                    ▲
  │                          ETH released on settle()
  ▼
Orchestrator Agent  ──── A2A task msg ────►  Specialist Agent
  (Claude API)                                  (GLM-5.1)
  (ZeroDev Kernel A)                            (ZeroDev Kernel B)
  (ERC-8004 profile A)                          (ERC-8004 profile B)
  │  reads 8004scan for talent query            │  x402 client for tool APIs
  │                                             │  EAS attest() for deliverable hash
  │  ◄──── A2A result (DataPart + hash) ────────┘
  │  validates hash · presents to human
  ▼
EAS attestation → ERC-8004 giveFeedback() → Reputation delta on 8004scan
```

---

### 3. Project Proposal — Final State

The GuildOS project proposal was finalized at v1.2 during Week 3. The proposal was substantially updated from its Week 2 initial draft to incorporate all research findings.

**Full proposal:** [`hackathon/PROJECT_PROPOSAL.md`](../hackathon/PROJECT_PROPOSAL.md) (v1.2)

Major additions in Week 3:
- Talent hunting via ERC-8004 pull model: Orchestrator actively queries the registry for candidates (Steps 3–4 in the Process Flow)
- Full A2A commerce protocol: quoting (`task/quote`), delivery (`task/delivered`), acceptance (`task/accepted`), escrow (AgentFightClub treasury from Day 1), automated evaluator pre-check (Orchestrator), reputation (6-field `giveFeedback()`), dispute stub (`DISPUTED` state → ragequit)
- Four explicit human confirmation gates (Gate 0: candidate selection; Gate 0.5: quote acceptance; Gate 1: membership vote; Gate 2: deliverable acceptance)
- Section 13: Architecture Decision — hybrid custom workflow + Claude Code MCP tool-manifest pack
- Section 14: Tech Stack — locked to Cobo CAW framing (ZeroDev Kernel delivery), Base Sepolia
- Changelog (v1.0 → v1.1 → v1.2)

**Supporting documents also produced:**
- Pre-analysis: [`hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md`](../hackathon/PROJECT_PROPOSAL_PRE_ANALYSIS.md)
- Track selection rationale: [`hackathon/TRACK_SELECTION.md`](../hackathon/TRACK_SELECTION.md)
- Second proposal analysis: [`hackathon/PROJECT_PROPOSAL_ANALYSIS_2.md`](../hackathon/PROJECT_PROPOSAL_ANALYSIS_2.md)

---

## Part 2 — Week 4 Ready Pack

Everything needed to start building on Monday June 8 without context loss.

---

### 4. Project One-Liner

> **GuildOS** — a programmable studio where a founding agent and specialist agents coordinate real work through A2A, share a Moloch-secured treasury through AgentFightClub, and build verifiable on-chain reputation — no platform, no middleman, no context loss.

**One-sentence pitch for sponsors/judges:**

> GuildOS lets one human founder and two AI agents — an Orchestrator and a Specialist — form an ephemeral work guild, complete a real task, and settle payment trustlessly on-chain, with every step provable via two Basescan transaction hashes and a before/after ERC-8004 reputation delta.

Full memo: [`hackathon/notes/project-one-liner.md`](../hackathon/notes/project-one-liner.md)

---

### 5. Team

**Status: Solo — Dogfooding Mode**

| Role | Person | GitHub |
|---|---|---|
| Human Founder / Developer | Santiago | [@santteegt](https://github.com/santteegt) |
| Orchestrator Agent | Sensei (Claude via Cowork / Claude Code) | — |
| Specialist Agent | GLM-5.1 (Z.AI) via Python service | — |

GuildOS is a solo entry. This is intentional: the project's thesis is that one person plus a coordinated set of specialist agents can execute work previously requiring a team. The build itself is a live proof-of-concept of the product it proposes.

Full module ownership map: [`hackathon/notes/TEAM_STATUS.md`](../hackathon/notes/TEAM_STATUS.md)

---

### 6. Hackathon Direction Card

Full card: [`hackathon/notes/DIRECTION_CARD.md`](../hackathon/notes/DIRECTION_CARD.md)

**Project:** GuildOS  
**Tracks:** Cobo | Agentic Economy × Cobo Agentic Wallet (primary) · Z.AI | Web3 × Long-Horizon Task (secondary)  
**Network:** Base Sepolia testnet  
**Deadline:** 2026-06-13 12:00 UTC+8

**Target users:** Independent developers and small dev shops who need short-duration specialist expertise without platform lock-in, and AI agent developers who want their agents to accept work, deliver verifiably, and accumulate portable on-chain reputation.

**Minimal demo loop (7 steps):**

1. Human founds guild via AgentFightClub — mandate on-chain, treasury funded
2. Orchestrator queries ERC-8004 registry; human selects Specialist from shortlist (Gate 0)
3. Specialist quotes scope and cost via A2A; human accepts (Gate 0.5)
4. Human votes to approve Specialist membership via AgentFightClub (Gate 1)
5. Orchestrator delegates real task to Specialist via A2A; Specialist executes using GLM-5.1
6. Specialist commits deliverable SHA-256 hash to Base Sepolia; Orchestrator pre-checks; human accepts (Gate 2)
7. AgentFightClub releases payment; Orchestrator writes 6-field delivery record to ERC-8004

**Proof of completion:** Two clickable Basescan tx hashes (deliverable hash commit + treasury settlement) + ERC-8004 Specialist profile before/after delta (0 → 1 verified delivery).

**Human confirmation gates:**

| Gate | Step | What the human decides |
|---|---|---|
| Gate 0 | Candidate selection | Approve invite to Specialist from ERC-8004 shortlist |
| Gate 0.5 | Quote acceptance | Confirm scope / cost / timeline before work starts |
| Gate 1 | Membership | Vote to admit Specialist into guild via AgentFightClub |
| Gate 2 | Deliverable acceptance | Review work + auto-evaluator report; unlock payment |

---

### 7. Track Alignment

#### Cobo | Agentic Economy × Cobo Agentic Wallet

Full alignment document: [`hackathon/notes/COBO_TRACK_ALIGNMENT.md`](../hackathon/notes/COBO_TRACK_ALIGNMENT.md)

GuildOS maps directly to every Cobo track requirement:

| Track requirement | GuildOS implementation |
|---|---|
| Agent holds a wallet | ZeroDev Kernel v3.3 smart accounts for both agents (ERC-4337, Base Sepolia) |
| Controllable fund operations | Session key policies: call whitelist (AgentFightClub only), gas cap (0.05 ETH/session), rate limit (1 tx/10 min), 24h expiry |
| Agent-to-agent work protocols | A2A v1.0.0: quote → accept → execute → deliver → settle loop |
| Agentic Economy / A2A Economy | AgentFightClub Moloch v3 shared treasury + settlement; ERC-8004 portable reputation; on-chain deliverable hash |
| Resource procurement | x402 protocol: Specialist pays API endpoints (GLM-5.1 inference) with USDC from smart account, no API keys |

**On wallet framing for judges:** ZeroDev Kernel was chosen over Cobo CAW because CAW was confirmed non-functional (empty GitHub repo, broken x402, broken signing API). ZeroDev delivers the same controllable-fund-operations pattern more completely via ERC-4337 session keys. The Cobo track's evaluation criteria is the pattern, not the SDK.

The complete economic loop: offer (`task/quote`) → counter-offer accepted → lock → execute → verify (deliverable hash) → pay (`settle()`). Every step traceable with on-chain tx hashes.

#### Z.AI | Web3 × Long-Horizon Task

Full alignment document: [`hackathon/notes/ZAI_TRACK_ALIGNMENT.md`](../hackathon/notes/ZAI_TRACK_ALIGNMENT.md)

GuildOS satisfies the Z.AI track on all three axes:

**Long-horizon execution:** The Specialist Agent runs an 11-step plan (decompose → fetch → analyze → review → merge → classify → recommend → compile → self-check → iterate → deliver) with up to 3 self-correction cycles and ~20 tool calls. No human touches it between task receipt and `task/delivered`. The execution log (step names, timestamps, tool call counts, correction cycles) is returned with the deliverable.

**Web3 integration:** Deliverable hash committed before human review, payment released on acceptance, and reputation record on ERC-8004 — all on Base Sepolia. The workflow cannot run on a Web2 backend; the payment gate and tamper-proof hash commitment are protocol-level, not database rows.

**Real GLM-5.1 usage:** The model drives the full execution loop — planning, tool orchestration, checklist evaluation, recommendation generation, self-correction, and report compilation. The chosen task type (smart contract audit / analysis) requires multi-step reasoning over technical content; a one-shot LLM call cannot complete it.

**Demo sequence for Z.AI judges:** A2A task message → GLM-5.1 plan in terminal → live tool call log → correction cycle (if triggered) → compiled report → `commit_hash` tx on Basescan → `task/delivered` A2A message with execution summary → human accepts → `settle()` tx → ERC-8004 reputation delta.

---

### 8. Scope Review

Full review: [`hackathon/notes/SCOPE_REVIEW.md`](../hackathon/notes/SCOPE_REVIEW.md)

**In scope — the one loop that must work by June 12:**

One founding agent · one specialist agent · one real task · one on-chain hash · one treasury release · one reputation delta.

Components confirmed in scope for the build sprint: AgentFightClub full governance lifecycle (`launch/commit/propose/vote/settle`), ERC-8004 profile read/write (before/after delta), A2A full 5-message flow (invite/quote/send/delivered/accepted), automated Orchestrator pre-check, GLM-5.1 long-horizon task execution, on-chain deliverable hash commit, four human CLI gates, dispute stub.

**Explicit out-of-scope (scope creep watchlist):**

- ERC-8183 per-task escrow — cut (no Base Sepolia contracts; AgentFightClub settle covers the hackathon)
- Semantic ERC-8004 registry query + LLM ranking — mocked (hardcoded agent pair is sufficient for demo)
- Multiple concurrent guild members — mocked (one pair shown; architecture supports N)
- Persistent shared memory (Mem0/LangChain) — mocked (JSON file per session)
- Third-party evaluator agent — mocked (Orchestrator hash + format check)
- Automated dispute resolution — stub (`DISPUTED` state, manual ragequit documented)
- Polished web UI — cut (two terminal windows is the demo surface)
- Custom Solidity contracts — cut (existing deployed contracts only)
- Base mainnet — cut (Base Sepolia testnet only)

**Build priority order:**

P0 (submission blocker): AgentFightClub full lifecycle · A2A task flow · GLM-5.1 execution · deliverable hash on-chain · settlement · ERC-8004 write-back  
P1 (demo quality): ERC-8004 profile delta · A2A quote round-trip · Orchestrator pre-check · human gate CLI  
P2 (judging evidence): Dispute stub · demo script · README  
P3 (presentation polish): Demo video

---

### 9. Technical Validation

Full validation plan with 10 sections and 50 checks: [`hackathon/notes/TECHNICAL_VALIDATION_PLAN.md`](../hackathon/notes/TECHNICAL_VALIDATION_PLAN.md)

**Day 1 priority order** (from `DEEP_RESEARCH.md §Day 1 Priority Order`):

1. `moloch-agent summon` on Base Sepolia — if this fails, everything shifts to DAOhaus SDK fallback immediately
2. ZeroDev Kernel — two accounts, Base Sepolia, sponsored UserOp (confirms wallet layer)
3. A2A FastAPI round-trip — Orchestrator → Specialist, metadata + DataPart artifact (runs `A2A_DAY1_TEST.py`)
4. EAS schema registration — one-time, must happen before any deliverable commit
5. ERC-8004 `register()` + `giveFeedback()` caller constraint validation
6. Security controls (secret detection + tool allowlist) — must be live before execution loop

**Validation sections summary:**

| Section | What is validated |
|---|---|
| §1 Agent Wallet (Cobo CAW/ZeroDev) | Wallet initialized, pact-scoped key limits confirmed, testnet tx succeeds |
| §2 AgentFightClub lifecycle | `launch` → `commit` → `propose` → `vote` → `settle` · guild context JSON written |
| §3 ERC-8004 identity + reputation | Profile readable, before-state captured, `giveFeedback()` succeeds, after-state shows +1 |
| §4 A2A protocol | Agent cards published, all 5 message types sent/received, full trace exported |
| §5 On-chain hash commitment | Deliverable file produced, SHA-256 computed, hash committed to Base Sepolia, stored hash readable |
| §6 GLM-5.1 execution | API reachable, ≥3-step plan logged, structured output produced, execution trace saved |
| §7 Orchestrator MCP | All 7 tools registered and callable, each returns expected output |
| §8 Human gates (CLI) | All 4 gates halt execution at correct points, dispute path confirmed |
| §9 End-to-end smoke test | Full loop runs twice (different inputs), both Basescan tx hashes clickable |
| §10 Submission evidence | README, demo video link, Basescan tx hashes, ERC-8004 screenshots, A2A trace, GLM trace |

**Fallback readiness summary:**

| Integration | Fallback |
|---|---|
| AgentFightClub Skill API (alpha) | DAOhaus SDK direct Moloch v3 deploy |
| Cobo CAW node indexing outage | Local private-key signer (already prototyped in `experiments/caw-payment-loop/`) |
| ERC-8004 / 8004scan API | Cached JSON profile files |
| Base Sepolia RPC | Alchemy primary + Infura backup |
| GLM-5.1 API | Pre-recorded output for demo task; deterministic fallback prompt |
| Live demo tx timing | Pre-staged tx hashes; pre-recorded Basescan screenshots |

---

### 10. Sprint Plan

Full plan: [`hackathon/notes/WEEK4_SPRINT_PLAN.md`](../hackathon/notes/WEEK4_SPRINT_PLAN.md)

| Day | Date | Theme | P0 Gate |
|---|---|---|---|
| **Day 8** | Mon Jun 8 | Validation | AgentFightClub `launch` live · A2A test suite green · GLM-5.1 task type locked |
| **Day 9** | Tue Jun 9 | Wallets + Identity | Both agent addresses on-chain · Guild funded with mandate · ERC-8004 registered |
| **Day 10** | Wed Jun 10 | A2A + Execution | `task/delivered` received · Hash committed to Base Sepolia · Basescan tx #1 saved |
| **Day 11** | Thu Jun 11 | Settlement + Reputation + E2E | `settle()` tx · ERC-8004 delta visible · Full loop smoke test passes |
| **Day 12** | Fri Jun 12 | Demo Prep + Evidence | README · demo script · all submission artifacts · repo clean and pushed |
| **Day 13** | Sat Jun 13 | Submission | Submitted before 12:00 UTC+8 (04:00 UTC) |

**If things slip — priority drop order:**

1. Never drop: deliverable hash tx (#1) + settlement tx (#2) — judges must click these
2. Never drop: ERC-8004 reputation delta — second key verification proof
3. Drop before those: ZeroDev session keys → design exhibit
4. Drop before those: A2A quote round-trip (Gate 0.5) → collapse to single `task/send`
5. Never drop: GLM-5.1 real execution (Z.AI track requires it)

**Tier B fallback** (invoke only if AgentFightClub AND ERC-8004 writes both fail by EOD Day 11): A2A message exchange + raw on-chain hash from Marco's EOA + GLM-5.1 execution log + design artifacts for treasury/session key/reputation. Drops formal governance and ERC-8004 delta.

---

### 11. Repo Skeleton

The GuildOS build repo has been scaffolded at `hackathon/guild-os/`. Full stack spec: [`hackathon/guild-os/docs/TECH_STACK.md`](../hackathon/guild-os/docs/TECH_STACK.md).

```
hackathon/guild-os/
├── src/
│   ├── orchestrator/
│   │   ├── server.py          # MCP server — 7 tools registered, starts listener on :3000
│   │   └── tools.py           # guild_launch · talent_query · task_invite · task_delegate
│   │                          # deliverable_review · settle · reputation_write
│   ├── specialist/
│   │   └── agent.py           # A2A HTTP server on :10001; receives tasks, runs GLM-5.1 plan
│   ├── shared/
│   │   ├── a2a.py             # A2A client — all 5 message types
│   │   ├── erc8004.py         # ERC-8004 register(), giveFeedback(), read profile
│   │   ├── agentfightclub.py  # launch, commit, propose, vote, settle
│   │   └── guild_context.py   # guild_context.json read/write helper
│   └── cli/
│       └── gates.py           # Human gate CLI prompts (Gate 0, 0.5, 1, 2)
├── tests/                     # pytest (empty; fill during Day 8–11)
├── docs/
│   ├── MVP_FLOW.md            # Full 15-step process flow
│   ├── TECH_STACK.md          # Stack decisions + naming conventions + decision log
│   ├── RISKS.md               # Risk register
│   ├── TRACK.md               # Track alignment summary
│   ├── PROBLEM.md             # Problem statement
│   └── VALIDATION_PLAN.md    # Integration validation checklist
├── scripts/
│   └── setup-github.sh        # Creates 14 labels + 6 sprint milestones in GitHub
├── guild_context.json          # Mock guild state store (one per session)
├── requirements.txt           # a2a-sdk · web3 · zhipuai · anthropic · etc.
├── .env.example               # All required env vars
├── .github/
│   ├── workflows/deploy.yml · diagnostics.yml
│   ├── PULL_REQUEST_TEMPLATE/default.md
│   └── ISSUE_TEMPLATE/bug.yml · definition.yml · design.yml · discovery.yml
├── .cursor/rules/7d-framework.mdc   # Cursor AI rules for 7-day build
├── .windsurf/rules/7d-framework.md  # Windsurf AI rules
└── CLAUDE.md                  # Agent rules for Claude Code sessions
```

**How to run (two terminals):**

```bash
# Terminal 1 — Orchestrator (MCP server)
python -m src.orchestrator.server

# Terminal 2 — Specialist Agent
python -m src.specialist.agent
```

Human gate prompts appear in Terminal 1. Gate 0 and 0.5 precede task execution; Gate 1 is membership vote; Gate 2 is deliverable acceptance.

**Guild context state machine:** `ACTIVE` → (Gate 2 accept) → `SETTLED` | (Gate 2 reject) → `DISPUTED`

---

### 12. Risk & Assumptions Memo

Full memo: [`hackathon/notes/RISK_ASSUMPTION_MEMO.md`](../hackathon/notes/RISK_ASSUMPTION_MEMO.md)

**Core assumptions (6 total):**

| Assumption | Status | Validation step |
|---|---|---|
| A1 — AgentFightClub API callable from Python | ⏳ | Day 8 — `launch` call live |
| A2 — ERC-8004 registry live + writable on Base Sepolia | ✅ Confirmed; gotchas documented | Day 8 — `register()` both agents |
| A3 — A2A SDK v1.0.0 supports GuildOS message pattern | ✅ GREEN | Day 8 — `A2A_DAY1_TEST.py` all 5 gates |
| A4 — GLM-5.1 produces usable structured output | ⏳ | Day 8 — test 3 task types; lock winner |
| A5 — ZeroDev Kernel session keys enforce limits on Base Sepolia | ⏳ | Day 9 — deploy account, configure session key |
| A6 — Base Sepolia RPC stable within demo timing | ✅ Expected; mitigation baked in | Pre-stage governance steps before live demo |

**Most likely failure points and fallbacks:**

| Risk | Probability | Fallback | Trigger |
|---|---|---|---|
| **F1 — AgentFightClub Skill API unavailable** | HIGH | DAOhaus SDK direct Moloch v3 deploy (~4h recovery) | Day 1 `launch` call fails; debug ≤ 2h then switch |
| **F2 — ERC-8004 `giveFeedback()` caller constraint** | HIGH | Route through Marco's EOA wallet | First `giveFeedback()` reverts — check `msg.sender` first |
| **F3 — GLM-5.1 output inconsistent** | MEDIUM | Deterministic fallback prompt (SHA-256 generator) | 3 failed Day 1 attempts → lock deterministic fallback |
| **F4 — ZeroDev Python SDK drops session key support** | MEDIUM | Basic EOA signing + session key policy as code exhibit | TypeScript bridge > 3h on Day 2 → document as design artifact |
| **F5 — A2A metadata extension rejected** | LOW | Carry GuildOS fields in message text body as JSON string | Day 1 gate 3/4 fails → switch to text-body encoding |
| **F6 — Base Sepolia congestion during demo** | LOW | Pre-recorded Basescan screenshots | Live tx > 30s → show pre-staged screenshot |

**Decision log (research findings already incorporated):**

| Date | Component | Result | Action |
|---|---|---|---|
| 2026-06-06 | Cobo CAW | ❌ Non-functional | Replaced with ZeroDev Kernel; x402 prototype completed in experiments/ |
| 2026-06-06 | ERC-8004 | ✅ Deployed; caller gotcha documented | Proceed with workaround; validate Day 8 |
| 2026-06-06 | A2A v1.0.0 | ✅ GREEN | Proceed; test Day 8 |
| 2026-06-06 | ERC-8183 | ⚠️ Alpha, no Base Sepolia deploy | Formally deferred post-hackathon |
| 2026-06-07 | AgentFightClub | ⏳ Not yet tested live | Validate Day 8 |
| 2026-06-07 | GLM-5.1 task types | ⏳ Not yet tested live | Validate Day 8 |
| 2026-06-07 | ZeroDev session keys | ⏳ Not yet tested live | Validate Day 9 |

---

## Summary

Week 3 produced: 8 component research analyses, a deep research synthesis, project proposal v1.2 (with commerce protocol, talent hunting, architecture decision, and tech stack), direction card, dual-track alignment documents (Cobo + Z.AI), scope review with explicit out-of-scope list, technical validation plan (50 checks), 6-day sprint plan, repo skeleton with full Python module structure, and risk/assumption memo with 6 assumptions and 6 fallbacks.

The build starts Monday June 8 with Day 1 validation of all live dependencies. Day 13 submission deadline is June 13 12:00 UTC+8.

---

*Week 3 PoW compiled: 2026-06-07 | Agent: Sensei (Claude via Cowork)*
*Sources: hackathon/research/ · hackathon/notes/ · hackathon/PROJECT_PROPOSAL.md v1.2 · hackathon/guild-os/*
