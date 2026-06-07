# GuildOS — Scope Review

> Hackathon: AI × Web3 Agentic Builders Hackathon  
> Build window: 2026-06-01 — 2026-06-12 · Submission deadline: 2026-06-13 12:00 UTC+8  
> Team: Solo (Santiago)  
> Last updated: 2026-06-07

---

## 1. What GuildOS Is (Hackathon Scope)

GuildOS is a **single-guild, single-task coordination demo** that proves one complete loop:

> A human founds a guild → an Orchestrator Agent sources and invites a Specialist Agent → the Specialist executes a real task via GLM-5.1 → delivers a hash-committed artifact on-chain → the human accepts → AgentFightClub releases payment → the Specialist's ERC-8004 profile gains a verified delivery record.

Every component either performs one real operation or holds a clearly-labeled mock. Nothing in the demo requires the audience to trust a simulation — two Basescan tx hashes and an ERC-8004 profile delta make the loop verifiable.

**In scope for the build sprint:**

- AgentFightClub: `launch` + `commit` (treasury open with mandate)
- AgentFightClub: `propose` + `vote` + `settle` (membership and payment)
- ERC-8004 profile read — before/after reputation delta for both agents
- ERC-8004 reputation write-back — 6 fields, on-chain event after acceptance
- A2A task flow: invite → quote → acceptance → delegation → delivery
- Automated deliverable pre-check (hash present, format valid) by Orchestrator
- GLM-5.1 long-horizon task execution by Specialist Agent
- On-chain deliverable hash commitment (one tx on Base Sepolia)
- Human review + acceptance via minimal CLI
- Four human confirmation gates (Gate 0 / 0.5 / 1 / 2)
- Dispute stub: `DISPUTED` state in guild context store; ragequit path documented
- Guild context store as a JSON file (one file per guild session)
- Hardcoded Orchestrator + Specialist agent pair (no live registry query)

**The one loop that must work by June 12:**  
One founding agent · one specialist agent · one real task · one on-chain hash · one treasury release · one reputation delta.

---

## 2. What GuildOS Is NOT (Explicit Out-of-Scope)

These items are **explicitly excluded** from the hackathon build. Raising any of them during the build sprint is a scope-creep signal — note it, and move on.

### Protocol / On-chain

- **ERC-8183 escrow lifecycle** — the full per-task payment/dispute/release contract. Hash-commit + AgentFightClub settle covers the hackathon. ERC-8183 is post-hackathon.
- **Custom Solidity contracts** — no new smart contract code. All on-chain calls go to existing deployed contracts (AgentFightClub / Moloch v3, ERC-8004 registry).
- **Cross-guild reputation aggregation** — a trust graph or score across multiple guilds. One guild, one profile delta.
- **Ragequit implementation** — the exit is documented and the `DISPUTED` state is recorded, but no actual ragequit call is executed in the demo.
- **Guild dissolution and pro-rata share distribution** — lifecycle ends at successful settlement. Teardown is post-hackathon.
- **Per-capability pricing** — all payments use the single mandate budget committed at `launch`. No per-task or per-deliverable escrow.

### Agent Capabilities

- **Semantic capability matching** — no live ERC-8004 registry query + LLM ranking. The Orchestrator uses a hardcoded Specialist profile for the demo. Full matching is post-hackathon.
- **Multiple concurrent active tasks** — the guild handles one task at a time. Parallelism is an architecture-level decision for post-hackathon.
- **Multiple concurrent guild members** — one Orchestrator + one Specialist. The architecture supports N; the demo shows 2.
- **Human-augmented agent profiles** — hybrid human + AI contributor records. Agents only.
- **Persistent shared memory** — no Mem0, LangChain memory, or equivalent OSS integration. The guild context store is a JSON file. Memory persistence between sessions is post-hackathon.
- **Third-party evaluator agent** — no separate evaluation agent. The Orchestrator runs a minimal hash + format check. Full evaluator is post-hackathon.
- **Automated dispute resolution agent** — `DISPUTED` state is a stub. Resolution is manual (ragequit) or human. Automation is post-hackathon.
- **Multi-harness Orchestrator** — no Openclaw or Hermes packaging for the Orchestrator. Claude Code (MCP server) only for hackathon. Porting is a post-hackathon packaging exercise.

### UX / Interface

- **Polished web UI or dashboard** — no React app, no visual guild explorer. Demo runs in two terminal windows (Orchestrator on Claude Code, Specialist as Python service).
- **Client-facing guild discovery** — no public listing of active guild mandates or open applications.
- **Non-technical users** — the demo targets developers and judges who can read a Basescan transaction. No onboarding flow, no explanatory UI.

### Product Scope

- **Enterprise procurement** — not a target user for this build.
- **Payment in production tokens** — testnet only (Base Sepolia). No mainnet, no real funds.
- **Account recovery or wallet management UI** — Cobo CAW handles signing. No wallet management surface.

---

## 3. Cut / Postpone / Mock Decision Table

| Feature | Decision | Reason | Resume When |
|---|---|---|---|
| Semantic ERC-8004 registry query + LLM ranking | **Mock** — hardcoded agent pair | Build time > value for demo; one pair is enough to show the loop | Post-hackathon Week 1 |
| Multiple concurrent guild members | **Mock** — one pair shown | Architecture supports N; demo clarity > completeness | Post-hackathon |
| ERC-8183 escrow lifecycle | **Cut** — not in demo | Alpha spec, high integration risk, not required by Cobo track rubric | Post-hackathon |
| Persistent shared memory (Mem0 / LangChain) | **Mock** — JSON file | OSS integration risk in build week; JSON is testable and deterministic | Post-hackathon Week 1 |
| Third-party evaluator agent | **Mock** — Orchestrator runs hash + format check | Building a separate evaluator agent is a second full integration; not needed for demo validity | Post-hackathon |
| Automated dispute resolution | **Stub** — record `DISPUTED` state | One rejected deliverable can be shown; automated arbitration is a research direction | Post-hackathon |
| Ragequit call (on-chain execution) | **Cut** — document path only | Not needed in the happy-path demo; Moloch v3 ragequit is well-documented and can be shown as a diagram | Post-hackathon |
| Guild dissolution + pro-rata shares | **Cut** | Lifecycle out of demo scope; guild ends at successful settlement | Post-hackathon |
| Cross-guild reputation graph | **Cut** | Requires multiple guilds; single guild suffices for reputation delta demo | Long-term roadmap |
| Polished web UI | **Cut** | Two terminal windows is the demo surface; UI is post-hackathon polish | Post-hackathon Week 2 |
| Client-facing guild discovery page | **Cut** | Read-only UI with no critical path value for judges | Post-hackathon |
| Openclaw / Hermes Orchestrator packaging | **Postpone** | MCP schema is written; porting is a packaging exercise; not needed for demo | Post-hackathon |
| Custom Solidity contracts | **Cut** | Uses existing deployed contracts only; no new contract code reduces audit and deploy risk | Never (unless ERC-8004 registry requires it) |
| Mainnet deployment | **Cut** | Testnet is sufficient for demo and hackathon submission evidence | Post-hackathon (if productionized) |
| Per-capability pricing | **Postpone** | Requires per-task escrow design; single mandate budget is correct abstraction for v1 | Post-hackathon |
| Human-augmented agent profiles | **Postpone** | Identity / Capability direction item; out of hackathon scope | Post-hackathon Quarter 2 |
| ERC-8004 write during Specialist registration | **Real (simple)** — single on-chain call | Keep real but keep it simple: one `mint` or `register` call; no complex attribute encoding | In scope; keep thin |
| A2A multi-agent marketplace / discovery | **Cut** | Full marketplace is the long-horizon product vision; guild is the v1 primitive | Post-hackathon |

---

## 4. Scope Creep Triggers to Watch

These are the most likely sources of mid-build drift. If you find yourself working on any of these without a deliberate scope change decision, stop.

- **"Let me also add a second specialist agent"** → one pair is the demo. Two agents are the architecture. Ship one.
- **"The JSON context store feels hacky — let me integrate Mem0"** → it is supposed to feel hacky. It is a stub. Ship the stub.
- **"I should query the full ERC-8004 registry for realism"** → hardcoded profile is realistic enough. Full query is post-hackathon.
- **"I should build a simple UI so the demo looks better"** → terminal windows are the demo surface. A UI that takes a day to build will not improve the judging score by a day's worth of margin.
- **"The dispute path should actually call ragequit"** → `DISPUTED` state in the JSON file is the stub. Ragequit is documented, not executed.
- **"I should deploy on mainnet to make it more credible"** → Base Sepolia tx hashes are credible. Mainnet adds gas costs and real-asset risk for zero judging benefit.
- **"ERC-8183 would make the payment story cleaner"** → AgentFightClub settle is the payment story. ERC-8183 is a different story.

---

## 5. Build Priority Order (Remaining Days)

| Priority | Task | Status |
|---|---|---|
| P0 | AgentFightClub `launch` + `commit` working end-to-end | ⬜ |
| P0 | A2A task message send/receive (Orchestrator ↔ Specialist) | ⬜ |
| P0 | GLM-5.1 Specialist execution for chosen demo task type | ⬜ |
| P0 | On-chain deliverable hash commit (Base Sepolia) | ⬜ |
| P0 | AgentFightClub `settle()` releasing payment | ⬜ |
| P0 | ERC-8004 reputation write-back (6 fields) | ⬜ |
| P1 | AgentFightClub `propose` + `vote` (membership) | ⬜ |
| P1 | ERC-8004 profile read before/after (delta visible) | ⬜ |
| P1 | A2A quote + acceptance message round-trip | ⬜ |
| P1 | Orchestrator automated pre-check (hash + format) | ⬜ |
| P1 | Human gate prompts (CLI — Gates 0, 0.5, 1, 2) | ⬜ |
| P2 | Dispute stub (`DISPUTED` state in JSON, ragequit path documented) | ⬜ |
| P2 | Demo script / run instructions for judges | ⬜ |
| P2 | README with architecture diagram, tx hash evidence, and API proof | ⬜ |
| P3 | Demo video (3–5 min) | ⬜ |

P0 = submission blocker. P1 = demo quality. P2 = judging evidence. P3 = presentation polish.

---

*Scope Review v1.0 · 2026-06-07 · Agent: Sensei (Claude via Cowork)*
