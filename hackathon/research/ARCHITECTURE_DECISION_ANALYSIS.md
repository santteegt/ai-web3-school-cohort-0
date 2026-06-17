# GuildOS — Architecture Decision: Custom Workflow vs. Harness Pack

> **Purpose:** Determine whether GuildOS should be built as a custom agentic workflow or as a skills/plugin pack compatible with OpenClaw, Hermes, Claude Code, and similar agent harnesses.
> **Created:** 2026-06-07
> **Researched by:** Sensei (Claude via Cowork)
> **Sources:** docs.openclaw.ai · hermes-agent.org · arize.com · flowtivity.ai · sajalsharma.com · agentskills.io · github.com/NousResearch/hermes-agent · agentfightclub.xyz/skill.md

---

## TL;DR

**Build custom first; add harness compatibility as a Day 4–5 layer.**

A pure harness pack cannot satisfy GuildOS's core requirements: two separate agent processes with distinct identities, different LLM providers (Claude for Orchestrator, GLM-5.1 for Specialist), A2A HTTP endpoints between them, and ZeroDev smart-account wallet signing for on-chain operations. No existing harness (OpenClaw, Hermes, Claude Code) manages this split-model, dual-process topology out of the box within a 7-day build.

However, a **harness compatibility layer** — an MCP server wrapping GuildOS operations plus SKILL.md files for ClawHub — is achievable in < 1 day after the core workflow is working, and it significantly raises the demo ceiling: judges can interact with GuildOS directly from their own Claude Code or OpenClaw session.

**Recommended path:** Custom Python workflow (Days 1–4) → MCP server + SKILL.md harness layer (Day 5) → demo polish (Days 6–7).

---

## 1. What Each Harness Actually Provides

### OpenClaw
[OpenClaw](https://docs.openclaw.ai) is an open-source self-hosted agent gateway (MIT license) with 20+ messaging channels, a plugin SDK, and a skills system.

**What it provides for GuildOS:**
- `fightclub_*` MCP tools (ClawBank integration) — direct AgentFightClub operations without any custom code: `fightclub_summon`, `fightclub_mint_shares`, `fightclub_vote`, `fightclub_process`, `fightclub_payment`
- Skills (AgentSkills-compatible SKILL.md format) with ClawHub marketplace — GuildOS skills can be published and installed with `openclaw skills install guildos`
- ACP (Agent Client Protocol) harness — routes sessions to Claude Code, Codex, Gemini CLI, Cursor, etc. through an `acpx` backend
- Plugin SDK — can register custom agent harnesses and LLM providers via TypeScript

**What it does NOT provide for GuildOS:**
- Two independent agent processes with separate ERC-8004 identities (OpenClaw runs one orchestrating agent per session; sub-agents are not first-class separate processes with distinct on-chain identities)
- GLM-5.1 as a first-class provider (not in the built-in provider list; requires a custom provider plugin — TypeScript only, not Python)
- A2A HTTP transport between agents (OpenClaw ACP coordinates harnesses, not A2A endpoints)
- ZeroDev wallet signing (no built-in EVM transaction signing; requires a custom plugin or external call)

### Hermes
[Hermes](https://hermes-agent.org) is NousResearch's open-source agent harness (Feb 2026, 140k+ GitHub stars, most-used agent on OpenRouter as of June 2026).

**What it provides for GuildOS:**
- Reads AGENTS.md / CLAUDE.md from cwd automatically — GuildOS context is injected immediately into any Hermes session started in this repo
- Open model support — can call any OpenAI-compatible API, including GLM-5.1 via ZhipuAI's OpenAI-compatible endpoint
- Messaging gateway (Telegram, Discord, Slack, WhatsApp) — could serve as the human review interface for Gate 1 (membership approval) and Gate 2 (deliverable acceptance), replacing the "minimal CLI" spec
- Session persistence (SQLite + FTS5 search) and cron scheduling
- Subagent delegation — child runs with structured returns to parent

**What it does NOT provide for GuildOS:**
- Two separate agent identities with distinct ERC-8004-anchored wallet addresses (Hermes profiles are isolated roots on one machine, not on-chain identities)
- A2A HTTP endpoints — Hermes subagent delegation is in-process parent→child, not A2A over HTTP between network-addressable agents
- AgentFightClub integration (no built-in Moloch skills; requires moloch-agent CLI called as a tool)
- ZeroDev wallet signing (no built-in EVM tooling; can call external scripts via exec tool)

### Claude Code / Claude Agent SDK
[Claude Code](https://code.claude.com) is Anthropic's coding agent harness with AGENTS.md/CLAUDE.md context injection, SKILL.md instruction packs, MCP tools, and subagent spawning.

**What it provides for GuildOS:**
- This repo already has AGENTS.md → Claude Code sessions in this directory have full GuildOS context automatically
- SKILL.md — packageable as Claude Code skills (works in OpenClaw, Hermes, Codex CLI, Gemini CLI via AgentSkills spec)
- MCP tools — any GuildOS MCP server is immediately callable from Claude Code sessions
- Subagents — isolated Claude Code child sessions for subtask work

**What it does NOT provide for GuildOS:**
- GLM-5.1 for the Specialist (Claude Code uses Anthropic models only; no provider swapping)
- A2A endpoints or dual-process topology
- EVM wallet signing

---

## 2. The Core Architecture Constraints That Drive the Decision

These five constraints together determine that a pure harness pack is not viable as the primary architecture:

| Constraint | Why it blocks a pure harness approach |
|---|---|
| **Dual agent identity** | Orchestrator and Specialist each need a distinct ERC-8004 on-chain address and a distinct ZeroDev smart account. No existing harness provisions two first-class agent identities in one session. |
| **Dual LLM providers** | Orchestrator uses Claude API; Specialist uses GLM-5.1 (ZhipuAI). No harness natively mixes providers per-agent in one session without a custom provider plugin. |
| **A2A HTTP transport** | A2A requires each agent to expose an HTTP endpoint (A2A card, task receive, result return). Existing harnesses route internal messages; they don't provision external A2A-compliant HTTP servers. |
| **ZeroDev wallet signing** | On-chain deliverable hash commitment and AgentFightClub settlement require Python-side transaction signing via ZeroDev Kernel. This is infrastructure, not a skill. |
| **Hackathon timeline** | Building custom provider plugins for Hermes/OpenClaw (TypeScript for OpenClaw, Python for Hermes) would consume 1–2 days before any GuildOS-specific code is written. |

---

## 3. Feature Coverage Matrix

For each GuildOS MVP feature, this matrix scores how much each architecture approach covers without custom code:

| GuildOS MVP Feature | Custom Workflow | OpenClaw harness pack | Hermes harness pack | Claude Code harness pack |
|---|---|---|---|---|
| Orchestrator Agent (Claude API) | ✅ Direct API call | ⚠️ Claude via ACP adapter | ✅ Via OpenAI-compat endpoint | ✅ Native model |
| Specialist Agent (GLM-5.1) | ✅ Direct ZhipuAI API call | ❌ No GLM-5.1 provider | ✅ Via OpenAI-compat endpoint | ❌ Anthropic only |
| ERC-8004 identity (separate addresses) | ✅ Two private keys, two accounts | ❌ Single agent session | ❌ Profiles share machine, not on-chain identities | ❌ Single agent session |
| A2A HTTP endpoints (Orch ↔ Spec) | ✅ FastAPI per agent process | ❌ No A2A server provisioning | ❌ No A2A server provisioning | ❌ No A2A server provisioning |
| AgentFightClub (summon/vote/process) | ✅ moloch-agent CLI subprocess | ✅ `fightclub_*` MCP tools built-in | ⚠️ moloch-agent CLI via exec tool | ⚠️ MCP server call |
| ERC-8004 profile read | ✅ HTTP call to 8004scan API | ⚠️ HTTP call via web tool | ⚠️ HTTP call via web tool | ⚠️ HTTP call via MCP/web tool |
| ERC-8004 reputation write-back | ✅ eth_sendTransaction (ZeroDev) | ❌ No EVM signing | ❌ No EVM signing (exec workaround) | ❌ No EVM signing |
| ZeroDev wallet signing | ✅ zerodev-aa Python SDK | ❌ No built-in EVM support | ⚠️ Possible via exec to Python script | ❌ No built-in EVM support |
| EAS deliverable attestation | ✅ `web3.py` `EASClient.attest()` | ❌ No EVM signing | ⚠️ Exec to Python script | ❌ No EVM signing |
| Human review CLI (Gate 1, Gate 2) | ✅ Python input() or simple web form | ✅ Via OpenClaw messaging gateway | ✅ Via Hermes Telegram/Discord | ⚠️ Manual Claude Code prompt |
| Guild context store (JSON mock) | ✅ Python dict / JSON file | ✅ `workspace-create` + `memory-post` | ✅ SQLite session store | ✅ File tool |
| AgentFightClub treasury settlement | ✅ moloch-agent subprocess | ✅ `fightclub_payment` MCP tool | ⚠️ moloch-agent via exec | ⚠️ MCP server call |

**Scorecard:**
| Architecture | ✅ Fully supported | ⚠️ Partial | ❌ Not supported |
|---|---|---|---|
| Custom Python Workflow | **11** | 0 | 0 |
| OpenClaw harness pack | 3 | 3 | **5** |
| Hermes harness pack | 3 | 5 | **3** |
| Claude Code harness pack | 2 | 3 | **6** |

---

## 4. The Harness Compatibility Layer (Additive — Day 5)

Even though a custom workflow is the right primary architecture, a harness compatibility layer is worth building on Day 5. It does three things:

1. **Judges can interact with GuildOS from their own Claude Code or OpenClaw session** — which is likely what judges are running during a demo. An MCP server + SKILL.md makes GuildOS an installable tool.
2. **ClawHub distribution** — publishing to clawhub.ai gives GuildOS post-hackathon discoverability.
3. **OpenClaw `fightclub_*` shortcut** — the ClawBank AgentFightClub MCP tools are already wired in OpenClaw. GuildOS's MCP server can delegate AgentFightClub calls to OpenClaw's built-in `fightclub_*` tools when running inside OpenClaw, eliminating the need for a separate moloch-agent subprocess in that context.

### MCP Server — `guildos-mcp` (FastAPI, ~4 tools)

```python
# guildos_mcp.py — exposes GuildOS operations as MCP tools

@mcp.tool()
async def guild_launch(mandate: str, treasury_eth: float) -> dict:
    """Launch a new GuildOS guild with mandate and funded treasury.
    Returns: {guild_address, tx_hash, dao_url}"""
    # calls moloch-agent summon + wrap-eth + approve-token + tribute

@mcp.tool()
async def task_delegate(guild_address: str, task_spec: dict) -> dict:
    """Delegate a task from Orchestrator to Specialist via A2A.
    Returns: {a2a_message_id, specialist_address, task_id}"""
    # POSTs A2A task message to Specialist's HTTP endpoint

@mcp.tool()
async def deliverable_accept(guild_address: str, deliverable_hash: str) -> dict:
    """Accept a deliverable and release treasury payment.
    Returns: {settlement_tx_hash, reputation_update_tx_hash}"""
    # calls moloch-agent payment + ZeroDev ERC-8004 write

@mcp.tool()
async def reputation_check(agent_address: str) -> dict:
    """Read an agent's ERC-8004 profile from 8004scan.
    Returns: {name, capabilities, delivery_count, acceptance_rate, recent_deliveries}"""
    # HTTP GET to 8004scan API
```

### SKILL.md (AgentSkills-compatible — works in Claude Code, OpenClaw, Hermes, Codex CLI, Gemini CLI)

```markdown
---
name: guildos
description: Launch and operate a GuildOS guild — agent coordination studio for verifiable work with on-chain reputation and Moloch treasury.
metadata: {"openclaw": {"requires": {"config": ["mcp.servers.guildos"]}, "homepage": "https://github.com/santteegt/ai-web3-school-cohort-0"}}
---

## GuildOS — Programmable Agent Coordination Studio

GuildOS coordinates founding agents and specialist agents for verifiable work:
treasury (Moloch v3), reputation (ERC-8004), communication (A2A), execution (GLM-5.1).

### /guildos-launch <mandate> <eth_amount>
Launch a new guild with a mandate string and ETH treasury commitment.
Steps: summon DAO → wrap ETH → tribute to treasury → return guild address and tx hash.

### /guildos-status <guild_address>
Show current guild state: treasury balance, active proposals, member list, and ERC-8004 profiles.

### /guildos-accept <guild_address> <deliverable_hash>
Accept a delivered task: sponsor + vote on payment proposal → process → reputation write-back.

### MCP tools required
- guildos_guild_launch
- guildos_task_delegate
- guildos_deliverable_accept
- guildos_reputation_check
```

---

## 5. Recommended Architecture

```
┌────────────────────────────────────────────────────────────┐
│                GuildOS Architecture (Hybrid)               │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Custom Python Workflow  (PRIMARY — Days 1–4) │  │
│  │                                                      │  │
│  │  guildos.py / orchestrator.py / specialist.py        │  │
│  │                                                      │  │
│  │  Orchestrator Agent          Specialist Agent        │  │
│  │  ├── Claude API              ├── GLM-5.1 (ZhipuAI)  │  │
│  │  ├── ERC-8004 identity A     ├── ERC-8004 identity B │  │
│  │  ├── ZeroDev wallet A        ├── ZeroDev wallet B    │  │
│  │  ├── FastAPI A2A endpoint    ├── FastAPI A2A endpoint│  │
│  │  └── moloch-agent CLI        └── task execution loop │  │
│  │                                                      │  │
│  │  shared: Base Sepolia RPC · 8004scan API             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     Harness Compatibility Layer  (ADDITIVE — Day 5)  │  │
│  │                                                      │  │
│  │  guildos_mcp.py                                      │  │
│  │  ├── guild_launch()    → wraps orchestrator.py       │  │
│  │  ├── task_delegate()   → A2A HTTP call               │  │
│  │  ├── deliverable_accept() → moloch settle + ERC-8004 │  │
│  │  └── reputation_check()   → 8004scan API             │  │
│  │                                                      │  │
│  │  skills/guildos/SKILL.md                             │  │
│  │  └── /guildos-* slash commands (Claude Code/OpenClaw)│  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘

Harness compatibility layer connects to:
  - Claude Code (via .claude/mcp.json MCP server registration)
  - OpenClaw  (via openclaw config + fightclub_* MCP shortcut)
  - Hermes    (via exec tool calling guildos_mcp.py)
  - Any AgentSkills harness (via skills/guildos/SKILL.md)
```

### Why not invert (harness-first, custom second)?

A harness-first approach would spend Days 1–2 setting up a harness runtime and registering custom plugins before writing any GuildOS-specific code. This adds at minimum:

- OpenClaw path: TypeScript GLM-5.1 provider plugin + custom EVM signing plugin (2 days)
- Hermes path: Python profile config + GLM-5.1 as custom provider + exec hooks for ZeroDev (1.5 days)
- Claude Code path: blocked entirely (cannot swap to GLM-5.1 for Specialist)

In each case, the harness integration work exceeds what the harness delivers in value for the hackathon demo. The custom workflow reaches a working end-to-end demo loop faster.

---

## 6. Harness-Specific Notes

### OpenClaw
**Best use:** Use the built-in `fightclub_*` MCP tools as a shortcut for AgentFightClub calls when the demo is running inside an OpenClaw session. Register the GuildOS MCP server as a plugin; OpenClaw's `plugin_tools_mcp_bridge` exposes it to ACP-spawned Claude Code sessions automatically.

**Key gap:** OpenClaw's AgentFightClub path uses ClawBank's Turnkey wallet, not ZeroDev. For the hackathon, ZeroDev is the recommended wallet layer (as established in ERC4337_CAW_ANALYSIS.md). This means the GuildOS custom workflow signs transactions, and OpenClaw's `fightclub_*` tools are an optional convenience layer for the demo UI only — not the primary signing path.

**Integration point:** `openclaw config set plugins.entries.guildos-mcp.enabled true` + register MCP server URL.

### Hermes
**Best use:** The existing AGENTS.md in this repo is automatically read by Hermes. A Hermes session started in `~/AIxWeb3_School` already has full GuildOS context. The Hermes messaging gateway (Telegram/Discord) is the cleanest implementation of the "human review" gates — Gate 1 (membership approval) and Gate 2 (deliverable acceptance) can be presented as Telegram messages to the human founder, with approve/reject buttons. This replaces the "minimal CLI" spec with something significantly more polished at near-zero extra cost.

**GLM-5.1 note:** Hermes supports OpenAI-compatible endpoints. ZhipuAI exposes a compatible API at `https://open.bigmodel.cn/api/paas/v4/`. A Hermes profile for the Specialist Agent configured with this endpoint would run GLM-5.1 natively. However, this still does not solve the dual-identity ERC-8004 requirement (two on-chain addresses), which requires two separate processes regardless.

**Integration point:** Create a Hermes profile for GuildOS: `hermes profile create guildos --model zhipuai/glm-4-long --system-prompt-file prompts/specialist-agent.md`.

### Claude Code / Claude Managed Agents
**Best use:** The AGENTS.md file already serves Claude Code sessions. Publishing `skills/guildos/SKILL.md` to ClawHub makes GuildOS available as a `/guildos-*` slash command to any Claude Code user. This is the lightest-weight harness path and takes ~2 hours on Day 5.

**Claude Managed Agents note:** For post-hackathon work, Claude Managed Agents could host the Orchestrator (Claude model, managed container, MCP tools). The Specialist would still need a separate process for GLM-5.1. This hybrid — Managed Agents for Orchestrator + custom Python for Specialist — is an interesting post-hackathon architecture.

---

## 7. Day 1 Test Checklist (Architecture Validation)

These are the operations to validate before committing to the custom workflow architecture:

1. **Two independent ZeroDev accounts from two separate private keys on Base Sepolia** — confirm each produces a distinct deterministic smart account address; these become the ERC-8004 agent identities.
2. **A2A FastAPI round-trip** — Orchestrator's FastAPI posts a task message to Specialist's FastAPI endpoint; Specialist returns a structured result; confirm message schema matches A2A spec.
3. **GLM-5.1 tool calling via ZhipuAI API** — call the API from Python, provide a task, receive structured output; confirm the output is hashable (SHA-256 consistent across two calls with same input).
4. **moloch-agent summon on Base Sepolia** — confirm `moloch-agent summon --params guild.json` produces a deployed Baal.sol contract address on Base Sepolia.
5. **ZeroDev UserOp on Base Sepolia** — confirm `account.send_user_op([Call(to=GUILD_CONTRACT, data=hash_calldata)])` succeeds and produces a visible tx hash on Basescan.

---

## 8. Build Schedule (Revised)

| Day | Primary focus | Architecture path |
|---|---|---|
| 1 | Validate Day 1 checklist (Section 7); set up two ZeroDev accounts; A2A FastAPI round-trip | Custom workflow |
| 2 | Guild formation: summon + wrap-eth + tribute; ERC-8004 profile reads | Custom workflow |
| 3 | A2A task delegation: Orchestrator → Specialist; GLM-5.1 execution loop | Custom workflow |
| 4 | On-chain deliverable hash commit; AgentFightClub settle; ERC-8004 reputation write-back | Custom workflow |
| 5 | MCP server (`guildos_mcp.py`) + SKILL.md; ClawHub publish; Hermes Gate 1/Gate 2 UI | Harness layer |
| 6 | End-to-end demo run; pre-stage membership proposal/vote; Basescan link verification | Both |
| 7 | Demo polish; fallback screens; submission checklist | Both |

---

## 9. Stability and Risk Assessment

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| GLM-5.1 API not OpenAI-compatible enough for Hermes | Low | Low (Hermes is additive) | Use direct ZhipuAI Python SDK in custom workflow; Hermes path is optional |
| OpenClaw `fightclub_*` tools use ClawBank wallet (Turnkey), not ZeroDev | Confirmed | Low (OpenClaw is additive) | GuildOS custom workflow signs all transactions; `fightclub_*` is a demo shortcut only |
| A2A FastAPI endpoints unreachable across machines | Medium | High | Run both agents on same machine for demo (localhost A2A); ngrok for remote judges |
| ZhipuAI API rate limit during live demo | Low | High | Pre-run the Specialist execution step; cache output; present live as "completed earlier" |
| SKILL.md format mismatch across harnesses | Low | Low (harness layer is additive) | AgentSkills spec is consistent; test in Claude Code first, then OpenClaw |

---

## Verdict

| Dimension | Custom Workflow | Pure Harness Pack |
|---|---|---|
| MVP feasibility in 7 days | ✅ Yes | ❌ No (dual-identity + dual-model + A2A not solvable) |
| Full demo loop completeness | ✅ All 12 steps | ❌ Steps 2, 3, 4, 7, 8, 12 require custom code anyway |
| Post-hackathon extensibility | ✅ MCP layer added Day 5 | ✅ If it could work |
| Judge accessibility | ⚠️ Custom CLI | ✅ Installable via ClawHub (but only after Day 5 layer) |
| AgentFightClub integration | ✅ moloch-agent CLI (primary) | ✅ `fightclub_*` (shortcut only) |
| GLM-5.1 Specialist | ✅ ZhipuAI Python SDK | ❌ Custom provider plugin needed in all harnesses |
| ERC-8004 dual identity | ✅ Two ZeroDev accounts | ❌ No harness supports dual on-chain agent identities |
| On-chain signing | ✅ ZeroDev Kernel | ❌ Not natively supported in any harness |

**Primary path: Custom Python workflow.**
**Additive path (Day 5): MCP server + SKILL.md for harness compatibility.**

The custom workflow is not a step backward from harnesses — it IS the harness for GuildOS. As the Sajal Sharma framing puts it: a workflow tells the agent what to do; a harness gives the agent what it needs to figure it out. GuildOS's custom workflow is both: it encodes the coordination protocol (what to do) while providing the infrastructure each agent needs (ZeroDev wallet, A2A endpoint, ERC-8004 identity). The harness compatibility layer on Day 5 exposes that infrastructure to the broader ecosystem.

---

*Research date: 2026-06-07 | Agent: Sensei | v1.0*
*Sources: [OpenClaw Docs](https://docs.openclaw.ai) · [OpenClaw ACP](https://docs.openclaw.ai/tools/acp-agents) · [OpenClaw Skills](https://docs.openclaw.ai/tools/skills) · [Hermes Agent](https://hermes-agent.org) · [Arize: Hermes Harness Architecture](https://arize.com/blog/how-hermes-implements-open-source-agent-harness-architecture/) · [Flowtivity: Framework Comparison 2026](https://flowtivity.ai/blog/agent-frameworks-comparison-2026/) · [Agents Have Outgrown Workflows](https://sajalsharma.com/posts/agentic-workflows-to-agent-harnesses/) · [AgentFightClub skill.md](https://agentfightclub.xyz/skill.md)*
