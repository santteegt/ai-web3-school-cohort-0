# ERC-8004 Resource Review — for Issue #5 (Agent Registration)

> **Purpose:** curate the most relevant items from [awesome-erc8004](https://github.com/sudeepb02/awesome-erc8004) for implementing [#5](https://github.com/santteegt/ai-web3-school-cohort-0/issues/5) — Specialist-first, Orchestrator-second registration on ERC-8004.
> **Date:** 2026-07-10 | **Blocked on:** #30 (WalletProvider) — this is prep reading, not a build start.
> Builds on prior research: [`ERC8004_ERC8183_ANALYSIS.md`](ERC8004_ERC8183_ANALYSIS.md) (fit analysis, 2026-06-06). This doc is narrower — resources specific to *doing the registration itself* well.

---

## ⚠️ Verify before you register — contract address discrepancy

Your `config/networks.json` (chain `8453`, role `canonical`) points `erc8004_identity_registry` at:

```
0x8004A818BFB912233c491871b3d84c89A494BD9e
```

I checked this on Basescan: it's a verified `ERC1967Proxy` (implementation `0xd53dE688...FF6499234`), live, with real `Register` and `Give Feedback` transactions since Feb 2026 — **19 total transactions**.

The awesome-erc8004 deployment table (and most ecosystem tools — 8004scan.io, Agent Arena, RNWY, Mintware, xbird, Obol, etc.) reference a different address as *the* Base mainnet Identity Registry:

```
0x8004A169FB4a3325136EB29fA0ceB6D2e539a432
```

I checked this one too: also verified, **69,017 transactions** — this is the one nearly every third-party explorer, scanner, and reputation tool in this ecosystem indexes by default.

Both are real, deployed, functioning contracts. I can't tell you which one is "correct" for your purposes without knowing why `0x8004A818...` was chosen originally — it may be intentional (a newer/upgraded registry version, or one your team specifically vetted). But given that:

- AC1 of #5 requires "Basescan shows `AgentRegistered`" as submission evidence, and
- half the ecosystem tooling below (explorers, reputation scanners, discovery APIs) won't find your agent unless it's registered on the address *they* index,

this is worth a two-minute confirmation with Santiago before Gate/register runs, not an assumption. If `0x8004A169...` is in fact the intended canonical registry, `config/networks.json` needs a one-line fix before this ticket starts — cheap to catch now, expensive to catch after both agents are registered on the "wrong" one.

Everything else below checked out clean: the `register(string)` selector in your `erc8004.py` stub (`0xf2c298be`) and in `config/pact.json`'s allowlist both match what I get computing `keccak256("register(string)")[:4]` independently — no action needed there.

---

## Official spec & best-practices (read these two first)

- **[ERC-8004 Best Practices — `Registration.md`](https://github.com/erc-8004/best-practices)** — the official guide for *how* to register well. Directly relevant to AC3 (Orchestrator's static agentURI on GitHub raw/IPFS) and AC1 (Specialist's live `agent-card.json`) — this doc is where the "static vs. live agentURI" pattern you're already using in #5 comes from upstream, so it's worth confirming your implementation matches their recommended shape.
- **[EIP-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)** — the registration schema (`services[]` array with `name`/`endpoint`/`version` per entry) is the exact shape your Specialist's live agent card and Orchestrator's static card both need to conform to. Worth a direct read since #5's ACs reference `agentURI` resolution behavior that's spec'd here, not invented.
- **[ERC8004SPEC.md](https://github.com/erc-8004/erc-8004-contracts/blob/master/ERC8004SPEC.md)** in the contracts repo — has the full Solidity interface if you need to double check `register(string,(string,bytes)[])` (the metadata-array overload) vs. the plain `register(string)` overload your stub already uses.

## Idempotency pattern (relevant to AC4 — "re-registering is a no-op")

Nothing in the awesome-list gives you a ready-made helper for this, but the pattern used across nearly every builder project that's already live (xbird, Obol, Mintware, MolTrust) is the same: **check `ownerOf`/`tokenURI` isn't already set for your wallet before calling `register()`**, since the Identity Registry is ERC-721-based and there's no on-chain "already registered" guard in the contract itself — the idempotency check is the caller's responsibility. That matches your negative-scenario AC exactly (mirroring the guild-formation idempotency pattern) — worth implementing the same way: query first, mint only if absent, rather than relying on a revert to catch the double-mint.

## Explorers — for manually verifying both registrations post-Gate

- **[8004scan.io](https://8004scan.io)** — the primary community explorer (built by AltLayer); good first stop to visually confirm both agentIds after registration.
- **[agentscan.info](https://agentscan.info)** and **[trust8004.xyz](https://www.trust8004.xyz)** — secondary lookups, useful for cross-checking that whichever registry address you settle on (see warning above) is actually the one these tools read from.
- Direct Basescan `Read Contract` tab on the Identity Registry address is still your ground truth for the `AgentRegistered` event evidence AC requires — don't rely solely on third-party explorers for the actual submission proof.

## SDKs (optional — you already have a hand-rolled `web3.py` stub)

Your `erc8004.py` stub builds calldata manually via `eth_abi.encode` + a hardcoded selector, pinned to `web3` `7.16.0` per your api-contracts spec. That's a reasonable, dependency-light choice for a two-function surface (`register`, `give_feedback`). If it ever gets more involved (metadata reads, `getAgentWallet`, multi-chain), these exist:

- **[erc-8004-py](https://github.com/tetratorus/erc-8004-py)** — lightweight Python implementation, closest in spirit to what you're already doing by hand.
- **[Agent0 SDK](https://sdk.ag0.xyz/)** — has Python support plus subgraph queries, which would solve the `getSummary()`-needs-`clientAddresses` gap your prior ERC-8004/ERC-8183 analysis already flagged — not needed for #5 itself, but relevant when #7 (reputation delta) comes around.
- **[chaoschain-sdk](https://pypi.org/project/chaoschain-sdk/)** — full-featured, PyPI-published, probably overkill for a two-call registration ticket.

Given #5's scope (one `register()` call each, no reads beyond a no-op check), I'd stick with your existing stub rather than pull in a dependency — flagging these mainly so the choice is deliberate, not just "we didn't know alternatives existed."

## Answering the ticket's own open question (§5: "should `register()` be an MCP tool?")

#5 explicitly asks whether `register()` should be an `OrchestratorTools` entry plus a separate one-time Specialist setup script. Skimming the ecosystem for precedent: **every live example in the awesome-list that self-registers does it as a one-time setup/CLI step, not a recurring agent-invokable tool** — e.g. Obol, xbird, MolTrust, Chitin all register once at deploy time via a script or CLI (`create-8004-agent` CLI is the generic version of this pattern), then expose *read* operations (score lookups, profile queries) as ongoing MCP/API tools. None of them wire `register()` itself into their agent's live tool surface, which lines up with your ticket's own instinct — the Specialist registering itself isn't something that should be re-triggerable through normal operation. Worth citing this as precedent when you confirm the answer with the user.

## Security posture (background confidence, not action items)

- Identity and Reputation Registry contracts are audited by **Cyfrin**, **Nethermind**, and the **Ethereum Foundation Security Team** — reassurance for the "no human gate required" call in §6 of the ticket (identity setup isn't a fund movement, and the underlying contracts have institutional audit coverage).
- Validation Registry remains explicitly unstable per the spec — consistent with your prior analysis; nothing new here, just confirms it's still correctly out of scope for #5.

## Skip list (interesting but not relevant to #5)

The awesome-list has a lot of adjacent material that's good background but not actionable for this specific ticket: x402 payment facilitators, TEE/zkML attestation SDKs (Automata, Phala, Sparsity), reputation-scoring platforms (RNWY, Helixa, DJD Agent Score, Mintware) that consume the Reputation Registry rather than the Identity Registry, and the academic papers on agent identity/governance. All of these become relevant for #7 (reputation delta) or later dogfooding phases — not for the two `register()` calls in front of you now.

---

**Bottom line:** the two things worth resolving before you start coding against #5 — (1) confirm `0x8004A818...` vs `0x8004A169...` is the deliberate choice for `erc8004_identity_registry` on chain `8453`, and (2) confirm the MCP-tool-vs-setup-script question using the "register once, expose reads as tools" precedent above. Everything else (selector, audits, spec shape) checks out against what your stub and specs already assume.
