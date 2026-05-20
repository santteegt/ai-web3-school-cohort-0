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
    payload: dict = {"procedure": procedure}
    if input_data:
        payload["input"] = input_data

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
# Program / track resolution
# ---------------------------------------------------------------------------

def _resolve_program(api_key: str) -> tuple[str, str]:
    """
    Return (programId, trackId).

    Sources (first non-empty wins):
      1. WCB_PROGRAM_ID / WCB_TRACK_ID env vars
      2. First enrollment from users.getProfile
    """
    program_id = os.environ.get("WCB_PROGRAM_ID", "").strip()
    track_id = os.environ.get("WCB_TRACK_ID", "").strip()
    if program_id:
        return program_id, track_id

    result = _post("users.getProfile", {}, api_key)
    if result.get("ok"):
        profile = result.get("result", {})
        # try common field names for enrollments
        enrollments = (
            profile.get("enrollments")
            or profile.get("programs")
            or profile.get("programMemberships")
            or []
        )
        if enrollments:
            first = enrollments[0]
            program_id = (
                first.get("programId")
                or first.get("id")
                or ""
            )
            track_id = first.get("trackId") or ""

    return program_id, track_id


def _tasks_input(program_id: str, track_id: str) -> dict:
    inp: dict = {}
    if program_id:
        inp["programId"] = program_id
    if track_id:
        inp["trackId"] = track_id
    return inp


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(api_key: str) -> None:
    """Today's tasks, events, and check-in status."""
    program_id, track_id = _resolve_program(api_key)

    today = datetime.date.today().isoformat()
    now_utc = datetime.datetime.utcnow()
    day_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%S.000Z"
    )
    day_end = now_utc.replace(hour=23, minute=59, second=59, microsecond=0).strftime(
        "%Y-%m-%dT%H:%M:%S.000Z"
    )

    tasks_res = _post("tasks.listForLearner", _tasks_input(program_id, track_id), api_key)
    history_res = _post("tasks.myTaskHistory", _tasks_input(program_id, track_id), api_key)

    events_inp: dict = {"rangeStart": day_start, "rangeEnd": day_end}
    if program_id:
        events_inp["programId"] = program_id
    events_res = _post("events.listForLearner", events_inp, api_key)

    # Identify today's check-in from task list
    all_tasks = tasks_res.get("result", []) if tasks_res.get("ok") else []
    checkin_today = None
    if isinstance(all_tasks, list):
        for t in all_tasks:
            name = (t.get("title") or t.get("name") or "").lower()
            if "check-in" in name or "checkin" in name or "check in" in name:
                checkin_today = t
                break

    output = {
        "date": today,
        "program_id": program_id or None,
        "track_id": track_id or None,
        "checkin_today": checkin_today,
        "tasks": tasks_res.get("result", tasks_res),
        "task_history": history_res.get("result", history_res),
        "events_today": events_res.get("result", events_res),
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_checkin_list(api_key: str) -> None:
    """List pending check-ins and submission history."""
    program_id, track_id = _resolve_program(api_key)

    tasks_res = _post("tasks.listForLearner", _tasks_input(program_id, track_id), api_key)
    history_res = _post("tasks.myTaskHistory", _tasks_input(program_id, track_id), api_key)

    all_tasks = tasks_res.get("result", []) if tasks_res.get("ok") else []
    checkins: list = []
    if isinstance(all_tasks, list):
        for t in all_tasks:
            name = (t.get("title") or t.get("name") or t.get("type") or "").lower()
            if "check" in name:
                checkins.append(t)

    # Determine submitted vs pending
    history = history_res.get("result", []) if history_res.get("ok") else []
    submitted_ids: set = set()
    if isinstance(history, list):
        for h in history:
            tid = h.get("taskId") or h.get("id") or ""
            if tid:
                submitted_ids.add(tid)

    pending = [c for c in checkins if (c.get("id") or c.get("taskId")) not in submitted_ids]

    output = {
        "total_checkins": len(checkins),
        "pending": pending,
        "submitted_count": len(submitted_ids),
        "history": history,
    }
    print(json.dumps(output, indent=2, default=str))


def cmd_tasks_upcoming(api_key: str) -> None:
    """Tasks with deadlines in the next 3 days (or unsubmitted tasks without a deadline)."""
    program_id, track_id = _resolve_program(api_key)

    tasks_res = _post("tasks.listForLearner", _tasks_input(program_id, track_id), api_key)

    now_utc = datetime.datetime.utcnow()
    cutoff = now_utc + datetime.timedelta(days=3)

    all_tasks = tasks_res.get("result", []) if tasks_res.get("ok") else []
    upcoming: list = []
    no_deadline: list = []

    if isinstance(all_tasks, list):
        for t in all_tasks:
            deadline_str = (
                t.get("deadline")
                or t.get("dueAt")
                or t.get("dueDate")
                or t.get("endsAt")
                or ""
            )
            if deadline_str:
                try:
                    dl = datetime.datetime.fromisoformat(
                        deadline_str.replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                    if now_utc <= dl <= cutoff:
                        t["_deadline_parsed"] = dl.isoformat()
                        upcoming.append(t)
                except ValueError:
                    pass
            else:
                # No explicit deadline — include if not completed
                if not t.get("completedAt") and not t.get("submittedAt"):
                    no_deadline.append(t)

    output = {
        "window_days": 3,
        "as_of": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "upcoming_with_deadline": upcoming,
        "active_without_deadline": no_deadline,
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
