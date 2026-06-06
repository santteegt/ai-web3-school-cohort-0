#!/usr/bin/env python3
"""
wcb_client.py — WCB Agent API CLI for Sensei

Zero external dependencies (stdlib only).

Usage:
  python tools/wcb_client.py status              # today's events + tasks due today
  python tools/wcb_client.py checkin list        # all pending + recently submitted tasks
  python tools/wcb_client.py tasks upcoming      # deadlines in the next 3 days
  python tools/wcb_client.py catalog             # dump live procedure catalog
  python tools/wcb_client.py call <procedure> [json_input]  # raw procedure call

API key resolution order (first non-empty wins):
  1. WCB_AGENT_SECRET_API_KEY environment variable
  2. env.WCB_AGENT_SECRET_API_KEY in ./.claude/settings.local.json
  3. env.WCB_AGENT_SECRET_API_KEY in ~/.claude/settings.local.json

Program/track resolution order:
  1. WCB_PROGRAM_ID / WCB_TRACK_ID environment variables
  2. programId: auto-discovered from users.getProfile (first ACCEPTED application)
  3. trackId: auto-discovered from program.getById -> curriculumWeeks[0].trackId
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
# Program + track resolution
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


def _resolve_track(program_id: str, api_key: str) -> str:
    """
    Return trackId.

    Sources (first non-empty wins):
      1. WCB_TRACK_ID env var
      2. curriculumWeeks[0].trackId from program.getById
         (tracks.mySelection and tracks.listForProgram are not exposed to agent calls)
    """
    track_id = os.environ.get("WCB_TRACK_ID", "").strip()
    if track_id:
        return track_id

    result = _post("program.getById", {"idOrSlug": program_id}, api_key)
    if result.get("ok"):
        for week in result.get("result", {}).get("curriculumWeeks", []):
            tid = week.get("trackId", "").strip()
            if tid:
                return tid

    return ""


# ---------------------------------------------------------------------------
# Task helpers
# ---------------------------------------------------------------------------

def _get_all_tasks(program_id: str, track_id: str, api_key: str) -> list:
    """
    Fetch the complete learner task list via tasks.listForLearner.
    This returns ALL tasks (including bonus/standalone tasks not linked to events).
    """
    res = _post(
        "tasks.listForLearner",
        {"programId": program_id, "trackId": track_id, "locale": "en"},
        api_key,
    )
    return res.get("result", []) if res.get("ok") else []


def _get_events(program_id: str, range_start: str, range_end: str, api_key: str) -> list:
    """Fetch events for a date range; return list (empty on error)."""
    res = _post(
        "events.listForLearner",
        {"programId": program_id, "rangeStart": range_start, "rangeEnd": range_end},
        api_key,
    )
    return res.get("result", []) if res.get("ok") else []


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


def _slim_task(task: dict) -> dict:
    """Return a compact task representation for output."""
    return {
        "id": task.get("id"),
        "title": task.get("title"),
        "status": task.get("status"),
        "points": task.get("points"),
        "validTo": task.get("validTo"),
        "available": task.get("available"),
        "proofRequired": task.get("proofRequired"),
    }


def _slim_submitted(task: dict) -> dict:
    sub = task.get("latestSubmission") or {}
    return {
        "id": task.get("id"),
        "title": task.get("title"),
        "status": task.get("status"),
        "points": task.get("points"),
        "latestSubmission": {
            "id": sub.get("id"),
            "status": sub.get("status"),
            "createdAt": sub.get("createdAt"),
            "reviewedAt": sub.get("reviewedAt"),
            "rejectionReason": sub.get("rejectionReason"),
        } if sub else None,
    }


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(api_key: str) -> None:
    """
    Today's events (with meeting URLs) + tasks that are either linked to
    today's events or have a deadline falling today.
    """
    program_id = _resolve_program(api_key)
    track_id = _resolve_track(program_id, api_key)
    now_utc = datetime.datetime.utcnow()

    today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now_utc.replace(hour=23, minute=59, second=59, microsecond=0)

    # Fetch today's events for meeting URLs
    events_today = _get_events(
        program_id, _utc_str(today_start), _utc_str(today_end), api_key
    )
    event_task_ids = {
        tid
        for ev in events_today
        for tid in ev.get("taskIds", [])
    }

    # Fetch all tasks directly — catches standalone/bonus tasks not linked to events
    all_tasks = _get_all_tasks(program_id, track_id, api_key)

    tasks_pending = []
    tasks_done = []
    for t in all_tasks:
        tid = t.get("id")
        dl = _parse_deadline(t)
        is_event_task = tid in event_task_ids
        deadline_today = dl and today_start <= dl <= today_end
        if not (is_event_task or deadline_today):
            continue
        if _is_done(t):
            tasks_done.append(_slim_submitted(t))
        else:
            tasks_pending.append(_slim_task(t))

    output = {
        "date": now_utc.date().isoformat(),
        "program_id": program_id or None,
        "track_id": track_id or None,
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
        "tasks_pending": tasks_pending,
        "tasks_done": tasks_done,
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_checkin_list(api_key: str) -> None:
    """
    All available pending tasks + tasks submitted in the last 14 days.
    Uses tasks.listForLearner directly so standalone/bonus tasks are included.
    """
    program_id = _resolve_program(api_key)
    track_id = _resolve_track(program_id, api_key)
    now_utc = datetime.datetime.utcnow()
    submission_window_start = now_utc - datetime.timedelta(days=14)

    all_tasks = _get_all_tasks(program_id, track_id, api_key)

    pending = []
    submitted = []

    for t in all_tasks:
        if _is_done(t):
            # Include submitted tasks with activity in the last 14 days
            sub = t.get("latestSubmission") or {}
            sub_at_str = sub.get("createdAt") or sub.get("reviewedAt") or ""
            try:
                sub_at = datetime.datetime.fromisoformat(
                    sub_at_str.replace("Z", "+00:00")
                ).replace(tzinfo=None)
                if sub_at >= submission_window_start:
                    submitted.append(_slim_submitted(t))
            except (ValueError, AttributeError):
                pass
        else:
            if not t.get("available"):
                continue
            dl = _parse_deadline(t)
            # Include tasks that haven't expired yet
            if dl is None or dl >= now_utc:
                pending.append(_slim_task(t))

    output = {
        "as_of": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_pending": len(pending),
        "total_submitted_last_14d": len(submitted),
        "pending": pending,
        "submitted": submitted,
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_tasks_upcoming(api_key: str) -> None:
    """Tasks with deadlines in the next 3 days that are not yet completed."""
    program_id = _resolve_program(api_key)
    track_id = _resolve_track(program_id, api_key)
    now_utc = datetime.datetime.utcnow()
    cutoff = now_utc + datetime.timedelta(days=3)

    all_tasks = _get_all_tasks(program_id, track_id, api_key)

    upcoming = []
    for t in all_tasks:
        if _is_done(t):
            continue
        if not t.get("available"):
            continue
        dl = _parse_deadline(t)
        if dl and now_utc <= dl <= cutoff:
            upcoming.append({
                "id": t.get("id"),
                "title": t.get("title"),
                "description": t.get("description"),
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


def cmd_call(api_key: str, rest: list) -> None:
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
