#!/usr/bin/env bash
# harness-claude-code.sh — Claude Code MCP-registration adapter.
#
# Source: code.claude.com/docs/en/mcp, /mcp-quickstart. Project-scoped MCP
# servers live in .mcp.json at the working-directory root; the confirmed CLI
# is `claude mcp add ... --scope project <name> -- <command> [args...]`
# (stdio) or `claude mcp add --transport http --scope project <name> <url>`
# (remote). We always go through the CLI, never hand-edit .mcp.json.
#
# Skill installation is NOT handled here — see install_skill_via_npx() in
# common.sh, shared across all three harnesses.
#
# Portability notes (macOS ships bash 3.2 by default as /usr/bin/bash):
# - `mapfile`/`readarray` don't exist before bash 4.0 — arrays below are
#   filled with a plain `while IFS= read -r` loop instead.
# - Every "${arr[@]}" is only ever expanded after being built incrementally
#   onto a guaranteed-non-empty prefix (cmd=(claude mcp add)), never
#   expanded directly while possibly empty — under `set -u`, bash < 4.4
#   throws "unbound variable" for "${arr[@]}" on a zero-element array.

claude_register_mcp() {
  local server_json="$1" workdir="$2"
  local name kind
  name=$(jq -r '.name' <<<"$server_json")
  kind=$(jq -r '.kind' <<<"$server_json")

  local -a cmd=(claude mcp add)

  local -a env_names=()
  local line
  while IFS= read -r line; do
    env_names+=("$line")
  done < <(jq -r '.env[]?' <<<"$server_json")
  if ((${#env_names[@]} > 0)); then
    local -a env_pairs=()
    while IFS= read -r line; do
      env_pairs+=("$line")
    done < <(resolve_env_values "$workdir" "${env_names[@]}")
    if ((${#env_pairs[@]} > 0)); then
      local pair
      for pair in "${env_pairs[@]}"; do
        cmd+=(--env "$pair")
      done
    fi
  fi

  echo "Registering MCP server '$name' with Claude Code..."
  if [[ "$kind" == "mcp_http_external" ]]; then
    local url
    url=$(jq -r '.url' <<<"$server_json")
    cmd+=(--transport http --scope project "$name" "$url")
  else
    local command
    command=$(jq -r '.command' <<<"$server_json")
    cmd+=(--transport stdio --scope project "$name" -- "$command")
    local -a args=()
    while IFS= read -r line; do
      args+=("$line")
    done < <(jq -r '.args[]?' <<<"$server_json")
    ((${#args[@]} > 0)) && cmd+=("${args[@]}")
  fi

  run_in_dir "$workdir" "${cmd[@]}"
}
