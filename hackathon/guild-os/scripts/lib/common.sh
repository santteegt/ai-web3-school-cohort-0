#!/usr/bin/env bash
# common.sh — shared helpers for setup-agent-profile.sh: prompts, prerequisite
# checks, manifest-driven module copy, .env handling, and the one shared
# skill-install path (npx skills, used by every harness). Sourced, not run
# directly — expects REPO_ROOT and MANIFEST to already be set by the caller.

DRY_RUN="${DRY_RUN:-false}"

# ─── Dry-run wrapper ─────────────────────────────────────────────────────────
# Every side-effecting call in this script goes through run() so --dry-run
# exercises the full control flow (prompts, manifest parsing, jq loops) and
# prints the exact commands it would issue, without touching any harness.
run() {
  if [[ "$DRY_RUN" == true ]]; then
    echo "+ $*"
  else
    "$@"
  fi
}

# Like run(), but executes the command with CWD set to $1 first. Dry-run
# mode never actually `cd`s (the target working directory may not exist yet
# — module copy is itself skipped under --dry-run) — it just prints what
# would run, prefixed with the intended directory, so a plain `(cd "$dir" &&
# run ...)` at the call site would fail with "No such file or directory"
# on a dry run against a not-yet-created workdir.
run_in_dir() {
  local dir="$1"
  shift
  if [[ "$DRY_RUN" == true ]]; then
    echo "+ (cd $dir && $*)"
  else
    (cd "$dir" && "$@")
  fi
}

# ─── Prerequisite checks ──────────────────────────────────────────────────────

require_cli() {
  local bin="$1" hint="$2"
  command -v "$bin" >/dev/null 2>&1 || {
    echo "ERROR: '$bin' is required but not found on PATH."
    echo "Install: $hint"
    exit 1
  }
}

require_harness_cli() {
  case "$1" in
    claude-code) require_cli claude "https://code.claude.com/docs — install Claude Code" ;;
    hermes) require_cli hermes "https://github.com/nousresearch/hermes-agent" ;;
    openclaw) require_cli openclaw "https://github.com/openclaw/openclaw" ;;
    *)
      echo "ERROR: unknown harness '$1'."
      exit 1
      ;;
  esac
}

# ─── Prompts ───────────────────────────────────────────────────────────────

confirm() {
  local prompt="$1" reply
  read -r -p "$prompt [y/N] " reply
  [[ "$reply" =~ ^[Yy]$ ]]
}

# prompt_choice "Label" opt1 opt2 ... — prints the menu to stderr, the chosen
# value to stdout (so callers can do VAR=$(prompt_choice ...) safely).
prompt_choice() {
  local label="$1"
  shift
  local -a options=("$@")
  echo "$label:" >&2
  local i=1
  for opt in "${options[@]}"; do
    echo "  $i) $opt" >&2
    i=$((i + 1))
  done
  local choice
  while true; do
    read -r -p "Enter number [1-${#options[@]}]: " choice
    if [[ "$choice" =~ ^[0-9]+$ ]] && ((choice >= 1 && choice <= ${#options[@]})); then
      echo "${options[$((choice - 1))]}"
      return 0
    fi
    echo "Invalid choice." >&2
  done
}

prompt_path() {
  local label="$1" path
  read -r -p "$label: " path
  echo "$path"
}

check_workdir_outside_repo() {
  local resolved="$1"
  if [[ "$resolved" == "$REPO_ROOT" || "$resolved" == "$REPO_ROOT"/* ]]; then
    echo "ERROR: working directory must be outside $REPO_ROOT (got $resolved)."
    echo "This script copies guild-os modules INTO the working directory —"
    echo "targeting the repo itself (or a path inside it) would copy files onto themselves."
    exit 1
  fi
}

# ─── Manifest accessors (shared[] + profiles.<profile>[], merged) ───────────

manifest_files() {
  local profile="$1"
  jq -r --arg p "$profile" '.shared.files[], .profiles[$p].files[]' "$MANIFEST"
}

manifest_mcp_servers() {
  local profile="$1"
  jq -c --arg p "$profile" '.shared.mcp_servers[], .profiles[$p].mcp_servers[]' "$MANIFEST"
}

manifest_skills() {
  local profile="$1"
  jq -c --arg p "$profile" '.shared.skills[], .profiles[$p].skills[]' "$MANIFEST"
}

manifest_cli_dependencies() {
  local profile="$1"
  jq -c --arg p "$profile" '.shared.known_cli_dependencies[], .profiles[$p].known_cli_dependencies[]' "$MANIFEST"
}

manifest_a2a_services() {
  local profile="$1"
  jq -c --arg p "$profile" '(.profiles[$p].a2a_services // [])[]' "$MANIFEST"
}

# ─── Module copy ─────────────────────────────────────────────────────────────
# Scoped strictly to manifest-declared paths — .venv/, logs/, output/, .env,
# and the install marker are never manifest entries, so they're structurally
# untouched here regardless of overwrite mode.

copy_manifest_files() {
  local workdir="$1" profile="$2"
  local rel
  while IFS= read -r rel; do
    local src="$REPO_ROOT/$rel"
    local dest="$workdir/$rel"
    if [[ ! -e "$src" ]]; then
      echo "WARNING: manifest path '$rel' not found in $REPO_ROOT — skipping."
      continue
    fi
    run mkdir -p "$(dirname "$dest")"
    if [[ -d "$src" ]]; then
      if command -v rsync >/dev/null 2>&1; then
        run rsync -a --delete "$src/" "$dest/"
      else
        echo "NOTE: rsync not found — falling back to cp -R (stale removed files won't be cleaned up)."
        run rm -rf "$dest"
        run cp -R "$src" "$dest"
      fi
    else
      run cp "$src" "$dest"
    fi
  done < <(manifest_files "$profile")
}

# ─── .env handling — its own confirmation, never derived from OVERWRITE_MODULES ──

sync_env_file() {
  local workdir="$1"
  if [[ ! -f "$workdir/.env" ]]; then
    run cp "$REPO_ROOT/.env.example" "$workdir/.env"
    echo "Created .env from .env.example — fill in secrets before running."
  else
    echo "An .env already exists at $workdir/.env."
    if confirm "Overwrite it with a fresh .env.example? This DESTROYS any credentials already entered."; then
      run cp "$REPO_ROOT/.env.example" "$workdir/.env"
    else
      echo "Leaving existing .env untouched."
    fi
  fi
}

# Reads the given env var NAMES out of <workdir>/.env (KEY=VALUE lines) and
# prints "NAME=VALUE" pairs, one per line, skipping names with no value set —
# used to build --env flags for harnesses that don't inherit the shell env.
resolve_env_values() {
  local workdir="$1"
  shift
  local env_file="$workdir/.env"
  [[ -f "$env_file" ]] || return 0
  local name value
  for name in "$@"; do
    value=$(grep -E "^${name}=" "$env_file" | tail -n1 | cut -d= -f2-)
    [[ -n "$value" ]] && echo "${name}=${value}"
  done
}

# ─── Skills — one shared mechanism for every harness (npx skills) ───────────

install_skill_via_npx() {
  local skill_json="$1" harness="$2" workdir="$3"
  local kind name agent_id
  kind=$(jq -r '.kind' <<<"$skill_json")
  name=$(jq -r '.name' <<<"$skill_json")
  agent_id=$(jq -r --arg h "$harness" '.harness_agent_ids[$h]' "$MANIFEST")

  local -a cmd=(npx skills add)
  if [[ "$kind" == "skill_local" ]]; then
    local source_path
    source_path=$(jq -r '.source_path' <<<"$skill_json")
    cmd+=("$REPO_ROOT/$source_path" --copy)
  else
    local source skill_filter
    source=$(jq -r '.source' <<<"$skill_json")
    skill_filter=$(jq -r '.skill_filter // empty' <<<"$skill_json")
    cmd+=("$source")
    [[ -n "$skill_filter" ]] && cmd+=(--skill "$skill_filter")
  fi
  cmd+=(--agent "$agent_id" --yes)

  echo "Installing skill '$name' for $harness..."
  run_in_dir "$workdir" "${cmd[@]}"
}

# ─── CLI-dependency status (informational only — no auto-install) ──────────
# The cobo-agentic-wallet / moloch-skills skills installed above carry their
# own onboarding instructions for these tools; this just reports whether
# they're already on PATH and points at the skill that covers them if not.

print_cli_dependency_status() {
  local profile="$1"
  local dep_json name check skill
  while IFS= read -r dep_json; do
    name=$(jq -r '.name' <<<"$dep_json")
    check=$(jq -r '.check_command' <<<"$dep_json")
    skill=$(jq -r '.covered_by_skill' <<<"$dep_json")
    if eval "$check" >/dev/null 2>&1; then
      echo "  [ok] $name found on PATH"
    else
      echo "  [ ] $name not found — ask your harness to follow the '$skill' skill's onboarding instructions."
    fi
  done < <(manifest_cli_dependencies "$profile")
}
