# Prompt: Bootstrap Learning Agent

> **Used on:** 2026-05-20  
> **Tool:** Cowork (Claude Sonnet) + Claude Code  
> **Purpose:** Initialize Sensei, the personal AI × Web3 School Learning Agent, and set up the full learning repository

---

## Prompt

```
Bootstrap the learning agent. Have in mind that any mentions to Hermes means that
you, as an agent should perform those tasks. In case you need to setup any API Keys
or secrets in general ask me to setup them under the project's local directory so
these are available during the session.

Also, make sure to create an AGENTS.md (with a CLAUDE.md symlink) file and update
it along the way as the project progresses.
```

## Follow-up prompt (startup file)

Included in the Cowork project instructions (loaded automatically each session):

```
Please act as my AI × Web3 School Learning Agent. First read the startup prompt at
https://aiweb3.school/learning-agent.en.txt, then use the Handbook at
https://aiweb3.school/en/handbook/ to help me initialize my personal learning plan,
GitHub learning repository, daily check-in drafts, key concept explanations,
a completion checklist, a list of open questions and Handbook feedback workflow.
```

---

## What this prompt triggered

1. Fetched the Learning Agent startup prompt from `https://aiweb3.school/learning-agent.en.txt`
2. Fetched the Handbook from `https://aiweb3.school/en/handbook/` (via Claude in Chrome — site is client-rendered)
3. Confirmed learner profile across two rounds of questions (AI background, Web3 background, coding level, target direction, daily time, language)
4. Created `AGENTS.md` with full agent rules, learner profile, learning map, and git conventions
5. Created `CLAUDE.md` as a symlink → `AGENTS.md`
6. Guided GitHub CLI install + `gh auth login`
7. Created GitHub repo `santteegt/ai-web3-school-cohort-0` and cloned it
8. Initialized full repo structure: `daily/`, `tasks/`, `experiments/`, `handbook-feedback/`, `hackathon/`, `submissions/`, `templates/`
9. Created `README.md`, `profile.md`, `learning-plan.md` (3-phase → later corrected to 5-week official schedule), `.gitignore`
10. Created `templates/daily-note.md` and `templates/task-note.md`
11. Created `daily/2026-05-20.md` (Day 0 note)
12. Scheduled three Cowork reminders: 9 AM kickoff, 6 PM review, 10 PM deadline warning
13. Set up shared memory at `~/AIxWeb3_School/memory/` with symlink from `~/.claude/projects/-Users-santteegt-AIxWeb3-School/memory/`
14. Built `tools/wcb_client.py` (via Claude Code) — WCB Agent API CLI, stdlib-only
15. Updated all three scheduled task prompts to use `wcb_client.py` instead of web scraping
16. Added handbook GitHub fallback: `https://github.com/lxdao-official/aiweb3school`

---

## Key decisions made during bootstrap

| Decision | Rationale |
|---|---|
| Agent named **Sensei** | User preference; "Hermes" in startup prompt referred to a different agent product |
| Memory in `~/AIxWeb3_School/memory/` | Accessible to both Cowork and Claude Code; `.claude/` dirs are blocked by Cowork sandbox |
| `AGENTS.md` + `CLAUDE.md` symlink | Both tools pick up the same rules; AGENTS.md is the canonical file |
| Scheduled tasks use Haiku model | Sufficient for structured read/call/write tasks; Sonnet reserved for interactive sessions |
| WCB API via CLI script | Cowork sandbox partially blocks `web3career.build`; script handles auth + fallback cleanly |
