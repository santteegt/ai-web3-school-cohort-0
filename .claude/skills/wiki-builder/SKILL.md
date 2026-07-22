# Wiki Builder

Incrementally process raw source notes in the AIxWeb3 Obsidian vault and build/update a structured, interlinked wiki.

## OKF alignment

This vault's schema is aligned with Google's [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) — a lightweight spec formalizing the "LLM wiki" pattern this vault already followed. Concretely:

- Every page's frontmatter has a non-empty `type` — OKF's only mandatory field. Already true for all existing pages.
- New/re-ingested pages also carry OKF's recommended fields: `description`, `resource` (source pages only), `tags`, `timestamp`.
- **Backward compatible, not retroactive.** Pages ingested before this alignment keep their original frontmatter shape (`title, type, tags, source_count, date_updated` for concepts/topics; `title, type, tags, source_file, source_hash, date_ingested` for sources) untouched. Both the old and new field names are valid in this vault — the schemas below describe the target shape for anything newly ingested or re-touched, not a rewrite requirement for existing pages. `concept-cards` and `quiz` only read fields common to both shapes (`title`, `tags`, body sections), so neither consumer skill is affected either way.
- **Links are intentionally dual-syntax.** New pages use OKF markdown path-links (`[Title](slug.md)`); pre-existing pages keep Obsidian `[[wikilinks]]`. Obsidian resolves both forms identically in its own graph view, so nothing is lost by leaving old pages alone.
- `log.md` stays oldest-first, append-only (not OKF's newest-first convention) — a deliberate deviation, since append-only keeps git diffs small and conflict-free for a git-tracked personal vault.
- `timestamp` values use a `T00:00:00Z` sentinel unless a real time is known — only date-level precision is actually tracked by this ingest process; don't mistake the sentinel for genuine intraday tracking.

## Trigger

`/wiki-build` — run without arguments to process all new or changed sources.

## When to use

- After adding new files to `knowledge-base/AIxWeb3/raw/`
- After editing an existing raw file (hash change triggers re-processing)
- First run builds the entire wiki from scratch

## Vault paths (absolute)

| Path | Purpose |
|---|---|
| `/Users/santteegt/AIxWeb3_School/knowledge-base/AIxWeb3/raw/` | Immutable source files (never modify) |
| `/Users/santteegt/AIxWeb3_School/knowledge-base/AIxWeb3/wiki/` | LLM-generated wiki pages |
| `wiki/.hashes.json` | Hash tracker for incremental processing |
| `wiki/index.md` | Content-oriented catalog of all pages |
| `wiki/log.md` | Append-only chronological ingest log |
| `wiki/sources/` | One summary page per raw source |

## Procedure

### Step 1 — Load existing hashes

Read `wiki/.hashes.json`. If missing, treat as `{}`.

### Step 2 — Detect changes

For each `*.md` file in `raw/`, compute SHA256:
```bash
shasum -a 256 "knowledge-base/AIxWeb3/raw/<filename>"
```
Compare against stored hash. Skip files with matching hashes. Queue new/changed files for processing.

### Step 3 — Process each queued source

For each source file to process:

**3a. Create/overwrite the source summary page** at `wiki/sources/<slug>.md`:
- `<slug>` = lowercase filename with spaces replaced by hyphens, no extension
- Frontmatter:
  ```yaml
  ---
  title: "<Source Title>"
  type: source
  description: "<one sentence summarizing what this source covers>"
  tags: [<2–5 topic tags>]
  resource: "raw/<filename>.md"
  source_hash: "sha256:<hash>"
  timestamp: "<YYYY-MM-DD>T00:00:00Z"
  ---
  ```
  (`resource` replaces the older `source_file` key name — same value/semantics, aligned to OKF's standard field name. `timestamp` replaces `date_ingested`.)
- Body sections: `## Summary` (3–5 sentences), `## Key Concepts` (bulleted list, OKF path-links — see Step 3c), `## Notable Points` (2–3 significant claims or quotes)

**3b. Extract concepts and topics** — identify all distinct concepts, frameworks, and named technical terms in the source. For each:

- Check `wiki/index.md` to see if a page already exists for it
- If the page exists: read it, add new info, update `source_count` in frontmatter, add a new `[[source slug]]` link in the references section
- If the page is new: create `wiki/<concept-slug>.md` with frontmatter:
  ```yaml
  ---
  title: "<Concept Name>"
  type: concept
  description: "<one sentence — reuse/trim the ## Definition opening line, no separate authoring pass>"
  tags: [<domain tags, e.g. ai-foundations, web3, bridge>]
  source_count: 1
  timestamp: "<YYYY-MM-DD>T00:00:00Z"
  ---
  ```
  (`timestamp` replaces the older `date_updated` key name, widened to full ISO 8601 — see OKF alignment note above for the sentinel-time caveat.)
  Body sections: `## Definition` (1–3 sentences), `## Key Points` (bulleted list), `## Related Concepts` (OKF path-links to related pages — see Step 3c), `## Sources` (links to source pages that cover this concept)

**3c. Add links** — after all concept pages for this source are written:
- Use OKF-style markdown path-links for every new cross-reference: `[Concept Name](concept-slug.md)` for a page in `wiki/`, `[Source Title](sources/source-slug.md)` for a source page.
- **Do not rewrite links in pre-existing pages** you're not otherwise touching — this vault is intentionally dual-syntax (see OKF alignment note above). Only convert an existing page's links to path-link form if you're already re-ingesting/rewriting that specific page's body for another reason.
- In the source summary page: link every mentioned concept.
- In each concept page: link to other co-appearing concepts and to parent/child topic pages.
- Ensure no orphan pages — every new page must be linked from at least one other page.

### Step 4 — Update `wiki/index.md`

Rewrite the index to reflect all current wiki pages. `index.md` carries a root frontmatter block declaring `okf_version` (the only place OKF permits frontmatter on an index file), followed by bulleted link-with-description sections. Structure:
```markdown
---
okf_version: "0.1"
---

# Wiki Index

_Last updated: YYYY-MM-DD — N pages_

## Topics (Overview Pages)
- [Topic Title](topic-slug.md) — one-line description
...

## Sources
- [Source Title](sources/source-slug.md) — one-line description
...

## Concepts
- [Concept Title](concept-slug.md) — one-line description
...

## Generated Outputs
- [concepts/](../concepts/) — filed-back Marp decks, diagrams, and other query outputs (not hash-tracked; see AGENTS.md's "answers can be filed back" idea)
```
Concepts may be split into per-domain subsections (e.g. `### AI Foundations: LLM`) as the list grows, matching this vault's existing practice — the exact grouping is a curation choice, not a fixed template.

Existing bullets already in `[[wikilink]]` form don't need to be reconverted just because the file is being rewritten this pass — but `index.md` itself (unlike body pages) is the vault's front door and single most-likely-read file for any external tool or GitHub visit, so its own bullets should use the `[Title](path.md)` form going forward.

### Step 5 — Append to `wiki/log.md`

Append one entry per processed source (do not overwrite earlier entries — this log stays oldest-first, append-only; see OKF alignment note above for why):
```markdown
## [YYYY-MM-DD] ingest | <Source Title>

- **Ingest**: <Source Title> processed from `raw/<filename>.md`
- Source: `raw/<filename>.md`
- Hash: `sha256:<hash>`
- Pages created/updated: N
- New concepts: <comma-separated list>
```

### Step 6 — Save updated hashes

Write updated `wiki/.hashes.json`:
```json
{
  "raw/<filename>.md": "sha256:<hash>",
  ...
}
```

Include entries for ALL raw files (not just the ones just processed), so the full state is always reflected.

## Page naming conventions

- Slugs are lowercase, spaces → hyphens: `retrieval-augmented-generation`
- Acronyms expanded in slug, kept in title: `llm.md` → title "Large Language Model (LLM)"
- Multi-word concepts: keep meaningful but concise — `context-window`, `agent-wallet`, `smart-contract`

## Tagging conventions

Use these tag namespaces consistently:
- Domain: `ai-foundations`, `web3-foundations`, `aixweb3-bridge`, `frontier`
- Type: `concept`, `source`, `topic`, `synthesis` (`synthesis` is reserved for filed-back query answers per the LLM-wiki pattern's "good answers can be filed back" idea — not yet used on any page, but valid when that need arises)
- Subtopic: **open vocabulary** — pick whatever specific tag best fits the concept. Examples already in use: `llm`, `prompt`, `context`, `rag`, `agent`, `wallet`, `defi`, `security`, `mcp`, `tool-use`, `identity-reputation`, `privacy-security`, `payment-commerce`, `verifiable-ai`, `wallet-permission`, `dev-tooling`, `governance-coordination`, `decentralized-ai`, plus one-off tags matching a single concept's own name. This list is non-exhaustive by design — don't treat it as a closed set.

## Model guidance

Run this skill with **Sonnet** (not Haiku). Wiki building requires synthesis, cross-referencing, and multi-step reasoning across all source files. Haiku should not be used for this skill.

## Lint procedure

Run on request, or periodically, to health-check the wiki. Two modes:

**Base (OKF conformance):**
- Every non-reserved `.md` file under `wiki/` has parseable YAML frontmatter with a non-empty `type`.
- `index.md` and `log.md` carry no frontmatter except `index.md`'s optional root `okf_version` block.
- Broken cross-links are reported informationally only — OKF explicitly tolerates them by design; never treat as an error.

**Strict (this vault's own hygiene — run this too, not just base):**
- Stale `.hashes.json` entries: recompute live SHA256 for each `raw/*.md` file and compare against the stored hash; flag any mismatch for re-ingest.
- Orphan pages: every page in `wiki/` should be linked from at least one other page.
- Untracked sibling output directories: confirm anything like `concepts/` is at least referenced from `index.md`'s `## Generated Outputs` section.
- Missing domain overview pages: each Concepts domain grouping in `index.md` should have a corresponding `-overview` topic page; flag any domain that doesn't.

## Verification

After running, confirm:
- `wiki/.hashes.json` has one entry per raw file
- `wiki/index.md` lists all source and concept pages, has root `okf_version` frontmatter, and uses `[Title](path.md)` links for its own bullets
- Re-running immediately skips all files (no changes detected)
- Obsidian graph view shows interconnected nodes with no isolated orphan pages (works regardless of `[[wikilink]]` vs `[Title](path.md)` — Obsidian indexes both for its graph)
