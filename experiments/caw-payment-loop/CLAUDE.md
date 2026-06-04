# CLAUDE.md — CAW Payment Loop

You are working on a **TypeScript prototype of an autonomous agentic payment loop** using Cobo Agentkit (CAW) and the x402 HTTP payment protocol on Base Sepolia testnet.
This is a solo experiment in `experiments/caw-payment-loop/` — not production code.

---

## Files

| File              | What it is                               | When to read / update            |
|-------------------|------------------------------------------|----------------------------------|
| `Product.md`      | Backlog, requirements, design decisions  | Before touching any feature      |
| `Tech.md`         | Stack, conventions, fix log              | Before adding deps or commands   |
| `src/authRequest.ts` | P-001: terminal auth request          | When working on approval flow    |
| `src/pactConfig.ts`  | P-002: CAW WalletOperator + Pact       | When working on wallet/pact init |
| `src/stubServer.ts`  | P-003: x402 Express stub               | When working on the stub API     |
| `src/paymentLoop.ts` | P-004: x402 + CAW payment execution   | When working on the core loop    |
| `src/auditLog.ts`    | P-005: audit trail                     | When working on logging          |

---

## How You Work

### Before building anything
1. Read `Product.md` — check which P-IDs are still Todo, confirm acceptance criteria
2. Read `Tech.md` — confirm stack choices and conventions before adding packages
3. Check the Fix Log in `Tech.md` — if the error you're solving is already there, use that fix first

### While building
- Match the project structure in `Tech.md` — each `src/*.ts` file maps to one P-ID
- Read env vars through `src/config.ts` only — never scatter `process.env.X` in other files
- Use `async/await`; never callbacks or raw `.then()` chains
- No `any` type — use `unknown` + type guards if the shape is uncertain
- x402 payment: use the `x402-axios` interceptor, do not hand-roll payment headers

### After building
- Run `pnpm typecheck` before declaring a feature done
- Update the Status column for the relevant P-ID in `Product.md` (Todo → Building → Done)
- If you hit an error not already in the Fix Log, add it to the Common Errors table in `Tech.md`

---

## When Unsure

**"Should I add a new package?"**
Check `Tech.md` Dependencies first. If the need isn't covered, confirm with the user before `npm install`.

**"Where does this logic go?"**
Map it to the nearest P-ID: auth approval → `authRequest.ts`, pact setup → `pactConfig.ts`, stub server → `stubServer.ts`, payment loop → `paymentLoop.ts`, logging → `auditLog.ts`. If it spans two files, put the orchestration in `index.ts`.

**"What's the x402 payment flow?"**
`paymentLoop.ts` makes the initial request → server returns `402` with `Payment-Required: <base64 JSON>` header → agent calls CAW's `POST /api/v1/wallets/{id}/payment` with `{ protocol: "x402", x402_payment_required: "<base64>" }` → CAW signs and returns `retry_headers["PAYMENT-SIGNATURE"]` → agent retries with that header → receives 200. No manual signing — CAW handles it.

**"What network / chain?"**
Base Sepolia testnet. CAW chain ID is `"SETH"`. Never mainnet. API endpoint via `AGENT_WALLET_API_URL` env var.

**"What is a Pact?"**
A structured delegation submitted via `PactsApi.submitPact()`. Human approves in the Cobo Agentic Wallet app. Once `status === "active"`, CAW issues a pact-scoped API key. Use that key for all subsequent `TransactionsApi` calls. The pact auto-revokes when any completion condition is met (`time_elapsed`, `tx_count`).

---

## Don't

- Don't use `any` type
- Don't use callbacks — always `async/await`
- Don't read `process.env` outside `src/config.ts`
- Don't hardcode wallet addresses, API keys, or wallet IDs — everything via env vars
- Don't connect to mainnet — testnet only (`AGENT_WALLET_API_URL` controls this)
- Don't sign x402 payments manually — always call CAW's `/payment` endpoint
- Don't use the owner API key for transactions — switch to the pact-scoped key returned after approval
- Don't add features not in the Product.md backlog without checking with Santiago first
- Don't create new source files outside `src/` without updating the project structure in `Tech.md`

---

## Customizing

To add a feature: add a row to the backlog in `Product.md`, write acceptance criteria, then build.
To change the network: update `AGENT_WALLET_API_URL` in `.env` and note the change in Tech.md Design Decisions.
To upgrade this to Level 2 (Architecture.md + component registry): run `/SevenD upgrade level 2` in Claude Code.
