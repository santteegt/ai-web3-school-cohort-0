# Concept Cards — Session Summary

**Date:** 2026-05-22  
**Agent:** Sensei (Claude Sonnet 4.6 via Claude Code)

---

## Initial Prompt

Santiago asked Sensei to:

1. **Build a wiki-like knowledge base** from the 7 raw notes in `knowledge-base/AIxWeb3/raw/` — creating wiki pages, concept pages, smart tags, wikilinks, and a maintained index. Each wiki page should reference its raw source and hash for incremental processing. The process should become a reusable skill stored in the project.

2. **Create Marp concept cards** for all topics in the wiki — one slide per concept with: one-sentence explanation, concrete example, and common misconception/boundary. Store the Marp deck in the vault's `concepts/` folder and export HTML to `submissions/`. This should also be a reusable skill.

3. Additionally: update `AGENTS.md` to document both skills, and write this summary file.

4. **Answer:** Is it recommended to plan with Sonnet and execute with Haiku subagents without sacrificing quality?

---

## Answer: Sonnet vs Haiku Model Split

**Recommendation: split by task type, not by phase.**

- **Wiki building → Sonnet only.** The task requires synthesis, cross-referencing across all 7 sources simultaneously, and reasoning about what merits its own page vs. a mention. Each step informs the next — you can't write cross-links until you've seen all related pages. Haiku cannot safely handle this without quality loss.

- **Concept card generation → Haiku subagents orchestrated by Sonnet.** Card generation is bounded and templated: read one wiki page → fill three fields. This is embarrassingly parallel. Spawn Haiku subagents per concept page. The structured format means Haiku won't sacrifice meaningful quality.

**How to implement:** In Claude Code, use `Agent(model: "haiku", ...)` in Agent tool calls for per-concept generation. The main Sonnet session handles orchestration, index reading, deck assembly, and export.

---

## Tasks Performed

### 1. Created Wiki Builder Skill

**File:** [`.claude/skills/wiki-builder/SKILL.md`](.claude/skills/wiki-builder/SKILL.md)

Encodes the complete procedure for incremental wiki building:
- SHA256 hash comparison via `shasum -a 256` to detect new/changed raw files
- Source summary pages in `wiki/sources/<slug>.md`
- Concept pages at `wiki/<concept-slug>.md` with YAML frontmatter (type, tags, source_count, source_hash)
- Wikilinks between all related concepts
- `wiki/index.md` catalog and `wiki/log.md` ingest log
- `wiki/.hashes.json` for incremental state

### 2. Built the Wiki from All 7 Raw Sources

Processed: `AI Fundamentals - Introduction.md`, `LLMs.md`, `Context.md`, `Prompt.md`, `RAG.md`, `AIxWeb3 School.md`, `Program Structure.md`

**Created 56 wiki files total:**
- 7 source summary pages (`wiki/sources/`)
- 47 concept and topic overview pages (`wiki/`)
- `wiki/index.md` — full catalog (54 content pages)
- `wiki/log.md` — ingest log with one entry per source
- `wiki/.hashes.json` — 7 hash entries; re-running `/wiki-build` on unchanged files will skip all processing

**Concept coverage:**
| Layer | Concepts Created |
|---|---|
| LLM | large-language-model, tokens, embeddings, transformer-architecture, hallucination, multimodal, maas |
| Context | context-window, context-engineering, five-layer-agent-context, information-governance, agent-memory, knowledge-base |
| Prompt | prompt-design, instruction, four-segment-prompt, four-control-layers, few-shot-prompting, structured-output, prompt-injection, verification-chain |
| RAG | retrieval-augmented-generation, chunking, vector-database, retriever, re-ranking, citations |
| Agent | ai-agent, prompt-workflow-agent-boundary, tool-calling, state-management, mcp, guardrails, agent-handoff, ai-agent-tracing, vibe-coding |
| AI × Web3 Bridge | chain-aware-context, web3-tool-use, agent-workflow, agent-wallet, machine-payment, agent-identity, verifiable-ai, ai-security |
| Topic Overviews | ai-foundations-overview, aixweb3-bridge-overview, frontier-exploration-overview |

### 3. Created Concept Cards Skill

**File:** [`.claude/skills/concept-cards/SKILL.md`](.claude/skills/concept-cards/SKILL.md)

Encodes the procedure for Marp concept card generation:
- Reads `wiki/index.md` to get all concept pages
- Spawns Haiku subagents per concept for card generation (parallelizable)
- Assembles Marp deck with title slide + one card per concept + sources slide
- Exports HTML via `npx @marp-team/marp-cli` (or CDN fallback if no npx)

### 4. Generated the Marp Concept Deck

**File:** [`knowledge-base/AIxWeb3/concepts/concepts-2026-05-22.md`](knowledge-base/AIxWeb3/concepts/concepts-2026-05-22.md)

37 concept cards covering all AI Foundations and AI × Web3 Bridge topics. Each card has:
- One-sentence explanation (jargon-minimal, self-contained)
- Concrete example (specific tool, scenario, or real-world use case)
- Boundary (real misconception or usage limit practitioners encounter)

To view slides: open in Obsidian with the Marp Slides plugin active.

### 5. Exported HTML

**File:** [`submissions/concept-cards.html`](submissions/concept-cards.html)

Standalone HTML file exported via `npx @marp-team/marp-cli`. Open in any browser — no server or dependencies required.

### 6. Updated AGENTS.md

Added **Section 13: Knowledge Base Skills** to [`AGENTS.md`](AGENTS.md) documenting both `/wiki-build` and `/concept-cards` — including model guidance, input/output paths, and when-to-use criteria.

---

## Files Created/Modified

| File | Action |
|---|---|
| `.claude/skills/wiki-builder/SKILL.md` | Created |
| `.claude/skills/concept-cards/SKILL.md` | Created |
| `knowledge-base/AIxWeb3/wiki/index.md` | Created |
| `knowledge-base/AIxWeb3/wiki/log.md` | Created |
| `knowledge-base/AIxWeb3/wiki/.hashes.json` | Created |
| `knowledge-base/AIxWeb3/wiki/sources/*.md` (7 files) | Created |
| `knowledge-base/AIxWeb3/wiki/*.md` (47 files) | Created |
| `knowledge-base/AIxWeb3/concepts/concepts-2026-05-22.md` | Created |
| `submissions/concept-cards.html` | Created |
| `AGENTS.md` | Updated (Section 13 added) |
| `submissions/CONCEPT_CARDS.md` | Created (this file) |

---

## How to Use the Skills Going Forward

### Add a new raw note and update the wiki:
1. Drop a `.md` file into `knowledge-base/AIxWeb3/raw/`
2. In Claude Code: `/wiki-build`
3. Only the new file gets processed (unchanged files skipped by hash check)

### Regenerate concept cards after new wiki content:
1. In Claude Code: `/concept-cards` (all concepts) or `/concept-cards rag` (filter by tag)
2. New Marp deck saved to `concepts/concepts-<date>.md`
3. New HTML saved to `submissions/concept-cards.html`
