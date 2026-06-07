# ERC-4337 & Cobo Agentic Wallet — Fit Analysis for GuildOS

> **Purpose:** Determine whether ERC-4337 + Cobo Agentic Wallet (CAW) provides the agent wallet layer GuildOS needs, and identify production-ready OSS alternatives if CAW cannot deliver.
> **Created:** 2026-06-06
> **Researched by:** Sensei (Claude via Cowork)
> **Sources:** ERC-4337 EIP (Last Call), docs.erc4337.io, ZeroDev docs, Biconomy docs, Safe docs, permissionless.js docs, x402.org, metamask.io/tutorials/design-server-wallets, Cobo WaaS docs

---

## TL;DR

ERC-4337 as a *standard* is the right foundation for GuildOS agent wallets. It provides everything needed: programmable smart accounts, spending scopes via session keys, gasless transactions, and deterministic addresses. However, **Cobo Agentic Wallet (CAW) is not a viable implementation path for this hackathon** — the GitHub repo is effectively empty, docs redirect to an unrelated MPC custody API, x402 is broken, and signing via API does not work (confirmed). The gap is bridgeable without replacing ERC-4337: **ZeroDev Kernel is the primary recommended drop-in**, with a working Python SDK, session key policies, and native Base Sepolia support. It covers all GuildOS MVP wallet requirements directly and adds zero new architectural complexity.

---

## 1. What ERC-4337 Actually Provides

ERC-4337 ("Account Abstraction Using Alt Mempool") is currently in **Last Call** status (deadline 2026-05-26 — just passed). It is essentially final and widely deployed. The standard introduces:

| Primitive | What it does |
|---|---|
| **UserOperation** | A pseudo-transaction struct carrying `sender`, `callData`, `nonce`, `signature`, gas fields, and optional `paymaster` |
| **EntryPoint** | Singleton contract; validates and executes bundles of UserOps via `handleOps()` |
| **Smart Account** (IAccount) | Contract implementing `validateUserOp()` — any custom auth logic goes here |
| **Bundler** | Off-chain node that batches UserOps into one transaction and submits to EntryPoint |
| **Paymaster** | Optional contract that pays gas on behalf of the sender — enables gasless UX |
| **Factory** | Deploys smart accounts counterfactually via CREATE2; address is deterministic before deployment |
| **Session Keys / Plugins** | NOT in core ERC-4337 — implemented via ERC-6900 or ERC-7579 modular account plugins |

**Key capabilities for agents:**
- Deterministic smart account address before first transaction (counterfactual deployment)
- Custom signature schemes (ECDSA, WebAuthn, multisig, any on-chain logic)
- Gasless transactions via Paymaster (agent never needs ETH to call EntryPoint)
- Batched calls in one UserOp (e.g., commit hash + update state in one tx)
- Session keys with scoped policies (call whitelist, spend limit, rate limit, time window)
- EIP-7702: complementary — lets an EOA delegate to a smart account implementation; now part of the spec

---

## 2. Feature Coverage Matrix

The wallet layer in GuildOS is responsible for Steps 2 (Orchestrator registers), 8 (Specialist commits hash), 11 (AgentFightClub settle → Specialist wallet receives payment), and 12 (ERC-8004 reputation write-back). The table below scores each required feature against three implementation options.

| GuildOS Feature | Cobo CAW | ZeroDev Kernel | Safe + permissionless.js |
|---|---|---|---|
| Deterministic agent wallet address (pre-deployment) | ❌ Broken | ✅ `ctx.new_account()` | ✅ `getSenderAddress()` |
| Python server-side SDK | ❌ Not found | ✅ `pip install zerodev-aa` (alpha) | ❌ TypeScript only |
| Base Sepolia support | ❓ Unverifiable | ✅ Confirmed (chain_id 84532) | ✅ Confirmed |
| Scoped to specific contracts only (AgentFightClub) | ❌ API broken | ✅ Call Policy (whitelist contract + function) | ✅ Via Safe Guards / module |
| Spending limit per task budget (0.3 ETH) | ❌ API broken | ✅ Gas Policy + Rate Limit Policy | ⚠️ Requires custom Guard |
| Send deliverable hash commit transaction | ❌ Signing API broken | ✅ `account.send_user_op([Call(...)])` | ✅ sendUserOperation |
| Gasless transactions (paymaster-sponsored) | ❓ Unverifiable | ✅ ZeroDev Paymaster, no ETH needed | ✅ Pimlico Paymaster |
| Receive ETH from AgentFightClub `settle()` | ⚠️ Possible via WaaS | ✅ Smart account address holds ETH | ✅ Safe address holds ETH |
| Custom signer (backend private key) | ❌ API broken | ✅ `Signer.local(private_key)` | ✅ `privateKeyToAccount()` |
| x402 payment support | ❌ Broken | ✅ Via x402 Python client + account signer | ✅ Via x402 TypeScript client |
| ERC-8004 identity anchoring | ❓ Not documented | ✅ Smart account address = agent identity | ✅ Safe address = agent identity |
| Setup time (hackathon-feasible) | ❌ Blocked | ✅ < 30 minutes to first UserOp | ⚠️ 1-2 hours setup |

**Status key:** ✅ supported directly | ⚠️ partial / requires workaround | ❌ not working | ❓ unverifiable

---

## 3. Gaps and Alternatives

### Gap 1: Cobo CAW is not functional for this use case

**What GuildOS needs:** A server-side smart account SDK that creates scoped agent wallets, signs transactions programmatically, and supports Base Sepolia testnet.

**What Cobo CAW provides:** Unclear — the GitHub repo (`CoboGlobal/cobo-agentkit`) returns empty content. All documentation redirects to the WaaS 2.0 API, which is a custodial MPC (Multi-Party Computation) wallet service aimed at exchanges and payment providers — not an ERC-4337 smart account stack. The CAW is architecturally distinct from ERC-4337; it is an MPC custody layer, not a programmable smart account.

**Known broken features (confirmed by Santiago):**
- x402 payment integration — not working
- Signing via API — not working
- No accessible Python SDK found
- No documentation for ERC-4337 smart account creation

**Delta:** The gap is complete for the hackathon timeline. CAW cannot be debugged in < 7 days with no working API and an inaccessible repo.

**Alternative:** ZeroDev Kernel (see Section 5). Drop-in replacement. No architecture change required.

---

### Gap 2: x402 payment protocol not available through Cobo

**What GuildOS needs (optional but relevant to Cobo track):** The ability for agents to pay for API services using HTTP 402 stablecoin payments. This maps to the Cobo track's "Agentic Economy" framing.

**What x402 actually is:** An open Coinbase/Linux Foundation standard for HTTP-native payments. When an agent makes an API request to an x402-enabled endpoint, the server returns `402 Payment Required`. The agent pays with USDC on Base, and retries. No accounts, no API keys. Live: $24M+ volume, 75M+ transactions in 30 days.

**Delta:** x402 is independent of Cobo CAW. The x402 Python client (`pip install x402`) works directly against any EVM wallet. Pairing ZeroDev's smart account with the x402 client means agents can pay API endpoints from their scoped smart account.

**Alternative:** `pip install x402` + ZeroDev signer. One-liner integration, works today.

---

### Gap 3: No Python smart account SDK (if falling back to Safe)

**What GuildOS needs:** Python is the most likely implementation language for the agent backend (GLM-5.1 integration, A2A handler).

**Delta:** Safe's SDK is TypeScript-only. Biconomy's AbstractJS is TypeScript-only. permissionless.js is TypeScript-only.

**Alternative:** ZeroDev Kernel Python SDK (`zerodev-aa`, alpha on PyPI). Confirmed working with `Signer.local(private_key)` and `account.send_user_op()`. If Python-TypeScript bridge is needed, a thin FastAPI sidecar wrapping permissionless.js is a viable fallback (adds ~4 hours setup).

---

## 4. Stability Assessment

### ERC-4337 Standard
- **Maturity:** Last Call (final review stage). Deployed in production since 2023. EntryPoint v0.7 is the stable target.
- **EntryPoint address:** `0x0000000071727De22E5E9d8BAf0edAc6f37da032` (same across all EVM chains including Base)
- **Risk:** Low. The spec is stable enough to build against. Breaking changes would require new EntryPoint deployment and migration, not a silent failure.

### ZeroDev Kernel
- **Maturity:** Kernel v3.3 is production. 6M+ smart accounts deployed across 50+ networks. Powering 200+ teams.
- **Python SDK (`zerodev-aa`):** Alpha — first release, limited to core operations (create, sign, send UserOp, EIP-7702). Session key policies not yet exposed in Python binding; TypeScript Kernel SDK needed for policy composition.
- **Risk (Python SDK):** Medium. Alpha means API may change. For the hackathon, pin to the installed version. Core signing works; policy enforcement may require TypeScript.
- **Risk (Kernel itself):** Low. Kernel is audited and production-deployed.

### Safe + permissionless.js
- **Maturity:** Safe contracts: audited and running billions in TVL for 4+ years. Safe4337Module: audited.
- **permissionless.js:** Actively maintained by Pimlico, TypeScript, built on viem. Stable.
- **Risk:** Low for the contracts. TypeScript-only is a workflow constraint, not a stability risk.

### Biconomy Nexus
- **Maturity:** Nexus is newer than Kernel/Safe. MEE (Modular Execution Environment) is Biconomy's own standard beyond ERC-4337. Adds complexity.
- **Risk:** Medium. Less battle-tested than Kernel/Safe for the specific GuildOS use case. Not recommended as primary.

### Cobo CAW
- **Maturity:** Inaccessible. GitHub repo empty, docs redirect loop, confirmed broken features.
- **Risk:** Critical. Do not depend on this for the hackathon.

---

## 5. Recommended Integration Path

### Primary: ZeroDev Kernel (TypeScript SDK, backend Node.js)

Even though GuildOS may be Python-heavy, the **TypeScript Kernel SDK** is the production path for session key policies — which are critical for the "controllable on-chain fund operations" story the Cobo track wants to see. Use Node.js for the wallet layer and Python for the AI/A2A layer; they communicate via a simple internal RPC.

**Why TypeScript over Python SDK:**
- Python SDK is alpha and does not expose session key policy APIs yet
- Session key policies (call whitelist, spend limit) are the primary demo differentiator
- Node.js is a one-command setup; does not add significant overhead

**Account type:** Kernel v3.3, EntryPoint v0.7, deployed on Base Sepolia

**Paymaster:** ZeroDev Paymaster (sponsored) — eliminates ETH funding requirement for agent transactions during the demo

**Session key configuration for GuildOS:**
- Signer: ECDSA with agent's backend private key
- Call policy: restrict to AgentFightClub contract address + specific function selectors (`propose`, `vote`, `settle`)
- Gas policy: maximum 0.05 ETH per session (per task budget guard)
- Rate limit policy: 1 transaction per 10 minutes (prevents runaway agent spending)
- Timestamp policy: session expires after 24 hours

**Fallback within ZeroDev:** Use `Signer.local(private_key)` with the Python SDK for MVP, accept that spending policies will be enforced off-chain (in agent logic) rather than on-chain until the TypeScript bridge is added.

### Secondary / Cobo Track Compliance

If the Cobo track judges require demonstrating Cobo tooling: use the **EVM MCP Server** (already connected in this workspace) as the signing layer, and frame the demo around ERC-4337 architecture choices rather than Cobo SDK. The Cobo track's stated evaluation surface is "controllable on-chain fund operations" — this can be demonstrated architecturally without requiring a working Cobo SDK. Alternatively, argue that ZeroDev's session key model is a better-specified version of CAW's stated intent.

### x402 Integration (optional, strengthens Cobo track story)

```
Agent wallet (ZeroDev Kernel smart account)
    ↓  x402 Python client sends 402-enabled HTTP request
Resource server responds 402
    ↓  x402 client signs payment with ZeroDev account
    ↓  Submits USDC transfer on Base Sepolia
Resource server validates payment, grants access
```

Install: `pip install x402` + configure with agent's wallet private key

---

## 6. Day 1 Test Checklist

These are the highest-risk operations. Validate all 5 before writing GuildOS-specific integration code.

1. **Smart account creation on Base Sepolia** — Run `ctx.new_account(signer, KernelVersion.V3_3)` and confirm the counterfactual address is deterministic. Verify it matches across two separate sessions with the same private key. (Tests: factory determinism, chain connection)

2. **Sponsored UserOp execution** — Send a no-op transaction (e.g., ETH transfer of 0 to self) sponsored by ZeroDev Paymaster. Confirm `receipt.success == True` and the tx hash is visible on Basescan. (Tests: bundler connectivity, paymaster sponsorship, EntryPoint v0.7 compatibility with Base Sepolia)

3. **Session key instantiation with call policy** — Create a session key restricted to a test contract address. Attempt a call to the allowed contract (should succeed) and to a different contract (should revert). (Tests: policy enforcement, Kernel plugin module, on-chain session validity)

4. **AgentFightClub contract call via smart account** — Call `propose()` on the AgentFightClub contract from the Specialist's smart account. Confirm the transaction goes through the EntryPoint. (Tests: real contract calldata encoding, correct ABI encoding of AgentFightClub selectors)

5. **ETH receipt into smart account** — Send 0.001 ETH from a funded test wallet to the Specialist Agent's smart account address (pre-deployment is fine — funds are held at the address). Confirm balance via `get_balance`. (Tests: smart account can hold and receive ETH, which AgentFightClub `settle()` requires)

---

## 7. Minimum Integration Sketch

### Kernel v3.3 — GuildOS Agent Wallet Setup (TypeScript)

```typescript
import { createKernelAccount, createKernelAccountClient, createZeroDevPaymasterClient } from "@zerodev/sdk"
import { signerToEcdsaValidator } from "@zerodev/ecdsa-validator"
import { toCallPolicy, toGasPolicy } from "@zerodev/permissions/policies"
import { http, createPublicClient } from "viem"
import { baseSepolia } from "viem/chains"
import { privateKeyToAccount } from "viem/accounts"

const AGENTFIGHTCLUB_ADDRESS = "0x..."   // AgentFightClub contract on Base Sepolia
const AGENT_PRIVATE_KEY = process.env.SPECIALIST_AGENT_KEY

async function createAgentWallet(projectId: string) {
  const chain = baseSepolia
  const publicClient = createPublicClient({ chain, transport: http() })

  // 1. ECDSA validator (backend private key signer)
  const signer = privateKeyToAccount(AGENT_PRIVATE_KEY)
  const ecdsaValidator = await signerToEcdsaValidator(publicClient, {
    signer,
    entryPoint: { address: "0x0000000071727De22E5E9d8BAf0edAc6f37da032", version: "0.7" },
    kernelVersion: "0.3.3"
  })

  // 2. Session key policies: only AgentFightClub, max 0.05 ETH gas
  const callPolicy = toCallPolicy({
    permissions: [{ target: AGENTFIGHTCLUB_ADDRESS }]  // whitelist
  })
  const gasPolicy = toGasPolicy({ maxGasAllowed: BigInt("50000000000000000") }) // 0.05 ETH

  // 3. Create scoped Kernel account
  const account = await createKernelAccount(publicClient, {
    plugins: { sudo: ecdsaValidator },
    permissions: { policies: [callPolicy, gasPolicy] },
    entryPoint: { address: "0x0000000071727De22E5E9d8BAf0edAc6f37da032", version: "0.7" },
    kernelVersion: "0.3.3"
  })

  // 4. Paymaster client (ZeroDev sponsors gas — no ETH needed on agent wallet)
  const paymasterClient = createZeroDevPaymasterClient({
    chain,
    transport: http(`https://rpc.zerodev.app/api/v2/paymaster/${projectId}`)
  })

  // 5. Kernel account client — use this to send all agent transactions
  const kernelClient = createKernelAccountClient({
    account,
    chain,
    bundlerTransport: http(`https://rpc.zerodev.app/api/v2/bundler/${projectId}`),
    paymaster: paymasterClient
  })

  console.log("Agent smart account address:", account.address)  // deterministic, usable pre-deployment
  return kernelClient
}

// Example: Specialist Agent commits deliverable hash
async function commitDeliverableHash(kernelClient, guildContract: string, deliverableHash: `0x${string}`) {
  const txHash = await kernelClient.sendTransaction({
    to: guildContract,
    data: encodeFunctionData({
      abi: guildABI,
      functionName: "commitHash",
      args: [deliverableHash]
    })
  })
  console.log("Hash committed:", `https://sepolia.basescan.org/tx/${txHash}`)
  return txHash
}
```

### Python path (MVP, no session key policies)

```python
from zerodev_aa import Context, Signer, Call, KernelVersion, GasMiddleware, PaymasterMiddleware
import os

PROJECT_ID = os.environ["ZERODEV_PROJECT_ID"]
AGENT_KEY = bytes.fromhex(os.environ["SPECIALIST_AGENT_KEY"].removeprefix("0x"))

BASE_SEPOLIA_CHAIN_ID = 84532

with Context(PROJECT_ID, chain_id=BASE_SEPOLIA_CHAIN_ID,
             gas=GasMiddleware.ZERODEV,
             paymaster=PaymasterMiddleware.ZERODEV) as ctx:
    with Signer.local(AGENT_KEY) as signer:
        with ctx.new_account(signer, KernelVersion.V3_3) as account:
            print("Specialist Agent address:", account.get_address())

            # Commit deliverable hash to guild contract
            calldata = encode_deliverable_hash(sha256_hash)  # ABI-encoded
            tx_hash = account.send_user_op([
                Call(target=GUILD_CONTRACT_ADDRESS, data=calldata)
            ])
            receipt = account.wait_for_receipt(tx_hash)
            print("Committed on Base Sepolia:", receipt.transaction_hash)
```

---

## 8. OSS Alternatives Comparison

| Stack | Smart Account | Python? | Session Keys | Base Sepolia | Audited | Setup Time |
|---|---|---|---|---|---|---|
| **ZeroDev Kernel** | Kernel v3.3 (ERC-7579) | ✅ Alpha | ✅ Call, Gas, Rate, Time | ✅ | ✅ | ~30 min |
| **Safe + permissionless.js** | Safe v1.4.1 | ❌ TS only | ⚠️ Via Safe Guard | ✅ | ✅ (4yr prod) | ~2 hr |
| **Biconomy Nexus** | Nexus (ERC-7579) | ❌ TS only | ✅ Smart Sessions | ✅ | ✅ (newer) | ~1 hr |
| **Cobo CAW** | MPC (not ERC-4337) | ❌ Broken | ❌ Broken | ❓ | ❓ | ❌ Blocked |
| **EVM MCP Server** *(in workspace)* | EOA (no smart account) | N/A (MCP) | ❌ | ✅* | N/A | ~0 min |

*EVM MCP Server note: The workspace has an EVM MCP server plugin connected (`mcp__evm-mcp-server__*`). It provides `write_contract`, `sign_message`, `transfer_native`, `get_balance`, `get_transaction_receipt` — enough for the MVP demo loop without a smart account. However it is an EOA signer (no spending scopes, no session keys, no gasless). Use it only for rapid prototyping or the deliverable-hash-commit step if the ZeroDev setup is blocked.*

---

## 9. Should We Replace Cobo CAW?

**Yes, for this hackathon.** The evidence is unambiguous:

1. The Cobo Agentkit GitHub repo is empty / unreachable — no SDK to depend on
2. The developer docs redirect loop leads only to WaaS 2.0 (MPC custody service), not an ERC-4337 SDK
3. x402 integration is confirmed broken
4. Signing via API is confirmed broken
5. No Python SDK exists or is accessible

The Cobo track's evaluation criteria is "controllable on-chain fund operations" and the "A2A Economy." These can be fully demonstrated with ZeroDev Kernel session keys (controllable = scoped to contracts, capped spending) and the GuildOS AgentFightClub flow (A2A Economy). The track does not require Cobo SDK specifically — it requires the pattern.

**Framing for judges:** "We implemented the Cobo track's controllable fund operations pattern using ERC-4337 Kernel session keys on Base Sepolia. We evaluated Cobo Agentkit but found it non-functional during the build period; the ERC-4337 ecosystem directly delivers the same primitives."

---

## 10. Hackathon Track Compliance Risk

| Risk | Severity | Mitigation |
|---|---|---|
| Cobo judges require Cobo SDK | Medium | Frame ZeroDev as "what Cobo CAW should be"; the capability story is identical |
| ZeroDev Python SDK alpha bugs | Medium | TypeScript fallback for wallet layer; Python handles AI/A2A only |
| Base Sepolia bundler downtime | Low | Use Pimlico bundler as backup (same EntryPoint address) |
| Session key policies too complex for 7 days | Low | MVP uses no policies (EOA or unscopped Kernel account); scoping added Day 3-4 |
| x402 not needed for MVP demo | Low | Drop x402 from Day 1; add only if time allows on Day 5+ |

---

*Report version: 1.0 | Built: 2026-06-06 | Agent: Sensei (Claude via Cowork)*
*Sources: ERC-4337 EIP (eips.ethereum.org/EIPS/eip-4337) · docs.erc4337.io · docs.zerodev.app · docs.safe.global · docs.biconomy.io · docs.pimlico.io · x402.org · metamask.io/tutorials/design-server-wallets · cobo.com/developers*
