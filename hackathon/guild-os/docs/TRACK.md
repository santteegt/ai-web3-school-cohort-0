# Track Alignment — GuildOS

## Cobo | Agentic Economy × Cobo Agentic Wallet {#cobo}

**Track thesis:** Can AI agents participate in an agentic economy — accepting work, making payments, managing shared capital, and trading resources — with human-readable, contractually enforced spending boundaries?

**GuildOS answer:** Yes — a complete economic loop with controllable fund operations.

| Track requirement | GuildOS implementation |
|------------------|----------------------|
| Agent holds a wallet | Specialist Agent owns a ZeroDev Kernel v3.3 smart account (ERC-4337, Base Sepolia) |
| Controllable fund operations | Session key policies: call whitelist (AgentFightClub contract only), gas cap (0.05 ETH/session), rate limit (1 tx / 10 min), 24-hour expiry |
| Agent-to-agent work protocols | A2A v1.0.0: quote → accept → execute → deliver → settle loop between Orchestrator and Specialist |
| Agentic Economy / A2A Economy | AgentFightClub (Moloch v3) shared treasury + settlement; ERC-8004 portable reputation; on-chain deliverable hash |
| Resource procurement | Specialist Agent pays for API services (e.g., GLM-5.1 inference endpoints) via x402 payment protocol using USDC from its smart account |

**Key demo evidence for Cobo track:**
- ZeroDev session key config shown as code exhibit (or live if TypeScript bridge completes in Day 2 window)
- Orchestrator calls `settle()` from the guild contract — not from its own wallet (demonstrates scoped operations)
- CAW/ZeroDev anonymized config snippet in README

---

## Z.AI | Web3 × Long-Horizon Task {#zai}

**Track thesis:** Can GLM-5.1 power a long-horizon, multi-step autonomous agent that produces real, verifiable work in a Web3 context?

**GuildOS answer:** Yes — Specialist Agent uses GLM-5.1 to decompose tasks, execute multi-step plans, and produce deliverables that are committed on-chain.

| Track requirement | GuildOS implementation |
|------------------|----------------------|
| GLM-5.1 for long-horizon execution | Specialist Agent uses Z.AI GLM-5.1 API; decomposes task into ≥ 3-step plan, executes with tool use loop, produces structured output |
| Web3 proof | Deliverable SHA-256 hash committed to guild contract on Base Sepolia before human acceptance |
| Long-horizon task run log | `hackathon/notes/glm_trace_{date}.json` — every step: plan → tool call → result → next step |
| Agentic dev context | Orchestrator→Specialist A2A task delegation is the Web3-native agent workflow |

**Key demo evidence for Z.AI track:**
- `glm_trace_*.json` showing multi-step plan execution
- Non-trivial task output (code generation, security analysis, or spec writing — locked on Day 8)
- On-chain hash commit of GLM-5.1 output as the deliverable

---

## Evaluation Scorecard

| Question | GuildOS Answer |
|----------|---------------|
| Would this problem exist without AI? | Yes — but it becomes a DAO for humans (Raid Guild). AI adds: agents as first-class economic members, long-horizon execution, A2A capability matching. |
| Would this problem exist without Web3? | Yes — but reputation is a platform row, payment depends on a platform, mandate history is editable. Web3 provides: ERC-8004 portable reputation, Moloch v3 enforced treasury, tamper-proof delivery records. |
| Who initiates / executes / pays / accepts / arbitrates? | Initiates: Human. Executes: Specialist Agent. Pays: Guild treasury. Accepts: Human. Arbitrates: AgentFightClub governance + human vote. Chain is complete. |
| How is the result verified? | Deliverable hash committed before acceptance; payment only releases after hash match + human approval. ERC-8004 reputation updated on-chain after each accepted delivery. |

---

## Hackathon Links

| Resource | URL |
|----------|-----|
| Event page | https://casualhackathon.com/hackathons/cmpsjubkg0003p80kxuzrdyjy |
| Submission deadline | 2026-06-13 12:00 UTC+8 (04:00 UTC) |
| Demo Day | 2026-06-14 |
| Prize pool | 7000 USDT (Cobo: 3500 USDT · Z.AI: 3500 USDT) |
