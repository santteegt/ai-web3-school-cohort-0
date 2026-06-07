# AgentFightClub — Fit Analysis for GuildOS

> Research date: 2026-06-04 | Agent: Sensei  
> Sources: agentfightclub.xyz/skill.md · agentfightclub.xyz/how-it-works · HausDAO/moloch-skills moloch-agent/SKILL.md · docs.daohaus.club/contracts · PROJECT_PROPOSAL.md · PROTOTYPING_RESOURCES.md

---

## TL;DR

AgentFightClub (AFC) **partially fits** GuildOS, covering about 40% of the MVP feature surface directly. The treasury, membership proposal/vote/process lifecycle, and payment settlement are all real and usable. However, three critical gaps exist: (1) the proposal uses AFC command names (`launch`, `commit`, `settle`) that don't match the actual API (`summon`, `tribute`, `process`); (2) AFC has zero ERC-8004 integration — agent identity is entirely external; (3) AFC has no native deliverable hash commitment operation. The fallback path (direct Moloch v3 via `moloch-agent` CLI) is not a fallback at all — it IS the recommended primary path, and it is more stable than ClawBank for a hackathon build. The ClawBank path adds Turnkey wallet provisioning complexity with no benefit for GuildOS's use case. Core recommendation: **use the direct integration path** (`moloch-agent` CLI via `@raidguild/meta-clawtel`) as primary, drop ClawBank entirely.

---

## Feature Coverage Matrix

| GuildOS MVP Feature (Proposal §5–6) | AFC / Moloch Operation | Status | Notes |
|---|---|---|---|
| Guild formation — mandate on-chain, treasury initialized | `moloch-agent summon --params guild.json` | ✅ | Deploys Baal.sol + Gnosis Safe. Mandate goes in DAO metadata `communityMemoryURI`. |
| Fund treasury ("commit 0.3 ETH") | `wrap-eth` → `approve-token` → `tribute` | ✅ | Three commands, not one `commit`. ETH must be wrapped to WETH first. |
| Membership proposal — Specialist joins | `mint-shares` (no tribute) or `join-dao` (with tribute) | ✅ | `mint-shares` for a zero-tribute membership grant; requires `--to 0xSPECIALIST`. |
| Sponsor membership proposal | `moloch-agent sponsor --dao 0xGUILD --proposal <id>` | ✅ | Must sponsor before voting opens. |
| Human votes to approve membership | `moloch-agent vote --dao 0xGUILD --proposal <id> --approved true` | ✅ | Works. Needs `sponsor` first and short `votingPeriod` for demo. |
| Process (settle) membership proposal | `moloch-agent process-ready --dao 0xGUILD` | ✅ | After grace period. The actual "settle" command. |
| ERC-8004 profile read (Orchestrator + Specialist) | — | ❌ | AFC has no ERC-8004 integration. Use 8004scan API directly, separately. |
| A2A task delegation (Orchestrator → Specialist) | — | ❌ | Completely outside AFC scope. Separate A2A layer. |
| A2A result return (Specialist → Orchestrator) | — | ❌ | Completely outside AFC scope. |
| Real task execution via GLM-5.1 | — | ❌ | Completely outside AFC scope. |
| On-chain deliverable hash commitment | `signal` (indexed) or `custom-proposal` (on-chain action) | ⚠️ | No native hash commit. See gap analysis below. |
| Human review + acceptance (triggers payment) | Manual vote on `payment` proposal | ⚠️ | No single "accept" action; human acceptance maps to sponsoring + voting on the payment proposal. |
| Treasury payment settlement on acceptance | `moloch-agent payment --dao 0xGUILD --recipient 0xSPECIALIST --amount 0.3` | ✅ | Full proposal lifecycle required: payment → sponsor → vote → grace → process. |
| ERC-8004 reputation write-back | `memory-post` (off-chain index only) | ⚠️ | `memory-post` writes to DAOhaus's Poster contract (indexed, not ERC-8004). On-chain ERC-8004 update requires a separate contract call. |
| Guild context store | `workspace-create` + `memory-post` | ✅ | AFC has a shared memory/workspace system; can supplement or replace the JSON mock. |

**Summary:** 6 ✅ fully supported · 3 ⚠️ partial/workaround required · 6 ❌ outside AFC scope (handled by other layers: ERC-8004, A2A, GLM-5.1)

---

## Gaps and Alternatives

### Gap 1 — Command naming mismatch (proposal terminology vs. actual API)

**What GuildOS needs:** A single mental model that maps the proposal's `launch`, `commit`, `propose`, `vote`, `settle()` to real API calls.

**What AFC provides:** The `how-it-works` page uses high-level names (`launch`, `commit`, `propose`, `vote`, `settle`). The actual API commands (both direct and ClawBank) use different names.

**Real mapping:**

| Proposal term | Actual command |
|---|---|
| `launch` | `summon` |
| `commit` | `wrap-eth` + `approve-token` + `tribute` |
| `propose` (membership) | `mint-shares` or `join-dao` |
| `vote` | `sponsor` + `vote` |
| `settle()` | `process` (after grace period) |

**Delta:** Not a capability gap — just a documentation inconsistency that the proposal propagated. Fix: rewrite the integration spec with actual command names before Day 1.

**Bridgeable?** Yes, immediately. No code workaround needed.

---

### Gap 2 — ERC-8004 is entirely outside AFC's scope

**What GuildOS needs:** Read the Specialist Agent's ERC-8004 profile before membership approval; include the profile reference in the membership proposal; write a new delivery record after acceptance.

**What AFC provides:** Nothing. AFC operates on Moloch v3 proposal data (title, description, calldata). There is no ERC-8004 field in any AFC command. The `memory-post` command writes to DAOhaus's Poster contract (on-chain indexed records, readable from the subgraph), which is NOT ERC-8004.

**Delta:** Two completely separate systems. ERC-8004 must be handled independently via the 8004scan API (for reads) and a direct contract call (for writes). The membership proposal can reference the ERC-8004 profile address in its `description` field as a string, but AFC does not parse or validate it.

**Alternative for reads:** 8004scan API (direct HTTP call) — works today, stable enough for demo.

**Alternative for writes (reputation update):** Two options:
1. Direct `eth_sendTransaction` to the ERC-8004 registry contract — requires knowing the contract ABI (from the EIP). Straightforward on Base testnet.
2. If ERC-8004 write API is unstable, emit a custom event from a lightweight registry contract deployed on Day 1 — same on-chain proof, without the ERC-8004 dependency.

**Bridgeable?** Yes, but requires separate integration work. Not bridgeable within AFC itself.

---

### Gap 3 — No native deliverable hash commitment

**What GuildOS needs:** Commit a SHA-256 hash of the deliverable to the guild contract before payment — tamper-proof, clickable on Basescan.

**What AFC provides:** No native `commit-hash` or equivalent operation.

**Delta:** AFC operates on proposal data and treasury movements, not arbitrary data anchoring.

**Options (in priority order):**

1. **`signal` proposal with hash in description** — `moloch-agent signal --dao 0xGUILD --title "Deliverable hash T001" --description "sha256:0xHASH ipfs://CID"`. The proposal is stored on-chain via Poster contract; readable from Basescan. Indexed by the DAOhaus subgraph. Verdict: **fastest path**, but the hash is in proposal metadata, not a contract storage slot — not as clean as a true registry write.

2. **`custom-proposal` with calldata to a hash registry** — Deploy a minimal `HashRegistry.sol` (3 lines of Solidity, no audit required), then call it via `custom-proposal --actions '[{"target":"0xREGISTRY","value":"0","calldata":"<encoded>"}]'`. The proposal executes the registry write on-chain when processed. Verdict: **cleanest on-chain proof**, requires ~1 hour to deploy registry contract on Day 1.

3. **Direct `eth_sendTransaction` to the registry outside AFC** — Specialist Agent signs a transaction directly. Simpler but breaks the "all on-chain actions go through guild governance" story.

**Recommendation:** Option 1 (signal proposal) for the hackathon demo — it's the fastest, produces a Basescan-visible transaction, and the hash is permanently on-chain. Option 2 as stretch goal if a clean registry write is needed for judging.

**Bridgeable?** Yes, with Option 1 in under an hour.

---

### Gap 4 — Proposal lifecycle timing breaks live demo

**What GuildOS needs:** A live demo that shows `propose → vote → settle` in real time without waiting hours.

**What AFC provides:** Default Moloch v3 voting periods are typically 7 days + 1 day grace. AFC's `summon` parameters include `votingPeriod` (in seconds) and `gracePeriod` (in seconds).

**Delta:** The summon params must set very short periods for demo. Example: `votingPeriod: 60, gracePeriod: 60`. This means each proposal-to-settlement cycle takes ~2 minutes.

**Risk:** Two full proposal cycles in the demo (membership + payment) = ~4 minutes of on-chain waiting. Mitigation: pre-stage the membership proposal/vote BEFORE the demo starts (as stated in the proposal's risk table). During the live demo, only run Steps 6–12 (A2A, GLM, hash, payment).

**Bridgeable?** Yes, by configuring summon parameters correctly.

---

### Gap 5 — ClawBank path requires Turnkey wallet provisioning

**What GuildOS needs:** An agent that can sign Moloch v3 transactions autonomously.

**What ClawBank provides:** Turnkey-backed managed wallets — requires ClawBank account setup, wallet provisioning, and API authentication.

**What the direct path provides:** Local private key signing (`PRIVATE_KEY` env var). No ClawBank dependency.

**Delta:** For a 7-day hackathon, ClawBank wallet provisioning is setup overhead with no benefit over local signing. The ClawBank path also introduces additional failure modes (`wallet_not_provisioned`, `signing_timeout`, `sidecar_unavailable`) that don't exist on the direct path.

**Recommendation:** Drop ClawBank for the hackathon. Use direct path exclusively. The `moloch-agent` CLI (`@raidguild/meta-clawtel`) is the right tool.

---

### Gap 6 — Base Sepolia support is unverified (open question)

**What GuildOS needs:** All operations on Base testnet (Base Sepolia).

**What AFC/moloch-agent provides:** The direct path defaults to Base mainnet (`https://mainnet.base.org`). Base Sepolia requires setting `RPC_URL=https://sepolia.base.org`. Whether the Baal Summoner factory contracts are deployed on Base Sepolia is not confirmed by any of the reviewed docs.

**Delta:** If Summoner contracts aren't on Base Sepolia, `moloch-agent summon` will fail. This must be validated on Day 1.

**Alternatives if Base Sepolia is unsupported:**
1. Use Base mainnet — real ETH cost, but Base fees are negligible. Verdict: acceptable for hackathon.
2. Deploy the Baal Summoner factory to Base Sepolia manually using the Foundry deployment from `HausDAO/Baal` — ~2 hours of work. Verdict: only if Base mainnet is unacceptable.

**Open question: Must validate Day 1.** Run `moloch-agent summon` against Base Sepolia before any other integration work.

---

## Integration Stability Assessment

| Dimension | Assessment |
|---|---|
| **API maturity** | Alpha. How-it-works page explicitly states "Alpha — work in progress." Roadmap phases 1 (core infra) and 2 (agent activation) are listed as "Live." |
| **Direct path stability** | Higher than ClawBank. Signing is local; hosted service (`moloch-service-production.up.railway.app`) only required for Graph reads + IPFS pinning. If hosted service is down, writes still work via direct RPC. |
| **ClawBank path stability** | Lower. Multiple additional failure modes: `sidecar_unavailable`, `wallet_not_provisioned`, `signing_timeout`. Not recommended for GuildOS. |
| **Versioning guarantees** | None documented. The `moloch-agent` CLI is published as `@raidguild/meta-clawtel` on npm — pin to a specific version before the hackathon starts. |
| **Failure mode during demo** | Direct path: Graph reads fail → fallback to direct RPC reads (slower but functional). ClawBank path: sidecar down → all writes fail, no fallback. |
| **Hackathon risk level** | **Medium** for direct path. The core Moloch v3 contracts (Baal.sol) are audited, 4 years in production, and immutable. The risk is in the `moloch-agent` CLI tooling layer, not the contracts. Pin the CLI version and test thoroughly on Day 1. |

---

## Should the Fallback (Direct Moloch v3) Replace AFC as the Primary Path?

**Yes — and it already is, once you understand the architecture correctly.**

The "fallback" the proposal describes (deploying Moloch v3 directly via DAOhaus SDK) is precisely what `moloch-agent summon` does. The direct integration path IS deploying and operating Moloch v3 directly. "AgentFightClub" is a brand name for the Moloch v3 stack running on DAOhaus infrastructure, operated via either ClawBank (convenience) or the `moloch-agent` CLI (direct).

The only reason to use the ClawBank path would be if GuildOS needs embedded wallet infrastructure (Turnkey/Wiretap) that ClawBank provides. Since the wallet architecture decision points to Cobo CAW (not Wiretap) for the Cobo track, ClawBank's wallet value is irrelevant.

**Recommendation:** Rebrand internally. "Direct integration path via `moloch-agent` CLI" is the primary path. ClawBank is deprecated for this build. The fallback (if `moloch-agent` CLI fails) is using the Baal contracts via Foundry/ethers.js directly — which is only needed if the CLI layer is broken.

---

## Recommended Integration Path

**Primary: Direct integration via `moloch-agent` CLI**

```bash
npm install -g @raidguild/meta-clawtel
# Pin to a specific version: check npm for latest
```

Environment:

```bash
export PRIVATE_KEY=0x...        # Orchestrator/Founder agent signing key
export RPC_URL=https://sepolia.base.org  # Base Sepolia (or mainnet if Sepolia unsupported)
export MOLOCH_SERVICE_URL=https://moloch-service-production.up.railway.app
```

**Why direct over ClawBank:**
- No Turnkey wallet provisioning
- Signing stays local — no signing_timeout or sidecar_unavailable failure modes
- Same Moloch v3 contract operations, simpler setup
- Better for a 7-day hackathon

**What the direct path cannot do that GuildOS needs:**
- ERC-8004 reads/writes → use 8004scan API separately
- A2A messaging → use A2A 0.3.0 spec separately
- Deliverable hash commitment → use `signal` proposal (Option 1) or deploy `HashRegistry.sol` (Option 2)
- On-chain reputation write-back → direct `eth_sendTransaction` to ERC-8004 registry

---

## Day 1 Test Checklist

Run these in order before starting any other build work. Each is a go/no-go gate.

**1. Base Sepolia summoner availability (HIGHEST RISK)**
```bash
export RPC_URL=https://sepolia.base.org
moloch-agent summon --params test-summon.json
```
Success: returns DAO address on Base Sepolia Basescan. Failure: fall back to Base mainnet.

**2. Membership proposal full lifecycle**
```bash
moloch-agent mint-shares --dao 0xTEST_GUILD --to 0xSPECIALIST --amount 10 --title "Test membership"
moloch-agent sponsor --dao 0xTEST_GUILD --proposal 0
moloch-agent vote --dao 0xTEST_GUILD --proposal 0 --approved true
# Wait 60s (if summon params: votingPeriod=60, gracePeriod=60)
moloch-agent process-ready --dao 0xTEST_GUILD
```
Success: Specialist address appears in `moloch-agent members --dao 0xTEST_GUILD`.

**3. Payment proposal full lifecycle**
```bash
moloch-agent payment --dao 0xTEST_GUILD --recipient 0xSPECIALIST --amount 0.01
moloch-agent sponsor --dao 0xTEST_GUILD --proposal 1
moloch-agent vote --dao 0xTEST_GUILD --proposal 1 --approved true
# Wait 60s
moloch-agent process-ready --dao 0xTEST_GUILD
```
Success: payment tx visible on Basescan.

**4. Deliverable hash commitment via signal**
```bash
moloch-agent signal --dao 0xTEST_GUILD \
  --title "Deliverable hash TEST-T001" \
  --description "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 task:TEST-T001"
```
Success: signal proposal tx on Basescan, content indexed in DAOhaus subgraph.

**5. Hosted service health check**
```bash
moloch-agent health
moloch-agent capabilities
```
Expected: `graph.configured: true`, `pinning.configured: true`, `signing.handledByService: false`.

---

## Minimum Integration Sketch

Full guild lifecycle pseudocode for the GuildOS demo, using the direct path.

### Pre-hackathon: Deploy guild (can be staged)

```python
# guild-summon.json
summon_params = {
    "name": "GuildOS-Demo-Guild",
    "tokenName": "GUILD",
    "tokenSymbol": "GLD",
    "lootTokenName": "GUILD-LOOT",
    "lootTokenSymbol": "GLDL",
    "votingPeriod": 60,       # 60 seconds for demo — SET THIS
    "gracePeriod": 60,         # 60 seconds for demo — SET THIS
    "quorum": 1,               # 1% quorum — lowest possible
    "minRetention": 66,
    "sponsorThreshold": 0,
    "newOffering": 0,
    "memberAddresses": ["0xFOUNDER"],
    "memberShares": ["1000000000000000000"],   # 1 share (18 decimals)
    "memberLoot": ["0"]
}

# Deploy
run("moloch-agent summon --params guild-summon.json")
# Returns: GUILD_DAO_ADDRESS
```

### Step 1: Fund treasury

```python
run(f"moloch-agent wrap-eth --amount 0.3")
run(f"moloch-agent approve-token --token 0xWETH_BASE_SEPOLIA --amount 0.3")
run(f"moloch-agent tribute --dao {GUILD} --token 0xWETH --amount 300000000000000000 --shares 0")
```

### Step 2: Specialist membership proposal

```python
# Include ERC-8004 reference in description (AFC doesn't parse it — just metadata)
specialist_erc8004 = "0xSPECIALIST_PROFILE_ADDR"
run(f"""moloch-agent mint-shares \
    --dao {GUILD} \
    --to {SPECIALIST_ADDR} \
    --amount 10 \
    --title "Specialist Agent Membership Application" \
    --description "ERC-8004: {specialist_erc8004} | capabilities: security-audit | A2A: {SPECIALIST_A2A_URL}" """)

proposal_id = parse_proposal_id_from_output()

# Sponsor (founder)
run(f"moloch-agent sponsor --dao {GUILD} --proposal {proposal_id}")

# Human Gate 1: Marco votes to approve
run(f"moloch-agent vote --dao {GUILD} --proposal {proposal_id} --approved true --reason 'Profile verified; 12 deliveries, 94% acceptance'")

# Wait votingPeriod + gracePeriod (120s with demo params)
sleep(125)
run(f"moloch-agent process-ready --dao {GUILD}")
# Specialist is now a member
```

### Step 3: A2A task delegation (external to AFC)

```python
# Orchestrator Agent sends A2A 0.3.0 task message to Specialist
task_message = {
    "taskId": "T001",
    "from": ORCHESTRATOR_A2A_CARD,
    "to": SPECIALIST_A2A_ENDPOINT,
    "task": "Audit the staking contract at [source]",
    "acceptanceCriteria": ["OWASP checklist passed", "no critical findings unmitigated"],
    "deadline": "2026-06-14T18:00:00Z",
    "paymentRef": f"moloch:{GUILD}:T001"
}
send_a2a(task_message)

# GLM-5.1 executes — Specialist returns result via A2A
result = receive_a2a_result()
deliverable_hash = sha256(result.deliverable)
```

### Step 4: Commit deliverable hash (via signal proposal — fastest)

```python
run(f"""moloch-agent signal \
    --dao {GUILD} \
    --title "Deliverable hash T001" \
    --description "sha256:{deliverable_hash} | task:T001 | deliverable:{result.ipfs_cid}" """)
# Returns Basescan tx hash — proof point #1 for judges
```

### Step 5: Human accepts → payment proposal

```python
# Human Gate 2: Marco accepts the deliverable
# Trigger: Marco approves in GuildOS interface (minimal CLI)

run(f"""moloch-agent payment \
    --dao {GUILD} \
    --recipient {SPECIALIST_ADDR} \
    --amount 0.3 \
    --title "Payment: T001 audit accepted" \
    --description "sha256:{deliverable_hash} accepted at {timestamp}" """)

payment_id = parse_proposal_id_from_output()
run(f"moloch-agent sponsor --dao {GUILD} --proposal {payment_id}")
run(f"moloch-agent vote --dao {GUILD} --proposal {payment_id} --approved true")

sleep(125)  # voting + grace
run(f"moloch-agent process-ready --dao {GUILD}")
# Settlement tx — proof point #2 for judges
```

### Step 6: ERC-8004 reputation write-back (external to AFC)

```python
# Direct contract call to ERC-8004 registry
# Parameters: agent_addr, task_type, deliverable_hash, payment_amount, guild_addr
write_erc8004_delivery(
    agent=SPECIALIST_ADDR,
    task_type="security-audit",
    deliverable_hash=deliverable_hash,
    payment_wei=int(0.3 * 1e18),
    guild=GUILD
)
# Returns Basescan tx — reputation delta proof for judges
```

---

## Open Questions

These points are ambiguous in the reviewed docs. Flag and test before assuming.

1. **Are Baal Summoner factory contracts deployed on Base Sepolia?** Not confirmed. The `moloch-agent` CLI defaults to mainnet. Test `summon` on Base Sepolia on Day 1 before any other work.

2. **Is the hosted moloch service (`moloch-service-production.up.railway.app`) indexing Base Sepolia?** The Graph subgraph must include Base Sepolia for `proposals`, `members`, and `dao` reads to work on testnet. If not, direct RPC reads are the only fallback — and not all operations have direct-RPC equivalents in the CLI.

3. **Does `custom-proposal` with calldata work end-to-end in the current `moloch-agent` CLI?** The SKILL.md describes it but the format for `--actions` (JSON array with `target`/`value`/`calldata`) must be tested against a live DAO before using for the hash registry option.

4. **What is the current `@raidguild/meta-clawtel` npm version?** The SKILL.md doesn't pin a version. Pin the version on Day 1 and do not upgrade during the hackathon week.

---

*Last updated: 2026-06-04 | Agent: Sensei (Claude via Cowork)*
