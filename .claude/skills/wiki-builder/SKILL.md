# Wiki Builder

Incrementally process raw source notes in the AIxWeb3 Obsidian vault and build/update a structured, interlinked wiki.

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
  tags: [<2–5 topic tags>]
  source_file: "raw/<filename>.md"
  source_hash: "sha256:<hash>"
  date_ingested: "<YYYY-MM-DD>"
  ---
  ```
- Body sections: `## Summary` (3–5 sentences), `## Key Concepts` (bulleted list with `[[wikilinks]]`), `## Notable Points` (2–3 significant claims or quotes)

**3b. Extract concepts and topics** — identify all distinct concepts, frameworks, and named technical terms in the source. For each:

- Check `wiki/index.md` to see if a page already exists for it
- If the page exists: read it, add new info, update `source_count` in frontmatter, add a new `[[source slug]]` link in the references section
- If the page is new: create `wiki/<concept-slug>.md` with frontmatter:
  ```yaml
  ---
  title: "<Concept Name>"
  type: concept
  tags: [<domain tags, e.g. ai-foundations, web3, bridge>]
  source_count: 1
  date_updated: "<YYYY-MM-DD>"
  ---
  ```
  Body sections: `## Definition` (1–3 sentences), `## Key Points` (bulleted list), `## Related Concepts` (`[[wikilinks]]` to related pages), `## Sources` (links to source pages that cover this concept)

**3c. Add wikilinks** — after all concept pages for this source are written:
- In the source summary page: link every mentioned concept with `[[concept-slug]]`
- In each concept page: link to other co-appearing concepts and to parent/child topic pages
- Ensure no orphan pages — every new page must be linked from at least one other page

### Step 4 — Update `wiki/index.md`

Rewrite the index to reflect all current wiki pages. Structure:
```markdown
# Wiki Index

_Last updated: YYYY-MM-DD — N pages_

## Sources
- [[source-slug]] — one-line description
...

## Concepts
- [[concept-slug]] — one-line description
...

## Topics
- [[topic-slug]] — one-line description (topic pages are high-level groupings)
...
```

### Step 5 — Append to `wiki/log.md`

Append one entry per processed source (do not overwrite earlier entries):
```markdown
## [YYYY-MM-DD] ingest | <Source Title>

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
- Type: `concept`, `source`, `topic`, `synthesis`
- Subtopic: `llm`, `prompt`, `context`, `rag`, `agent`, `wallet`, `defi`, `security`, `mcp`, `tool-use`

## Model guidance

Run this skill with **Sonnet** (not Haiku). Wiki building requires synthesis, cross-referencing, and multi-step reasoning across all source files. Haiku should not be used for this skill.

## Verification

After running, confirm:
- `wiki/.hashes.json` has one entry per raw file
- `wiki/index.md` lists all source and concept pages
- Re-running immediately skips all files (no changes detected)
- Obsidian graph view shows interconnected nodes with no isolated orphan pages
