# Setup Reference

One-time environment setup for Sensei sessions. Read this when setting up a
new machine or Claude Code/Cowork installation — not part of routine
per-session context.

---

## Memory Setup (one-time terminal command)

To make Claude Code and Cowork share the same memory, run once:

```bash
mkdir -p ~/.claude/projects/-Users-santteegt-AIxWeb3-School
ln -sf ~/AIxWeb3_School/memory ~/.claude/projects/-Users-santteegt-AIxWeb3-School/memory
```

---

## MCP Servers — Recommended Local Configuration

Add the following to `.mcp.json` (gitignored) to enable agent-assisted EVM
interaction and live documentation lookup during development.

```json
{
  "mcpServers": {
    "evm-mcp-server": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "@mcpdotdirect/evm-mcp-server"
      ],
      "env": {
        "ETHERSCAN_API_KEY": "<API-KEY>"
      }
    },
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "<API-KEY>"
      }
    }
  }
}
```

### Server Reference

| Server | Package | Purpose |
|--------|---------|---------|
| `evm-mcp-server` | `@mcpdotdirect/evm-mcp-server` | Tools for interacting with 60+ EVM-compatible networks — balance checks, contract reads/writes, tx lookup, ENS resolution, NFT info, and more |
| `context7` | hosted at `mcp.context7.com` | Up-to-date code docs for any library or framework injected directly into the agent prompt — avoids stale training-data answers |

### Setup Notes

- `CONTEXT7_API_KEY` — obtain from [context7.com](https://context7.com) and store in `.mcp.json` under `mcpServers.context7.headers`; never commit the key
- `evm-mcp-server` requires Node/npx; set `ETHERSCAN_API_KEY` in its `env` block to enable contract ABI fetching and network metadata lookups via Etherscan
- Both servers are passive tools — the agent decides when to call them; no auto-execution
