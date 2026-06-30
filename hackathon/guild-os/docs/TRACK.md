# Track Alignment — GuildOS

## Cobo | Agentic Economy × Cobo Agentic Wallet {#cobo}

**Track thesis:** Can AI agents participate in an agentic economy — accepting work, making payments, managing shared capital, and trading resources — with human-readable, contractually enforced spending boundaries?

**GuildOS answer:** Yes — a complete economic loop with controllable fund operations.

| Track requirement | GuildOS implementation |
|------------------|----------------------|
| Agent holds a wallet | Orchestrator and Specialist each hold a wallet through a **provider-agnostic `WalletProvider`** (Cobo CAW default, TSS local node; ZeroDev/Turnkey swappable); Base (chain_id 8453) |
| Controllable fund operations | Treasury is **DAO-held** — no agent custodies funds. CAW **Pacts** scope, at the signature level, the DAO governance calls the agent may make (`propose`/`vote`/`process` on the guild contract) and cap **tribute** (the only fund-moving agent call). No EOA fallback |
| Agent-to-agent work protocols | A2A v1.0.0: quote → accept → execute → deliver → payment-proposal → settle → feedback loop between Orchestrator and Specialist (validated Day 9) |
| Agentic Economy / A2A Economy | AgentFightClub (Moloch v3) shared treasury + DAO-voted settlement; ERC-8004 portable reputation; EAS-attested deliverable (UID embedded in A2A result message) |
| Resource procurement | Specialist Agent pays for API services (e.g., GLM-5.1 inference via x402) from its CAW wallet; full x402 pipeline confirmed Day 8 |

**Key demo evidence for Cobo track:**
- CAW Pact config shown as live proof (TSS node running) — allowlists the DAO `propose`/`vote`/`process` calls and caps tribute
- Payment released through a DAO **payment proposal** the human votes and processes (Gate 3) — not from any agent wallet
- Provider-agnostic `WalletProvider` (CAW default; ZeroDev/Turnkey swappable) keeps the same scoping
- CAW wallet address + anonymized Pact config in README

---

## Z.AI | Web3 × Long-Horizon Task {#zai}

**Track thesis:** Can GLM-5.1 power a long-horizon, multi-step autonomous agent that produces real, verifiable work in a Web3 context?

**GuildOS answer:** Yes — Specialist Agent uses GLM-5.1 to decompose tasks, execute multi-step plans, and produce deliverables that are committed on-chain.

| Track requirement | GuildOS implementation |
|------------------|----------------------|
| GLM-5.1 for long-horizon execution | **Hermes agent** deployed as Specialist; uses Z.AI GLM-5.1 API; decomposes task into ≥ 3-step plan, executes with ReAct tool-use loop, produces structured output (stack locked Day 9) |
| Web3 proof | Deliverable SHA-256 hash attested via **EAS** on Base mainnet before human acceptance; attestation UID embedded in A2A `task/delivered` message and queryable on `base.easscan.org` |
| Long-horizon task run log | `./logs/glm_trace_{date}.json` — every step: plan → tool call → result → next step |
| Agentic dev context | Orchestrator→Specialist A2A task delegation is the Web3-native agent workflow |

**Key demo evidence for Z.AI track:**
- `glm_trace_*.json` showing multi-step plan execution
- Non-trivial task output (code generation, security analysis, or spec writing — task type locked Day 9 via Hermes)
- EAS attestation of GLM-5.1 output hash on Base mainnet — queryable at `https://base.easscan.org/attestation/{uid}`

---

## Evaluation Scorecard

| Question | GuildOS Answer |
|----------|---------------|
| Would this problem exist without AI? | Yes — but it becomes a DAO for humans (Raid Guild). AI adds: agents as first-class economic members, long-horizon execution, A2A capability matching. |
| Would this problem exist without Web3? | Yes — but reputation is a platform row, payment depends on a platform, mandate history is editable. Web3 provides: ERC-8004 portable reputation, Moloch v3 enforced treasury, tamper-proof delivery records. |
| Who initiates / executes / pays / accepts / arbitrates? | Initiates: Human. Executes: Specialist Agent. Pays: Guild treasury. Accepts: Human. Arbitrates: AgentFightClub governance + human vote. Chain is complete. |
| How is the result verified? | Specialist creates an EAS attestation of the deliverable hash before acceptance; attestation UID is embedded in the A2A result. Payment releases only through a DAO **payment proposal** the human votes and processes (Gate 3). The Specialist then triggers reputation via `feedback/request`; the guild submits an executable `submitFeedback` proposal (`AgentFightClub.propose()` encoding 6 feedback fields); human votes (Gate 4); only on vote pass does `giveFeedback()` fire with the guild contract as `msg.sender` — ensuring both money and reputation are governed, multi-party records, not unilateral writes. |

---

## Hackathon Links

| Resource | URL |
|----------|-----|
| Event page | https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy |
| Submission deadline | 2026-06-13 12:00 UTC+8 (04:00 UTC) |
| Demo Day | 2026-06-14 |
| Prize pool | 7000 USDT (Cobo: 3500 USDT · Z.AI: 3500 USDT) |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-06-30 | Cobo track reframed: treasury is DAO-held; CAW Pact scopes the DAO `propose`/`vote`/`process` calls + caps tribute (not a per-task ceiling/contract whitelist); provider-agnostic `WalletProvider` (CAW default, ZeroDev/Turnkey swappable); no EOA fallback. Settlement now flows through a DAO **payment proposal** (Gate 3); reputation gate renumbered to **Gate 4** and is Specialist-triggered. Scorecard "how verified" updated. Mirrors `specs/` design feedback. |
