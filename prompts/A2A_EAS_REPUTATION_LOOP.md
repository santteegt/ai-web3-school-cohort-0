# Prompt — A2A × EAS × ERC-8004 Reputation Loop (Autonomous PoC)

> **Usage:** Paste the fenced block below into a fresh autonomous coding session (or launch it as a
> background agent — see "Running it as a long-running loop" at the bottom).
> **Working dir:** `experiments/a2a-eas-reputation-loop/` (already contains a `.env` with two funded
> Base Sepolia keys).
> **What it builds:** A toy two-agent coordination loop — a CLIENT agent requests a hello-world script
> from a DEV agent — that integrates ERC-8004 (identity + reputation), A2A (coordination), and EAS
> (proof-of-work attestation embedded in the A2A delivery), running end to end on Base Sepolia.
> **SDK:** scaffolded with `create-8004-agent` (TypeScript).

---

## Prompt

```
ROLE & MISSION
You are an autonomous build agent. Build AND run a working proof-of-concept that proves a
toy coordination workflow between two agents on Base Sepolia. Operate as a loop:
  build a phase → run it against Base Sepolia → read the on-chain result → fix → repeat,
until the full 6-step workflow below completes with verifiable on-chain evidence.
First complete PHASE 0 (scaffold the agents with create-8004-agent and bootstrap a Level-1
SevenD project); then run the build loop.
A task is NOT done at "scaffolding compiles." It is done when the whole loop runs end to end
and the on-chain artifacts (agent IDs, attestation UID, feedback tx) are real and queryable.

═══════════════════════════════════════════════════════════════════════════════
WORKING DIRECTORY — HARD BOUNDARY
═══════════════════════════════════════════════════════════════════════════════
- Create and edit files ONLY under experiments/a2a-eas-reputation-loop/.
- You MAY READ (never write) these for reference/inspiration:
    hackathon/research/ERC8004_ERC8183_ANALYSIS.md   (addresses, register/giveFeedback/getSummary)
    hackathon/research/EAS_ANALYSIS.md                (addresses, schema, attest, refUID, GraphQL)
    hackathon/research/A2A_ANALYSIS.md                (A2A AgentCard, artifact, metadata conventions)
    experiments/a2a-coordination-loop/                (a Python A2A project — protocol-shape
                                                       reference only; you build in TypeScript)
- Touch nothing else in the repo. Do NOT git commit or git push — leave the working tree for
  Santiago to review.

═══════════════════════════════════════════════════════════════════════════════
SECRETS — NON-NEGOTIABLE
═══════════════════════════════════════════════════════════════════════════════
- experiments/a2a-eas-reputation-loop/.env defines exactly two vars:
      PRIVATE_KEY_CLIENT   PRIVATE_KEY_DEV
  (two pre-funded Base Sepolia EOAs — CLIENT and DEV).
- Load them ONLY via a dotenv loader into a signer (privateKeyToAccount / new Wallet) — read from
  the environment, never inline a key.
- NEVER cat the .env, never print/log/echo a key, never write a key (or any substring of one)
  into source, output, traces, the RUN_LOG, or the README. Reference keys only by variable name.
- Derive each key's PUBLIC address and use/log those freely — addresses are safe.
- First file you write: a .gitignore in the PoC dir that excludes .env (and node_modules, dist).
- The keys are already funded. If any tx fails for insufficient funds, STOP and report the
  address + needed amount — do NOT attempt to acquire funds or move money.

═══════════════════════════════════════════════════════════════════════════════
WHAT TO BUILD
═══════════════════════════════════════════════════════════════════════════════
Two agents:
- CLIENT — signs with PRIVATE_KEY_CLIENT. Requests a "hello world" script; approves; leaves reputation.
- DEV    — signs with PRIVATE_KEY_DEV. Runs an A2A server; produces the script; attests; delivers.

Three standards, interlinked:
1. ERC-8004 — on-chain agent identity (register) + reputation (giveFeedback / getSummary).
2. A2A — agent discovery + task delegation + structured delivery (via the create-8004-agent A2A server).
3. EAS — the DEV signs a proof-of-work attestation over the deliverable hash; the attestation UID
   is EMBEDDED inside the A2A delivery artifact so the CLIENT can verify it before approving.

═══════════════════════════════════════════════════════════════════════════════
PHASE 0 — BOOTSTRAP & SCAFFOLD (do this BEFORE Step 1; it sets up the project)
═══════════════════════════════════════════════════════════════════════════════
0A — SCAFFOLD with create-8004-agent (the locked SDK for this PoC — TypeScript).
       create-8004-agent   https://github.com/Eversmile12/create-8004-agent
     Run `npx create-8004-agent` to generate the agent project(s). It produces a full TS agent:
     register.ts (ERC-8004 registration), a2a-server.ts + .well-known/agent-card.json (A2A), plus
     MCP + x402 scaffolding you can IGNORE for this PoC. The wizard is interactive — BEFORE coding,
     check `npx create-8004-agent --help` and the README for non-interactive / headless flags (to
     preset answers) and prefer them; only if none exist, reproduce the equivalent structure by hand.
     TWO agents: scaffold per role — a DEV project (needs the A2A server) and a CLIENT project (acts
     as the A2A client + leaves feedback) — OR scaffold once and add the second role. Reuse the
     generated ERC-8004 register + A2A wiring; do NOT rebuild identity or A2A from scratch.
     What create-8004-agent does NOT give you — ADD these on top:
       - ERC-8004 reputation: giveFeedback / getSummary (Steps 5-6)
       - EAS attestation, embedded in the A2A delivery artifact (Step 3)
       - the CLIENT-side approval logic (Step 4)
     agent0-sdk (https://sdk.ag0.xyz/docs, v0.31 alpha) was the considered alternative — record in
     0B WHY create-8004-agent won (fastest ERC-8004 + A2A head start; stable vs alpha). If
     create-8004-agent proves unworkable, fall back to a hand-rolled TS build (viem/ethers +
     @a2a-js/sdk) or agent0-sdk — stay in TypeScript, never switch to Python.

0B — Bootstrap experiments/a2a-eas-reputation-loop/ as a LEVEL-1 SevenD project BEFORE coding.
     Use the SevenD skill (invoke /SevenD, choose Level 1). If the skill is unavailable, create the
     Level-1 files by hand:
       - Product.md  vision (this PoC) · backlog with IDs (P-001 register identities, P-002 A2A
                     delegation, P-003 EAS attest + deliver, P-004 client approves, P-005 dev
                     review + client feedback) · acceptance criteria for the top items · a Design
                     Decisions section recording the SDK choice (create-8004-agent, TypeScript) + why.
       - Tech.md     stack table (TypeScript + create-8004-agent + EAS SDK + viem/ethers) · project
                     structure · setup/run/test commands · conventions · env-var NAMES
                     (PRIVATE_KEY_CLIENT, PRIVATE_KEY_DEV, optional RPC_URL) — never values.
       - CLAUDE.md   IDE rules at the PoC-folder root (experiments/a2a-eas-reputation-loop/CLAUDE.md,
                     NOT the repo-root CLAUDE.md): "read Product.md + Tech.md before coding", the
                     6-step flow, the SECRETS rules above, and a Don't list.
     Keep every SevenD file inside the PoC dir. Then build Steps 1-6 as the Development phase,
     flipping each Product.md backlog item to done as it lands on-chain.

═══════════════════════════════════════════════════════════════════════════════
THE WORKFLOW — must run end to end, in this exact order
═══════════════════════════════════════════════════════════════════════════════
STEP 1 — Register identity (both agents)
  CLIENT calls ERC-8004 IdentityRegistry.register(agentURI_client) from PRIVATE_KEY_CLIENT  -> client agentId
  DEV    calls ERC-8004 IdentityRegistry.register(agentURI_dev)    from PRIVATE_KEY_DEV     -> dev agentId
  (the create-8004-agent register.ts is your starting point.) agentURI = a self-contained
  registration JSON describing the agent. Simplest: a data:application/json;base64,... URI (no
  hosting needed), OR a file the DEV's HTTP server serves. The DEV's registration JSON MUST advertise
  its A2A endpoint URL (this is how the three standards interlink: identity -> A2A endpoint). Log
  both agentIds + both tx hashes.

STEP 2 — Client coordinates + delegates via A2A
  DEV runs an A2A server (the create-8004-agent scaffold's a2a-server) exposing an AgentCard with a
  skill like "write_hello_world".
  CLIENT resolves the DEV AgentCard, then sends an A2A task message: "Write a hello world script
  in Python." Put coordination context in Message.metadata, e.g.
  { "client_agent_id": <n>, "dev_agent_id": <n>, "task_id": "<uuid>" }.

STEP 3 — Dev produces work, attests, and delivers
  DEV generates the hello_world.py content.
  DEV computes the deliverable hash (keccak256 or sha256 — pick one and be consistent everywhere).
  DEV registers an EAS schema once (if not already) and calls eas.attest(...) from PRIVATE_KEY_DEV
    -> deliverable attestation UID. Suggested schema:
       "bytes32 deliverableHash, string taskType, string a2aTaskId, address devAgent"
  DEV returns the A2A result as a structured artifact (data part) that EMBEDS:
       { deliverable (or a reference), deliverable_hash, eas_attestation_uid, eas_schema_uid }
  This embedding of the EAS UID in the A2A delivery message is a required PoC outcome.

STEP 4 — Client approves work
  CLIENT reads the artifact, recomputes the hash of the delivered content, fetches the EAS
  attestation by UID (easscan GraphQL OR eas.getAttestation(uid) directly), and asserts the
  on-chain attested hash == the recomputed hash. On match, CLIENT sends an A2A "accepted" message.

STEP 5 — Dev requests review
  DEV sends a follow-up A2A message to the CLIENT requesting a review / feedback for the completed task
  (reuse the same context/task id).

STEP 6 — Client provides feedback (reputation write-back)
  CLIENT calls ERC-8004 ReputationRegistry.giveFeedback(
      dev_agentId, value=100, valueDecimals=0, tag1="code", tag2="accepted",
      endpoint, feedbackURI, feedbackHash) from PRIVATE_KEY_CLIENT.
  CRITICAL: giveFeedback REVERTS if the caller is the agent's owner/operator. CLIENT and DEV are
  different EOAs, so CLIENT-on-DEV is valid — never have the DEV feedback its own agent.
  feedbackURI -> a small JSON containing a2a.taskId, deliverable_hash, eas_attestation_uid;
  feedbackHash = keccak256 of that JSON's bytes.
  Then PROVE the reputation changed: scan NewFeedback events to collect the client address, call
  getSummary(dev_agentId, [client_address], "code", "") and show count went 0 -> 1. Log the tx hash.

═══════════════════════════════════════════════════════════════════════════════
GROUND TRUTH — Base Sepolia (chain_id 84532)
═══════════════════════════════════════════════════════════════════════════════
NETWORK: Base Sepolia ONLY. chain_id 84532. Explorer: https://sepolia.basescan.org/tx/<hash>
  (This PoC is testnet — do NOT apply any "Base mainnet" rule from other parts of this repo.)

ERC-8004 (verify the live ABI before calling — fetch from Basescan or an RPC):
  IdentityRegistry   0x8004A818BFB912233c491871b3d84c89A494BD9e
  ReputationRegistry 0x8004B663056A597Dffe9eCcC1965A193B7388713
  Read path for STEP 6 proof: getSummary() requires non-empty clientAddresses, so collect them
  from NewFeedback events first.

EAS (Base Sepolia):
  EAS             0x4200000000000000000000000000000000000021
  SchemaRegistry  0x4200000000000000000000000000000000000020
  Use @ethereum-attestation-service/eas-sdk — SchemaRegistry.register(...) once, then
  eas.attest({schema, data:{recipient, expirationTime, revocable, refUID, data}}) encoded with
  SchemaEncoder; eas.getAttestation(uid) to read back. Verify the schema/encoding against the
  deployed contract before your first attest.
  Read-back explorer: easscan GraphQL is likely https://base-sepolia.easscan.org/graphql; if it
  does not index testnet, fall back to getAttestation(uid) on-chain (the contract is the truth).

A2A:
  Use the A2A server that the create-8004-agent scaffold ships (a2a-server.ts + agent-card.json) for
  the DEV side; write the CLIENT as an A2A client that resolves the DEV agent card and sends the
  task. The deliverable returns as a structured data artifact (with the EAS UID embedded), and
  coordination fields (client/dev agentId, task id) ride in the message metadata.
  (experiments/a2a-coordination-loop/ is a Python A2A project — useful only as a protocol-shape
  reference for the message / artifact / metadata conventions, not as code to copy.)

═══════════════════════════════════════════════════════════════════════════════
STACK
═══════════════════════════════════════════════════════════════════════════════
- TypeScript (locked — create-8004-agent is TS). Node 20+. The scaffold provides each agent's
  package.json; keep the PoC under one workspace if convenient.
- Libraries: create-8004-agent output (ERC-8004 register + A2A server), @ethereum-attestation-
  service/eas-sdk, viem or ethers (contract calls + signing), dotenv.
- RPC: a public Base Sepolia endpoint (e.g. https://sepolia.base.org) or RPC_URL from .env if
  present. Keep both agents runnable on localhost (different ports).

═══════════════════════════════════════════════════════════════════════════════
AUTONOMY / LOOP RULES
═══════════════════════════════════════════════════════════════════════════════
- Work phase by phase (Step 1 → 6). After each phase, actually run it against Base Sepolia and
  confirm the on-chain effect before moving on. Append every result to RUN_LOG.md immediately:
  agentIds, every tx hash + its sepolia.basescan link, the EAS schema UID + attestation UID, the
  getSummary before/after counts.
- Time-box any single blocker to ~45 min. If a non-core integration is genuinely stuck, take the
  documented fallback (e.g. EAS not indexed -> read via getAttestation; agentURI hosting awkward ->
  use a data: URI; create-8004-agent wizard won't run headlessly -> reproduce its structure by hand)
  and note the deviation in RUN_LOG.md. Do not silently drop a workflow step.
- Idempotency: re-running must not crash if identities/schema already exist — detect-and-reuse.
- Never weaken the SECRETS rules to make something work.

═══════════════════════════════════════════════════════════════════════════════
DEFINITION OF DONE (all must be true)
═══════════════════════════════════════════════════════════════════════════════
1. A single documented entrypoint reproduces the full loop (e.g. `npm run demo` — it may spawn/await
   the DEV A2A server) or a clearly documented 2-terminal sequence.
2. A clean run prints/logs, with real Base Sepolia evidence: client agentId, dev agentId,
   EAS schema UID, EAS delivery attestation UID, the giveFeedback tx hash, and getSummary
   count 0 -> 1 for the DEV agent.
3. RUN_LOG.md contains every tx hash with a https://sepolia.basescan.org link and the two
   explorer references (basescan for ERC-8004/feedback, easscan or on-chain read for the attestation).
4. README.md in the PoC dir explains: what the PoC proves, the 6-step flow, how the three standards
   interlink (especially the EAS-UID-inside-A2A-artifact handoff), required env var NAMES (not
   values), and how to run it.
5. .env is gitignored and no secret appears anywhere in the tree or logs.
6. The code is readable and the workflow steps are obvious in the source (name modules/functions
   after the steps, e.g. identity / coordinate-a2a / attest-eas / approve / feedback).
7. The PoC dir is a Level-1 SevenD project: Product.md (with the SDK Design Decision and the
   P-001..P-005 backlog marked done), Tech.md, and a PoC-scoped CLAUDE.md are present.
8. The PHASE 0 decision is written down — create-8004-agent (TS) chosen, agent0-sdk considered, with
   the rationale (in Product.md Design Decisions, or a short SDK_EVALUATION.md).

Report at the end: a short summary with the live agentIds, attestation UID, feedback tx hash, and
the before/after reputation counts — plus any fallback you took and why.
```

---

## How to use

1. Confirm `experiments/a2a-eas-reputation-loop/.env` has `PRIVATE_KEY_CLIENT` and `PRIVATE_KEY_DEV`,
   both funded with a little Base Sepolia ETH (faucet: https://www.alchemy.com/faucets/base-sepolia).
2. Copy the fenced block above into a fresh Claude Code / autonomous coding session.
3. Let it run. It will scaffold the agents with create-8004-agent (TypeScript), bootstrap a Level-1
   SevenD project, build each phase, and execute against Base Sepolia — logging on-chain evidence to
   `RUN_LOG.md` as it goes.

## Running it as a long-running loop

- **Background agent:** launch the prompt with the `Agent` tool (`subagent_type: general-purpose`,
  `run_in_background: true`) so it builds-and-runs autonomously while you do other work; you're
  notified on completion. It needs web/network access (npm + the SDK docs + Base Sepolia RPC).
- **Fresh session:** paste the block into a new session and let it run uninterrupted — the AUTONOMY /
  LOOP RULES are written so it iterates (build → run on-chain → fix) without needing prompts between phases.

## Notes / decisions baked in

- **SDK locked to create-8004-agent (TypeScript).** A TS `npx` scaffolder that generates each agent's
  ERC-8004 registration + A2A server + agent card (plus MCP/x402 we ignore). TypeScript also gives the
  first-class EAS SDK. agent0-sdk (TS ERC-8004 library, v0.31 alpha) was the considered alternative;
  the rationale is recorded as a SevenD Design Decision.
- **What the scaffold doesn't cover — added on top:** ERC-8004 reputation (giveFeedback / getSummary),
  the EAS attestation embedded in the A2A delivery, and the CLIENT-side approval logic.
- **Level-1 SevenD bootstrap.** The PoC dir becomes a Level-1 SevenD project (`Product.md` + `Tech.md`
  + a PoC-scoped `CLAUDE.md`) before any workflow code, giving the build lightweight structure and the
  agent its onboarding rules. The PoC-scoped `CLAUDE.md` lives in the PoC folder — it does not touch
  the repo-root `CLAUDE.md`.
- **Base Sepolia (84532), testnet.** Deliberately different from the Base-mainnet rule that governs
  `hackathon/guild-os/` — the prompt calls this out so the agent doesn't inherit the wrong network.
- **Reputation direction.** CLIENT leaves feedback on DEV's agent; they're separate EOAs, which is
  exactly what ERC-8004 `giveFeedback()` requires (it reverts on self-feedback).
