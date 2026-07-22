#!/usr/bin/env bash
# harness-openclaw.sh — OpenClaw MCP-registration adapter.
#
# Source: user-supplied usage examples for both transports:
#   openclaw mcp add local-tools --command node --arg ./dist/mcp-server.js \
#     --cwd /srv/openclaw-tools --env API_BASE=https://internal.example
#   openclaw mcp add docs --url https://mcp.example.com/mcp \
#     --transport streamable-http --auth oauth --oauth-scope docs.read \
#     --timeout 20 --connect-timeout 5 --include 'search,read_*'
# Note --arg is SINGULAR, repeated once per argument (not --args). Config
# lands in openclaw.json under mcp.servers, but we always go through the
# CLI, never hand-edit that file. `openclaw mcp doctor <name> --probe`
# verifies each registration; `openclaw mcp reload` refreshes config after
# the full batch (see openclaw_reload(), called once from the main script).
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

openclaw_register_mcp() {
  local server_json="$1" workdir="$2"
  local name kind line
  name=$(jq -r '.name' <<<"$server_json")
  kind=$(jq -r '.kind' <<<"$server_json")

  local -a cmd=(openclaw mcp add "$name")

  if [[ "$kind" == "mcp_http_external" ]]; then
    local url auth oauth_scope timeout connect_timeout include
    url=$(jq -r '.url' <<<"$server_json")
    cmd+=(--url "$url" --transport streamable-http)
    auth=$(jq -r '.auth // empty' <<<"$server_json")
    [[ -n "$auth" ]] && cmd+=(--auth "$auth")
    oauth_scope=$(jq -r '.oauth_scope // empty' <<<"$server_json")
    [[ -n "$oauth_scope" ]] && cmd+=(--oauth-scope "$oauth_scope")
    timeout=$(jq -r '.timeout // empty' <<<"$server_json")
    [[ -n "$timeout" ]] && cmd+=(--timeout "$timeout")
    connect_timeout=$(jq -r '.connect_timeout // empty' <<<"$server_json")
    [[ -n "$connect_timeout" ]] && cmd+=(--connect-timeout "$connect_timeout")
    include=$(jq -r '.include // empty' <<<"$server_json")
    [[ -n "$include" ]] && cmd+=(--include "$include")
  else
    local command
    command=$(jq -r '.command' <<<"$server_json")
    cmd+=(--command "$command")
    local -a args=()
    while IFS= read -r line; do
      args+=("$line")
    done < <(jq -r '.args[]?' <<<"$server_json")
    if ((${#args[@]} > 0)); then
      local a
      for a in "${args[@]}"; do
        cmd+=(--arg "$a")
      done
    fi
    cmd+=(--cwd "$workdir")
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
    if ((${#env_pairs[@]} > 0)); then
      local pair
      for pair in "${env_pairs[@]}"; do
        cmd+=(--env "$pair")
      done
    fi
  fi

  echo "Registering MCP server '$name' with OpenClaw..."
  run "${cmd[@]}"
  run openclaw mcp doctor "$name" --probe
}

openclaw_reload() {
  echo "Reloading OpenClaw MCP config..."
  run openclaw mcp reload
}
