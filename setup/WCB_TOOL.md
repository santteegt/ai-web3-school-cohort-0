# WCB API Tool (`tools/wcb_client.py`)

Sensei has a CLI tool for interacting with the WCB Agent API programmatically.
No external dependencies — stdlib only. All output is clean JSON.

See `AGENTS.md` §9 for the "when to call this tool" trigger table — that
stays inline since it's a decision-relevant behavioral rule. This file is
usage/setup reference, read on demand.

## Usage

```bash
python tools/wcb_client.py status              # today's tasks + events + check-in status
python tools/wcb_client.py checkin list        # pending check-ins vs. submitted history
python tools/wcb_client.py tasks upcoming      # deadlines in the next 3 days
python tools/wcb_client.py catalog             # dump live procedure catalog
python tools/wcb_client.py call <procedure> [json_input]  # raw procedure call
```

## API Key Setup (one of these, in priority order)

1. **Env var** (recommended for terminal sessions):
   ```bash
   export WCB_AGENT_SECRET_API_KEY=your_key_here
   ```

2. **`.claude/settings.local.json`** (gitignored — safe for persistent local config):
   ```json
   {
     "env": {
       "WCB_AGENT_SECRET_API_KEY": "your_key_here"
     }
   }
   ```

## Program/Track Resolution

The tool auto-discovers `programId` and `trackId` from `users.getProfile`.
Override with env vars if needed:
```bash
export WCB_PROGRAM_ID=your_program_id
export WCB_TRACK_ID=your_track_id
```
