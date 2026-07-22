# /quiz — Interactive AI × Web3 Knowledge Quiz

Run a 5-question multi-choice quiz drawn randomly from the wiki knowledge base. Provides instant feedback with concept explainers on wrong answers. Tracks covered topics so each session explores a fresh concept.

## Trigger

- Slash command: `/quiz`
- Scheduled task: any message asking to "start quiz", "run quiz", or "start the daily quiz"

## Vault & cache paths

| Path | Purpose |
|---|---|
| `knowledge-base/AIxWeb3/wiki/index.md` | Topic catalog — source of all concept slugs |
| `knowledge-base/AIxWeb3/wiki/<slug>.md` | Individual concept pages — quiz source material |
| `logs/quiz-cache.json` | Covered topics tracker — resets every 72 hours |

---

## Procedure

### Step 1 — Load and manage topic cache

Read `logs/quiz-cache.json`. If missing, create it:
```json
{"covered": [], "reset_at": "<ISO timestamp: now + 72 hours>"}
```
A prior rule said "If `reset_at` is in the past, reset `covered` to `[]` and set `reset_at` to now + 72 hours. Write the file." Omit this completely for now, covered topic list should not reset

### Step 2 — Select topic

1. Read `knowledge-base/AIxWeb3/wiki/index.md`. Collect all entries under `## Concepts` sections — lines matching **either** `- [[slug]] — description` (older Obsidian-wikilink bullets) **or** `- [title](slug.md) — description` (current OKF-style path-link bullets, e.g. `- [AI Agent](ai-agent.md) — ...`). Extract the slug from whichever form matched: for `[[slug]]` it's the bracketed text; for `[title](slug.md)` it's the parenthesized path with the `.md` suffix stripped. Both forms may appear in the same file — treat this as normal, not an error.
2. Exclude from the pool:
   - Any slug already in `covered`
   - Slugs ending in `-overview`
   - `index`, `log`
   - Anything starting with `sources/` (a source-page link, whether written `[[sources/slug]]` or `[title](sources/slug.md)`)
3. Pick one slug **at random** from the remaining pool.
4. If the pool is empty (all covered), reset `covered` to `[]` in the cache (log: "Cache reset — all concepts covered, starting fresh"), then pick freely.

### Step 3 — Read wiki page

Read `knowledge-base/AIxWeb3/wiki/<selected-slug>.md`. Extract:
- Concept `title` (from YAML frontmatter or first `#` heading)
- `## Definition` section
- `## Key Points` section
- `## Related Concepts` (for distractor material)
- Any external URLs present in the page

### Step 4 — Generate 5 questions

Using the wiki page as the **only factual source**, generate 5 multiple-choice questions. Store all 5 in conversation context. Do NOT display them yet.

Structure per question:
```
question: <text>
options: {A: <text>, B: <text>, C: <text>, D: <text>}
correct: <letter>
explanation: <2–3 sentences grounded in the wiki page — shown only if answer is wrong>
```

**Question type mix (use each type once):**
1. **Definition** — "Which best describes X?" or "What is X?"
2. **Example** — "In which scenario is X most appropriate?"
3. **Boundary** — "Which of the following is NOT true about X?" or "What does X NOT do?"
4. **Process** — "What is the correct order / what happens when...?"
5. **Application** — "An agent needs to do Y. Which approach aligns with X?"

**Distractor rules:**
- Wrong options must be plausible but clearly wrong to someone who read the page
- Draw wrong options from neighboring concepts in the wiki (Related Concepts) to add productive confusion
- Never make wrong answers obviously absurd
- Exactly one correct answer per question
- No two questions test the same wiki page point

### Step 5 — Topic preview widget

Show a widget with the topic overview and a Start button. Use `mcp__visualize__show_widget`:

```html
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;padding:16px">
  <div style="background:linear-gradient(135deg,#1e3a5f,#2d6a9f);color:white;border-radius:12px;padding:24px;margin-bottom:16px">
    <div style="font-size:11px;opacity:.7;margin-bottom:8px;text-transform:uppercase;letter-spacing:1px">AI × Web3 Quiz · 5 Questions</div>
    <h2 style="margin:0 0 8px 0;font-size:22px">CONCEPT_TITLE</h2>
    <p style="margin:0;opacity:.9;font-size:14px;line-height:1.5">CONCEPT_DEFINITION_SENTENCE</p>
  </div>
  <div style="background:#f8f9fa;border-radius:8px;padding:14px;margin-bottom:16px;font-size:13px;color:#555;line-height:1.8">
    <strong>📄 Wiki page:</strong> knowledge-base/AIxWeb3/wiki/SLUG.md<br>
    <strong>🔗 Related:</strong> RELATED_CONCEPTS_LIST
  </div>
  <p style="font-size:14px;color:#666;margin-bottom:16px">Take a moment to review the wiki page above if you'd like, then start when ready.</p>
  <button onclick="sendPrompt('Start quiz: SLUG')" style="background:#2d6a9f;color:white;border:none;padding:13px 28px;border-radius:8px;font-size:15px;cursor:pointer;width:100%;font-weight:500">
    Start Quiz →
  </button>
</div>
```

Replace `CONCEPT_TITLE`, `CONCEPT_DEFINITION_SENTENCE`, `SLUG`, `RELATED_CONCEPTS_LIST` with real values.

### Step 6 — Display each question

When the session starts (or continues), display the current question widget. Show questions one at a time. Use `mcp__visualize__show_widget`:

```html
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;padding:16px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
    <span style="font-size:12px;color:#888;text-transform:uppercase;letter-spacing:.8px;font-weight:500">CONCEPT_TITLE</span>
    <span style="background:#e8f4f8;color:#2d6a9f;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:bold">Q CURRENT/5</span>
  </div>
  <div style="background:white;border:1px solid #e0e0e0;border-radius:12px;padding:20px;margin-bottom:14px;box-shadow:0 1px 3px rgba(0,0,0,.06)">
    <p style="font-size:16px;font-weight:500;margin:0 0 20px 0;line-height:1.55;color:#1a1a2e">QUESTION_TEXT</p>
    <div style="display:flex;flex-direction:column;gap:9px">
      <button onclick="sendPrompt('Answer Q_NUM: A')" style="text-align:left;background:#f8f9fa;border:1px solid #dee2e6;border-radius:8px;padding:12px 16px;cursor:pointer;font-size:14px;color:#333">
        <strong style="color:#2d6a9f">A.</strong> OPTION_A
      </button>
      <button onclick="sendPrompt('Answer Q_NUM: B')" style="text-align:left;background:#f8f9fa;border:1px solid #dee2e6;border-radius:8px;padding:12px 16px;cursor:pointer;font-size:14px;color:#333">
        <strong style="color:#2d6a9f">B.</strong> OPTION_B
      </button>
      <button onclick="sendPrompt('Answer Q_NUM: C')" style="text-align:left;background:#f8f9fa;border:1px solid #dee2e6;border-radius:8px;padding:12px 16px;cursor:pointer;font-size:14px;color:#333">
        <strong style="color:#2d6a9f">C.</strong> OPTION_C
      </button>
      <button onclick="sendPrompt('Answer Q_NUM: D')" style="text-align:left;background:#f8f9fa;border:1px solid #dee2e6;border-radius:8px;padding:12px 16px;cursor:pointer;font-size:14px;color:#333">
        <strong style="color:#2d6a9f">D.</strong> OPTION_D
      </button>
    </div>
  </div>
</div>
```

Replace `CONCEPT_TITLE`, `CURRENT`, `QUESTION_TEXT`, `Q_NUM` (e.g. `Q1`, `Q2`…), and each `OPTION_*`.

### Step 7 — Handle each answer

When user sends `"Answer Q<N>: <letter>"`:

1. Look up the correct answer for Q`<N>` from the in-context question list.
2. **If correct:** Show the compact ✅ banner widget, then immediately call `mcp__visualize__show_widget` again with the next question (Step 6), or the final score (Step 8) if this was Q5. Increment score.
3. **If wrong:** Show the ❌ feedback widget. Wait for `"Continue to Q<N+1>"` before showing the next question.

**Correct feedback banner** (show above the next question widget in the same turn):
```html
<div style="font-family:system-ui;max-width:600px;margin:0 auto 8px;padding:11px 16px;background:#d4edda;border:1px solid #b8dfc6;border-radius:8px;color:#155724;font-size:14px;display:flex;align-items:center;gap:8px">
  ✅ <strong>Correct!</strong> Nice work — moving to the next one.
</div>
```

**Wrong answer feedback widget:**
```html
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;padding:16px">
  <div style="background:#f8d7da;border:1px solid #f1b0b7;border-radius:12px;padding:18px;margin-bottom:14px">
    <p style="margin:0 0 6px 0;color:#721c24;font-weight:600;font-size:15px">❌ Not quite.</p>
    <p style="margin:0;color:#721c24;font-size:14px"><strong>Correct answer:</strong> CORRECT_LETTER. CORRECT_OPTION_TEXT</p>
  </div>
  <div style="background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:16px;margin-bottom:16px">
    <p style="margin:0 0 6px 0;font-size:11px;color:#8a6400;text-transform:uppercase;font-weight:700;letter-spacing:.6px">Concept Refresher</p>
    <p style="margin:0;font-size:14px;color:#333;line-height:1.65">EXPLANATION_TEXT</p>
  </div>
  <button onclick="sendPrompt('Continue to Q_NEXT')" style="background:#2d6a9f;color:white;border:none;padding:12px 24px;border-radius:8px;font-size:14px;cursor:pointer;width:100%;font-weight:500">
    Next Question →
  </button>
</div>
```

Replace `CORRECT_LETTER`, `CORRECT_OPTION_TEXT`, `EXPLANATION_TEXT`, `Q_NEXT`.

### Step 8 — Final score widget

After Q5 is answered, display the score summary. Use `mcp__visualize__show_widget`:

```html
<div style="font-family:system-ui,sans-serif;max-width:600px;margin:0 auto;padding:16px">
  <div style="background:linear-gradient(135deg,#1e3a5f,#2d6a9f);color:white;border-radius:12px;padding:28px;margin-bottom:16px;text-align:center">
    <div style="font-size:52px;font-weight:700;margin-bottom:8px;letter-spacing:-1px">SCORE/5</div>
    <div style="font-size:16px;opacity:.9;line-height:1.4">SCORE_MESSAGE</div>
  </div>
  <div style="background:#f8f9fa;border-radius:8px;padding:14px;margin-bottom:16px;font-size:13px;color:#555;line-height:1.8">
    <strong>Topic reviewed:</strong> CONCEPT_TITLE<br>
    <strong>Wiki page:</strong> knowledge-base/AIxWeb3/wiki/SLUG.md
  </div>
  <button onclick="sendPrompt('/quiz')" style="background:#28a745;color:white;border:none;padding:13px 24px;border-radius:8px;font-size:14px;cursor:pointer;width:100%;font-weight:500">
    🔄 Run Another Quiz
  </button>
</div>
```

**Score messages:**
- 5/5 — "Perfect score! You've nailed this concept."
- 4/5 — "Great work! One small gap to revisit."
- 3/5 — "Solid foundation — worth one more pass through this page."
- ≤2/5 — "Good attempt — recommend re-reading the wiki page before the next session."

### Step 9 — Update cache

Append the selected topic slug to `covered` in `logs/quiz-cache.json`. Do not change `reset_at`:
```json
{"covered": ["existing-slug-1", "existing-slug-2", "NEW_SLUG"], "reset_at": "existing-timestamp"}
```

---

## In-context state

Keep the full quiz session in conversation memory throughout the interaction:

| Key | Content |
|---|---|
| `quiz_topic` | `{slug, title}` |
| `questions` | Array of 5 `{question, options{A,B,C,D}, correct, explanation}` |
| `current_q` | Index 1–5 |
| `score` | Correct answers so far |

No file writes are needed during the quiz — only at the end (Step 9 cache update).

---

## Model guidance

Run this skill with **Haiku**. Question generation requires factual grounding in the wiki page, plausible distractor construction, and multi-turn state tracking.

You should assist in the quiz creation but NEVER participate by answering the quiz by yourself. This is to test the human knowledge.

---

## Error handling

| Condition | Response |
|---|---|
| `wiki/index.md` missing | "Wiki not found. Run `/wiki-build` first to populate the knowledge base." |
| Selected page unreadable | Pick the next random topic silently. |
| `logs/quiz-cache.json` unwritable | Proceed with quiz; note cache was not updated. |
| All concepts covered | Reset cache, log the reset, pick freely from full index. |
