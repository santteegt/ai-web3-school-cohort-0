# Concept Cards

Generate Marp concept card slides from wiki pages in the AIxWeb3 Obsidian vault.

## Trigger

`/concept-cards [topic]`

- No argument: generate cards for all concepts in `wiki/index.md`
- With argument: filter to concepts tagged with that topic (e.g. `/concept-cards rag`, `/concept-cards llm`)

## When to use

- After `/wiki-build` has been run and `wiki/index.md` is populated
- When preparing study materials or presentations from the knowledge base
- To generate an updated deck after new sources have been ingested

## Vault paths (absolute)

| Path | Purpose |
|---|---|
| `knowledge-base/AIxWeb3/wiki/index.md` | Source of truth for all wiki pages |
| `knowledge-base/AIxWeb3/wiki/<concept-slug>.md` | Individual concept pages to read |
| `knowledge-base/AIxWeb3/concepts/` | Output: Marp `.md` slide decks |
| `submissions/concept-cards.html` | Output: standalone HTML export |

## Card format (per concept)

Each concept gets exactly one slide:

```markdown
---

# <Concept Name>

> <One-sentence explanation — precise, jargon-minimal.>

**Example:** <Concrete, specific example that grounds the concept in practice.>

**Boundary:** <Common misconception or usage limit — what this concept is NOT, or when it breaks down.>

```

The three fields must be:
- **Explanation**: a single sentence, complete and self-contained
- **Example**: specific (a named system, real use case, or concrete scenario — not "for example, you could...")
- **Boundary**: a real misconception practitioners encounter, not a trivial caveat

## Marp deck structure

```markdown
---
marp: true
theme: default
paginate: true
footer: "AI × Web3 School — Concept Cards"
---

# AI × Web3 Concepts

**Study deck** · <YYYY-MM-DD> · N concepts

---

# <Concept 1>
...

---
# <Concept N>
...

---

# Sources

<bulleted list of raw source files that informed these cards>

```

## Procedure

### Step 1 — Read wiki index

Read `wiki/index.md`. Build a list of all concept pages. If a `[topic]` argument was given, filter to pages whose `tags` frontmatter includes the topic string.

### Step 2 — Generate concept cards (Haiku subagents)

For each concept page to include:
1. Spawn a **Haiku subagent** (model: "haiku") with the concept page content as input
2. The subagent returns the three fields: explanation, example, boundary
3. Collect all results

This step is embarrassingly parallel — spawn all subagents simultaneously.

**Subagent prompt template:**
```
Read this wiki concept page and generate a concept card with exactly three fields:

1. One-sentence explanation (precise, jargon-minimal, self-contained)
2. Concrete example (specific system, tool, or real scenario — not hypothetical)
3. Boundary (a real misconception or usage limit practitioners encounter)

Return only these three fields, clearly labeled. No preamble.

<concept page content>
```

### Step 3 — Assemble Marp deck

Compose the full Marp `.md` file from the title slide + all concept cards + sources slide.

Order concepts by wiki index order (Sources first, then Concepts alphabetically within tag groups: `ai-foundations` → `web3-foundations` → `aixweb3-bridge` → `frontier`).

Save to: `knowledge-base/AIxWeb3/concepts/concepts-<YYYY-MM-DD>.md`

### Step 4 — HTML export

**Option A** (preferred — if npx is available):
```bash
which npx && npx @marp-team/marp-cli \
  "knowledge-base/AIxWeb3/concepts/concepts-<date>.md" \
  --html --allow-local-files \
  -o "submissions/concept-cards.html"
```

**Option B** (fallback — no tooling required):
Generate a standalone HTML file at `submissions/concept-cards.html` using this template:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI × Web3 Concept Cards</title>
  <script src="https://cdn.jsdelivr.net/npm/@marp-team/marp-core/lib/browser/marp.min.js"></script>
  <style>
    body { margin: 0; background: #1a1a2e; display: flex; justify-content: center; align-items: center; min-height: 100vh; flex-direction: column; font-family: sans-serif; }
    .nav { color: #aaa; margin: 1em 0; }
    button { background: #444; color: white; border: none; padding: 0.5em 1em; margin: 0 0.3em; cursor: pointer; border-radius: 4px; }
    .slide-container { width: 800px; max-width: 95vw; }
  </style>
</head>
<body>
  <div class="slide-container">
    <div id="slide"></div>
    <div class="nav">
      <button onclick="prev()">◀ Prev</button>
      <span id="counter"></span>
      <button onclick="next()">Next ▶</button>
    </div>
  </div>
  <script>
    const slides = /* SLIDES_JSON_ARRAY */;
    let current = 0;
    function render() {
      document.getElementById('slide').innerHTML = slides[current];
      document.getElementById('counter').textContent = (current+1) + ' / ' + slides.length;
    }
    function next() { if (current < slides.length-1) { current++; render(); } }
    function prev() { if (current > 0) { current--; render(); } }
    render();
  </script>
</body>
</html>
```

Inject the rendered HTML for each slide into the `/* SLIDES_JSON_ARRAY */` placeholder. Render each Marp slide's markdown to HTML manually (h1 → title, blockquote → explanation box, bold fields → labeled sections).

## Model guidance

- **Sonnet** handles: reading the wiki index, orchestrating subagents, assembling the deck, HTML export
- **Haiku** handles: per-concept card generation (Steps 2 subagents)

This split is intentional. Card generation is templated and bounded — Haiku quality is sufficient. Orchestration and final assembly require Sonnet.

## Verification

After running:
- `concepts/concepts-<date>.md` exists and has `marp: true` frontmatter
- Opening the file in Obsidian with the Marp Slides plugin renders slides
- `submissions/concept-cards.html` opens in a browser and is navigable
- Every concept card has all three fields (explanation, example, boundary)
- No concept card has a blank or placeholder field
