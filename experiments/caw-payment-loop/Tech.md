# Tech — CAW Payment Loop

> How we build, test, and run this prototype.
> Read **Product.md** first — it defines WHAT to build. This file defines HOW.

---

## Stack

| Layer            | Choice                        | Version  |
|------------------|-------------------------------|----------|
| Language         | TypeScript                    | 5.x      |
| Runtime          | Node.js                       | 20+      |
| TS runner        | tsx (no compile step)         | latest   |
| Agent wallet SDK | @cobo/agentic-wallet          | latest   |
| HTTP client      | axios                         | 1.x      |
| Stub server      | Express                       | 4.x      |
| x402 server      | x402-express (Coinbase)       | latest   |
| Package manager  | pnpm                          |          |
| Network          | Base Sepolia (SETH chain ID)  |          |

---

## Project Structure

```
experiments/caw-payment-loop/
├── Product.md              ← what to build (read first)
├── Tech.md                 ← this file
├── CLAUDE.md               ← AI agent rules
├── .env.example            ← env var template (copy → .env)
├── package.json
├── tsconfig.json
├── pact-config.json        ← created at runtime by P-001 on human approval
├── logs/
│   └── audit.json          ← created at runtime by P-005
└── src/
    ├── index.ts            ← entry point: orchestrates the full loop
    ├── authRequest.ts      ← P-001: terminal auth request + approval
    ├── pactConfig.ts       ← P-002: CAW WalletOperator + Pact init
    ├── stubServer.ts       ← P-003: x402-protected Express endpoint
    ├── paymentLoop.ts      ← P-004: axios + x402 interceptor + CAW pay
    └── auditLog.ts         ← P-005: append to logs/audit.json + print tx link
```

---

## Setup

```bash
cd experiments/caw-payment-loop
pnpm install
cp .env.example .env
# Fill in AGENT_WALLET_API_KEY, AGENT_WALLET_WALLET_ID, STUB_SERVER_ADDRESS in .env

# Terminal 1 — start the stub server
pnpm stub

# Terminal 2 — run the payment loop (prompts for Pact approval if no pact-config.json)
pnpm dev
```

---

## Environment Variables

| Variable                | Purpose                                   | Default                              |
|-------------------------|-------------------------------------------|--------------------------------------|
| `AGENT_WALLET_API_URL`  | CAW API base URL                          | `https://api.agenticwallet.cobo.com` |
| `AGENT_WALLET_API_KEY`  | Agent API key (from `caw onboard`)        | —                                    |
| `AGENT_WALLET_WALLET_ID`| Wallet UUID (from `caw onboard`)          | —                                    |
| `STUB_SERVER_PORT`      | Port for the x402 stub server             | `3402`                               |
| `STUB_SERVER_ADDRESS`   | Receiver address for x402 payments        | —                                    |
| `BASESCAN_URL`          | Basescan testnet base URL                 | `https://sepolia.basescan.org`       |

---

## Conventions

- `const` / `let` only — no `var`
- `async/await` only — no callbacks, no raw `.then()` chains
- No `any` type — use `unknown` + type guards where needed
- All env vars read via a single `src/config.ts` (not scattered `process.env.X` calls)
- No side effects at module load time — everything behind exported functions
- x402 payment flow: call CAW's `POST /wallets/{id}/payment` with the raw `Payment-Required` header value; use returned `retry_headers["PAYMENT-SIGNATURE"]` on the retry — do not sign payments manually

---

## Testing

| Test       | Command                   | Last Run | Result |
|------------|---------------------------|----------|--------|
| Lint       | `pnpm lint`               |          |        |
| Type check | `pnpm typecheck`          |          |        |
| Run loop   | `pnpm dev`                |          |        |

> This is a prototype — unit tests are out of scope. Type check + manual loop run is the bar.

---

## Deployment

**Method:** Local run only — `npx tsx src/index.ts`
**Network:** Base Sepolia testnet
**Wallet funding:** Use the [Base Sepolia faucet](https://www.coinbase.com/faucets/base-ethereum-goerli-faucet)

---

## Fix Log

### Open

| ID | Error | Cause | Status |
|----|-------|-------|--------|
|    |       |       |        |

### Resolved

| ID | Error | Cause | Fix | Date |
|----|-------|-------|-----|------|
|    |       |       |     |      |

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing required environment variable: AGENT_WALLET_API_KEY` | Env var not set | Copy `.env.example` → `.env` and fill in keys from `caw onboard` |
| `Payment-Required header missing` | x402 server not returning correct header | Check `x402-express` version; log raw 402 response headers |
| `insufficient funds` on Base Sepolia | Agent wallet has no testnet ETH | Run `caw faucet deposit` or use the Cobo API's `/deposit` endpoint |
| `TRANSFER_LIMIT_EXCEEDED` from CAW | Payment amount exceeds per-tx cap in Pact | Check `deny_if.amount_gt` in Pact policy; reduce amount or re-submit Pact |
| `Pact in terminal status: expired` | Pact's `time_elapsed` completion condition triggered | Submit a new Pact via `authRequest.ts` |
| `ECONNREFUSED :3402` | Stub server not running | Start `npx tsx src/stubServer.ts` first |

---

## Dependencies

| Package                  | Purpose                                              | Version  |
|--------------------------|------------------------------------------------------|----------|
| `@cobo/agentic-wallet`   | CAW SDK — PactsApi, TransactionsApi, AuditApi        | latest   |
| `axios`                  | HTTP client for agent requests to the stub server    | 1.x      |
| `x402-express`           | x402 paywall middleware for Express stub server      | latest   |
| `express`                | Stub server framework                                | 4.x      |
| `tsx`                    | Run TypeScript directly (dev only)                   | latest   |
| `typescript`             | Type checking                                        | 5.x      |
| `@types/node`            | Node type definitions                                | 20.x     |
| `@types/express`         | Express type definitions                             | 4.x      |
