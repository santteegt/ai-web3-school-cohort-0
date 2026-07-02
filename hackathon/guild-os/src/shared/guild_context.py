"""GuildContext — guild_context.json read/write helper.

The guild context store is a JSON file that tracks guild state across
the 15-step MVP flow. It is the mock replacement for a real shared
memory store (deferred post-hackathon).
"""

from __future__ import annotations

import json
from pathlib import Path

CONTEXT_PATH = Path(__file__).parent.parent.parent / "guild_context.json"

VALID_STATES = {"INIT", "ACTIVE", "SETTLED", "DISPUTED"}


def load() -> dict:
    with open(CONTEXT_PATH) as f:
        return json.load(f)


def save(ctx: dict) -> None:
    if ctx.get("task_state") not in VALID_STATES:
        raise ValueError(f"Invalid task_state: {ctx.get('task_state')}. Must be one of {VALID_STATES}")
    with open(CONTEXT_PATH, "w") as f:
        json.dump(ctx, f, indent=2)


def update(**fields) -> dict:
    ctx = load()
    ctx.update(fields)
    save(ctx)
    return ctx


def reset() -> dict:
    ctx = {
        "guild_address": None,
        "mandate": None,
        "treasury_wei": "0",
        "member_list": [],
        "task_state": "INIT",
        "proposal_id": None,
        "a2a_task_id": None,
        "deliverable_hash": None,
        "deliverable_tx": None,
        "settlement_tx": None,
        "reputation_tx": None,
    }
    save(ctx)
    return ctx
