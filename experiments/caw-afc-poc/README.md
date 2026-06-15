# CAW × Moloch-Agent Minimal PoC

A minimal proof-of-concept demonstrating an Orchestrator agent using a Cobo Agentic Wallet (CAW) to interact with Moloch DAO via AgentFightClub.

## What This Demonstrates

1. **Summon a Moloch DAO** - Deploy a new DAO contract on Base mainnet
2. **Propose Membership** - Submit a membership proposal for a Specialist agent
3. **Vote on Proposal** - Cast a vote using CAW wallet with human approval

Each on-chain action requires human approval via the paired CAW wallet.

---

## Project Structure

```
.
├── README.md              # This file
├── pyproject.toml         # uv project config and dependencies
├── .python-version        # Python version pin (3.11)
├── .env.example           # Environment variables template
├── caw_client.py          # CAW API client (approval requests)
├── pact.py                # Pact configuration (whitelist)
├── orchestrator.py        # Main PoC script
└── test_poc.py            # Simple test to verify flow
```

---

## Prerequisites

### 1. CLI Tools

#### moloch-agent CLI
```bash
npm install -g @raidguild/meta-clawtel
moloch-agent --version
```

#### Cobo CAW CLI (optional, for wallet setup)
```bash
curl -fsSL https://raw.githubusercontent.com/CoboGlobal/cobo-agentic-wallet/master/install.sh | bash
caw --version (should be >= 0.2.86)
```

### 2. Project setup

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Navigate to project
cd experiments/caw-afc-poc

# 3. Install dependencies
uv sync

# 4. Configure environment
cp .env.example .env
# Edit .env with your CAW wallet and API credentials
```

### 3. Cobo CAW Wallet Setup

**Via CLI:**
```bash
caw onboard --wait
caw wallet pair --code-only
# Download Cobo Agentic Wallet App and enter the pairing code
caw wallet pair-status
```

### 4. Set wallet-related environment variables

```bash
caw address list # set ORCHESTRATOR_CAW_ADDRESS
caw address create --chain-id BASE_ETH # Optional if you want a fresh address
caw wallet current --show-api-key # AGENT_WALLET_API_KEY=api_key | AGENT_WALLET_WALLET_ID=wallet_uuid
```

### 5. Fund Wallet

Fund the `ORCHESTRATOR_CAW_ADDRESS` with some ETH on Base mainnet for gas

```bash
# From your personal wallet to CAW wallet
cast send $ORCHESTRATOR_CAW_ADDRESS --value 0.05ether --rpc-url https://mainnet.base.org
```

### 6. Pact Configuration

[pact.py](pact.py) has the pact definition for this PoC. Basically, it sets a `contract_call` policy that allows an agent to be able to call specific functions on both the DAO summoner contract and the DAO contract. For each function call, `always_review` enforce the user to always approve the tx before execution.

In terms of `completion_conditions`, a `tx_count=1` and 1-hour execution window per-tx are set.

Something that can be improved is to submit a single pact-per contract with all policy conditions instead of one pact per action.

---

## Running the PoC

Prior executing, make sure to set `USE_MOCK_CAW=true` to execute on-chain transactions on Base mainnet

```bash
# Run main script
uv run orchestrator.py

# Run tests
uv run pytest test_poc.py
```

### Expected Output

```
=== CAW × Moloch-Agent PoC ===

✓ Summoning GuildOS-POC DAO...
📱 Approval required: Summon DAO
[Check your CAW app - approve the request]
✓ DAO summoned at 0x...

✓ Proposing membership for specialist 0x...
📱 Approval required: Submit membership proposal
[Check your CAW app - approve the request]
✓ Proposal submitted: 0x...

✓ Voting YES on proposal...
📱 Approval required: Vote on proposal
[Check your CAW app - approve the request]
✓ Vote cast!

=== Summary ===
DAO: 0x...
Proposal: 0x...
Vote: YES
Status: Awaiting processing (after voting period)
```

---

## Architecture

```
Human Founder → CAW Wallet → Pact Check → Approval Request → Human Approves
                                                                  ↓
Orchestrator Agent ← moloch-agent CLI ← CAW Signature ← On-Chain Execution
```

**Flow:**
1. Agent initiates action (summon, propose, vote)
2. Pact validates against whitelist
3. Approval request sent to paired human wallet
4. Human approves in CAW app/dashboard
5. CAW signs transaction
6. Action executed on-chain via moloch-agent CLI

---

## Documentation

- **moloch-agent:** https://github.com/raid-guild/moloch-agent
- **AgentFightClub:** https://docs.agentfightclub.com
- **Cobo CAW:** https://www.cobo.com/cobo-agentic-wallet
- **uv:** https://astral.sh/uv

---

## Troubleshooting

### Sign/Tx gets stuck 

Check the local TSS node status and restart if required:

```bash
caw node logs -f
caw node restart
```

---

## License

MIT
