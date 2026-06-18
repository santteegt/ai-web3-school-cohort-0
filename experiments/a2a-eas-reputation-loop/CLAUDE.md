# CLAUDE.md — A2A × EAS × ERC-8004 Reputation Loop PoC

> Scope: experiments/a2a-eas-reputation-loop/ ONLY.
> This file governs AI agent behavior for this sub-directory.
> Read Product.md + Tech.md before writing a single line of code.

---

## Required Context Load

Before writing any code in this directory, read:
1. `Product.md` — backlog, acceptance criteria, SDK design decisions
2. `Tech.md` — stack, file structure, env vars, contract addresses

---

## The 6-Step Workflow (must implement in order)

```
Step 1 — Identity:     CLIENT registers ERC-8004 identity; DEV registers ERC-8004 identity (with A2A endpoint in agentURI)
Step 2 — Coordinate:   CLIENT resolves DEV's A2A agent card; sends task "Write a hello world script in Python" via A2A
Step 3 — Attest:       DEV generates hello_world.py; computes keccak256 hash; calls EAS.attest() → attestation UID; returns artifact with UID embedded
Step 4 — Approve:      CLIENT reads artifact; recomputes hash; calls eas.getAttestation(uid); asserts hash match; sends A2A "accepted"
Step 5 — Review req:   DEV sends A2A follow-up requesting review (same context/task)
Step 6 — Feedback:     CLIENT calls ERC-8004 ReputationRegistry.giveFeedback(devAgentId, 100, 0, "code", "accepted", ...); proves getSummary count 0→1
```

---

## SECRETS — Non-Negotiable Rules

- Load keys ONLY via dotenv from `.env` file — never inline
- NEVER log, print, echo, or write private keys anywhere
- NEVER write key substrings into source, traces, RUN_LOG.md, or README
- Derive and log public addresses freely (addresses are safe)
- If tx fails for insufficient funds: STOP and report address + amount needed; do NOT attempt to move funds

---

## Don't List

- Do NOT commit or push (`git commit`, `git push`) from this directory
- Do NOT use Base mainnet — Base Sepolia ONLY (chain_id 84532)
- Do NOT use the custom Express JSON-RPC server pattern — use `@a2a-js/sdk` `AgentExecutor` + `ClientFactory`
- Do NOT attempt to install agent0-sdk (has `@babel/code-frame` version conflict)
- Do NOT create Python files — this PoC is TypeScript only
- Do NOT modify any file outside `experiments/a2a-eas-reputation-loop/`
- Do NOT use IPFS or Pinata — use `data:` URIs for agentURI and feedbackURI
- Do NOT hardcode any key value anywhere, even partially
- Do NOT run `giveFeedback` where caller == agent owner (CLIENT gives feedback on DEV, never vice versa)
- Do NOT register the EAS schema twice — compute the deterministic UID first, check existence, then register if missing
- Do NOT skip logging tx hashes to RUN_LOG.md immediately after each on-chain action

---

## File Ownership (one concern per file)

| File | Concern |
|------|---------|
| `src/abis.ts` | ERC-8004 + EAS contract ABIs |
| `src/config.ts` | Env loading, provider, signers, addresses |
| `src/state.ts` | Load/save state.json for idempotency |
| `src/identity.ts` | Step 1: ERC-8004 register |
| `src/attest-eas.ts` | Step 3: EAS schema + attestation (called from dev-server) |
| `src/dev-server.ts` | DEV's A2A server (Steps 2+3 server side) |
| `src/coordinate-a2a.ts` | Step 2: CLIENT sends A2A task |
| `src/approve.ts` | Step 4: CLIENT verifies EAS + accepts via A2A |
| `src/feedback.ts` | Steps 5-6: DEV review request + CLIENT giveFeedback |
| `src/demo.ts` | Orchestrates full loop; appends to RUN_LOG.md |
