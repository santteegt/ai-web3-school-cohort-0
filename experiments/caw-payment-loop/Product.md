# Product — CAW Payment Loop

> Minimal x402 paywall + Cobo CAW agent autonomous payment loop prototype.
> Discovery + Definition + Design in one file.

---

## Vision

Demonstrate that an AI agent can transact autonomously — not because it decides to pay, but because a human explicitly pre-authorized the action. A **service provider** exposes an API (or AI inference endpoint) protected by **x402**: calls without payment return `402 Payment Required`. A **consumer agent** recognizes the 402, reads the payment requirement, and uses **Cobo Agentkit (CAW)** to complete the transaction. CAW enforces a **Pact** — a human-approved permission policy that binds the agent to a budget cap, a specific endpoint scope, and a time window. The agent cannot exceed those bounds. Once paid, the service responds and a complete **audit trail** (tx hash, amount, Pact ID, timestamp) is recorded on-chain and locally.

The emphasis is on control, not convenience: every payment is traceable, every constraint is machine-enforced, and no money moves without a prior human decision.

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        HUMAN (operator)                      │
│                                                              │
│  Approves Pact: endpoint scope, budget cap, time window      │
│  Reviews audit log after session                             │
└──────────────────────┬───────────────────────────────────────┘
                       │  Pact approval (once, upfront)
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    CONSUMER SIDE                             │
│                                                              │
│  ┌─────────────────┐      ┌──────────────────────────────┐  │
│  │  Agent Client   │─────▶│  CAW (Cobo Agentkit)         │  │
│  │  (paymentLoop)  │      │  WalletOperator + Pact       │  │
│  │                 │      │  - budget ceiling enforced   │  │
│  │  1. call API    │      │  - scope: approved endpoint  │  │
│  │  2. recv 402    │      │  - expiry: time window       │  │
│  │  3. build pay   │◀─────│  signs tx on Base Sepolia    │  │
│  │  4. retry req   │      └──────────────────────────────┘  │
│  └────────┬────────┘                                        │
│           │                                                  │
│           │ audit record (tx hash, amount, ts, status)       │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │  Audit Log      │  logs/audit.json + Basescan link        │
│  └─────────────────┘                                        │
└──────────────────────────────────────────────────────────────┘
                       │  HTTP with X-PAYMENT header
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   SERVICE PROVIDER SIDE                      │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  x402 Paywall Middleware                            │    │
│  │  - no payment → 402 + X-PAYMENT-REQUIRED header     │    │
│  │  - valid payment → verify on-chain → pass request   │    │
│  └───────────────────────┬─────────────────────────────┘    │
│                          │                                   │
│  ┌───────────────────────▼─────────────────────────────┐    │
│  │  Protected Endpoint  (mock AI inference / price feed)│    │
│  │  GET /api/inference                                  │    │
│  │  Returns: { result, model, timestamp }               │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
                       │  on-chain settlement
                       ▼
              Base Sepolia testnet
              (tx hash → Basescan)
```

---

## Interaction Flow

```
Human          Agent Client        CAW / Pact          x402 Server        Base Sepolia
  │                  │                  │                   │                   │
  │ approve Pact     │                  │                   │                   │
  │─────────────────▶│                  │                   │                   │
  │                  │─── init Pact ───▶│                   │                   │
  │                  │◀── Pact ready ───│                   │                   │
  │                  │                  │                   │                   │
  │                  │── GET /api/inference ───────────────▶│                   │
  │                  │◀── 402 + X-PAYMENT-REQUIRED ─────────│                   │
  │                  │                  │                   │                   │
  │                  │── check Pact ───▶│                   │                   │
  │                  │◀── within budget │                   │                   │
  │                  │                  │                   │                   │
  │                  │── sign + send tx ───────────────────────────────────────▶│
  │                  │◀── tx hash ────────────────────────────────────────────── │
  │                  │                  │                   │                   │
  │                  │── GET /api/inference + X-PAYMENT: <tx> ─────────────────▶│
  │                  │◀── 200 { result, model, timestamp } ─│                   │
  │                  │                  │                   │                   │
  │                  │── deduct from Pact budget ──────────▶│                   │
  │                  │── write audit record ─────────────────────────────────── │
  │                  │                  │                   │                   │
  │◀── audit log + Basescan link ────── │                   │                   │
```

---

## Backlog

| ID    | Feature                        | Status   | Priority    |
|-------|--------------------------------|----------|-------------|
| P-001 | x402 Service Provider          | Done     | Must Have   |
| P-002 | CAW Pact Authorization         | Done     | Must Have   |
| P-003 | Agent Consumer Loop            | Done     | Must Have   |
| P-004 | Auditable Settlement Records   | Done     | Must Have   |
| P-005 | Demo Package                   | Done     | Should Have |

> Status: Todo → Building → Done
> Priority: Must Have / Should Have / Nice to Have

---

## Requirements

### P-001: x402 Service Provider

**What it does:** Express server acting as the service provider. One endpoint protected by x402 middleware — it returns `402 Payment Required` with payment terms, and `200` with a mock AI inference response once payment is verified on-chain.

**Acceptance Criteria:**
- [ ] `GET /api/inference` returns `402` with `X-PAYMENT-REQUIRED` header (amount in ETH, receiver address, network: Base Sepolia) when no payment is attached
- [ ] x402 middleware verifies the on-chain payment before passing the request to the handler — no fake payments accepted
- [ ] Handler returns `{ result: string, model: string, timestamp: number }` on verified payment
- [ ] Server logs each request: method, path, payment status (missing / invalid / verified), amount
- [ ] Price per call is configurable via env var (`PRICE_PER_CALL_ETH`)

**Out of Scope:** Real AI model calls, multiple endpoints, persistent revenue tracking, auth beyond x402

---

### P-002: CAW Pact Authorization

**What it does:** Human-facing CLI step that presents an authorization summary and, on approval, creates a CAW Pact that bounds all subsequent agent payments. The Pact is the machine-enforced contract between human intent and agent execution.

**Acceptance Criteria:**
- [ ] CLI displays: target endpoint, max total budget (ETH), price ceiling per call, time window (start → expiry)
- [ ] Human confirms with `y` or rejects with `n`; rejection exits without creating a Pact
- [ ] On approval: initializes Cobo `WalletOperator`, creates a Pact with the approved parameters, saves Pact ID + config to `pact-config.json`
- [ ] Pact enforces: spend only to the service provider's receiver address, never above budget cap, never above per-call ceiling, never after expiry
- [ ] Pact details (ID, budget, scope, expiry) printed to console on creation

**Out of Scope:** Multi-asset Pacts, revocation flow, Pact amendments without re-approval, on-chain Pact registry

---

### P-003: Agent Consumer Loop

**What it does:** The core of the prototype. Agent reads the active Pact, calls the x402-protected endpoint, recognizes the 402, uses CAW to construct and sign the payment transaction within Pact constraints, and retries the request with the payment proof. This is autonomous but bounded.

**Acceptance Criteria:**
- [ ] Reads `pact-config.json` on startup — fails loudly if no Pact exists or Pact is expired
- [ ] Makes `GET /api/inference` — correctly parses `402` and `X-PAYMENT-REQUIRED` header
- [ ] Checks: requested payment amount ≤ Pact per-call ceiling; cumulative spend + new amount ≤ Pact budget cap; current time < Pact expiry — rejects and halts if any check fails
- [ ] Uses CAW `WalletOperator` to sign and broadcast the tx to Base Sepolia
- [ ] Retries with `X-PAYMENT: <tx-hash>` header
- [ ] Receives and logs the 200 response payload
- [ ] Deducts the paid amount from the running Pact budget tracker

**Out of Scope:** Parallel calls, streaming, retry backoff, multi-hop payment routes

---

### P-004: Auditable Settlement Records

**What it does:** After each successful payment and API response, write a complete settlement record. The record must be sufficient for an independent audit: who paid, how much, to what endpoint, for what result, provable on-chain.

**Acceptance Criteria:**
- [ ] Each record contains: `timestamp`, `pactId`, `endpoint`, `amountPaid` (ETH), `txHash`, `receiver`, `responseStatus`, `resultSnippet` (first 100 chars of response)
- [ ] Records appended to `logs/audit.json` (created on first run, never overwritten)
- [ ] Basescan testnet link (`https://sepolia.basescan.org/tx/<txHash>`) printed per payment
- [ ] Session summary printed at end of run: total calls, total ETH spent, remaining Pact budget
- [ ] Audit file is human-readable JSON (pretty-printed, one record per array entry)

**Out of Scope:** On-chain audit contract, IPFS pinning, structured log format (ECS, JSON Lines), dashboard

---

### P-005: Demo Package

**What it does:** Self-contained demo artifact that a judge or technical reviewer can read in under 10 minutes. Combines the architecture diagram, interaction flow, key API surface, and risk boundaries in one document.

**Acceptance Criteria:**
- [ ] `docs/DEMO.md` includes: architecture diagram (ASCII or Mermaid), full interaction sequence, x402 payment header spec (`X-PAYMENT-REQUIRED` and `X-PAYMENT` formats), CAW Pact parameters table, risk boundaries (see Design Decisions below)
- [ ] Demo walkthrough section: 5 numbered steps that map to P-001 through P-004, each with the expected console output
- [ ] At least one real `logs/audit.json` sample entry included as a code block
- [ ] At least one real Basescan testnet tx link included

**Out of Scope:** Slide deck, video, hosted demo

---

## Key API Notes

### x402 Payment Flow (via CAW native endpoint)

CAW handles x402 signing natively — the agent never constructs payment proofs manually.

**Step 1 — Server returns 402:**
```
HTTP/1.1 402 Payment Required
Payment-Required: <base64-encoded JSON challenge>
```
The `Payment-Required` value is a base64 JSON object containing receiver address, amount, chain, and asset details.

**Step 2 — Agent calls CAW payment endpoint:**
```
POST /api/v1/wallets/{wallet_uuid}/payment
{ "protocol": "x402", "x402_payment_required": "<base64 value from Payment-Required header>", "request_id": "<idempotency-key>" }
```
CAW signs the transaction and returns:
```json
{ "result": { "status": "completed", "retry_headers": { "PAYMENT-SIGNATURE": "..." } } }
```

**Step 3 — Agent retries original request:**
```
GET /api/inference
PAYMENT-SIGNATURE: <value from retry_headers>
```

**Idempotency:** supplying the same `request_id` to the payment endpoint returns the cached result and `retry_headers` without re-signing.

### CAW SDK Imports

```typescript
import { Configuration, PactsApi, TransactionsApi, AuditApi, type PactSpecInput } from '@cobo/agentic-wallet';
```

### CAW Pact Spec Structure

```typescript
const PACT_SPEC: PactSpecInput = {
  policies: [{
    name: "x402-payment-policy",
    type: "transfer",
    rules: {
      effect: "allow",
      when: {
        chain_in: ["SETH"],                                    // Base Sepolia chain ID
        destination_address_in: [{ chain_id: "SETH", address: "0x<receiver>" }],
      },
      deny_if: {
        amount_gt: "0.001",                                    // per-call ceiling
        usage_limits: { rolling_24h: { amount_gt: "0.01" } }, // session budget cap
      },
    },
  }],
  completion_conditions: [
    { type: "time_elapsed", threshold: "3600" },  // 1-hour window
    { type: "tx_count",    threshold: "10" },     // or 10 calls, whichever first
  ],
};
```

### CAW Pact Lifecycle

| State | Meaning |
|-------|---------|
| `pending_approval` | Submitted; awaiting human approval in Cobo app |
| `active` | Approved; pact-scoped API key issued |
| `completed` | Completion condition met; key auto-revoked |
| `rejected` | Human rejected in Cobo app |
| `revoked` | Owner manually revoked |

---

## Risk Boundaries

| Risk | Boundary | Enforced By |
|------|----------|-------------|
| Agent overspends session budget | `deny_if.usage_limits.rolling_24h.amount_gt` in Pact policy | CAW policy engine — hard deny, returns `TRANSFER_LIMIT_EXCEEDED` |
| Agent pays wrong address | `destination_address_in` in Pact `when` clause | CAW policy engine — fail-closed; unmatched destination → deny |
| Agent pays after window expires | `completion_conditions: [{ type: "time_elapsed" }]` | CAW auto-revokes pact-scoped API key on condition trigger |
| Agent pays more than ceiling per call | `deny_if.amount_gt` in Pact policy | CAW policy engine — per-tx hard deny |
| Service provider fakes payment verification | x402 middleware verifies tx on-chain before serving response | x402-express checks Base Sepolia for the tx receipt |
| Audit log tampered locally | Local JSON only; no cryptographic integrity | Known limitation — on-chain tx hash is the authoritative record |
| Testnet ETH drained | Session budget cap + testnet only | Pact completion condition + `AGENT_WALLET_API_URL` points to testnet |

---

## Design Decisions

| Decision             | Choice                              | Why                                                      |
|----------------------|-------------------------------------|----------------------------------------------------------|
| x402 library         | `x402-axios` + `x402-express`       | Coinbase reference implementation; handles full header cycle |
| Payment network      | Base Sepolia testnet                | Cobo agentkit targets Base; free testnet ETH via faucet  |
| Human approval UX    | Terminal CLI (readline)             | Prototype — no UI; keeps the control boundary explicit   |
| Pact storage         | `pact-config.json` (local file)     | Single session; no DB needed for a prototype             |
| Protected endpoint   | Mock AI inference (not real model)  | Keeps prototype self-contained; real model = P-001 upgrade |
| TypeScript runner    | `tsx` (no compile step)             | Fast iteration in experiments/                           |

---

## Out of Scope

- Production wallet with real ETH
- Real AI model integration (replace mock in P-001 to add)
- Multi-agent delegation (A2A) — that belongs in GuildOS
- Web / mobile UI of any kind
- Multiple service endpoints or multi-asset payments
- On-chain Pact registry or audit contract

---

## Related Files

- **Tech.md** — Stack, setup, commands, fix log. Read Product.md first.

## Changelog

| Date       | Change                                                        |
|------------|---------------------------------------------------------------|
| 2026-06-02 | Product.md created — Level 1 setup                           |
| 2026-06-02 | Revised: reframed as explicit-authorization loop; added arch diagram, interaction flow, key API notes, risk boundaries; backlog restructured to provider/consumer/audit/demo split |
