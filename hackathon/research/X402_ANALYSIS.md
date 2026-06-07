# x402 — Fit Analysis for GuildOS

> **Purpose:** Determine whether x402 belongs in GuildOS's payment stack — as a replacement, an additive layer, or not at all — and if additive, where exactly it fits.
> **Researched:** 2026-06-06 | Agent: Sensei (Claude via Cowork)
> **Sources:** x402.org, docs.x402.org, github.com/x402-foundation/x402 (spec, README, scheme_exact_evm.md, sdk-features.md, batch-settlement, offer-receipt extension)

---

## TL;DR

x402 does **not** replace AgentFightClub. It solves a different problem: HTTP-native per-request micropayments between automated clients and servers. GuildOS's payment problem is multi-party conditional escrow with governance gating — which is Moloch v3 territory.

However, x402 is a **genuine additive fit** in one specific place: the Specialist Agent's tool use during task execution (Step 7). When GLM-5.1 needs to call paid APIs — oracle data, code analysis services, search tools — x402 handles those payments automatically, without API keys, in ~10 lines of Python. This strengthens the agentic narrative and adds a real x402 integration story without touching the treasury mechanics.

There is also an optional but compelling secondary fit: expose the Orchestrator's mandate-discovery endpoint as an x402-gated resource, letting agents pay-per-query to inspect open guild mandates. This is hackathon-optional but architecturally coherent.

**Verdict: Keep AgentFightClub for treasury/governance/settlement. Add x402 as the Specialist Agent's HTTP payment client for tool use. Integration risk: low.**

---

## What x402 Actually Provides

x402 is an open standard (Apache-2.0, Linux Foundation) for HTTP-native payments. The core mechanic:

1. Client sends HTTP request
2. Server responds `402 Payment Required` + payment requirements in `PAYMENT-REQUIRED` header (base64 JSON: amount, asset, network, payTo, scheme)
3. Client signs a payment payload (EIP-3009 `transferWithAuthorization`, Permit2, or ERC-7710 delegation)
4. Client retries with `PAYMENT-SIGNATURE` header
5. Server verifies via local logic or a facilitator's `/verify` endpoint
6. Server settles via facilitator's `/settle` endpoint (facilitator broadcasts on-chain, pays gas)
7. Server returns `200` + `PAYMENT-RESPONSE` header (settlement confirmation)

**Payment schemes available:**
- `exact` — fixed price per request (USDC, EIP-3009 or Permit2, EVM + Solana + others)
- `upto` — usage-based, client authorizes a maximum; server charges actual consumption
- `batch-settlement` — off-chain cumulative vouchers, batched on-chain redemption; deposit once, sign per request

**Facilitator model:** A trusted-but-not-custodial service (Coinbase runs the reference one; others exist) that verifies payment payloads and broadcasts settlement transactions. The facilitator cannot move funds except to the declared `payTo` address — it is a broadcaster, not a custodian.

**Key extensions:**
- `offer-receipt` — server signs an offer on every `402`, a receipt on every `200`; produces portable cryptographic proof-of-interaction artifacts usable in reputation systems
- `payment-identifier` — idempotency for retried requests
- MCP server/client wrappers — x402-gated MCP tools work natively with Claude and other AI clients

**SDKs:** Python (`pip install x402`), TypeScript, Go. Python supports FastAPI, Flask; client supports httpx, requests. Base Sepolia (EVM `eip155:84532`) is the default testnet target.

**Production status:** Live — $24M volume, 94K buyers, 22K sellers. Backed by Stripe, AWS, Cloudflare, Vercel, Alchemy, Nansen, Quicknode. Coinbase is the primary sponsor. Apache-2.0 open source, now under LF Projects / x402 Foundation governance.

---

## Feature Coverage Matrix

GuildOS MVP feature → x402 operation → Status

| GuildOS Feature (Section 5/6) | x402 Operation/Field | Status | Notes |
|---|---|---|---|
| Guild treasury (shared multi-party escrow) | — | ❌ | x402 has no escrow or custody model; funds move per-request |
| Membership proposal + vote | — | ❌ | No governance primitives in x402 |
| AgentFightClub `settle()` on deliverable acceptance | — | ❌ | x402 is per-request, not conditional on human acceptance |
| Specialist Agent pays for external APIs during execution | `exact` or `batch-settlement` scheme, Python SDK | ✅ | Core use case — this is precisely what x402 is for |
| Orchestrator delegates task to Specialist (A2A) | x402 middleware on A2A endpoint (optional) | ⚠️ | Possible, but loses human approval gate unless gating is re-engineered |
| On-chain payment proof (clickable Basescan tx) | Facilitator broadcasts settlement tx on Base | ✅ | Settlement tx is visible on Basescan; receipts include optional txHash |
| Signed proof-of-service delivery | `offer-receipt` extension (TypeScript only in v2) | ⚠️ | Offers/receipts are signed artifacts — useful for reputation, but offer-receipt not yet in Python SDK |
| Deliverable hash commitment on Base | — | ❌ | Out of scope; x402 does not store arbitrary data on-chain |
| ERC-8004 reputation write-back | — | ❌ | Not in x402's scope |
| Human review + acceptance gate | — | ❌ | x402 has no human-in-the-loop confirmation step |

---

## Gaps and Alternatives

### Gap 1: x402 cannot replace AgentFightClub (multi-party escrow + governance + conditional settlement)

**GuildOS needs:** A shared treasury that holds funds until a human approves a deliverable, then releases to the Specialist. Governance rails (propose/vote) for membership. Settlement triggered by human acceptance, not by HTTP request completion.

**x402 provides:** Payment on HTTP request completion. The server (resource) receives payment when it serves a valid response. There is no concept of "hold funds until a third party approves."

**Delta:** Fundamental architectural mismatch. x402 settles in seconds on request completion; GuildOS needs escrow that holds for days until a human reviews and accepts a deliverable.

**Alternative:** Keep AgentFightClub (Moloch v3). This gap is unbridgeable with x402 — they are different financial primitives.

### Gap 2: `offer-receipt` extension — Python SDK gap

**GuildOS needs:** Signed proof-of-service artifacts that the Specialist can attach to its ERC-8004 reputation record after completing a paid tool call.

**x402 provides:** `offer-receipt` extension produces EIP-712 or JWS signed offers (on 402) and receipts (on 200). These are portable, third-party-verifiable artifacts.

**Delta:** `offer-receipt` is TypeScript-only as of the current SDK feature matrix. Python SDK does not yet implement it. Python supports `exact`, `batch-settlement`, and most other features, but not `offer-receipt`.

**Alternative 1 (minimal):** Use the settlement response's txHash from the facilitator as the proof artifact — it's on Basescan and sufficient for demo purposes.

**Alternative 2 (if reputation artifacts are important):** Implement a thin TypeScript x402 sidecar for the resource server side (where offer/receipt signing happens), while keeping the Specialist Agent's client in Python. The Python client doesn't need `offer-receipt` — only the server emits it.

### Gap 3: Orchestrator → Specialist payment via x402 loses the human gate

**GuildOS needs:** Specialist gets paid only after Marco (human founder) accepts the deliverable. This requires AgentFightClub's `settle()` call — a deliberate human-triggered action.

**x402 provides:** Automatic payment on valid HTTP response. If the Orchestrator's A2A endpoint is gated with x402, the Specialist would pay the Orchestrator per task message — not get paid by the treasury. This inverts the payment direction and removes the human gate entirely.

**Delta:** The payment relationship is inverted (Specialist pays Orchestrator, not treasury pays Specialist) and the human approval gate disappears. Using x402 here would require redesigning the payment architecture.

**Alternative:** Do not use x402 for the Orchestrator ↔ Specialist payment. Keep AgentFightClub `settle()` for treasury release. Use x402 only for the Specialist's outbound tool calls.

---

## Stability Assessment

**Protocol maturity:** Production-ready. Apache-2.0, Linux Foundation governance. $24M volume in live production. Not alpha software.

**API stability:** x402 V2 was recently released (V1→V2 migration guide exists). The Python SDK is current with V2. Schemes (`exact`, `batch-settlement`) are stable with versioned specs.

**Base Sepolia support:** Confirmed. Default EVM network in examples is `eip155:84532` (Base Sepolia). Settlement transactions appear on Basescan.

**Facilitator availability:** Coinbase runs a production facilitator at `https://facilitator.x402.org`. Multiple third-party facilitators exist. Downtime risk during demo is low — Coinbase's infrastructure.

**Hackathon risk level: LOW.** x402 is the most stable component in this entire stack. The Python SDK is pip-installable, works with FastAPI and httpx, and the full integration (client + server) is ~30 lines of code. If x402 is added only for Specialist tool use (not for treasury), the failure surface is minimal.

---

## Recommended Integration Path

**Primary: x402 as Specialist Agent HTTP payment client for tool calls during GLM-5.1 execution**

The Specialist Agent's execution loop (Step 7 in GuildOS flow) uses GLM-5.1 and makes HTTP calls to external tools and data sources. Wrap those HTTP calls with the x402 Python client. Any API the Specialist encounters that returns a `402` is automatically paid.

This is:
- Architecturally correct (exactly what x402 is for)
- Low risk (~10–15 lines of code change to the Specialist's HTTP layer)
- Narratively compelling ("the agent paid for its own research tools using stablecoins, no API key required")
- Adds a real on-chain payment tx to the demo proof chain

**Secondary (optional, hackathon Day 3+): x402-gated Orchestrator mandate-discovery endpoint**

Expose a `GET /mandate` endpoint on the Orchestrator that returns the guild's mandate, required capabilities, and budget. Gate it with x402 at a small price ($0.001 USDC). Agents querying the ecosystem pay to read guild opportunities. This is a one-line middleware addition to the Orchestrator server and makes the "open agentic economy" story concrete.

**Do NOT use x402 for:**
- Treasury escrow (use AgentFightClub)
- Governance (use AgentFightClub)
- Treasury settlement/payment release (use AgentFightClub `settle()`)
- Deliverable hash commitment (use direct `eth_sendTransaction`)
- ERC-8004 reputation writes (use on-chain contract calls)

---

## Day 1 Test Checklist

Before building x402 into the Specialist Agent's execution loop, validate these five operations:

1. **Python client auto-pay:** Stand up a minimal FastAPI server with `payment_middleware` (exact scheme, $0.001 USDC, Base Sepolia). Run the Specialist's httpx client with `x402_httpx_transport`. Confirm the client auto-pays and receives the 200.

2. **Basescan tx visible:** After settlement, check `https://sepolia.basescan.org` for the payment transaction. Confirm it shows the USDC transfer to the `payTo` address. This is the demo proof point.

3. **Batch-settlement for multi-call tool use:** If GLM-5.1 calls the same API multiple times, switch to `batch-settlement` scheme. Confirm the client opens a channel (deposit tx), signs vouchers per call, and redeems in batch. The deposit tx and claim tx should both appear on Basescan.

4. **Facilitator availability on Base Sepolia:** Call `https://facilitator.x402.org/verify` directly with a test payload. Confirm it responds in <2s. If slow, identify an alternative facilitator from the x402 ecosystem page before the hackathon starts.

5. **ERC-7710 delegation option (if using Cobo CAW):** If Cobo Agentkit uses a smart account that supports ERC-7710 delegation, the Specialist can authorize tool payments without holding USDC directly — the delegation manager handles it. Test this before Day 1 only if the Cobo wallet architecture decision has landed. Otherwise, use a simple EOA with USDC on Base Sepolia.

---

## Minimum Integration Sketch

**Specialist Agent — tool call payments with x402 (Python)**

```python
import httpx
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402_httpx_transport
from x402.mechanisms.evm import EthAccountSignerWithRPC
from x402.mechanisms.evm.exact import ExactEvmScheme

# Set up once at Specialist Agent startup
account = Account.from_key(os.environ["SPECIALIST_WALLET_PRIVATE_KEY"])
signer = EthAccountSignerWithRPC(account, rpc_url="https://sepolia.base.org")
exact_scheme = ExactEvmScheme(signer)

client = x402Client().register("eip155:84532", exact_scheme)

# Wrap the Specialist's HTTP transport — all tool calls go through here
async def specialist_http_client():
    return httpx.AsyncClient(transport=x402_httpx_transport(client))

# During GLM-5.1 execution loop — tool call that may require payment
async def call_tool(url: str, params: dict) -> dict:
    async with specialist_http_client() as http:
        # If the tool returns 402, x402 client auto-pays and retries
        response = await http.get(url, params=params)
        response.raise_for_status()
        return response.json()
```

**Orchestrator — optional mandate-discovery endpoint (Python + FastAPI)**

```python
from fastapi import FastAPI
from x402.http.middleware.fastapi import payment_middleware
from x402 import x402ResourceServer
from x402.http import HTTPFacilitatorClient, FacilitatorConfig
from x402.mechanisms.evm.exact import SCHEME_EXACT

app = FastAPI()
facilitator = HTTPFacilitatorClient(FacilitatorConfig(url="https://facilitator.x402.org"))
resource_server = x402ResourceServer(facilitator)

routes = {
    "GET /mandate": {
        "accepts": {
            "scheme": SCHEME_EXACT,
            "price": "$0.001",         # 0.001 USDC per mandate query
            "network": "eip155:84532", # Base Sepolia
            "payTo": ORCHESTRATOR_WALLET,
        },
        "description": "Read this guild's active mandate, required capabilities, and budget",
    }
}

@app.middleware("http")
async def x402_middleware(request, call_next):
    return await payment_middleware(routes, resource_server)(request, call_next)

@app.get("/mandate")
async def get_mandate():
    return {
        "mandate": "Build and audit a staking contract",
        "requiredCapabilities": ["smart-contract-audit", "solidity"],
        "budget": "0.3 ETH",
        "deadline": "2026-06-14",
        "guild": GUILD_CONTRACT_ADDRESS,
    }
```

---

## Open Questions

1. **Does the Specialist's wallet need USDC pre-funded on Base Sepolia?** Yes — the `exact` scheme uses EIP-3009 `transferWithAuthorization` which requires the payer to hold USDC. For the demo, fund the Specialist's EOA with test USDC from the Base Sepolia faucet before the hackathon. If using Cobo CAW with a smart account, confirm the CAW can hold and spend USDC, or evaluate ERC-7710 delegation.

2. **Is there a live x402-gated API on Base Sepolia to test against?** Check the x402 ecosystem page (`x402.org/ecosystem`) and the Bazaar discovery layer. If no suitable test API exists, deploy the minimal FastAPI server above as the target — this validates the client-side integration without depending on a third party.

3. **Can the x402 settlement tx serve as a demo proof point alongside the AgentFightClub settlement?** Yes, and this strengthens the demo: two on-chain proof points — one for "Specialist paid for research tools" (x402 settlement), one for "treasury released payment to Specialist" (AgentFightClub settle). Different layers, both visible on Basescan.

---

*Research: 2026-06-06 | Agent: Sensei (Claude via Cowork)*
*Sources: x402.org · docs.x402.org · github.com/x402-foundation/x402 (spec, README, scheme_exact_evm.md, sdk-features.md, batch-settlement.md, offer-receipt.md) · hackathon/PROJECT_PROPOSAL.md · hackathon/PROTOTYPING_RESOURCES.md*
