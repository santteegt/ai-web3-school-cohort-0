# CAW Payment Loop — Demo Guide

> **Prototype:** Agentic Payment Loop using Cobo Agentic Wallet (CAW) + x402  
> **Network:** Base Sepolia testnet (eip155:84532)  
> **Status:** P-001–P-004 complete; P-005 (this document)

---

## 1. Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CAW Payment Loop                                │
│                                                                         │
│   ┌─────────────────────┐            ┌──────────────────────────────┐   │
│   │   CONSUMER SIDE     │            │    SERVICE PROVIDER SIDE     │   │
│   │                     │            │                              │   │
│   │  ┌───────────────┐  │            │  ┌────────────────────────┐  │   │
│   │  │  index.ts     │  │            │  │  stubServer.ts         │  │   │
│   │  │  (orchestrator│  │            │  │  Express + @x402/      │  │   │
│   │  │   CALL_COUNT  │  │            │  │  express middleware     │  │   │
│   │  │   iterations) │  │            │  │                        │  │   │
│   │  └──────┬────────┘  │            │  │  GET /api/inference    │  │   │
│   │         │           │   HTTP     │  │  ────────────────────  │  │   │
│   │  ┌──────▼────────┐  │◄──GET─────►│  │  No payment → 402 +   │  │   │
│   │  │ paymentLoop.ts│  │   402      │  │  PAYMENT-REQUIRED hdr  │  │   │
│   │  │               │  │◄──────────┤  │                        │  │   │
│   │  │  1. GET →402  │  │           │  │  Valid sig → 200 JSON  │  │   │
│   │  │  2. Decode    │  │  Retry +  │  └───────────┬────────────┘  │   │
│   │  │     payload   │  │  PAYMENT- │              │               │   │
│   │  │  3. Sign EIP- │  │  SIGNATURE│              │ verify/settle │   │
│   │  │     3009      │  │──────────►│  ┌───────────▼────────────┐  │   │
│   │  │  4. Retry→200 │  │           │  │  x402.org/facilitator  │  │   │
│   │  │  5. Audit log │  │           │  │  (testnet verify +     │  │   │
│   │  └──────┬────────┘  │           │  │   settle on-chain)     │  │   │
│   │         │           │           │  └────────────────────────┘  │   │
│   │  ┌──────▼────────┐  │           │                              │   │
│   │  │ pactConfig.ts │  │           └──────────────────────────────┘   │
│   │  │  (Pact state) │  │                                              │
│   │  └──────┬────────┘  │           ┌──────────────────────────────┐   │
│   │         │           │           │  COBO AGENTIC WALLET (CAW)   │   │
│   │  ┌──────▼────────┐  │           │                              │   │
│   │  │ auditLog.ts   │  │           │  • MPC wallet (TBASE_SETH)   │   │
│   │  │ logs/audit.json│ │           │  • Pact: budget + time cap   │   │
│   │  └───────────────┘  │           │  • messageSign: EIP-712      │   │
│   │                     │           │  • payment: x402 native      │   │
│   └─────────────────────┘           └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

Signing paths (USE_LOCAL_SIGNER controls which is active):
  Production (CAW):   paymentLoop → CAW /wallets/{id}/payment → EIP-3009 sig
  Dev bypass (local): paymentLoop → localSigner.ts (viem signTypedData) → EIP-3009 sig
```

---

## 2. Interaction Sequence

```
Operator         index.ts          pactConfig.ts      CAW API         stubServer       x402 facilitator
   │                │                   │               │                │                  │
   │  pnpm dev      │                   │               │                │                  │
   │───────────────►│                   │               │                │                  │
   │                │  loadActivePact() │               │                │  pnpm stub       │
   │                │──────────────────►│               │                │◄─────────────────│
   │                │  (not found)      │               │                │  listening :3402 │
   │                │◄──────────────────│               │                │                  │
   │                │                   │               │                │                  │
   │   ┌─── STEP 1: AUTHORIZATION ──────────────────────────────────┐   │                  │
   │   │            │  requestAndSubmitPact()                        │   │                  │
   │   │            │──────────────────►│                           │   │                  │
   │   │            │                   │  PactsApi.submitPact()    │   │                  │
   │   │            │                   │──────────────────────────►│   │                  │
   │   │ Approve?   │                   │  pact_id + pending_approval│   │                  │
   │◄──┤            │                   │◄──────────────────────────│   │                  │
   │   │ [y]        │                   │  (human approves in app)  │   │                  │
   │───┤            │                   │  poll → status=active     │   │                  │
   │   │            │                   │──────────────────────────►│   │                  │
   │   │            │                   │  ← pact_api_key           │   │                  │
   │   │            │                   │◄──────────────────────────│   │                  │
   │   │            │  saves pact-config.json                       │   │                  │
   │   └────────────────────────────────────────────────────────────┘   │                  │
   │                │                   │               │                │                  │
   │   ┌─── STEP 2: PAYMENT LOOP (×CALL_COUNT) ────────────────────────────────────────┐  │
   │   │            │                   │               │                │               │  │
   │   │            │  runPaymentLoop() │               │                │               │  │
   │   │            │  GET /api/inference               │                │               │  │
   │   │            │───────────────────────────────────────────────────►│               │  │
   │   │            │  ← 402 + PAYMENT-REQUIRED header  │                │               │  │
   │   │            │◄───────────────────────────────────────────────────│               │  │
   │   │            │                   │               │                │               │  │
   │   │            │  decode base64 → PaymentAccept    │                │               │  │
   │   │            │  build EIP-712 TransferWithAuthorization           │               │  │
   │   │            │                   │               │                │               │  │
   │   │  [CAW path]│  POST /wallets/{id}/payment       │                │               │  │
   │   │            │──────────────────────────────────►│               │               │  │
   │   │            │  ← retry_headers[PAYMENT-SIGNATURE]               │               │  │
   │   │            │◄──────────────────────────────────│               │               │  │
   │   │  [local]   │  localSignEip3009() → sig         │                │               │  │
   │   │            │  build PAYMENT-SIGNATURE header   │                │               │  │
   │   │            │                   │               │                │               │  │
   │   │            │  retry GET /api/inference (+ PAYMENT-SIGNATURE)    │               │  │
   │   │            │───────────────────────────────────────────────────►│               │  │
   │   │            │                   │               │  verify + settle              │  │
   │   │            │                   │               │               │──────────────►│  │
   │   │            │                   │               │               │◄──────────────│  │
   │   │            │  ← 200 inference JSON             │                │               │  │
   │   │            │◄───────────────────────────────────────────────────│               │  │
   │   │            │  appendAuditRecord() → logs/audit.json             │               │  │
   │   └────────────────────────────────────────────────────────────────────────────────┘  │
   │                │                   │               │                │                  │
   │   ┌─── STEP 3: SUMMARY ──────────────────┐         │                │                  │
   │   │            │  printSessionSummary()  │         │                │                  │
   │◄──┤            │  total spend / results  │         │                │                  │
   │   └────────────────────────────────────────         │                │                  │
```

---

## 3. x402 Payment Header Specification

### 3a. Challenge — `PAYMENT-REQUIRED` (server → client, on 402)

The server returns this header on every unauthenticated request. Value is a **base64-encoded JSON string**.

**Decoded structure:**
```json
{
  "x402Version": 2,
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:84532",
      "amount": "1000",
      "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      "payTo": "0xRECEIVER_ADDRESS",
      "maxTimeoutSeconds": 300,
      "extra": {
        "name": "USDC",
        "version": "2"
      }
    }
  ]
}
```

| Field | Description |
|---|---|
| `x402Version` | Protocol version (always `2` for current x402) |
| `scheme` | `"exact"` — fixed-amount EIP-3009 transfer |
| `network` | CAIP-2 chain identifier (`eip155:84532` = Base Sepolia) |
| `amount` | Token amount in atomic units (`"1000"` = $0.001 USDC, 6 decimals) |
| `asset` | USDC contract address on Base Sepolia |
| `payTo` | Receiver address (stub server operator) |
| `maxTimeoutSeconds` | Validity window for the payment authorization |
| `extra.name/version` | EIP-712 domain separator components |

### 3b. Payment Proof — `PAYMENT-SIGNATURE` (client → server, on retry)

Client builds and sends this header after signing. Value is a **base64-encoded JSON string**.

**Decoded structure:**
```json
{
  "x402Version": 2,
  "accepted": {
    "scheme": "exact",
    "network": "eip155:84532",
    "amount": "1000",
    "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "payTo": "0xRECEIVER_ADDRESS",
    "maxTimeoutSeconds": 300,
    "extra": { "name": "USDC", "version": "2" }
  },
  "payload": {
    "signature": "0xSIGNATURE_HEX",
    "authorization": {
      "from": "0xPAYER_ADDRESS",
      "to": "0xRECEIVER_ADDRESS",
      "value": "1000",
      "validAfter": "1749200000",
      "validBefore": "1749200300",
      "nonce": "0xRANDOM_32_BYTES"
    }
  }
}
```

**EIP-712 / EIP-3009 typed data signed:**
```
domain:
  name:              "USDC"
  version:           "2"
  chainId:           84532
  verifyingContract: 0x036CbD53842c5426634e7929541eC2318f3dCF7e

type: TransferWithAuthorization
  from:        address    (payer — CAW wallet or local signer)
  to:          address    (receiver — stub server)
  value:       uint256    (atomic USDC units, e.g. 1000)
  validAfter:  uint256    (unix timestamp — 10 min past grace)
  validBefore: uint256    (unix timestamp — now + maxTimeoutSeconds)
  nonce:       bytes32    (random 32 bytes, one-time use)
```

---

## 4. CAW Pact Parameters

| Parameter | Env var | Default | Effect |
|---|---|---|---|
| Per-call ceiling | `PACT_PER_CALL_CEILING_USD` | `$0.01` | Rejects any x402 asking more than this per call |
| Session budget | `PACT_SESSION_BUDGET_USD` | `$0.10` | Rolling 24h spend cap enforced by Cobo |
| Time window | `PACT_WINDOW_SECONDS` | `3600` | Pact auto-revokes after this many seconds |
| Chain | `CAW_CHAIN_ID` | `TBASE_SETH` | Base Sepolia testnet chain identifier |
| Price per call | `PRICE_PER_CALL_USD` | `$0.001` | Stub server x402 price ($0.001 = 1000 USDC atomic units) |
| Call count | `CALL_COUNT` | `3` | Number of paid calls per `pnpm dev` run |

**PactSpec submitted to CAW:**
```json
{
  "policies": [
    {
      "name": "x402-inference-payment",
      "type": "transfer",
      "rules": {
        "effect": "allow",
        "when": {
          "chain_in": ["TBASE_SETH"],
          "destination_address_in": [{ "chain_id": "TBASE_SETH", "address": "0xRECEIVER" }]
        },
        "deny_if": {
          "amount_usd_gt": "0.01",
          "usage_limits": { "rolling_24h": { "amount_usd_gt": "0.10" } }
        }
      }
    },
    {
      "name": "x402-eip712-signing",
      "type": "message_sign",
      "rules": {
        "effect": "allow",
        "when": { "chain_in": ["TBASE_SETH"] }
      }
    }
  ],
  "completion_conditions": [{ "type": "time_elapsed", "threshold": "3600" }]
}
```

**Pact lifecycle:**
```
submit → pending_approval → [human approves in Cobo app] → active → completed/expired/revoked
                          → rejected (if human denies)
```

Once active, CAW issues a **pact-scoped API key** stored in `pact-config.json`. All subsequent payment calls use that key — not the owner key.

---

## 5. Risk Boundaries

| Risk | Mitigation | Status |
|---|---|---|
| Runaway spending | Pact per-call ceiling ($0.01) + rolling 24h cap ($0.10) | Enforced by Cobo |
| Expired authorization | `loadActivePact()` checks `expiresAt` before each run | Code-level guard |
| Budget exceeded mid-session | Loop stops on `TRANSFER_LIMIT_EXCEEDED` code | Handled in `index.ts` |
| Malicious server overcharging | Client checks amount against `PACT_PER_CALL_CEILING_USD` before signing | Pre-sign check |
| Replay attack (nonce reuse) | Random 32-byte nonce per call; EIP-3009 contract rejects replays | Protocol-level |
| Timestamp window attack | `validAfter`=now-600, `validBefore`=now+maxTimeout; short window | EIP-712 domain |
| Local key exposure | `LOCAL_SIGNER_PRIVATE_KEY` in `.env` only; `.gitignore`-d | Dev-only bypass |
| On-chain data leakage | `pact-config.json` is `.gitignore`-d; no secrets in source files | Policy enforced |
| Mainnet access | `AGENT_WALLET_API_URL` points to testnet; CAW chain is `TBASE_SETH` | Env-controlled |
| CAW infra outage | Local signer bypass (`USE_LOCAL_SIGNER=true`) for dev continuity | Active workaround |

---

## 6. Demo Walkthrough

### Prerequisites

```bash
# Install dependencies
cd experiments/caw-payment-loop
pnpm install

# Configure environment
cp .env.example .env
# Fill in:
#   AGENT_WALLET_API_KEY=     ← from `caw onboard`
#   AGENT_WALLET_WALLET_ID=   ← from `caw onboard`
#   AGENT_WALLET_ADDRESS=     ← your CAW MPC wallet EVM address
#   STUB_SERVER_ADDRESS=      ← any Base Sepolia address to receive test USDC
#
# For local signer (dev bypass while Cobo infra is down):
#   USE_LOCAL_SIGNER=true
#   LOCAL_SIGNER_PRIVATE_KEY= ← funded testnet key (never a key holding real funds)
```

### Step 1 — Start the stub server (Terminal 1)

```bash
pnpm stub
```

**Expected output:**
```
[stub] x402 inference API running
[stub]   endpoint:  http://localhost:3402/api/inference
[stub]   health:    http://localhost:3402/health
[stub]   payTo:     0xRECEIVER_ADDRESS
[stub]   price:     $0.001 USDC per call
[stub]   network:   Base Sepolia (eip155:84532)
[stub]   facilitator: https://x402.org/facilitator
[stub] Waiting for requests...
```

### Step 2 — Run the payment loop (Terminal 2)

```bash
pnpm dev
```

**Expected output — authorization flow (first run only):**
```
╔══════════════════════════════════════╗
║        CAW Payment Loop v0.1         ║
╚══════════════════════════════════════╝
  CAW API:  https://api.agenticwallet.cobo.com
  Wallet:   wlt_abc123...
  Stub:     http://localhost:3402/api/inference
  Calls:    3
═══════════════════════════════════════

[main] No active pact found: No ./pact-config.json found.
[main] Starting authorization flow...

╔═══════════════════════════════════════════╗
║      CAW Pact Authorization Request       ║
╚═══════════════════════════════════════════╝
  Endpoint:          http://localhost:3402/api/inference
  Receiver address:  0xRECEIVER_ADDRESS
  Per-call ceiling:  $0.01 USD
  Session budget:    $0.10 USD
  Time window:       3600s (expires 2026-06-06T15:00:00.000Z)
  Chain:             TBASE_SETH (Base Sepolia)
  Network:           eip155:84532
═══════════════════════════════════════════

Approve this authorization? [y/N]: y

[pact] Submitting pact to Cobo...
[pact] Submitted: id=pact_xyz789 — status=pending_approval
[pact] Open the Cobo Agentic Wallet app on your phone and approve the pact...
[pact] status → pending_approval
[pact] status → active

[pact] ✓ Active. Config saved to ./pact-config.json
  Pact ID:        pact_xyz789
  Per-call cap:   $0.01 USD
  Session budget: $0.10 USD
  Expires:        2026-06-06T15:00:00.000Z
```

**Expected output — payment loop (3 calls):**
```
[main] Starting 3 paid inference calls...

──── Call 1 / 3 ────────────────────────────────
[loop:1] → GET http://localhost:3402/api/inference
[loop:1] ← 402 Payment Required
[loop:1]   PAYMENT-REQUIRED: eyJ4NDAyVmVyc2lvbiI6Miw…
[loop:1]   paymentRequired (decoded): {
  "x402Version": 2,
  "accepts": [{ "scheme": "exact", "network": "eip155:84532", "amount": "1000", ... }]
}
[loop:1] → local EIP-712 sign (USE_LOCAL_SIGNER=true, from: 0xPAYER)
[loop:1] ← locally signed: 0x1234abcd...
[loop:1] → retry GET http://localhost:3402/api/inference (with PAYMENT-SIGNATURE)
[loop:1] ← 200 OK
[loop:1]   result: "Machine-to-machine payments unlock composable service markets."
[audit] ✓ Record saved to ./logs/audit.json
[audit]   Basescan: https://sepolia.basescan.org/tx/0xTX_HASH

──── Call 2 / 3 ────────────────────────────────
...

──── Call 3 / 3 ────────────────────────────────
...

[main] Loop complete: 3/3 calls succeeded

╔════════════════════════════════╗
║       Session Summary          ║
╚════════════════════════════════╝
  Successful calls: 3
  Total spent:      $0.0030 USD
  Last result:      "On-chain authorization creates auditable, enforceable permission boundaries."
  Last tx:          https://sepolia.basescan.org/tx/0xTX_HASH
  Audit log:        ./logs/audit.json
════════════════════════════════
```

### Step 3 — Verify type safety

```bash
pnpm typecheck
# Expected: no output (clean)
```

---

## 7. Sample Audit Record

`logs/audit.json` after one successful session:

```json
[
  {
    "timestamp": "2026-06-06T14:01:23.456Z",
    "pactId": "pact_xyz789",
    "endpoint": "http://localhost:3402/api/inference",
    "amountPaidUsd": "0.001",
    "txHash": "0xabc123def456789abcdef0123456789abcdef0123456789abcdef0123456789ab",
    "receiverAddress": "0xRECEIVER_ADDRESS",
    "responseStatus": 200,
    "resultSnippet": "Machine-to-machine payments unlock composable service markets."
  },
  {
    "timestamp": "2026-06-06T14:01:25.789Z",
    "pactId": "pact_xyz789",
    "endpoint": "http://localhost:3402/api/inference",
    "amountPaidUsd": "0.001",
    "txHash": "0xdef456abc789012345678901234567890123456789012345678901234567890123",
    "receiverAddress": "0xRECEIVER_ADDRESS",
    "responseStatus": 200,
    "resultSnippet": "Decentralized trust enables autonomous coordination without intermediaries."
  },
  {
    "timestamp": "2026-06-06T14:01:28.012Z",
    "pactId": "pact_xyz789",
    "endpoint": "http://localhost:3402/api/inference",
    "amountPaidUsd": "0.001",
    "txHash": null,
    "receiverAddress": "0xRECEIVER_ADDRESS",
    "responseStatus": 200,
    "resultSnippet": "On-chain authorization creates auditable, enforceable permission boundaries."
  }
]
```

---

## 8. Restoring the CAW Production Path

The current code uses a local signer workaround due to a Cobo Base Sepolia node indexing
issue (as of 2026-06-06). Once Cobo confirms infrastructure recovery, restore the normal
flow in `src/paymentLoop.ts`:

1. Delete the `WORKAROUND START → WORKAROUND END` comment block (lines ~109–310).
2. Uncomment the `txApi.payment()` block that follows it.
3. Set `USE_LOCAL_SIGNER=false` in `.env`.
4. The `message_sign` policy in `pactConfig.ts` can be removed from the PactSpec
   (only the `transfer` policy is needed for the production path).

**Normal CAW x402 payment call:**
```typescript
const resp = await txApi.payment(config.caw.walletId, {
  protocol: 'x402',
  x402_payment_required: paymentRequired,  // raw base64 from PAYMENT-REQUIRED header
  request_id: requestId,
});
// resp.data.result.retry_headers['PAYMENT-SIGNATURE'] → use directly for retry
```

---

## 9. Known Issues & Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Missing required environment variable: AGENT_WALLET_API_KEY` | `.env` not populated | `cp .env.example .env` and fill values |
| `Got 402 but PAYMENT-REQUIRED header is missing` | `@x402/express` not wired | Ensure `stubServer.ts` uses `paymentMiddleware` with `accepts: [...]` array |
| `TRANSFER_LIMIT_EXCEEDED` | Pact session budget hit | Wait 24h or submit new pact with higher budget |
| `Pact expired` | `PACT_WINDOW_SECONDS` elapsed | Delete `pact-config.json`, run again |
| `X402_INSUFFICIENT_BALANCE / available: "0"` | Cobo node indexing outage | Set `USE_LOCAL_SIGNER=true` |
| `messageSign stuck in "signing"` | CAW MPC ceremony stalled | Same as above — local signer bypass |
| `token_not_mapped` for USDC address | Cobo hasn't indexed the token | Contact Cobo to register `0x036CbD53842c5426634e7929541eC2318f3dCF7e` on `TBASE_SETH` |
| `paymentRequired could not be decoded as base64 JSON` | Wrong facilitator URL | Use `https://x402.org/facilitator` (not `https://facilitator.x402.org`) |

---

*Generated by Sensei (Claude via Cowork) — 2026-06-06*
