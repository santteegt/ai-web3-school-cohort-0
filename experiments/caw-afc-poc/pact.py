"""
Pact spec builder for Moloch-Agent PoC.

Builds CAW pact specs that scope the agent's on-chain authority to specific
Moloch / AgentFightClub contracts using the contract_call policy type.
"""

from cobo_agentic_wallet_api import PactSpecInput

# AgentFightClub Summoner (Base mainnet) — deploys new Baal DAOs
AFC_SUMMONER = "0x97aaa5be8b38795245f1c38a883b44cccdfb3e11"

# CAW chain identifier for Base mainnet
BAAL_CHAIN_ID = "BASE_ETH"

# Function selectors (keccak256(sig)[:4]) for the three allowed operations
_SEL_SUMMON_BAAL = "0x1f1bb0ef"          # summonBaalFromReferrer
_SEL_SUBMIT_PROPOSAL = "0x3a82ffc8"      # submitProposal(bytes,uint32,uint256,string)
_SEL_SUBMIT_VOTE = "0x67f61f07"          # submitVote(uint32,bool)

# ABI fragments required by CAW to validate calldata against each selector
_FUNCTION_ABIS = [
    {
        "type": "function",
        "selector": _SEL_SUMMON_BAAL,
        "inputs": [
            {"name": "summoner", "type": "address[]"},
            {"name": "shares", "type": "uint256[]"},
            {"name": "loot", "type": "uint256"},
            {"name": "sharesLoot", "type": "string"},
            {"name": "initializationParams", "type": "bytes"},
            {"name": "deployTokens", "type": "bool"},
            {"name": "saltNonce", "type": "string"},
        ],
    },
    {
        "type": "function",
        "selector": _SEL_SUBMIT_PROPOSAL,
        "inputs": [
            {"name": "proposalData", "type": "bytes"},
            {"name": "expiration", "type": "uint32"},
            {"name": "baalGas", "type": "uint256"},
            {"name": "details", "type": "string"},
        ],
    },
    {
        "type": "function",
        "selector": _SEL_SUBMIT_VOTE,
        "inputs": [
            {"name": "id", "type": "uint32"},
            {"name": "approved", "type": "bool"},
        ],
    },
]


def make_pact_spec(allowed_contracts: list[str], tx_count: int = 3) -> PactSpecInput:
    """
    Build a CAW pact spec that allows contract_call on whitelisted addresses
    restricted to the specific function selectors for Moloch governance.

    Args:
        allowed_contracts: List of contract addresses the agent may call.
            Pass [AFC_SUMMONER] for summon, [dao_address] for propose/vote,
            or [AFC_SUMMONER, dao_address] for the full PoC flow.
        tx_count: Number of transactions expected under this pact (default 3:
            summon + submitProposal + submitVote).

    Returns:
        Pact spec dict ready to pass to submit_pact(spec=...).
    """
    # Build per-contract target entries, mapping each contract to its allowed selectors
    summoner_addr = AFC_SUMMONER.lower()
    target_in = []
    for addr in allowed_contracts:
        addr_lower = addr.lower()
        if addr_lower == summoner_addr:
            target_in.append({
                "chain_id": BAAL_CHAIN_ID,
                "contract_addr": addr_lower,
                "function_id": _SEL_SUMMON_BAAL,
            })
        else:
            # DAO contract — allow submitProposal and submitVote
            target_in.append({
                "chain_id": BAAL_CHAIN_ID,
                "contract_addr": addr_lower,
                "function_id": _SEL_SUBMIT_PROPOSAL,
            })
            target_in.append({
                "chain_id": BAAL_CHAIN_ID,
                "contract_addr": addr_lower,
                "function_id": _SEL_SUBMIT_VOTE,
            })

    return {
        "policies": [
            {
                "name": "moloch-governance",
                "type": "contract_call",
                "rules": {
                    "effect": "allow",
                    "when": {
                        "chain_in": [BAAL_CHAIN_ID],
                        "target_in": target_in,
                    },
                    "always_review": True,
                    # not required when "params_match" is not used
                    # "function_abis": _FUNCTION_ABIS
                },
            }
        ],
        "completion_conditions": [
            {"type": "tx_count", "threshold": str(tx_count)},
            {"type": "time_elapsed", "threshold": "3600"},
        ],
    }


def get_pact_summary() -> dict:
    """Return a summary of the pact configuration (for logging)."""
    return {
        "chain": BAAL_CHAIN_ID,
        "summoner": AFC_SUMMONER,
        "policy_type": "contract_call",
        "allowed_selectors": {
            "summoner": f"summonBaal {_SEL_SUMMON_BAAL}",
            "dao": f"submitProposal {_SEL_SUBMIT_PROPOSAL}, submitVote {_SEL_SUBMIT_VOTE}",
        },
        "tx_count": 3,
        "gas_limit": "CAW-managed",
    }
