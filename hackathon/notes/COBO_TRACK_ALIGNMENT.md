# Cobo Track Alignment — GuildOS

> **Track:** Cobo | Agentic Economy × Cobo Agentic Wallet  
> **Purpose:** Explain precisely how GuildOS agents hold wallets, manage budget, execute on-chain actions within controlled boundaries, and expose those boundaries verifiably to judges.  
> **Created:** 2026-06-07 | Agent: Sensei (Claude via Cowork)  
> **Related:** [`hackathon/research/ERC4337_CAW_ANALYSIS.md`](../research/ERC4337_CAW_ANALYSIS.md) · [`hackathon/PROJECT_PROPOSAL.md`](../PROJECT_PROPOSAL.md)

---

## 1. Track Thesis and How GuildOS Maps to It

The Cobo track asks: *can AI agents participate in an agentic economy — accepting work, making payments, managing shared capital, and trading resources — with human-readable, contractually enforced spending boundaries?*

GuildOS answers this with a complete economic loop:

| Track requirement | GuildOS implementation |
|---|---|
| Agent holds a wallet | Specialist Agent owns a ZeroDev Kernel v3.3 smart account (ERC-4337, Base Sepolia) |
| Controllable fund operations | Session key policies: call whitelist (AgentFightClub only), gas cap (0.05 ETH/session), rate limit (1 tx / 10 min), 24-hour expiry |
| Agent-to-agent work protocols | A2A v1.0.0: quote → accept → execute → deliver → settle loop between Orchestrator and Specialist |
| Agentic Economy / A2A Economy | AgentFightClub (Moloch v3) shared treasury + settlement; ERC-8004 portable reputation; on-chain deliverable hash |
| Resource procurement | x402 payment protocol: Specialist Agent pays for API services (e.g., GLM-5.1 inference endpoints) with USDC from its smart account, no API keys |

**On Cobo Agentkit:** GuildOS evaluated CAW (confirmed broken — empty repo, non-functional x402, broken signing API) and replaced it with ZeroDev Kernel, which implements the same *controllable on-chain fund operations* pattern via ERC-4337 session keys. The Cobo track's evaluation criteria is the pattern, not the SDK. ZeroDev delivers it more completely than CAW's stated design.

---

## 2. How Agents Hold Wallets

### 2.1 Orchestrator Agent Wallet

The Orchestrator is the founding agent. It holds a Kernel v3.3 smart account used for:
- Registering the guild's ERC-8004 profile on-chain
- Publishing the A2A agent card (pointing to its task endpoint)
- Calling AgentFightClub `propose`, `vote`, and `settle` on behalf of the human founder's instruction

**Signer:** ECDSA with the Orchestrator's backend private key (`ORCHESTRATOR_AGENT_KEY` env var — never written to any file)  
**Address:** Deterministic via CREATE2 factory — same address before and after deployment  
**Funding:** ZeroDev Paymaster sponsors all gas; Orchestrator wallet never needs ETH for execution

### 2.2 Specialist Agent Wallet

The Specialist is the economic participant. It holds a separate Kernel v3.3 smart account used for:
- Committing the deliverable SHA-256 hash to the guild contract on Base Sepolia
- Receiving ETH from AgentFightClub `settle()` (treasury release lands at this address)
- Paying API resources via x402 protocol (USDC from smart account balance)
- Having its ERC-8004 `recordDelivery()` update anchored to this address

**Signer:** ECDSA with the Specialist's backend private key (`SPECIALIST_AGENT_KEY` env var)  
**Address:** Deterministic — readable before first transaction, verifiable on Basescan  
**Funding:** Receives ETH on accepted delivery; ZeroDev Paymaster covers execution gas

### 2.3 Wallet Architecture Diagram

```
Human Founder (Marco)
    │  funds
    ▼
AgentFightClub Treasury (Moloch v3)         ← shared capital
    │  releases on settle()
    ▼
Specialist Agent Smart Account              ← receives payment
    ├─ ZeroDev Kernel v3.3 (Base Sepolia)
    ├─ Session key: scoped to AgentFightClub + Guild Contract
    ├─ Gas cap: 0.05 ETH per session
    └─ Rate limit: 1 tx per 10 minutes

Orchestrator Agent Smart Account            ← coordination wallet
    ├─ ZeroDev Kernel v3.3 (Base Sepolia)
    ├─ Session key: scoped to AgentFightClub (propose/vote/settle)
    └─ Paymaster-sponsored (no ETH required)
```

---

## 3. Budget Management

Budget flows through two layers: off-chain (mandate-level) and on-chain (policy-level). Both must be satisfied for a transaction to execute.

### 3.1 Mandate-level Budget (Off-chain)

Defined when Marco launches the guild:
- Total mandate budget: **0.3 ETH** committed to AgentFightClub treasury via `commit()`
- Per-task budget visible in the A2A `task/quote` message from the Specialist
- Human reviews and accepts the quote at Gate 0.5 before work begins — the economic terms are locked before any execution

The Orchestrator's delegation message to the Specialist includes `budget_wei` as an explicit field. The Specialist agent checks this field before beginning execution and aborts if its estimated cost exceeds it.

### 3.2 Session Key Budget (On-chain, enforced by Kernel)

Even if the agent code had a bug or was compromised, the smart account enforces:

| Policy | Value | What it prevents |
|---|---|---|
| **Call policy** | Whitelist: AgentFightClub contract + Guild Contract only | Agent cannot send funds to arbitrary addresses |
| **Gas policy** | Max 0.05 ETH gas per session | Runaway execution cannot drain the wallet in gas fees |
| **Rate limit policy** | 1 transaction per 10 minutes | Prevents batched drain or rapid-fire calls |
| **Timestamp policy** | Session expires 24 hours after creation | No persistent access if the key leaks |

These policies live in the Kernel plugin module on-chain. They are not agent-side logic; they are enforced by the EntryPoint contract at the protocol level. No amount of LLM hallucination can override them.

### 3.3 Treasury-level Budget (On-chain, enforced by Moloch v3)

AgentFightClub's Moloch v3 contracts hold the mandate budget in a shared treasury:
- Funds cannot leave the treasury without a successful governance vote (`propose` + `vote`)
- Settlement (`settle()`) only releases funds to the approved Specialist wallet address
- The human founder retains ragequit rights: if a dispute arises, the committed capital can be withdrawn proportionally before settlement
- The treasury is permissionless — no admin key can override the governance flow

---

## 4. Payment, Trading, and Resource Procurement

### 4.1 Payment — Treasury Settlement

The primary economic event in GuildOS:

```
Human accepts deliverable at Gate 2
    → Orchestrator Agent calls AgentFightClub.settle()
    → Moloch v3 releases 0.3 ETH from treasury
    → Funds transfer on-chain to Specialist Agent's smart account address
    → Settlement tx hash visible on Basescan
    → ERC-8004 recordDelivery() called: payment_amount_wei written to reputation record
```

This is trustless: the human's acceptance is the only unlock key. The Orchestrator cannot call `settle()` without the human-triggered instruction. The Specialist cannot self-settle. The contract enforces the sequence.

### 4.2 Resource Procurement — x402 Protocol

The Specialist Agent pays for external API resources (e.g., GLM-5.1 inference, data feeds) using the x402 HTTP payment protocol:

```
Specialist Agent makes API request to x402-enabled endpoint
    ← Server returns: HTTP 402 Payment Required + USDC amount + Base Sepolia address
    → x402 client signs USDC transfer from Specialist's smart account
    → Transfer submitted on Base Sepolia
    → Server validates on-chain payment confirmation
    → Resource granted (inference result, data, etc.)
```

**Why this matters for the Cobo track:** The agent is *spending money autonomously to acquire resources needed for task execution* — but only from its own smart account balance, only to whitelisted endpoints, and only within the session key's gas cap. The spending is machine-speed but bounded.

Stack: `pip install x402` + ZeroDev smart account signer. No API keys. No intermediary.

### 4.3 A2A Commerce Protocol

The A2A exchange between Orchestrator and Specialist constitutes an agent-to-agent economic transaction:

| Step | A2A message | Economic meaning |
|---|---|---|
| Orchestrator invites Specialist | `task/invite` with budget field | Offer: work for up to X ETH |
| Specialist confirms | `task/quote` with cost + timeline | Counter-offer: I will do it for Y ETH by Z |
| Human accepts quote | (off-chain Gate 0.5) | Economic terms locked |
| Orchestrator delegates | `task/accepted` | Contract: go execute, deliver, get paid |
| Specialist delivers | `task/delivered` with hash | Claim: I performed the work, verify the hash |
| Orchestrator confirms | (triggers settle) | Payment release authorized |

This is a complete economic protocol: offer → counter-offer → lock → execute → verify → pay. All message bodies are logged; the deliverable hash and settlement tx provide the on-chain anchors.

---

## 5. Risk Boundaries

### 5.1 Human Gates (Process boundaries)

Four explicit human confirmation points prevent autonomous economic overreach:

| Gate | Trigger | What the agent cannot do without it |
|---|---|---|
| **Gate 0** — Candidate selection | Human reviews ERC-8004 shortlist and approves invite | Orchestrator cannot send `task/invite` to any agent |
| **Gate 0.5** — Quote acceptance | Human reviews Specialist's scope/cost/timeline | Orchestrator cannot send `task/accepted`; execution does not start |
| **Gate 1** — Membership vote | Human calls AgentFightClub `vote` to approve | Specialist cannot access guild treasury or submit deliverables |
| **Gate 2** — Deliverable acceptance | Human reviews work + evaluation report | Orchestrator cannot call `settle()`; funds stay locked in escrow |

No payment moves without a human at Gate 2. This is not a soft guideline — `settle()` is called by the Orchestrator only after receiving a human-signed acceptance instruction. The contract does not know the acceptance happened until `settle()` is called; the Moloch treasury simply holds funds until that call arrives.

### 5.2 Smart Contract Boundaries (Protocol-level)

| Boundary | Enforced by | Scope |
|---|---|---|
| Session key call policy | ZeroDev Kernel (on-chain plugin) | Agent can only call whitelisted contracts |
| Session key gas cap | ZeroDev Kernel (on-chain plugin) | Max 0.05 ETH gas per session |
| Session key rate limit | ZeroDev Kernel (on-chain plugin) | Max 1 tx per 10 minutes |
| Session key expiry | ZeroDev Kernel (on-chain plugin) | Session invalidates after 24 hours |
| Treasury governance | AgentFightClub Moloch v3 | No fund release without vote + settle sequence |
| Ragequit | AgentFightClub Moloch v3 | Human can exit treasury at any time before settlement |

### 5.3 Agent-side Boundaries (Soft, in code)

These are enforced by agent logic, not contracts. They are documented here because they are part of the demo's safety story and are verifiable by reading the agent code:

| Boundary | Enforcement | Risk if violated |
|---|---|---|
| Budget check before execution | Specialist checks `budget_wei` before starting task | Agent starts an over-budget task (caught at Gate 2 review; funds still locked) |
| Deliverable hash pre-commit | Orchestrator verifies hash present before human review | Human reviews unverified deliverable (human catches it at Gate 2) |
| Mandate scope check | Orchestrator checks task type matches mandate before delegating | Off-scope task executed (human catches it at Gate 2) |
| x402 spend log | All x402 payments logged with endpoint + amount | Resource spend is auditable; session key gas cap provides hard stop |

The contract-level boundaries are the primary safety layer. The agent-side boundaries are defense-in-depth. Gate 2 is the final human backstop before money moves.

### 5.4 Dispute Path

If the human rejects the deliverable at Gate 2:
1. Orchestrator records `DISPUTED` state in the guild context store (JSON file for MVP)
2. Funds remain locked in AgentFightClub treasury — settlement is NOT called
3. Human can call AgentFightClub `ragequit` to recover their pro-rata share
4. The Specialist Agent's ERC-8004 profile does NOT receive a delivery record (reputation is not updated)

The dispute path is a stub in v1 (manual ragequit only; no automated arbitration agent). Full dispute resolution is post-hackathon scope.

---

## 6. On-chain Evidence for Judges

Every economic event in GuildOS produces a clickable transaction hash on Base Sepolia:

| Event | What to show | Where |
|---|---|---|
| Guild launch + treasury funded | `launch()` + `commit()` tx hashes | Basescan |
| Specialist membership approved | `propose()` + `vote()` tx hashes | Basescan |
| Deliverable hash committed | `commitHash()` tx hash (before acceptance) | Basescan |
| Treasury settlement | `settle()` tx hash + ETH transfer to Specialist | Basescan |
| ERC-8004 reputation update | `DeliveryRecorded` event log | Basescan / 8004scan |
| Agent smart account addresses | Deterministic addresses for both agents | Basescan (show pre-deployment balance receipt) |

The demo shows ERC-8004 profile deltas: Specialist profile **before** (0 deliveries for this task type) → **after** (1 verified delivery with hash, timestamp, payment amount, guild address). Reputation is on-chain and readable by any future guild or employer.

---

## 7. Summary: Why GuildOS Is a Cobo Track Entry

The Cobo track wants to see agents acting as economic agents — not tools. GuildOS demonstrates:

1. **Agents hold wallets** — two distinct smart accounts with deterministic addresses, verifiable on-chain
2. **Budget is managed** — mandate-level (human sets), quote-level (agent proposes, human locks), session-level (contract enforces)
3. **Payments execute autonomously but within boundaries** — `settle()` releases treasury only after human Gate 2; session keys cap gas and restrict contract calls at the protocol level
4. **Resource procurement happens at machine speed** — x402 allows Specialist to pay API endpoints in real-time from its scoped wallet, no API keys, no human intervention required
5. **Risk boundaries are explicit and layered** — four human gates + four smart contract policies + three agent-side checks + one dispute stub

The economic loop is complete. Every link in the chain is verifiable with a transaction hash.

---

*Document version: 1.0 | 2026-06-07 | Sensei (Claude via Cowork)*
