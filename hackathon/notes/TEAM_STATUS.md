# Team / Solo Status — GuildOS Hackathon

> Event: AI × Web3 Agentic Builders Hackathon  
> Deadline: 2026-06-13 12:00 UTC+8  
> Author: Santiago ([@santteegt](https://github.com/santteegt))  
> Written: 2026-06-07

---

## Status: Solo — Dogfooding Mode

GuildOS is a **solo entry**. There is no human co-founder, no human teammate, and no team formation planned before the deadline.

This is intentional. GuildOS's thesis is that one person plus a coordinated set of specialist agents can execute work that previously required a team. The hackathon build is itself a live proof of concept: the project is being built by one human developer using the same agent-coordination pattern the product proposes.

**The dogfood framing:** Santiago is the Human Founder (Marco, in the proposal's scenario). Sensei / Claude is the Orchestrator Agent. Specialist agents — code generation, research synthesis, on-chain interaction — are invoked as needed per task type. Every module owned below maps to a capability that, in the GuildOS product, would be delegated to a registered specialist agent via A2A.

---

## Modules I Own

The following modules are Santiago's direct responsibility to ship before the deadline. Each maps to a GuildOS layer.

### 1. Guild Formation Layer (`guild/`)

Scripted integration with AgentFightClub (Moloch v3):
- `launch()` — initialize guild with mandate string and treasury address
- `commit()` — fund treasury with 0.3 ETH equivalent on Base Sepolia
- `propose()` + `vote()` — admit Specialist Agent as guild member
- `settle()` — release treasury to Specialist on deliverable acceptance

Fallback: DAOhaus SDK direct deploy if AgentFightClub alpha API is unstable.

### 2. ERC-8004 Identity Module (`identity/`)

On-chain agent profile reads and reputation write-back:
- Read Orchestrator Agent profile (capability claims, A2A endpoint)
- Read Specialist Agent profile (before state: delivery count, acceptance rate)
- Write delivery record after acceptance: 6 fields via `recordDelivery()` (task type, deliverable hash, acceptance block, payment in wei, guild address, A2A message ID)
- Cache profile responses for demo resilience (JSON fallback)

### 3. Orchestrator Agent (`orchestrator/`)

The coordination brain — runs on Claude Code as an MCP server:
- MCP tools: `guild_launch`, `talent_query`, `task_invite`, `task_delegate`, `deliverable_review`, `settle`, `reputation_write`
- Mandate parsing from human input
- ERC-8004 talent shortlist generation (MVP: hardcoded Specialist profile)
- A2A message construction and dispatch (task delegation, acceptance)
- Automated deliverable pre-check (hash present, format valid)
- Human review presentation (summary + evaluation report)
- Gate management: surfaces Gate 0, 0.5, 1, 2 checkpoints to human

### 4. A2A Communication Layer (`a2a/`)

Cross-agent message protocol using `a2a-sdk` v1.0.0:
- Orchestrator A2A card (hosted endpoint, capability manifest)
- Specialist A2A card (endpoint, capability claims)
- Message types implemented: `task/invite`, `task/quote`, `task/accepted`, `task/delivered`
- Message log (append-only JSON) for demo traceability
- A2A message ID generation and propagation to ERC-8004 write

### 5. Specialist Agent (`specialist/`)

Execution agent — runs as a separate Python service backed by GLM-5.1:
- Receives A2A task messages from Orchestrator
- Decomposes task using GLM-5.1 long-horizon planning
- Executes task (code generation, analysis, or spec writing — task type locked Day 1)
- Hashes deliverable (SHA-256)
- Commits hash to Base Sepolia guild contract
- Returns `task/delivered` A2A message with deliverable reference and hash
- Exposes A2A endpoint (local service, port-forwarded or ngrok for demo)

### 6. On-Chain Deliverable Commitment (`chain/`)

Minimal on-chain integration (no custom Solidity):
- Submit deliverable hash to guild contract storage slot via `eth_sendTransaction`
- Record settlement tx hash for demo verification
- Emit ERC-8004 `DeliveryRecorded` event after `settle()` confirms
- All interactions via ethers.py + Alchemy RPC on Base Sepolia

### 7. Guild Context Store (`store/`)

Shared state bus for the guild session (MVP: JSON file per guild):
- Guild session record: mandate, treasury address, member list, task state, deliverable hash, settlement tx
- State transitions: `FORMING → ACTIVE → DELIVERED → SETTLED` (or `DISPUTED`)
- Dispute stub: `DISPUTED` state written on Gate 2 rejection; ragequit path documented

### 8. Demo Harness (`demo/`)

The thin CLI wrapper that runs the end-to-end demo loop:
- Launches Orchestrator and Specialist in two terminal windows
- Presents human gates as explicit y/N prompts with context
- Prints Basescan links for every on-chain transaction
- Shows ERC-8004 profile before/after delta for Specialist
- Graceful error output at every integration boundary

### 9. Submission Artifacts (`hackathon/`)

Non-code deliverables required by the platform:
- GitHub README with problem, architecture diagram, run instructions, API/SDK used
- 3–5 min demo video or live demo link
- Basescan transaction hashes: (1) deliverable hash commitment, (2) settlement release
- ERC-8004 profile before/after screenshots
- Cobo CAW key config and agent wallet address evidence

---

## Agent Assistance Map

Each module above was or will be developed using Sensei as the Orchestrator Agent and specialist sub-agents as needed:

| Module | Human (Santiago) owns | Agent assists with |
|---|---|---|
| Guild Formation | Integration, debug, tx signing | Scripting, ABI calls, error analysis |
| ERC-8004 Identity | Profile schema, write-back logic | API call scaffolding, field mapping |
| Orchestrator Agent | MCP tool definitions, gate logic | Tool handler boilerplate, prompt templates |
| A2A Layer | Message schema, endpoint wiring | SDK usage, message log structure |
| Specialist Agent | GLM-5.1 prompt design, service wiring | Python service scaffold, A2A handler |
| On-Chain Commitment | Tx construction, RPC config | ethers.py snippets, hash verification |
| Guild Context Store | State machine design | JSON schema, state transition code |
| Demo Harness | UX flow, gate sequencing | CLI scaffold, Basescan link formatting |
| Submission Artifacts | Review, final edit | Draft text, diagram generation |

---

*This memo documents solo status and module ownership for clarity during the build sprint and for submission record-keeping.*
