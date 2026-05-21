#!/usr/bin/env python3
"""
wcb_client.py — WCB Agent API CLI for Sensei

Zero external dependencies (stdlib only).

Usage:
  python tools/wcb_client.py status              # today's tasks + events + check-in status
  python tools/wcb_client.py checkin list        # pending check-ins
  python tools/wcb_client.py tasks upcoming      # deadlines in the next 3 days
  python tools/wcb_client.py catalog             # dump live procedure catalog
  python tools/wcb_client.py call <procedure> [json_input]  # raw procedure call

API key resolution order (first non-empty wins):
  1. WCB_AGENT_SECRET_API_KEY environment variable
  2. env.WCB_AGENT_SECRET_API_KEY in ./.claude/settings.local.json
  3. env.WCB_AGENT_SECRET_API_KEY in ~/.claude/settings.local.json

Program/track resolution order:
  1. WCB_PROGRAM_ID / WCB_TRACK_ID environment variables
  2. Auto-discovered from users.getProfile (first enrollment)
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://web3career.build"
AGENT_CALL_URL = f"{BASE_URL}/api/agent/call"
AGENT_CATALOG_URL = f"{BASE_URL}/api/agent/catalog"


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    """
    Resolve WCB_AGENT_SECRET_API_KEY.

    Order:
      1. OS environment variable
      2. env block in ./.claude/settings.local.json  (project-level)
      3. env block in ~/.claude/settings.local.json  (global)
    """
    key = os.environ.get("WCB_AGENT_SECRET_API_KEY", "").strip()
    if key:
        return key

    candidates = [
        Path.cwd() / ".claude" / "settings.local.json",
        Path.home() / ".claude" / "settings.local.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                data = json.loads(path.read_text())
                key = data.get("env", {}).get("WCB_AGENT_SECRET_API_KEY", "").strip()
                if key:
                    return key
            except (json.JSONDecodeError, OSError):
                pass

    return ""


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

# Cloudflare blocks Python-urllib/* UA with error 1010.
# Use a neutral agent string that passes CF bot checks.
_HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (compatible; Sensei-WCB-Client/1.0)",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}


def _post(procedure: str, input_data: dict, api_key: str) -> dict:
    """POST a single procedure call to the agent endpoint."""
    payload: dict = {"procedure": procedure, "input": input_data}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        AGENT_CALL_URL,
        data=data,
        headers={
            **_HEADERS_BASE,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return json.loads(body)
        except Exception:
            return {"ok": False, "error": {"code": str(exc.code), "message": body}}
    except Exception as exc:
        return {"ok": False, "error": {"code": "REQUEST_FAILED", "message": str(exc)}}


def _get_catalog(api_key: str) -> dict:
    """GET the live procedure catalog."""
    req = urllib.request.Request(
        AGENT_CATALOG_URL,
        headers={
            **_HEADERS_BASE,
            "Authorization": f"Bearer {api_key}",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return json.loads(body)
        except Exception:
            return {"ok": False, "error": {"code": str(exc.code), "message": body}}
    except Exception as exc:
        return {"ok": False, "error": {"code": "REQUEST_FAILED", "message": str(exc)}}


# ---------------------------------------------------------------------------
# Program resolution
# ---------------------------------------------------------------------------

def _resolve_program(api_key: str) -> str:
    """
    Return programId.

    Sources (first non-empty wins):
      1. WCB_PROGRAM_ID env var
      2. First ACCEPTED application from users.getProfile
    """
    program_id = os.environ.get("WCB_PROGRAM_ID", "").strip()
    if program_id:
        return program_id

    result = _post("users.getProfile", {}, api_key)
    if result.get("ok"):
        for app in result.get("result", {}).get("programApplications", []):
            if app.get("status") == "ACCEPTED":
                return app.get("programId", "")

    return ""


# ---------------------------------------------------------------------------
# Event + task helpers
# ---------------------------------------------------------------------------

_TASK_BATCH = 50  # max taskIds per listForLearnerByIds call


def _get_events(program_id: str, range_start: str, range_end: str, api_key: str) -> list:
    """Fetch events for a date range; return list (empty on error)."""
    res = _post(
        "events.listForLearner",
        {"programId": program_id, "rangeStart": range_start, "rangeEnd": range_end},
        api_key,
    )
    return res.get("result", []) if res.get("ok") else []


def _get_tasks_for_events(events: list, program_id: str, api_key: str) -> list:
    """
    Collect unique taskIds from events, fetch via listForLearnerByIds (batched),
    return deduplicated task list.
    """
    seen: set = set()
    task_ids: list = []
    for ev in events:
        for tid in ev.get("taskIds", []):
            if tid not in seen:
                seen.add(tid)
                task_ids.append(tid)

    if not task_ids:
        return []

    tasks: list = []
    for i in range(0, len(task_ids), _TASK_BATCH):
        batch = task_ids[i : i + _TASK_BATCH]
        res = _post(
            "tasks.listForLearnerByIds",
            {"programId": program_id, "taskIds": batch},
            api_key,
        )
        if res.get("ok") and isinstance(res.get("result"), list):
            tasks.extend(res["result"])

    return tasks


def _utc_str(dt: datetime.datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _parse_deadline(task: dict):
    raw = task.get("validTo") or task.get("deadline") or task.get("dueAt") or ""
    if not raw:
        return None
    try:
        return datetime.datetime.fromisoformat(raw.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _is_done(task: dict) -> bool:
    return task.get("status") in {"APPROVED", "COMPLETED", "SUBMITTED"} or bool(
        task.get("latestSubmission")
    )


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(api_key: str) -> None:
    """Today's events + linked tasks with their current submission status."""
    program_id = _resolve_program(api_key)
    now_utc = datetime.datetime.utcnow()

    today_start = _utc_str(now_utc.replace(hour=0, minute=0, second=0, microsecond=0))
    today_end = _utc_str(now_utc.replace(hour=23, minute=59, second=59, microsecond=0))

    events_today = _get_events(program_id, today_start, today_end, api_key)
    tasks = _get_tasks_for_events(events_today, program_id, api_key)

    pending = [t for t in tasks if not _is_done(t)]
    done = [t for t in tasks if _is_done(t)]

    output = {
        "date": now_utc.date().isoformat(),
        "program_id": program_id or None,
        "events_today": [
            {
                "title": e.get("title"),
                "startAt": e.get("startAt"),
                "endAt": e.get("endAt"),
                "meetingUrl": e.get("meetingUrlPrimary"),
                "replayUrl": e.get("replayUrl"),
                "taskIds": e.get("taskIds", []),
            }
            for e in events_today
        ],
        "tasks_pending": pending,
        "tasks_done": done,
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_checkin_list(api_key: str) -> None:
    """
    Pending vs. submitted tasks across a rolling 14-day window (past week + next week).
    Tasks carry status and latestSubmission directly — no separate history call needed.
    """
    program_id = _resolve_program(api_key)
    now_utc = datetime.datetime.utcnow()

    window_start = _utc_str(now_utc - datetime.timedelta(days=7))
    window_end = _utc_str(now_utc + datetime.timedelta(days=7))

    events = _get_events(program_id, window_start, window_end, api_key)
    tasks = _get_tasks_for_events(events, program_id, api_key)

    pending = [t for t in tasks if not _is_done(t) and t.get("available")]
    submitted = [t for t in tasks if _is_done(t)]

    output = {
        "window": {"from": window_start, "to": window_end},
        "total_tasks_in_window": len(tasks),
        "pending": [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "points": t.get("points"),
                "validTo": t.get("validTo"),
                "available": t.get("available"),
            }
            for t in pending
        ],
        "submitted": [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "points": t.get("points"),
                "latestSubmission": t.get("latestSubmission"),
            }
            for t in submitted
        ],
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_tasks_upcoming(api_key: str) -> None:
    """Tasks with deadlines in the next 3 days that are not yet completed."""
    program_id = _resolve_program(api_key)
    now_utc = datetime.datetime.utcnow()
    cutoff = now_utc + datetime.timedelta(days=3)

    window_start = _utc_str(now_utc)
    window_end = _utc_str(cutoff)

    events = _get_events(program_id, window_start, window_end, api_key)
    tasks = _get_tasks_for_events(events, program_id, api_key)

    upcoming = []
    for t in tasks:
        if _is_done(t):
            continue
        dl = _parse_deadline(t)
        if dl and now_utc <= dl <= cutoff:
            upcoming.append({
                "id": t.get("id"),
                "title": t.get("title"),
                "status": t.get("status"),
                "points": t.get("points"),
                "deadline": dl.isoformat(),
                "available": t.get("available"),
                "proofRequired": t.get("proofRequired"),
            })

    upcoming.sort(key=lambda t: t["deadline"])

    output = {
        "as_of": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_days": 3,
        "upcoming_count": len(upcoming),
        "upcoming": upcoming,
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_catalog(api_key: str) -> None:
    """Dump the live WCB procedure catalog."""
    result = _get_catalog(api_key)
    print(json.dumps(result, indent=2, default=str))


def cmd_call(api_key: str, rest: list[str]) -> None:
    """Raw call: call <procedure> [json_input]"""
    if not rest:
        _die('Usage: python tools/wcb_client.py call <procedure> [\'{"key":"value"}\']')
    procedure = rest[0]
    input_data: dict = {}
    if len(rest) > 1:
        try:
            input_data = json.loads(rest[1])
        except json.JSONDecodeError as exc:
            _die(f"Invalid JSON input: {exc}")
    result = _post(procedure, input_data, api_key)
    print(json.dumps(result, indent=2, default=str))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _die(msg: str, code: int = 1) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    api_key = load_api_key()
    if not api_key:
        _die(
            "WCB_AGENT_SECRET_API_KEY not found. "
            "Export it as an env var, or add it under env.WCB_AGENT_SECRET_API_KEY "
            "in .claude/settings.local.json (gitignored)."
        )

    cmd = args[0]
    sub = args[1] if len(args) > 1 else ""

    if cmd == "status":
        cmd_status(api_key)
    elif cmd == "checkin" and sub == "list":
        cmd_checkin_list(api_key)
    elif cmd == "tasks" and sub == "upcoming":
        cmd_tasks_upcoming(api_key)
    elif cmd == "catalog":
        cmd_catalog(api_key)
    elif cmd == "call":
        cmd_call(api_key, args[1:])
    else:
        _die(f"Unknown command: '{' '.join(args)}'. Run with --help for usage.")


if __name__ == "__main__":
    main()
