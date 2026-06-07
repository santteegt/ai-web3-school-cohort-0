# ERC-8004 + ERC-8183 — Fit Analysis for GuildOS

> **Research date:** 2026-06-06 | **Hackathon start:** 2026-06-07 | **Agent:** Sensei (Claude via Cowork)  
> **Sources:** EIP-8004, EIP-8183, erc-8004/erc-8004-contracts GitHub, erc-8183/base-contracts GitHub, 8004scan best practices

---

## TL;DR

**ERC-8004** is a strong fit for the MVP — deployed on Base Sepolia with vanity addresses, live on mainnet since January 2026, and sufficient for Steps 2, 3, 5, and 12 of the GuildOS flow. The key gotcha is that there is no native "delivery record" concept — reputation write-back means calling `giveFeedback()` with A2A task metadata in an off-chain JSON, not writing a typed delivery struct. Design your agent profile and write-back logic around `giveFeedback()` from the start, not after.

**ERC-8183** is architecturally correct but carries high hackathon risk: proposed February 2026 (~3 months old), 5 stars on the reference repo, no deployed Base Sepolia contracts (you must self-deploy), and no existing integrations to validate against. The spec is clean and the `submit()` + `complete()` lifecycle maps perfectly to GuildOS Steps 8–12 — but the risk/reward is unfavorable for a 7-day build. The proposal already defers ERC-8183 full lifecycle to post-hackathon, and this research confirms that decision is correct.

**MVP path:** ERC-8004 for identity and reputation; AgentFightClub for settlement; simple deliverable hash commit (either AgentFightClub's `settle()` with hash argument or a 50-line custom escrow). ERC-8183 is the right upgrade for Week 2+.

---

## Feature Coverage Matrix

### ERC-8004

| GuildOS Feature | ERC-8004 Operation | Status | Notes |
|---|---|---|---|
| Step 2: Orchestrator registers on-chain | `register(agentURI)` → `agentId` | ✅ | Mints ERC-721 NFT; `agentURI` points to JSON with A2A endpoint. One call. |
| Step 2: Agent profile advertises A2A endpoint | Registration file `services[].{name:"A2A", endpoint, version}` | ✅ | Fully supported. Set `version: "0.3.0"` per spec. |
| Step 3: Specialist reads Orchestrator's A2A card | `tokenURI(agentId)` → parse registration file | ✅ | ERC-721 standard call; works on Base Sepolia at `0x8004A818...` |
| Step 5: Human reads Specialist profile (before) | `readAllFeedback(agentId, clientAddresses, ...)` + `getSummary(...)` | ⚠️ | Requires `clientAddresses` — cannot do open "show all" without knowing who gave feedback. Need indexing strategy. |
| Step 5: Show delivery history / acceptance rate | Off-chain feedback JSON with `a2a.taskId`, `value`, `tag1="successRate"` | ⚠️ | No typed "delivery record" struct. Must encode as feedback + off-chain JSON. Works but is custom. |
| Step 12: Reputation write-back after accepted delivery | `giveFeedback(agentId, value, valueDecimals, tag1, tag2, endpoint, feedbackURI, feedbackHash)` | ✅ | Caller must NOT be agent owner/operator. Guild contract or human wallet calls this. |
| Step 12: Link reputation record to task/deliverable | Off-chain JSON: `a2a.taskId`, `a2a.contextId`, `proofOfPayment.txHash` | ✅ | Spec explicitly supports A2A task references in feedback JSON. |
| Agent wallet (receives payment) | `setAgentWallet(agentId, newWallet, deadline, sig)` via EIP-712 | ✅ | Reserved `agentWallet` metadata key; requires signature proof. |
| Cross-chain portability | Same vanity addresses on 20+ chains | ✅ | Base Sepolia + mainnet deployed. No re-deployment needed. |
| Validation of deliverable work | `validationRequest` / `validationResponse` | ❌ | Validation Registry is still under active spec revision. Not production-stable. Skip for MVP. |
| Capability matching / registry query | Off-chain: read `services[].skills` / `services[].domains` from registration file | ⚠️ | No on-chain queryable capability index. Must pull registration files off-chain and filter. MVP mocks this anyway. |

### ERC-8183

| GuildOS Feature | ERC-8183 Operation | Status | Notes |
|---|---|---|---|
| Step 8: Deliverable hash commit | `submit(jobId, bytes32 deliverable, optParams?)` | ✅ | Exact match. `deliverable` = SHA-256 of output. Emits `JobSubmitted(jobId, provider, deliverable)`. |
| Step 10: Human accepts deliverable | `complete(jobId, reason, optParams?)` | ✅ | Only evaluator can call. `reason` = optional attestation hash. |
| Step 11: Payment release to Specialist | Auto-transfer in `complete()` minus platform fee | ✅ | ERC-20 only. Native ETH not supported — need WETH. |
| Step 8: Provider protected after submission | Once Submitted, only evaluator can reject | ✅ | Provider cannot be drained. Client cannot withdraw unilaterally. |
| Human rejects deliverable | `reject(jobId, reason?)` by evaluator | ✅ | Funds returned to client. |
| Timeout refund (demo safety) | `claimRefund(jobId)` after `expiredAt` | ✅ | Not hookable — cannot be blocked by malicious hook. |
| Reputation write-back via hook | `afterAction` on `complete` → calls ERC-8004 `giveFeedback()` | ✅ | EIP explicitly recommends this pattern. Hook address set at `createJob`. |
| AgentFightClub membership governance | ❌ not in scope | N/A | ERC-8183 is task escrow only. Guild membership/vote stays with AgentFightClub. |
| Native ETH payment | ❌ not supported | ❌ | ERC-20 only. Need WETH for the 0.3 ETH demo scenario. |
| Base Sepolia deployed contract | ❌ not found | ❌ | No vanity addresses. Must self-deploy from reference impl. |
| Bidding / provider discovery | Optional via `BiddingHook` | ⚠️ | Requires custom hook. Post-hackathon complexity. |

---

## Gaps and Alternatives

### ERC-8004 Gaps

**Gap 1 — No "delivery record" struct**

What GuildOS needs: a typed on-chain record (task type, deliverable hash, acceptance timestamp, payment amount, guild address) per accepted delivery — readable as a delta before/after.

What ERC-8004 provides: a generic `giveFeedback()` call with numerical `value`, two string tags, and a pointer to an off-chain JSON. The off-chain JSON supports `a2a.taskId`, `a2a.contextId`, and `proofOfPayment.txHash`, which is exactly the data GuildOS needs — but it's not typed on-chain.

Delta: The before/after demo can still work. Before: `getSummary()` shows `count=0` for the relevant `tag1`. After: `count=1` with the feedback entry visible. The "12 prior audit deliveries, 94% acceptance rate" scenario from the proposal maps to: 12 `giveFeedback` calls with `tag1="audit"`, `value=94, valueDecimals=0` for the aggregate.

Workaround: Define a GuildOS feedback schema:
- `tag1` = task type (e.g., `"audit"`, `"code"`, `"analysis"`)
- `tag2` = outcome (e.g., `"accepted"`, `"rejected"`)
- `feedbackURI` = IPFS or HTTPS pointer to off-chain JSON with `a2a.taskId`, `deliverableHash`, `guildAddress`, `paymentAmount`, `timestamp`
- `value` = 100 for accepted, 0 for rejected; `valueDecimals=0`

This is a thin schema on top of ERC-8004 — buildable in hours, not a blocker.

**Gap 2 — `getSummary()` requires clientAddresses**

What GuildOS needs: read the Specialist Agent's full reputation history without knowing in advance which wallets gave feedback.

What ERC-8004 provides: `getSummary(agentId, clientAddresses, tag1, tag2)` requires non-empty `clientAddresses`. Open queries are blocked to mitigate Sybil spam.

Delta: Need to either (a) track which addresses have given feedback from on-chain events (`NewFeedback` emitted with `clientAddress`), or (b) use the 8004scan API/indexer.

Workaround (MVP): Read `NewFeedback` events from the Reputation Registry to build the `clientAddresses` list, then call `getSummary()` and `readAllFeedback()`. A one-time event scan. The 8004scan API likely handles this automatically.

**Gap 3 — Validation Registry is not stable**

What GuildOS needs (post-hackathon): independent validation of deliverable quality by third-party verifiers.

What ERC-8004 provides: Validation Registry with `validationRequest/Response` — but the spec explicitly warns this section is under active revision.

Workaround: Skip Validation Registry entirely in MVP. Use EAS (Ethereum Attestation Service) for any third-party attestation need, as already planned in the proposal (Section 7 of PROTOTYPING_RESOURCES.md).

### ERC-8183 Gaps

**Gap 1 — ERC-20 only, no native ETH**

The demo scenario uses 0.3 ETH. ERC-8183's `fund()` calls `paymentToken.safeTransferFrom()` — ERC-20 only.

Workaround: Wrap ETH to WETH before creating the job. One extra tx. Not a blocker, but adds UX friction in the demo. The alternative is to denominate the demo in a test USDC or use MockUSDC from the reference implementation.

**Gap 2 — No deployed Base Sepolia contracts**

The reference repo (`erc-8183/base-contracts`) has only 5 stars and 2 commits. No published deployment addresses for Base Sepolia.

Delta: Must deploy `AgenticCommerce.sol` yourself. The contract is UUPS upgradeable — requires a proxy deployment. This is a Day 1 operational risk: if deployment fails or the contract behaves unexpectedly, there is no fallback address to pivot to.

Workaround for MVP: Skip ERC-8183. Use the deliverable hash commit in AgentFightClub's `settle()` call (or a 50-line custom escrow contract — see Integration Design below).

**Gap 3 — No existing ERC-8183 + ERC-8183 ERC-8004 hook integrations to learn from**

The hook pattern that calls ERC-8004 `giveFeedback()` in `afterAction` on `complete` is the right architecture — but there are no reference examples of it running in the wild. Any bug in the hook integration would be a novel debugging problem during a 7-day hackathon.

---

## Spec Maturity Assessment

### ERC-8004

| Dimension | Assessment |
|---|---|
| Spec status | Draft ERC; stable enough for integration (no breaking changes since Jan 2026 mainnet launch) |
| Mainnet deployment | January 29, 2026 — live on ETH mainnet, Base mainnet, 20+ chains |
| Base Sepolia | IdentityRegistry: `0x8004A818BFB912233c491871b3d84c89A494BD9e`; ReputationRegistry: `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| GitHub repo | 209 stars, 85 forks, 130 commits — active community |
| Risk level for hackathon | **LOW** — contracts are live and stable; the main risk is Sybil-protection design (clientAddresses requirement) catching GuildOS off-guard |
| Known issues | Validation Registry still under active spec revision — do not use it |
| 8004scan API | Live at 8004scan.io; best practices at best-practices.8004scan.io |
| v2 in development | Enhanced MCP support, improved x402 integration — no known breaking changes to existing v1 operations |

### ERC-8183

| Dimension | Assessment |
|---|---|
| Spec status | Draft ERC; proposed February 25, 2026 — ~3 months old |
| Mainnet/testnet deployment | No published addresses in reference repo; Virtuals Protocol has production deployments but not documented for Base Sepolia |
| GitHub repo | 5 stars, 3 forks, 2 commits — very early |
| Risk level for hackathon | **HIGH** — must self-deploy, no community integrations to reference, ERC-20-only creates demo friction |
| Known issues | None documented (too early for a known-issues corpus) |
| Reference impl quality | Solid: UUPS upgradeable, reentrancy guards, CEI pattern, hook whitelist. The Solidity is clean and follows OpenZeppelin patterns. |
| Ecosystem | Virtuals Protocol is a major early adopter; ERC-8183 Open Build hackathon track exists — there is community momentum, just not yet a mature reference implementation on Base |

---

## Recommended Integration Path

### MVP (Hackathon Days 1–7)

**ERC-8004:** Use for identity and reputation. Read from Base Sepolia vanity addresses. Design the GuildOS feedback schema on Day 1 (tag1=task type, tag2=outcome, feedbackURI=IPFS JSON). Register both agents. Call `giveFeedback()` from the guild contract or human wallet on task acceptance. The before/after delta is the primary demo proof.

**ERC-8183:** Skip. The current GuildOS design uses AgentFightClub's `settle()` for payment release and a separate deliverable hash commit for tamper-proof records. This is sufficient for the demo. Do not add ERC-8183 deployment risk to Week 1.

**Deliverable hash commitment alternative (if AgentFightClub is unstable):** Deploy a minimal custom escrow:

```solidity
// ~50 lines — deploy this in 2 hours if AgentFightClub's settle() is unavailable
contract GuildEscrow {
    address public client;
    address public provider;
    bytes32 public deliverableHash;
    bool public accepted;
    
    constructor(address _provider) payable { 
        client = msg.sender; provider = _provider; 
    }
    
    function submit(bytes32 hash) external {
        require(msg.sender == provider);
        deliverableHash = hash;
        emit Submitted(hash);
    }
    
    function accept() external {
        require(msg.sender == client && !accepted);
        accepted = true;
        payable(provider).transfer(address(this).balance);
        emit Accepted(deliverableHash, block.timestamp);
    }
    
    event Submitted(bytes32 hash);
    event Accepted(bytes32 hash, uint256 ts);
}
```

This is not a standard — it's a 2-hour fallback. The deliverable hash + acceptance timestamp in the event log gives the same Basescan-verifiable proof as the proposal requires.

### Post-Hackathon (Week 2+)

Integrate ERC-8183 as the per-task escrow layer alongside AgentFightClub:
- AgentFightClub: guild formation + membership governance (launch, propose, vote)
- ERC-8183: per-task escrow + deliverable hash (`submit`) + payment release (`complete`)
- ERC-8183 hook (`afterAction` on `complete`): calls ERC-8004 `giveFeedback()` atomically

This is the principled 3-layer architecture the specs were designed for. ERC-8183 replaces the AgentFightClub `settle()` call for per-task payment, and the hook wires reputation automatically. Implement this as Week 2's architecture upgrade.

---

## Day 1 Test Checklist

These five operations carry the most integration risk and must be validated live before building the rest of the stack.

1. **ERC-8004 `register()` on Base Sepolia** — Call `register(agentURI)` on `0x8004A818...` with a test JSON file. Confirm `agentId` is returned, `Registered` event is emitted, and `tokenURI(agentId)` resolves to the uploaded JSON. This validates the identity layer end-to-end.

2. **ERC-8004 `giveFeedback()` caller constraint** — Confirm the feedback caller CANNOT be the agent owner or an approved operator. Test that a separate wallet (guild contract address) CAN call `giveFeedback()` successfully. Misunderstanding this prevents the reputation write-back from working at all.

3. **`readAllFeedback()` + event scan for clientAddresses** — Emit a test `giveFeedback()` then scan `NewFeedback` events to collect `clientAddresses`. Call `readAllFeedback(agentId, [thatAddress], ...)` and confirm the data comes back correctly. This is the full read path for the before/after delta.

4. **Off-chain JSON upload + `feedbackURI` resolution** — Upload a test feedback JSON (with `a2a.taskId`, `deliverableHash` fields) to IPFS or an HTTPS endpoint. Call `giveFeedback()` with `feedbackURI` pointing to it. Confirm `keccak256(fileContent) == feedbackHash` matches. This is required for the tamper-proof delivery record.

5. **`setAgentWallet()` + EIP-712 signature flow** — Test updating the Specialist Agent's `agentWallet` via EIP-712 signature. This determines whether the agent's smart account (Cobo CAW or equivalent) can receive payment at the registered wallet address. If this fails, the payment release in Step 11 has no verified on-chain destination.

---

## Minimum Integration Sketch

### ERC-8004 Registration + Read + Write-back

```python
from web3 import Web3

# Base Sepolia
IDENTITY_REGISTRY = "0x8004A818BFB912233c491871b3d84c89A494BD9e"
REPUTATION_REGISTRY = "0x8004B663056A597Dffe9eCcC1965A193B7388713"

# --- Step 1: Register Specialist Agent (Day 1 setup) ---
agent_uri = "ipfs://QmSpecialistAgentRegistrationJSON"
# registration file includes: A2A endpoint, services, supportedTrust

tx = identity_registry.functions.register(agent_uri).build_transaction(...)
receipt = w3.eth.send_raw_transaction(sign(tx))
agent_id = receipt.logs[0]["args"]["agentId"]  # from Registered event

# --- Step 2: Read profile for membership approval (Step 5) ---
# Collect clientAddresses from NewFeedback events
new_feedback_events = reputation_registry.events.NewFeedback.get_logs(
    fromBlock=DEPLOY_BLOCK, argument_filters={"agentId": agent_id}
)
client_addresses = list({e["args"]["clientAddress"] for e in new_feedback_events})

# Read aggregate
count, summary_value, decimals = reputation_registry.functions.getSummary(
    agent_id, client_addresses, "audit", ""  # tag1 filter
).call()
# e.g.: count=12, summary_value=94, decimals=0 → 94% acceptance rate on audit tasks

# --- Step 3: Write-back after accepted delivery (Step 12) ---
# Called by guild contract or human wallet (NOT agent owner)
deliverable_hash = Web3.keccak(deliverable_content)  # bytes32
feedback_uri = upload_to_ipfs({
    "agentRegistry": f"eip155:84532:{IDENTITY_REGISTRY}",
    "agentId": agent_id,
    "clientAddress": guild_contract_address,
    "createdAt": datetime.utcnow().isoformat() + "Z",
    "value": 100,
    "valueDecimals": 0,
    "tag1": "audit",
    "tag2": "accepted",
    "a2a": {
        "taskId": a2a_task_id,
        "contextId": a2a_context_id
    },
    "proofOfPayment": {
        "fromAddress": guild_treasury_address,
        "toAddress": specialist_wallet,
        "chainId": "84532",
        "txHash": settlement_tx_hash
    }
})
feedback_hash = Web3.keccak(feedback_uri_content)

tx = reputation_registry.functions.giveFeedback(
    agent_id,           # agentId
    100,                # value (100 = accepted)
    0,                  # valueDecimals
    "audit",            # tag1 = task type
    "accepted",         # tag2 = outcome
    a2a_endpoint,       # endpoint (OPTIONAL)
    feedback_uri,       # feedbackURI (IPFS)
    feedback_hash       # feedbackHash (keccak256 of file)
).build_transaction({"from": guild_contract_or_human_wallet})
```

### ERC-8183 Hook for ERC-8004 (Post-Hackathon Pattern)

```solidity
// ERC-8183 hook that writes ERC-8004 reputation on job completion
contract GuildOS8004Hook is BaseACPHook {
    IReputationRegistry public reputationRegistry;
    
    function _postComplete(uint256 jobId, bytes calldata data) internal override {
        (bytes32 reason,) = abi.decode(data, (bytes32, bytes));
        
        // reason = bytes32 feedback hash; feedbackURI stored at job creation
        Job memory job = agenticCommerce.getJob(jobId);
        
        // Call ERC-8004 giveFeedback from the hook (evaluator = guild contract)
        reputationRegistry.giveFeedback(
            providerAgentId[job.provider],  // ERC-8004 agentId mapped from provider address
            100,        // value: accepted
            0,          // valueDecimals
            "audit",    // tag1: task type (stored at job creation)
            "accepted", // tag2
            "",         // endpoint
            feedbackURI[jobId],  // stored when job was created
            reason      // feedbackHash = bytes32 reason passed to complete()
        );
    }
}
```

---

## Should ERC-8183 Replace AgentFightClub for MVP?

**No.** The reasons:

1. AgentFightClub (Moloch v3) provides both treasury AND governance. ERC-8183 only provides per-task escrow. You still need AgentFightClub for `propose` + `vote` — the membership gate that is a core demo element.

2. Deploying ERC-8183 contracts adds an unknown on Day 1. AgentFightClub is live; the fallback (DAOhaus SDK) is documented. ERC-8183 has no documented fallback.

3. The deliverable hash commit step is achievable without ERC-8183. The `reason` field in AgentFightClub's `settle()` can carry the SHA-256 hash. If not, the minimal custom escrow above handles it in 2 hours.

4. The project proposal already decided this: "Per-capability pricing and per-task escrow (ERC-8183 full lifecycle)" is explicitly in the Deferred list. This research confirms that decision.

**The right question is:** should ERC-8183 replace the custom hash commit step within the MVP? Answer: only if you can deploy and validate ERC-8183 contracts on Base Sepolia on Day 1 without it becoming a blocker for the rest of the stack. Given that the reference repo has 2 commits and no deployed addresses, this is a significant risk to take on Day 1 of a 7-day build.

---

## Open Questions

These could not be definitively answered from the specs and must be validated with live API calls:

1. **Does 8004scan index Base Sepolia?** The API at `8004scan.io` is confirmed for mainnet. Whether it indexes Base Sepolia (84532) is not documented. If it doesn't, the GuildOS demo UI must query the contracts directly, not via the API.

2. **What does a realistic Specialist Agent profile look like at `agent_count=0`?** The before state of the demo (Specialist with 0 prior deliveries of the specific task type) may render oddly in a profile display. Test this edge case on Day 1 so the demo framing is calibrated.

3. **Can AgentFightClub's `settle()` carry a deliverable hash as a `bytes32` argument?** If it can, the GuildOS deliverable hash commit is a zero-extra-contract operation. If not, the minimal custom escrow is needed. Check the ClawBank `settle()` ABI before Day 1.

4. **What is the ERC-8183 deployed address on Base Sepolia (if any)?** The reference repo doesn't document it. The Virtuals Protocol or ERC-8183 Ethereum Magicians thread may have a community deployment. Search `erc-8183/base-contracts` issues on Day 1.

---

*Report version: 1.0 | Built: 2026-06-06 | Agent: Sensei (Claude via Cowork)*  
*Sources: [EIP-8004](https://eips.ethereum.org/EIPS/eip-8004) · [EIP-8183](https://eips.ethereum.org/EIPS/eip-8183) · [erc-8004-contracts](https://github.com/erc-8004/erc-8004-contracts) · [erc-8183/base-contracts](https://github.com/erc-8183/base-contracts) · [8004scan best practices](https://best-practices.8004scan.io) · [QuickNode ERC-8004 guide](https://blog.quicknode.com/erc-8004-a-developers-guide-to-trustless-ai-agent-identity/) · [QuickNode ERC-8183 guide](https://blog.quicknode.com/erc-8183-agentic-commerce/)*
