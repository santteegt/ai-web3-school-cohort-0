# 7D Framework (Level 1) — CAW Payment Loop

TypeScript prototype: autonomous agent requests human-approved Cobo Pact budget, calls an x402-protected API stub, CAW executes the micropayment on Base Sepolia, audit trail logged.

## Files to read before coding

- `Product.md` — backlog (P-001–P-005), acceptance criteria, design decisions
- `Tech.md` — stack, conventions (especially the env var and async rules), fix log

## Source file map

| File | P-ID |
|------|------|
| `src/authRequest.ts` | P-001 — terminal auth request + human approval |
| `src/pactConfig.ts` | P-002 — CAW WalletOperator + Pact init |
| `src/stubServer.ts` | P-003 — x402 Express stub server |
| `src/paymentLoop.ts` | P-004 — x402 + CAW payment execution loop |
| `src/auditLog.ts` | P-005 — audit trail (logs/audit.json + Basescan link) |
| `src/index.ts` | Entry point — orchestrates the above |

## Rules

- `async/await` only — no callbacks
- No `any` type — use `unknown` + type guards
- All env vars through `src/config.ts`
- No mainnet — Base Sepolia (chain ID 84532) only
- x402 payments via `x402-axios` interceptor, not hand-rolled headers
- After completing a P-ID: update its status in `Product.md`, run `npm run typecheck`
