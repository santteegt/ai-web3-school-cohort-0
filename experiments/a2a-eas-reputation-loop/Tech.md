# Tech.md — A2A × EAS × ERC-8004 Reputation Loop PoC

> SevenD Level-1 | PoC scope only

---

## Stack

| Layer | Technology |
|-------|-----------|
| Language | TypeScript (ESM, Node 20+) |
| Package manager | pnpm |
| Agent scaffold | create-8004-agent structure (reproduced by hand — wizard is interactive-only) |
| ERC-8004 calls | ethers v6 — direct contract calls (no agent0-sdk / Pinata needed) |
| A2A protocol | **@a2a-js/sdk** v0.3 — `AgentExecutor` server + `ClientFactory` client |
| EAS | @ethereum-attestation-service/eas-contracts (ABIs only — SDK bypassed due to lodash ESM issue) |
| Runtime utilities | dotenv, uuid, express, tsx (dev runner) |

---

## Project Structure

```
experiments/a2a-eas-reputation-loop/
├── .env                     # PRIVATE_KEY_CLIENT, PRIVATE_KEY_DEV (gitignored)
├── .gitignore               # excludes .env, node_modules, dist, state.json
├── package.json             # pnpm demo | pnpm dev:server
├── tsconfig.json
├── Product.md               # SevenD Level-1 product spec + backlog
├── Tech.md                  # (this file)
├── CLAUDE.md                # PoC-scoped agent rules
├── README.md                # What the PoC proves + how to run
├── RUN_LOG.md               # Live on-chain evidence (tx hashes, UIDs)
├── state.json               # Persisted run state (gitignored)
└── src/
    ├── abis.ts              # ERC-8004 IdentityRegistry + ReputationRegistry ABIs
    ├── config.ts            # Env, provider, signers, addresses, logger
    ├── state.ts             # Load/save state.json
    ├── identity.ts          # Step 1 — register CLIENT + DEV on ERC-8004
    ├── attest-eas.ts        # Step 3 — EAS schema registration + attestation
    ├── dev-server.ts        # DEV's A2A server — @a2a-js/sdk AgentExecutor (port 3001)
    ├── coordinate-a2a.ts    # Step 2 — CLIENT delegates task via @a2a-js/sdk ClientFactory
    ├── approve.ts           # Step 4 — CLIENT verifies EAS, sends A2A "accepted" via SDK client
    ├── feedback.ts          # Steps 5-6 — DEV review request + CLIENT giveFeedback
    └── demo.ts              # Orchestrates full 6-step loop
```

---

## Setup and Run

### One-time setup
```bash
cd experiments/a2a-eas-reputation-loop
pnpm install

# Ensure .env exists with:
# PRIVATE_KEY_CLIENT=<pre-funded Base Sepolia EOA>
# PRIVATE_KEY_DEV=<pre-funded Base Sepolia EOA>
# RPC_URL=https://sepolia.base.org  (optional — this is the default)
```

### Run the full 6-step demo
```bash
pnpm run demo
```
Spawns the DEV A2A server inline, runs all steps, prints on-chain evidence, appends to RUN_LOG.md.

### Run just the DEV server (separate terminal)
```bash
pnpm run dev:server
# DEV A2A server (SDK) listening at http://localhost:3001
# Agent card:    GET  http://localhost:3001/.well-known/agent-card.json
# A2A endpoint:  POST http://localhost:3001/a2a/jsonrpc
```

### Run identity registration only
```bash
pnpm run identity
```

---

## Conventions

- Never log or echo private keys; log public addresses freely
- All BigInt values use `n` suffix in TypeScript (e.g., `100n`)
- ReputationRegistry `giveFeedback` takes `int128` for value (not int256)
- EAS schema UID is deterministic — always compute before attempting to register
- State file (`state.json`) stores all on-chain IDs so re-runs are idempotent

---

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `PRIVATE_KEY_CLIENT` | ✅ | — | CLIENT signer for ERC-8004 identity + giveFeedback |
| `PRIVATE_KEY_DEV` | ✅ | — | DEV signer for ERC-8004 identity + EAS attestation |
| `RPC_URL` | ❌ | `https://sepolia.base.org` | Base Sepolia RPC endpoint |
| `DEV_PORT` | ❌ | `3001` | DEV A2A server port |

---

## Contract Addresses (Base Sepolia, chain_id 84532)

| Contract | Address |
|----------|---------|
| ERC-8004 IdentityRegistry | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| ERC-8004 ReputationRegistry | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| EAS | `0x4200000000000000000000000000000000000021` |
| SchemaRegistry | `0x4200000000000000000000000000000000000020` |
