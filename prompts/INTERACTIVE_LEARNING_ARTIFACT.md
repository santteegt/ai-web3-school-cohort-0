# Interactive Learning Artifact — Design & Build Log

**Created:** 2026-05-25  
**Agent:** Sensei (Claude Sonnet 4.6 via Cowork)  
**Skill file:** `skills/quiz/SKILL.md`  
**Cache file:** `logs/quiz-cache.json`

---

## Initial Prompt (from Santiago)

> Help me create an "interactive learning artifact" using the wiki-like knowledge base that we've been building throughout the journey.
>
> **Main Features**
> - Make a user defined schedule Interactive quiz
> - It could be setup as an scheduled task for co-work or a generic skill
> - I can be started either by a cron job (if used by another agent framework) or by calling a slash command to start the interactive session
>
> **Quiz mechanics:**
> - The agent should use the knowledge base in `knowledge-base/AIxWeb3/wiki` and randomly select a topic
> - The agent should display the related wiki page or external link found in the wiki so the user can review it if he wants before answering the quiz
> - At the same time, the agent uses these sources as reference to generate a five question quiz with multi-choice that the user should use to answer in one shot. Quiz MUST be based on factual knowledge gathered from the wiki. Wrong answers can be made up a little to confuse the learner
> - The quiz aim is to help explain a concept, process, tool, or practical task around the selected topic
> - If the user scores on a question, it should go straight to the next one, otherwise it should display a short concept explainer to refresh the user's understanding
> - At the end of the quiz, the agent should manage a small cache with topics already covered so these are not picked again in subsequent quizzes. These cache resets every three days
>
> **Actions**
> - Create a plan on how to build this interactive learning artifact using the main features listed above
> - Any skill should be stored in the `skills` folder
> - After executing the plan, document the process including initial prompts, etc in `prompts/INTERACTIVE_LEARNING_ARTIFACT.md`
> - For my learning journey, use the created artifact/skill to create a scheduled task that runs a quiz every two hours

---

## Architecture Decisions

### Why a SKILL.md rather than a standalone Cowork artifact?

The quiz requires reading local wiki files (`knowledge-base/AIxWeb3/wiki/`) that exist on the user's filesystem. Cowork HTML artifacts run in a browser sandbox and cannot directly access local files without an MCP connector. A SKILL.md file that Claude reads and executes as an orchestrated procedure gives Claude direct file access via the `Read` tool — the right tool for this use case.

The interactive UI is produced via `mcp__visualize__show_widget` calls, which renders rich HTML widgets inline in the Cowork chat. Buttons in those widgets call `sendPrompt(text)`, which sends a message back to the agent — enabling a real multi-turn interactive loop without needing a separate web app.

### Why conversation-context state tracking?

The quiz session state (questions array, current question index, score) is kept entirely in Claude's conversation context between turns. This avoids unnecessary file I/O during the quiz and keeps the session fast. The only file write is the cache update at the end of the session (Step 9).

### Why a 72-hour cache reset?

A 3-day (72-hour) window was chosen to balance two goals:
1. Avoid repeating the same topic in back-to-back sessions (spaced repetition)
2. Not wait so long that the full concept list becomes available again after forgetting

With ~130 concepts in the wiki, a 72-hour cycle at 12 quizzes/day (every 2 hours) means topics rotate across ~11 sessions before the reset. This is a reasonable review cadence for the bootcamp timeline.

### Skill location

Skills are stored in `skills/` (top-level repo folder) rather than `.claude/skills/` because `.claude/` is a protected hidden directory in the Cowork sandbox. Both Claude Code and Cowork can read `skills/quiz/SKILL.md` using the `Read` tool.

---

## Implementation Plan (Executed)

| Step | Task | Output |
|---|---|---|
| 1 | Read existing skill format (`/wiki-build`, `/concept-cards`) | Understood SKILL.md conventions |
| 2 | Read `wiki/index.md` | Confirmed 130+ concept slugs available |
| 3 | Write `skills/quiz/SKILL.md` | 9-step quiz procedure with HTML widget templates |
| 4 | Initialize `logs/quiz-cache.json` | Empty covered list, reset_at = +72h |
| 5 | Update `AGENTS.md` Section 14 | `/quiz` skill documented |
| 6 | Write this documentation file | `prompts/INTERACTIVE_LEARNING_ARTIFACT.md` |
| 7 | Create Cowork scheduled task | Every 2 hours, cron `0 */2 * * *` |

---

## Skill Design: `skills/quiz/SKILL.md`

### Invocation
- Slash command: `/quiz`
- Scheduled task trigger: any message asking to "start quiz" or "run quiz"
- External (Hermes/other agent framework): call with prompt referencing the SKILL.md path

### Quiz Flow

```
[Start]
  │
  ▼
Load quiz-cache.json → check reset_at → filter covered topics
  │
  ▼
Randomly select 1 concept from wiki/index.md (excluding covered, overviews, sources)
  │
  ▼
Read wiki/<slug>.md → extract definition, key points, related concepts
  │
  ▼
Generate 5 questions internally (definition / example / boundary / process / application)
  │
  ▼
Show Topic Preview widget → user clicks "Start Quiz"
  │
  ▼
Q1 widget (A/B/C/D buttons via sendPrompt)
  ├── Correct → brief ✅ banner + Q2 immediately
  └── Wrong   → ❌ widget with explainer + "Next Question" button → Q2
  │
  ▼  (repeat for Q2–Q5)
  │
  ▼
Final Score widget (X/5, score message, wiki link, "Run Another Quiz" button)
  │
  ▼
Append slug to quiz-cache.json → done
```

### Widget System

All interactive elements use `mcp__visualize__show_widget` with inline HTML. Buttons use `onclick="sendPrompt('...')"` to route answers back to Claude. The SKILL.md contains reusable HTML templates for:
- Topic preview card (gradient header, wiki path, start button)
- Question card (progress badge, question text, 4 answer buttons)
- Correct feedback banner (green, compact)
- Wrong answer card (red header with correct answer, yellow concept refresher, next button)
- Score summary card (large score, gradient header, message, replay button)

### Question Generation Rules

1. All 5 questions must be answerable from the wiki page alone — no hallucination
2. One question per type: definition, example, boundary, process, application
3. Distractors drawn from neighboring concepts in `## Related Concepts` for productive confusion
4. Exactly one correct answer per question
5. No two questions test the same wiki page point

---

## Scheduled Task

**Schedule:** Every 2 hours  
**Cron:** `0 */2 * * *`  
**Prompt:** `"It's quiz time! Read skills/quiz/SKILL.md and run an interactive quiz for Santiago."`

The task fires at the top of every even hour. Since AGENTS.md (= CLAUDE.md) is loaded as project instructions, the agent has full context and can immediately read the skill and begin the quiz flow.

---

## Files Created / Modified

| File | Action |
|---|---|
| `skills/quiz/SKILL.md` | Created — full quiz skill |
| `logs/quiz-cache.json` | Created — empty cache, reset_at +72h |
| `AGENTS.md` | Updated — Section 14 added |
| `prompts/INTERACTIVE_LEARNING_ARTIFACT.md` | Created — this file |

---

## Usage Going Forward

### Run manually (Cowork or Claude Code)
```
/quiz
```

### Run manually (any agent framework)
Point the agent at `skills/quiz/SKILL.md` and instruct it to execute the procedure. The skill is self-contained and framework-agnostic.

### Extend the quiz
- Add more concepts: run `/wiki-build` after adding raw notes — new concepts auto-appear in `wiki/index.md` and become available to the quiz
- Change reset window: edit `reset_at` calculation in Step 1 of the skill
- Add difficulty levels: extend Step 4 with a `difficulty` parameter (`/quiz hard` for application-heavy questions)
- Topic-filtered quiz: extend Step 2 to accept an optional tag filter (`/quiz rag`, `/quiz web3`)

### Reset the cache manually
Delete or empty the `covered` array in `logs/quiz-cache.json`:
```json
{"covered": [], "reset_at": "<new timestamp>"}
```
