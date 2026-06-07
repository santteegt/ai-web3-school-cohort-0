#!/usr/bin/env python3
"""
casual_hackathon_client.py — Casual Hackathon API CLI for Sensei

Zero external dependencies (stdlib only).  Run from the repo root.

Usage:
  python tools/casual_hackathon_client.py status          # registration + project + submission status
  python tools/casual_hackathon_client.py form-schema     # show active registration & submission schemas
  python tools/casual_hackathon_client.py tracks          # list event tracks with IDs and slugs
  python tools/casual_hackathon_client.py register        # show pre-filled registration draft, then submit
  python tools/casual_hackathon_client.py project         # create/update the GuildOS project
  python tools/casual_hackathon_client.py submit          # draft project submission payload, then submit
  python tools/casual_hackathon_client.py raw <method> <path> [json_body]  # raw API call

API key resolution order (first non-empty wins):
  1. CASUAL_HACKATHON_API_KEY environment variable
  2. env.CASUAL_HACKATHON_API_KEY in ./.claude/settings.local.json  (project-level)
  3. env.CASUAL_HACKATHON_API_KEY in ~/.claude/settings.local.json  (global)

Required scopes on your Personal Access Key:
  registration:read  registration:write
  project:read       project:write
  submission:read    submission:write

Create your key at: https://casualhackathon.com/profile
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_URL = "https://casualhackathon.com"
EVENT_ID = "cmpsjubkg0003p80kxuzrdyjy"
EVENT_URL = f"{BASE_URL}/hackathons/{EVENT_ID}"
REGISTRATION_URL = f"{BASE_URL}/registrations?eventId={EVENT_ID}"
SUBMISSION_URL = f"{BASE_URL}/submissions?eventId={EVENT_ID}"

# Pre-filled project info — edit before running `project` or `submit`
PROJECT_TITLE = "GuildOS"
PROJECT_DESCRIPTION = (
    "A programmable agent coordination studio where founding and specialist agents "
    "coordinate real work through A2A, share a Moloch-secured treasury via "
    "AgentFightClub, and build verifiable on-chain reputation via ERC-8004."
)
PRIMARY_TRACK_SLUG = "cobo-agentic-economy-cobo-agentic-wallet"
GITHUB_REPO = "https://github.com/santteegt/ai-web3-school-cohort-0"

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def load_api_key() -> str:
    key = os.environ.get("CASUAL_HACKATHON_API_KEY", "").strip()
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
                key = data.get("env", {}).get("CASUAL_HACKATHON_API_KEY", "").strip()
                if key:
                    return key
            except (json.JSONDecodeError, OSError):
                pass
    return ""


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

_HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (compatible; Sensei-CasualHackathon-Client/1.0)",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def _request(method: str, path: str, api_key: str, body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={**_HEADERS_BASE, "Authorization": f"Bearer {api_key}"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode()
        try:
            return {"_http_error": exc.code, **json.loads(body_text)}
        except Exception:
            return {"_http_error": exc.code, "message": body_text}
    except Exception as exc:
        return {"_error": str(exc)}


def _get(path: str, api_key: str) -> dict:
    return _request("GET", path, api_key)


def _post(path: str, body: dict, api_key: str) -> dict:
    return _request("POST", path, api_key, body)


def _patch(path: str, body: dict, api_key: str) -> dict:
    return _request("PATCH", path, api_key, body)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _out(obj: object) -> None:
    print(json.dumps(obj, indent=2, default=str))


def _die(msg: str, code: int = 1) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(code)


def _confirm(prompt: str) -> bool:
    try:
        ans = input(f"\n{prompt} [y/N]: ").strip().lower()
        return ans == "y"
    except (EOFError, KeyboardInterrupt):
        return False


def _get_tracks(api_key: str) -> list:
    resp = _get(f"/api/partner/tracks?eventId={EVENT_ID}", api_key)
    return resp.get("data", [])


def _find_track_id(tracks: list, slug: str) -> str:
    for t in tracks:
        if t.get("slug") == slug:
            return t.get("id", "")
    return ""


def _get_participation(api_key: str) -> dict | None:
    resp = _get(f"/api/partner/participations?eventId={EVENT_ID}", api_key)
    rows = resp.get("data", [])
    return rows[0] if rows else None


def _get_projects(api_key: str) -> list:
    resp = _get(f"/api/partner/projects?eventId={EVENT_ID}", api_key)
    return resp.get("data", [])


def _get_submissions(api_key: str) -> list:
    resp = _get(f"/api/partner/submissions?eventId={EVENT_ID}", api_key)
    return resp.get("data", [])


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_status(api_key: str) -> None:
    """Registration + project + submission status in one call."""
    participation = _get_participation(api_key)
    projects = _get_projects(api_key)
    submissions = _get_submissions(api_key)

    reg_status = None
    if participation:
        reg_status = {
            "id": participation.get("id"),
            "status": participation.get("status"),
            "registeredAt": participation.get("registeredAt"),
            "answers": participation.get("answers"),
        }

    proj_summary = []
    for p in projects:
        sub = p.get("latestSubmission") or {}
        proj_summary.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "tracks": [t.get("slug") for t in p.get("tracks", [])],
            "latestSubmission": {
                "id": sub.get("id"),
                "version": sub.get("version"),
                "submittedAt": sub.get("submittedAt"),
            } if sub else None,
        })

    _out({
        "event": EVENT_URL,
        "registration": reg_status or "NOT_REGISTERED",
        "projects": proj_summary or [],
        "submission_count": len(submissions),
        "submission_url": SUBMISSION_URL,
        "registration_url": REGISTRATION_URL,
    })


def cmd_form_schema(api_key: str) -> None:
    """Print the active registration and submission form schemas."""
    resp = _get(f"/api/partner/form-schemas?eventId={EVENT_ID}", api_key)
    _out(resp)


def cmd_tracks(api_key: str) -> None:
    """List event tracks with IDs, slugs, and descriptions."""
    tracks = _get_tracks(api_key)
    _out([
        {
            "id": t.get("id"),
            "name": t.get("name"),
            "slug": t.get("slug"),
            "projectCount": t.get("projectCount"),
        }
        for t in tracks
    ])


def cmd_register(api_key: str) -> None:
    """
    Fetch the active registration form schema, show a pre-filled draft,
    and submit on confirmation.

    Registration enters DRAFT and requires organizer review before teams unlock.
    """
    # Fetch form schema first to know required fields
    schema_resp = _get(f"/api/partner/form-schemas?eventId={EVENT_ID}", api_key)
    reg_schema = None
    for s in schema_resp.get("data", []) if isinstance(schema_resp, dict) else []:
        if s.get("type") == "registration" and s.get("isActive"):
            reg_schema = s.get("schema")
            break

    # Check existing participation
    existing = _get_participation(api_key)
    if existing:
        status = existing.get("status")
        if status == "REGISTERED":
            print(json.dumps({
                "already_registered": True,
                "status": status,
                "registeredAt": existing.get("registeredAt"),
                "message": "Already REGISTERED. No action needed.",
            }, indent=2))
            return
        print(json.dumps({
            "existing_participation": {
                "status": status,
                "registeredAt": existing.get("registeredAt"),
            },
            "note": "Will resubmit this draft.",
        }, indent=2))

    # Build answers — adapt keys based on actual schema if available
    answers: dict = {}
    if reg_schema and isinstance(reg_schema, dict):
        props = reg_schema.get("properties", {})
        # Map common field names to GuildOS values
        field_map = {
            "name":         "Santiago",
            "project_name": PROJECT_TITLE,
            "project":      PROJECT_TITLE,
            "idea":         PROJECT_DESCRIPTION,
            "description":  PROJECT_DESCRIPTION,
            "track":        PRIMARY_TRACK_SLUG,
            "github":       GITHUB_REPO,
            "team":         "Solo (+ 2 AI coding agents)",
            "role":         "Developer",
            "background":   "Intermediate AI (API, agents, MCP) + Web3 (DeFi, L2s, account abstraction). Building GuildOS — agent coordination + on-chain reputation + treasury.",
        }
        for field_key in props:
            for map_key, val in field_map.items():
                if map_key in field_key.lower():
                    answers[field_key] = val
                    break
    else:
        # Fallback when schema is unavailable
        answers = {
            "project_name": PROJECT_TITLE,
            "description": PROJECT_DESCRIPTION,
            "track": PRIMARY_TRACK_SLUG,
            "github": GITHUB_REPO,
            "team_status": "Solo",
            "background": "Developer — AI × Web3, intermediate AI, familiar with DeFi/L2s.",
        }

    payload = {"eventId": EVENT_ID, "answers": answers}

    print("\n=== Registration Draft ===")
    print(json.dumps(payload, indent=2))
    print(f"\nRegistration URL (web fallback): {REGISTRATION_URL}")
    if reg_schema:
        print("\nSchema fields detected:", list(reg_schema.get("properties", {}).keys()))

    if not _confirm("Submit this registration? (enters DRAFT — organizer must approve)"):
        print(json.dumps({"status": "cancelled", "message": "No changes made."}))
        return

    resp = _post("/api/partner/participations", payload, api_key)
    _out(resp)


def cmd_project(api_key: str) -> None:
    """
    Create or update the GuildOS project, selecting the primary Cobo track.
    Requires REGISTERED status first.
    """
    # Check registration
    participation = _get_participation(api_key)
    if not participation or participation.get("status") != "REGISTERED":
        _die(
            "Not yet REGISTERED. Run `register` first and wait for organizer approval. "
            f"Current status: {participation.get('status') if participation else 'NOT_REGISTERED'}"
        )

    # Resolve track ID
    tracks = _get_tracks(api_key)
    track_id = _find_track_id(tracks, PRIMARY_TRACK_SLUG)
    if not track_id:
        _die(
            f"Could not find track with slug '{PRIMARY_TRACK_SLUG}'. "
            f"Available: {[t.get('slug') for t in tracks]}"
        )

    # Check for existing project
    projects = _get_projects(api_key)
    existing_project = next(
        (p for p in projects if p.get("title") == PROJECT_TITLE), None
    )

    if existing_project:
        print(json.dumps({
            "existing_project": {
                "id": existing_project.get("id"),
                "title": existing_project.get("title"),
                "tracks": [t.get("slug") for t in existing_project.get("tracks", [])],
            },
            "note": "Project already exists. Will PATCH to update tracks.",
        }, indent=2))
        payload = {
            "eventId": EVENT_ID,
            "projectId": existing_project.get("id"),
            "trackIds": [track_id],
        }
        print("\n=== PATCH Payload ===")
        print(json.dumps(payload, indent=2))
        if not _confirm("Update this project?"):
            print(json.dumps({"status": "cancelled"}))
            return
        resp = _patch(
            f"/api/partner/projects?projectId={existing_project.get('id')}",
            payload,
            api_key,
        )
    else:
        payload = {
            "eventId": EVENT_ID,
            "title": PROJECT_TITLE,
            "trackIds": [track_id],
        }
        print("\n=== New Project Payload ===")
        print(json.dumps(payload, indent=2))
        print(f"\nTrack: {PRIMARY_TRACK_SLUG} (id={track_id})")
        if not _confirm("Create this project?"):
            print(json.dumps({"status": "cancelled"}))
            return
        resp = _post("/api/partner/projects", payload, api_key)

    _out(resp)


def cmd_submit(api_key: str) -> None:
    """
    Build and submit the GuildOS project submission.
    Fetches the active submission form schema to build the payload.
    Requires an existing project (run `project` first).
    """
    # Check registration
    participation = _get_participation(api_key)
    if not participation or participation.get("status") != "REGISTERED":
        _die(
            "Not yet REGISTERED. Run `register` and wait for organizer approval. "
            f"Current status: {participation.get('status') if participation else 'NOT_REGISTERED'}"
        )

    # Resolve project
    projects = _get_projects(api_key)
    project = next((p for p in projects if p.get("title") == PROJECT_TITLE), None)
    if not project:
        _die(f"Project '{PROJECT_TITLE}' not found. Run `project` command first.")

    project_id = project.get("id")
    print(f"Project: {PROJECT_TITLE} (id={project_id})")

    # Fetch submission schema
    schema_resp = _get(f"/api/partner/form-schemas?eventId={EVENT_ID}", api_key)
    sub_schema = None
    for s in schema_resp.get("data", []) if isinstance(schema_resp, dict) else []:
        if s.get("type") == "submission" and s.get("isActive"):
            sub_schema = s.get("schema")
            break

    # Build submission payload from GuildOS proposal
    submission_payload: dict = {
        "project_name": PROJECT_TITLE,
        "description": PROJECT_DESCRIPTION,
        "github_repo": GITHUB_REPO,
        "track": PRIMARY_TRACK_SLUG,
        "demo_description": (
            "End-to-end agent coordination demo on Base Sepolia: "
            "human launches guild → specialist agent with ERC-8004 profile joins via "
            "governance vote → orchestrator delegates task via A2A → specialist executes "
            "with GLM-5.1 → deliverable hash committed on-chain → treasury releases "
            "payment via AgentFightClub → ERC-8004 reputation updated."
        ),
        "tech_stack": (
            "Cobo Agentic Wallet (CAW) · x402 payment protocol · A2A Protocol · "
            "ERC-8004 on-chain agent registry · AgentFightClub (Moloch v3) · "
            "GLM-5.1 (Z.AI) · Base Sepolia testnet"
        ),
        "caw_usage": (
            "CAW Pact with per-call ceiling ($0.01) and rolling 24h budget ($0.10). "
            "Full x402 payment loop prototype complete: `experiments/caw-payment-loop/`. "
            "Production path: txApi.payment() with EIP-712/EIP-3009. "
            "Local signer bypass active while Cobo Base Sepolia node indexing is being resolved."
        ),
        "team": "Solo — Santiago + 2 AI coding agents (GuildOS as its own proof of concept)",
        "status": "Week 4 build in progress — submission deadline June 13",
    }

    if sub_schema and isinstance(sub_schema, dict):
        # Try to remap keys to match actual schema properties
        props = sub_schema.get("properties", {})
        mapped: dict = {}
        for field_key in props:
            for src_key, val in submission_payload.items():
                if src_key.lower() in field_key.lower() or field_key.lower() in src_key.lower():
                    mapped[field_key] = val
                    break
        if mapped:
            submission_payload = mapped

    full_payload = {
        "eventId": EVENT_ID,
        "projectId": project_id,
        "payload": submission_payload,
    }

    print("\n=== Submission Draft ===")
    print(json.dumps(full_payload, indent=2))
    print(f"\nSubmission URL (web fallback): {SUBMISSION_URL}")
    print(f"Deadline: 2026-06-13 12:00 UTC+8 (04:00 UTC)")

    if not _confirm("Submit this payload? (creates a new submission version)"):
        print(json.dumps({"status": "cancelled", "message": "No changes made."}))
        return

    resp = _post("/api/partner/submissions", full_payload, api_key)
    _out(resp)


def cmd_raw(api_key: str, rest: list) -> None:
    """Raw API call: raw <GET|POST|PATCH|DELETE> <path> [json_body]"""
    if len(rest) < 2:
        _die("Usage: python tools/casual_hackathon_client.py raw <METHOD> <path> [json_body]")
    method = rest[0].upper()
    path = rest[1]
    body = None
    if len(rest) > 2:
        try:
            body = json.loads(rest[2])
        except json.JSONDecodeError as exc:
            _die(f"Invalid JSON body: {exc}")
    resp = _request(method, path, api_key, body)
    _out(resp)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    api_key = load_api_key()
    if not api_key:
        _die(
            "CASUAL_HACKATHON_API_KEY not found. "
            "Export it as an env var, or add it under env.CASUAL_HACKATHON_API_KEY "
            "in .claude/settings.local.json or ~/.claude/settings.local.json."
        )

    cmd = args[0]

    if cmd == "status":
        cmd_status(api_key)
    elif cmd == "form-schema":
        cmd_form_schema(api_key)
    elif cmd == "tracks":
        cmd_tracks(api_key)
    elif cmd == "register":
        cmd_register(api_key)
    elif cmd == "project":
        cmd_project(api_key)
    elif cmd == "submit":
        cmd_submit(api_key)
    elif cmd == "raw":
        cmd_raw(api_key, args[1:])
    else:
        _die(f"Unknown command: '{cmd}'. Run with --help for usage.")


if __name__ == "__main__":
    main()
