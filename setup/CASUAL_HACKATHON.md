# Casual Hackathon Platform — Reference

Platform-level CLI/API reference for [Casual Hackathon](https://casualhackathon.com),
kept for reuse if Santiago participates in a future event on this platform.

> Event-specific facts for the AI × Web3 Agentic Builders Hackathon
> (concluded) — dates, tracks, prize pool, submission requirements — live in
> `hackathon/guild-os/CHANGELOG.md`'s "Casual Hackathon — Event Record"
> section, not here.

Platform llms.txt: https://casualhackathon.com/llms.txt
Platform API docs: https://casualhackathon.com/llms/api.md

## CLI Tool

**`tools/casual_hackathon_client.py`** — stdlib-only CLI for all participation management. Must be run from the local terminal (the bash sandbox cannot reach `casualhackathon.com`).

```bash
python tools/casual_hackathon_client.py status          # registration + project + submission status
python tools/casual_hackathon_client.py form-schema     # active registration & submission schemas
python tools/casual_hackathon_client.py tracks          # list tracks with IDs and slugs
python tools/casual_hackathon_client.py register        # draft + submit registration
python tools/casual_hackathon_client.py project         # create/update project
python tools/casual_hackathon_client.py submit          # draft + submit project submission
python tools/casual_hackathon_client.py raw GET /api/partner/participations?eventId=...
```

## Registration & Participation API

The platform exposes public reads (no auth) via tRPC at `/api/trpc` and authenticated reads/writes via `/api/partner/*` with a Personal Access Key (`chp_user_` prefix, created at `https://casualhackathon.com/profile`).

**To enable agent-managed participation (one-time setup):**
1. Go to https://casualhackathon.com/profile → create a Personal Access Key
2. Required scopes: `registration:read registration:write project:read project:write submission:read submission:write`
3. Store as `CASUAL_HACKATHON_API_KEY` in `.claude/settings.local.json` (gitignored)

**Key API endpoints (bearer token required):**

```bash
# Check registration status
GET /api/partner/participations?eventId=<event-id>

# Submit registration (enters DRAFT — organizer must approve)
POST /api/partner/participations
{ "eventId": "<event-id>", "answers": { ... } }

# Create / update project
POST /api/partner/projects
{ "eventId": "<event-id>", "title": "<project-title>", "trackIds": ["<track-id>"] }

# Submit project
POST /api/partner/submissions
{ "eventId": "<event-id>", "projectId": "<id>", "payload": { ... } }
```

**Registration flow:**
1. POST → enters `DRAFT` (requires organizer review before `REGISTERED`)
2. Once `REGISTERED`, teams unlock and project submission opens
3. Project submission open until the event's `endsAt`

## Agent Rules for Hackathon Management

| Action | Behavior |
|---|---|
| Check registration status | Query `/api/partner/participations?eventId=...` if key is available; otherwise direct Santiago to the event page |
| Draft registration answers | Show draft to Santiago before any POST — never auto-submit |
| Draft project submission | Show full payload to Santiago for review — never auto-submit |
| Withdraw registration | Show exact action and get explicit confirmation first |
| Manage submission | Fetch form schema first; pre-fill from prior project proposal notes; show Santiago the rendered payload |
