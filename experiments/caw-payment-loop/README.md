# CAW Payment Loop

A minimal prototype of an **autonomous agentic payment loop** using:

- **[Cobo Agentic Wallet (CAW)](https://www.cobo.com/products/agentic-wallet)** — MPC wallet with human-approved Pact constraints (budget cap, scope, time window)
- **[x402](https://x402.org)** — HTTP payment protocol (Coinbase) that turns a `402 Payment Required` response into a machine-readable payment challenge

The agent calls an x402-protected AI inference endpoint, recognizes the 402, signs an EIP-3009 authorization within the Pact limits, and retries — all automatically, but only within bounds the human pre-approved.

> **Network:** Base Sepolia testnet (`eip155:84532`)  
> **Language:** TypeScript 5 + Node 20 + pnpm  
> See [`docs/DEMO.md`](docs/DEMO.md) for full architecture, sequence diagram, and expected console output.

---

## Quick Start

### 1. Install the CAW CLI

```bash
npm install -g @cobo/agentic-wallet-cli
caw --version
```

### 2. Onboard — create your agent API key + wallet

```bash
# Create an API key and pair it to a new Cobo wallet
caw onboard --wait

# Pair your mobile Cobo app to the wallet (scan QR code)
caw wallet pair --code-only

# Confirm the pairing is complete
caw wallet pair-status

# List wallet addresses (copy the EVM address — you'll need it for AGENT_WALLET_ADDRESS)
caw address list
```

After `caw onboard` you'll have:
- `AGENT_WALLET_API_KEY` — the API key printed to stdout
- `AGENT_WALLET_WALLET_ID` — the wallet UUID printed to stdout
- `AGENT_WALLET_ADDRESS` — your wallet's EVM address from `caw address list`

### 3. Fund the wallet with testnet USDC

The stub server charges **$0.001 USDC per call**. Top up the wallet address that will pay (either `AGENT_WALLET_ADDRESS` for the CAW path, or your local signer address for the dev bypass):

```bash
# List available tokens on Base Sepolia
caw meta tokens --chain-ids TBASE_SETH

# Request testnet USDC from the Cobo faucet
caw faucet tokens

# Deposit to your wallet address
caw faucet deposit --token-id TBASE_USDC --address <YOUR_WALLET_ADDRESS>
```

Alternatively, get testnet USDC directly from [Circle's faucet](https://faucet.circle.com) (select Base Sepolia).

### 4. Install dependencies

```bash
cd experiments/caw-payment-loop
pnpm install
```

### 5. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in:

| Variable | Where to get it |
|---|---|
| `AGENT_WALLET_API_KEY` | Printed by `caw onboard` |
| `AGENT_WALLET_WALLET_ID` | Printed by `caw onboard` |
| `AGENT_WALLET_ADDRESS` | Printed by `caw address list` |
| `STUB_SERVER_ADDRESS` | Any Base Sepolia address — this receives x402 payments (can be same wallet) |

For the **local signer bypass** (use while CAW's Base Sepolia infrastructure is being restored):

```bash
USE_LOCAL_SIGNER=true
LOCAL_SIGNER_PRIVATE_KEY=0xYOUR_FUNDED_TEST_KEY  # never a key holding real funds
```

> `LOCAL_SIGNER_PRIVATE_KEY` bypasses CAW's MPC signing using `viem.signTypedData` locally.
> The signing key must own the address used as `from` in the EIP-3009 authorization.

### 6. Run the demo — two terminals

**Terminal 1 — start the x402 stub server:**
```bash
pnpm stub
```

**Terminal 2 — run the payment loop:**
```bash
pnpm dev
```

On first run, the loop prompts for Pact authorization. Type `y` and approve the notification in the Cobo mobile app. Subsequent runs reuse the saved pact from `pact-config.json` until it expires (default: 1 hour).

---

## What Happens

```
pnpm dev
  └─ Checks pact-config.json         (P-002: Pact Authorization)
      └─ Not found → CLI prompt → human approves in Cobo app
      └─ Found + valid → skips auth
  └─ Loop CALL_COUNT times            (P-003 + P-004: Payment Loop)
      ├─ GET /api/inference → 402 + PAYMENT-REQUIRED header
      ├─ Decode base64 payment challenge
      ├─ Sign EIP-3009 TransferWithAuthorization (CAW or local signer)
      ├─ Retry with PAYMENT-SIGNATURE header → 200 inference result
      └─ Append audit record to logs/audit.json
  └─ Print session summary            (P-005: Audit trail)
```

See [`docs/DEMO.md`](docs/DEMO.md) for the full interaction sequence, x402 header format, and expected console output.

---

## Project Files

| File | Purpose |
|---|---|
| [`Product.md`](Product.md) | Vision, backlog (P-001–P-005), requirements, architecture |
| [`Tech.md`](Tech.md) | Stack, env vars, conventions, fix log |
| [`docs/DEMO.md`](docs/DEMO.md) | Full demo guide — architecture diagram, sequence, API spec, walkthrough |
| [`docs/`](docs/) | Cobo CAW reference docs (downloaded from llms.txt) |
| `src/stubServer.ts` | P-001 — x402-protected Express endpoint |
| `src/pactConfig.ts` | P-002 — CAW Pact submit, poll, and load |
| `src/paymentLoop.ts` | P-003+P-004 — 402→sign→retry loop |
| `src/auditLog.ts` | P-005 — `logs/audit.json` writer + session summary |
| `src/localSigner.ts` | Dev bypass — local EIP-712 signer via viem |
| `src/config.ts` | Single source for all env vars |
| `src/index.ts` | Entry point — orchestrates everything |
| `.env.example` | Environment variable template |
| `pact-config.json` | Created at runtime after Pact approval (gitignored) |
| `logs/audit.json` | Created at runtime — one record per paid call |

---

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `AGENT_WALLET_API_URL` | `https://api.agenticwallet.cobo.com` | CAW API base URL |
| `AGENT_WALLET_API_KEY` | — | Agent API key from `caw onboard` |
| `AGENT_WALLET_WALLET_ID` | — | Wallet UUID from `caw onboard` |
| `AGENT_WALLET_ADDRESS` | — | Wallet EVM address from `caw address list` |
| `CAW_CHAIN_ID` | `TBASE_SETH` | Cobo chain ID for Base Sepolia |
| `STUB_SERVER_PORT` | `3402` | Port for the x402 stub server |
| `STUB_SERVER_ADDRESS` | — | Address that receives x402 payments |
| `PRICE_PER_CALL_USD` | `0.001` | Price the stub charges per inference call |
| `PACT_PER_CALL_CEILING_USD` | `0.01` | Pact rejects calls above this amount |
| `PACT_SESSION_BUDGET_USD` | `0.10` | Rolling 24h Pact spend cap |
| `PACT_WINDOW_SECONDS` | `3600` | Pact auto-revokes after this many seconds |
| `CALL_COUNT` | `3` | Number of paid calls per `pnpm dev` run |
| `BASESCAN_URL` | `https://sepolia.basescan.org` | Used for audit log tx links |
| `USE_LOCAL_SIGNER` | `false` | Set `true` to bypass CAW MPC signing |
| `LOCAL_SIGNER_PRIVATE_KEY` | — | Dev-only test key for local EIP-712 signing |

---

## Commands

```bash
pnpm stub        # Start the x402 stub server (Terminal 1)
pnpm dev         # Run the payment loop (Terminal 2)
pnpm typecheck   # TypeScript type check (no output = clean)
pnpm lint        # ESLint
```

---

## CAW Pact — Key Concepts

A **Pact** is a human-approved delegation agreement submitted to CAW before any payments happen. It bounds the agent to:

- **Destination address** — can only pay the approved receiver
- **Per-call ceiling** — rejects any x402 charge above `PACT_PER_CALL_CEILING_USD`
- **Rolling budget** — enforces a 24h spend cap of `PACT_SESSION_BUDGET_USD`
- **Time window** — Pact auto-revokes after `PACT_WINDOW_SECONDS`

Once the human approves (via Cobo mobile app), CAW issues a **pact-scoped API key** saved to `pact-config.json`. All payment calls use that scoped key — not the owner key.

Full Pact parameter reference: [`docs/DEMO.md § 4`](docs/DEMO.md#4-caw-pact-parameters)

---

## Active Workaround (2026-06-06)

Cobo's Base Sepolia indexing nodes are currently experiencing issues (`X402_INSUFFICIENT_BALANCE / available: "0"` and `messageSign` MPC stalls). The normal `txApi.payment()` path is temporarily replaced by a local EIP-712 signer using `viem`.

**To activate:** set `USE_LOCAL_SIGNER=true` and `LOCAL_SIGNER_PRIVATE_KEY=<funded test key>` in `.env`.

**To restore the production path** once Cobo confirms recovery: see [`docs/DEMO.md § 8`](docs/DEMO.md#8-restoring-the-caw-production-path).

---

## References

- [Cobo Agentic Wallet docs](https://www.cobo.com/products/agentic-wallet/manual/llms.txt) — full CAW SDK + API reference
- [x402 protocol](https://x402.org) — HTTP payment standard
- [x402 GitHub](https://github.com/coinbase/x402) — source for `@x402/express`, `@x402/core`, `@x402/evm`
- [Base Sepolia Faucet](https://www.coinbase.com/faucets/base-ethereum-goerli-faucet)
- [Circle USDC Faucet](https://faucet.circle.com) — testnet USDC on Base Sepolia
- [Basescan (Base Sepolia)](https://sepolia.basescan.org) — tx explorer
