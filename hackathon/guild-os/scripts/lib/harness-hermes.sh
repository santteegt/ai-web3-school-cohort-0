#!/usr/bin/env bash
# harness-hermes.sh — Hermes Agent MCP-registration adapter.
#
# Source: user-supplied `hermes mcp add --help` output:
#   usage: hermes mcp add [-h] [--url URL] [--command MCP_COMMAND] [--args ...]
#                          [--auth {oauth,header}] [--preset PRESET] [--env [ENV ...]] name
# Config lands in $HERMES_HOME/config.yaml under mcp_servers:, but we always
# go through the CLI, never hand-edit that file. Hermes does not pass the
# full shell environment to stdio servers — only --env-declared vars plus a
# safe baseline — so env values are resolved explicitly from the working
# directory's .env via resolve_env_values() (common.sh).
#
# Skill installation is NOT handled here — see install_skill_via_npx() in
# common.sh, shared across all three harnesses.
#
# Portability note (macOS ships bash 3.2 by default as /usr/bin/bash):
# `mapfile`/`readarray` don't exist before bash 4.0 — arrays below are
# filled with a plain `while IFS= read -r` loop instead, and every
# "${arr[@]}" expansion is guarded by a length check first (bash < 4.4
# throws "unbound variable" for "${arr[@]}" on a zero-element array under
# `set -u`).

# hermes_select_profile — lists real Hermes profiles on this machine and lets
# the user pick one; the choice determines $HERMES_HOME for every `hermes`
# command this script issues for the rest of the run. Per explicit user
# instruction: never invent a profile name, always read real ones.
hermes_select_profile() {
  local -a profiles=()
  local line
  # UNVERIFIED: exact `hermes profile list` output format (table vs. plain
  # names) was not supplied — best-effort parse takes the first
  # whitespace-delimited token of each non-blank line as a candidate name.
  # Flagged for smoke-testing on a real Hermes install.
  while IFS= read -r line; do
    profiles+=("$line")
  done < <(hermes profile list 2>/dev/null | grep -Ev '^[[:space:]]*$' | awk '{print $1}')
  if ((${#profiles[@]} == 0)); then
    echo "ERROR: 'hermes profile list' returned no profiles — is Hermes set up on this machine?" >&2
    exit 1
  fi
  prompt_choice "Hermes profile to target (determines \$HERMES_HOME for all MCP registration in this run)" "${profiles[@]}"
}

hermes_register_mcp() {
  local server_json="$1" hermes_profile="$2" workdir="$3"
  local name kind line
  name=$(jq -r '.name' <<<"$server_json")
  kind=$(jq -r '.kind' <<<"$server_json")

  # NOTE on flag ordering — UNVERIFIED, smoke-test before trusting: the
  # user-supplied usage line shows the positional `name` LAST, but both
  # --env and --args are variadic (space-separated value lists), and two
  # variadic flags in one command line is ambiguous for argparse-style
  # parsers depending on position. Best-effort choice below: `name` first
  # (parsed before any variadic flag is seen), --env before --args, --args
  # placed last since it's the command's own trailing arguments.
  local -a cmd=(hermes --profile "$hermes_profile" mcp add "$name")

  if [[ "$kind" == "mcp_http_external" ]]; then
    local url
    url=$(jq -r '.url' <<<"$server_json")
    cmd+=(--url "$url")
  else
    local command
    command=$(jq -r '.command' <<<"$server_json")
    cmd+=(--command "$command")
  fi

  local -a env_names=()
  while IFS= read -r line; do
    env_names+=("$line")
  done < <(jq -r '.env[]?' <<<"$server_json")
  if ((${#env_names[@]} > 0)); then
    local -a env_pairs=()
    while IFS= read -r line; do
      env_pairs+=("$line")
    done < <(resolve_env_values "$workdir" "${env_names[@]}")
    ((${#env_pairs[@]} > 0)) && cmd+=(--env "${env_pairs[@]}")
  fi

  if [[ "$kind" != "mcp_http_external" ]]; then
    local -a args=()
    while IFS= read -r line; do
      args+=("$line")
    done < <(jq -r '.args[]?' <<<"$server_json")
    ((${#args[@]} > 0)) && cmd+=(--args "${args[@]}")
  fi

  echo "Registering MCP server '$name' with Hermes (profile: $hermes_profile)..."
  run "${cmd[@]}"
}
