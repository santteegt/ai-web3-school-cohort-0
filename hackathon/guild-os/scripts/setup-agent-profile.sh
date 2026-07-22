#!/usr/bin/env bash
# setup-agent-profile.sh — Bootstrap a GuildOS agent profile (Orchestrator or
# Specialist) onto an already-running AI coding harness (Claude Code, Hermes
# Agent, or OpenClaw) in a clean, isolated working directory.
#
# Usage: ./scripts/setup-agent-profile.sh [--profile orchestrator|specialist]
#          [--harness claude-code|hermes|openclaw] [--workdir <path>] [--dry-run]
# All of the above may also be answered interactively if omitted.
#
# This script installs what's ALREADY BUILT in GuildOS (MCP servers, A2A
# servers, onboarding skills) onto a harness that's already installed on this
# machine — it does NOT install Claude Code / Hermes / OpenClaw themselves,
# and it does NOT build the not-yet-implemented "harness work engine" that
# would let a harness autonomously execute Specialist coding tasks (tracked
# separately — GitHub issues #40/#10).
#
# Component list (MCP servers, skills, CLI-dependency status, per-profile
# file lists) lives in agent-manifest.json, not hardcoded here — add/remove
# a component by editing that file only.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$SCRIPT_DIR/agent-manifest.json"
DRY_RUN=false

# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
# shellcheck source=lib/harness-claude-code.sh
source "$SCRIPT_DIR/lib/harness-claude-code.sh"
# shellcheck source=lib/harness-hermes.sh
source "$SCRIPT_DIR/lib/harness-hermes.sh"
# shellcheck source=lib/harness-openclaw.sh
source "$SCRIPT_DIR/lib/harness-openclaw.sh"

PROFILE=""
HARNESS=""
WORKDIR_ARG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --harness) HARNESS="$2"; shift 2 ;;
    --workdir) WORKDIR_ARG="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h | --help)
      echo "Usage: $0 [--profile orchestrator|specialist] [--harness claude-code|hermes|openclaw] [--workdir <path>] [--dry-run]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# ─── 0. Bootstrap-level prerequisites (hardcoded, not manifest-driven) ───────
# You can't jq-parse the manifest to discover you need jq.

require_cli jq "brew install jq  /  apt install jq"
require_cli uv "curl -LsSf https://astral.sh/uv/install.sh | sh"
require_cli node "https://nodejs.org (Node 20+) — needed by npx for skill install and any npx-based MCP servers"
require_cli npm "bundled with Node.js"

if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: manifest not found at $MANIFEST"
  exit 1
fi
jq empty "$MANIFEST" 2>/dev/null || {
  echo "ERROR: $MANIFEST is not valid JSON."
  exit 1
}

# ─── 1. Prompts: profile → harness → (hermes profile) → working directory ───

if [[ -z "$PROFILE" ]]; then
  PROFILE=$(prompt_choice "Agent profile" orchestrator specialist)
fi
if [[ "$PROFILE" != "orchestrator" && "$PROFILE" != "specialist" ]]; then
  echo "ERROR: unknown profile '$PROFILE' (expected orchestrator or specialist)."
  exit 1
fi

if [[ -z "$HARNESS" ]]; then
  HARNESS=$(prompt_choice "Target harness" claude-code hermes openclaw)
fi
if [[ "$HARNESS" != "claude-code" && "$HARNESS" != "hermes" && "$HARNESS" != "openclaw" ]]; then
  echo "ERROR: unknown harness '$HARNESS' (expected claude-code, hermes, or openclaw)."
  exit 1
fi

# Fail fast on a missing harness CLI, before any copying/installing.
require_harness_cli "$HARNESS"

HERMES_PROFILE=""
if [[ "$HARNESS" == "hermes" ]]; then
  HERMES_PROFILE=$(hermes_select_profile)
fi

if [[ -z "$WORKDIR_ARG" ]]; then
  WORKDIR_ARG=$(prompt_path "Base working directory (absolute path, outside the guild-os source tree)")
fi
if [[ -z "$WORKDIR_ARG" ]]; then
  echo "ERROR: a working directory is required."
  exit 1
fi
case "$WORKDIR_ARG" in
  /*) RESOLVED_WORKDIR="$WORKDIR_ARG" ;;
  *) RESOLVED_WORKDIR="$PWD/$WORKDIR_ARG" ;;
esac
check_workdir_outside_repo "$RESOLVED_WORKDIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setting up GuildOS: profile=$PROFILE harness=$HARNESS"
echo "Working directory: $RESOLVED_WORKDIR"
[[ -n "$HERMES_PROFILE" ]] && echo "Hermes profile: $HERMES_PROFILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
confirm "Proceed?" || exit 0

# ─── 2. Re-run / overwrite detection ─────────────────────────────────────────

MARKER="$RESOLVED_WORKDIR/.guildos-setup-manifest.json"
if [[ -f "$MARKER" ]]; then
  prev_profile=$(jq -r '.profile' "$MARKER")
  prev_harness=$(jq -r '.harness' "$MARKER")
  prev_installed_at=$(jq -r '.installed_at' "$MARKER")
  echo "Existing install found: profile=$prev_profile harness=$prev_harness (installed $prev_installed_at)"
  if [[ "$prev_profile" != "$PROFILE" || "$prev_harness" != "$HARNESS" ]]; then
    echo "WARNING: this run's profile/harness differs from what's recorded here."
  fi
  confirm "Overwrite/reinstall modules in this directory?" || {
    echo "Nothing to do — exiting."
    exit 0
  }
fi

# ─── 3. Manifest-driven module copy (never touches .env — see step 4) ───────

echo "Copying GuildOS modules for profile '$PROFILE'..."
copy_manifest_files "$RESOLVED_WORKDIR" "$PROFILE"

# ─── 4. .env — its OWN confirmation, structurally separate from step 3 ──────

sync_env_file "$RESOLVED_WORKDIR"
echo ""
echo "Fill in $RESOLVED_WORKDIR/.env with real credentials now — MCP server"
echo "registration below reads these values (neither Hermes nor OpenClaw"
echo "inherit the shell environment for stdio servers)."
if [[ "$DRY_RUN" != true ]]; then
  read -r -p "Press Enter once ready to continue (or Ctrl+C to stop and re-run later)... " _unused
fi

# ─── 5. Dependency install — Python only, no more curl|bash CLI installs ────
# (caw / moloch-agent are covered by the cobo-agentic-wallet / moloch-skills
# skills installed in step 7 — see the plan's CLI-dependency analysis.)

echo "Running 'uv sync' in $RESOLVED_WORKDIR..."
run_in_dir "$RESOLVED_WORKDIR" uv sync

# ─── 6. MCP server registration ──────────────────────────────────────────────

echo "Registering MCP servers..."
while IFS= read -r server_json; do
  case "$HARNESS" in
    claude-code) claude_register_mcp "$server_json" "$RESOLVED_WORKDIR" ;;
    hermes) hermes_register_mcp "$server_json" "$HERMES_PROFILE" "$RESOLVED_WORKDIR" ;;
    openclaw) openclaw_register_mcp "$server_json" "$RESOLVED_WORKDIR" ;;
  esac
done < <(manifest_mcp_servers "$PROFILE")

if [[ "$HARNESS" == "openclaw" ]]; then
  openclaw_reload
fi

# ─── 7. Skill installation — one shared mechanism for every harness ─────────

echo "Installing skills..."
while IFS= read -r skill_json; do
  install_skill_via_npx "$skill_json" "$HARNESS" "$RESOLVED_WORKDIR"
done < <(manifest_skills "$PROFILE")

# ─── 8. Marker file ───────────────────────────────────────────────────────────

if [[ "$DRY_RUN" != true ]]; then
  jq -n --arg p "$PROFILE" --arg h "$HARNESS" --arg t "$(date -u +%FT%TZ)" \
    '{profile: $p, harness: $h, installed_at: $t}' >"$MARKER"
fi

# ─── 9. Next steps ────────────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setup complete: $PROFILE on $HARNESS"
echo "Working directory: $RESOLVED_WORKDIR"
echo ""
echo "CLI dependency status:"
print_cli_dependency_status "$PROFILE"
echo ""
echo "Next steps:"
echo ""

NEXT_STEP=1
while IFS= read -r a2a_json; do
  a2a_command=$(jq -r '.command' <<<"$a2a_json")
  a2a_args=$(jq -r '.args | join(" ")' <<<"$a2a_json")
  a2a_port_env=$(jq -r '.port_env' <<<"$a2a_json")
  a2a_default_port=$(jq -r '.default_port' <<<"$a2a_json")
  a2a_card_path=$(jq -r '.agent_card_path' <<<"$a2a_json")
  echo "$((NEXT_STEP++)). Start the A2A server (separate terminal, from $RESOLVED_WORKDIR):"
  echo "   cd $RESOLVED_WORKDIR && $a2a_command $a2a_args"
  echo "   Listens on \$$a2a_port_env (default $a2a_default_port); Agent Card at"
  echo "   http://localhost:$a2a_default_port$a2a_card_path"
  echo ""
done < <(manifest_a2a_services "$PROFILE")

if [[ "$PROFILE" == "orchestrator" ]]; then
  echo "$((NEXT_STEP++)). The Orchestrator MCP server (guildos) is started BY your harness's"
  echo "   stdio MCP client, not run manually — it's already registered above."
  echo ""
fi

if [[ "$HARNESS" == "hermes" ]]; then
  echo "$((NEXT_STEP++)). Inside your Hermes chat session, run /reload-mcp to pick up the"
  echo "   newly registered MCP servers."
  echo ""
fi

echo "$((NEXT_STEP++)). Open your harness in $RESOLVED_WORKDIR and ask it to follow the"
echo "   onboarding instructions in each installed skill (see CLI dependency"
echo "   status above) to finish setting up caw / moloch-agent, etc."
echo ""
echo "$((NEXT_STEP++)). KNOWN LIMITATION: guild_context.json is per-directory mock state —"
echo "   running Orchestrator and Specialist in separate working directories"
echo "   (as this script does) means their guild state will NOT stay in sync"
echo "   automatically. This is a pre-existing guild-os limitation, not"
echo "   something this script papers over."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
