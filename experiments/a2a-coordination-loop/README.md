# a2a-coordination-loop

GuildOS A2A Day 1 gate tests — validates 5 go/no-go integration gates before building the full A2A coordination stack.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

## Setup

```bash
uv sync
```

## Running the tests

The test suite requires a local Specialist server. Open two terminals:

**Terminal 1 — start the test Specialist server:**

```bash
uv run python a2a_test.py server
```

The server starts on `http://127.0.0.1:9998`.

**Terminal 2 — run all 5 gate tests:**

```bash
uv run python a2a_test.py tests
```

## Gates

| Gate | What it validates |
|------|-------------------|
| Gate 1 | AgentCard fetch — skills and streaming capability declared |
| Gate 2 | `SendMessage` with GuildOS metadata round-trip — all keys echoed correctly |
| Gate 3 | Artifact with SHA-256 hash — deliverable integrity verifiable |
| Gate 4 | SSE streaming state transitions — WORKING → COMPLETED observed |
| Gate 5 | `CancelTask` API reachable and responds |

All 5 gates must pass before proceeding with the GuildOS build.

## Dependencies

| Package | Purpose |
|---------|---------|
| `a2a-sdk[http-server]` | A2A protocol client + server (Google) |
| `uvicorn` | ASGI server for the test Specialist |
| `starlette` | ASGI routing for agent routes |
| `httpx` | Async HTTP client used by A2A card resolver |
