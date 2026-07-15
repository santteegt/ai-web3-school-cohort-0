"""ERC8004 — interface for ERC-8004 IdentityRegistry and ReputationRegistry.

Contract addresses are network-specific and loaded from config/networks.json
via src/shared/network_config.py, keyed by the CHAIN_ID env var — never
hardcode an address or a network name here.

register() and setAgentURI() sign through WalletProvider (CAW TSS) — no raw
EOA key is ever read. The Pact allowlist covers both selectors exactly (see
config/pact.json). web3.py is used only to build calldata and to read/decode
on-chain data (balanceOf, tokenURI, event logs) — it never signs or
broadcasts a transaction; that responsibility stays entirely inside
WalletProvider.

Registration metadata is stored fully on-chain as a base64-encoded
`data:application/json;base64,...` URI (RFC 2397) — see
build_registration_uri() — so no IPFS pin or HTTPS host needs to stay alive
for the registration to remain resolvable. Capabilities/skills live on the
relevant services[] entry (a2aSkills on A2A, capabilities on MCP,
skills/domains on a dedicated OASF entry), per
https://github.com/erc-8004/best-practices and
https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html —
never as top-level fields.

register_agent() is the recommended entry point for registering an agent:
it registers, then immediately backfills the registrations[] self-reference
({agentId, agentRegistry}) via a setAgentURI() follow-up, since agentId
isn't known until register() succeeds. register() and
update_registration_uri() are the lower-level primitives it composes.

This module never reads AGENT_WALLET_ADDRESS (or any other env var) itself
— register()/register_agent() take wallet_address as an explicit parameter.
Resolving it from the environment is the calling MCP server's job (see
src/guild/server.py), keeping this module a plain, testable function of its
inputs.

CRITICAL: give_feedback() MUST be called from the guild contract address
(via DAO proposal execution) — NOT from the Specialist Agent's own wallet,
and not from a raw agent EOA. Calling from the agent's wallet will cause a
silent revert (specs/10-technical-design.md §8 F2).
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
from pathlib import Path

from web3 import Web3
from web3.exceptions import TransactionNotFound

from src.shared import network_config
from src.shared.wallet import UnsignedTx, get_wallet_provider

logger = logging.getLogger(__name__)

NOTES_DIR = Path(__file__).parent.parent.parent / "logs"
REGISTRATIONS_CACHE_PATH = NOTES_DIR / "erc8004_registrations.json"

_RECEIPT_RETRY_ATTEMPTS = 5
_RECEIPT_RETRY_DELAY_SECONDS = 2.0

# Minimal ABI fragments — only the entries this module actually calls.
# Source: https://eips.ethereum.org/EIPS/eip-8004
_IDENTITY_REGISTRY_ABI = [
    {
        "type": "function",
        "name": "register",
        "stateMutability": "nonpayable",
        "inputs": [{"name": "agentURI", "type": "string"}],
        "outputs": [{"name": "agentId", "type": "uint256"}],
    },
    {
        "type": "function",
        "name": "setAgentURI",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "newURI", "type": "string"},
        ],
        "outputs": [],
    },
    {
        # Standard ERC-721 — the Identity Registry is an ERC-721 registry.
        "type": "function",
        "name": "balanceOf",
        "stateMutability": "view",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
    },
    {
        # Standard ERC-721.
        "type": "function",
        "name": "tokenURI",
        "stateMutability": "view",
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "outputs": [{"name": "", "type": "string"}],
    },
    {
        "type": "event",
        "name": "Registered",
        "anonymous": False,
        "inputs": [
            {"name": "agentId", "type": "uint256", "indexed": True},
            {"name": "agentURI", "type": "string", "indexed": False},
            {"name": "owner", "type": "address", "indexed": True},
        ],
    },
]

_REPUTATION_REGISTRY_ABI = [
    {
        "type": "function",
        "name": "getSummary",
        "stateMutability": "view",
        "inputs": [
            {"name": "agentId", "type": "uint256"},
            {"name": "clientAddresses", "type": "address[]"},
            {"name": "tag1", "type": "string"},
            {"name": "tag2", "type": "string"},
        ],
        "outputs": [
            {"name": "count", "type": "uint64"},
            {"name": "summaryValue", "type": "int128"},
            {"name": "summaryValueDecimals", "type": "uint8"},
        ],
    },
]


class RegistrationStateError(RuntimeError):
    """balanceOf() shows a wallet already owns an agentId, but no matching
    Registered event could be recovered to identify which one.

    This should not happen in normal operation (the event scan filters by
    the exact owner address with no block-range restriction) — surfacing it
    as an error avoids the alternative of silently minting a second agentId.
    """


def _identity_registry_address() -> str:
    return network_config.get_contract_address("erc8004_identity_registry")


def _reputation_registry_address() -> str:
    return network_config.get_contract_address("erc8004_reputation_registry")


def _web3() -> Web3:
    return Web3(Web3.HTTPProvider(network_config.get_rpc_url()))


def _identity_registry_contract(w3: Web3):
    address = Web3.to_checksum_address(_identity_registry_address())
    return w3.eth.contract(address=address, abi=_IDENTITY_REGISTRY_ABI)


def _reputation_registry_contract(w3: Web3):
    address = Web3.to_checksum_address(_reputation_registry_address())
    return w3.eth.contract(address=address, abi=_REPUTATION_REGISTRY_ABI)


def _load_registration_cache() -> dict:
    if not REGISTRATIONS_CACHE_PATH.exists():
        return {}
    try:
        return json.loads(REGISTRATIONS_CACHE_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        logger.warning("Could not read %s, treating cache as empty", REGISTRATIONS_CACHE_PATH)
        return {}


def _save_registration_cache(cache: dict) -> None:
    REGISTRATIONS_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRATIONS_CACHE_PATH.write_text(json.dumps(cache, indent=2))


def _recover_registration_from_events(w3: Web3, identity, wallet_address: str) -> dict | None:
    """Scan Registered events filtered by owner to recover a lost cache entry.

    Only reached when balanceOf() says the wallet already owns an agentId
    but the local cache doesn't have it (e.g. a fresh checkout).
    """
    checksum = Web3.to_checksum_address(wallet_address)
    logs = identity.events.Registered().get_logs(
        from_block=0, to_block="latest", argument_filters={"owner": checksum}
    )
    if not logs:
        return None
    event = logs[-1]
    record = {
        "agent_id": event["args"]["agentId"],
        "tx_hash": event["transactionHash"].hex(),
        "agent_uri": event["args"]["agentURI"],
    }
    cache = _load_registration_cache()
    cache[wallet_address.lower()] = record
    _save_registration_cache(cache)
    return record


async def _get_receipt_with_retry(w3: Web3, tx_hash: str):
    """Fetch a transaction receipt, tolerating brief RPC-node propagation lag.

    WalletProvider.sign() already waits for CAW-side confirmation before
    returning tx_hash, but the RPC node backing this module's own web3.py
    client may take a moment to catch up.
    """
    for attempt in range(_RECEIPT_RETRY_ATTEMPTS):
        try:
            return w3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            if attempt == _RECEIPT_RETRY_ATTEMPTS - 1:
                raise
            await asyncio.sleep(_RECEIPT_RETRY_DELAY_SECONDS)


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def read_profile(agent_id: int) -> dict:
    """Read an ERC-8004 profile: name, capabilities, domains, delivery_count,
    a2a_endpoint.

    Primary path decodes the on-chain `data:` URI directly (no network call).
    Falls back to an https:// or ipfs:// fetch for forward-compatibility with
    a future update_registration_uri() call pointing elsewhere, tolerating
    connection failures gracefully rather than raising — a registered
    agentURI is not required to resolve immediately (see issue #5's erratum).

    Capabilities/domains are scanned from services[] per erc-8004 best
    practices, not read from top-level fields: a2aSkills from the A2A entry,
    capabilities from the MCP entry, skills/domains from the OASF entry —
    merged and deduplicated.
    """
    w3 = _web3()
    identity = _identity_registry_contract(w3)
    agent_uri = identity.functions.tokenURI(agent_id).call()

    registration = _resolve_registration_content(agent_uri)

    a2a_endpoint = None
    capabilities: list[str] = []
    domains: list[str] = []
    for service in registration.get("services", []):
        service_name = service.get("name")
        if service_name == "A2A":
            if a2a_endpoint is None:
                a2a_endpoint = service.get("endpoint")
            capabilities.extend(service.get("a2aSkills", []))
        elif service_name == "MCP":
            capabilities.extend(service.get("capabilities", []))
        elif service_name == "OASF":
            capabilities.extend(service.get("skills", []))
            domains.extend(service.get("domains", []))

    reputation = _reputation_registry_contract(w3)
    # Empty clientAddresses is correct by construction for a fresh/before-state
    # agent (count=0). Full clientAddresses aggregation is deferred — see
    # Gap 2 in hackathon/research/ERC8004_ERC8183_ANALYSIS.md.
    count, _value, _decimals = reputation.functions.getSummary(agent_id, [], "", "").call()

    return {
        "agent_id": agent_id,
        "name": registration.get("name"),
        "capabilities": _dedupe_preserve_order(capabilities),
        "domains": _dedupe_preserve_order(domains),
        "delivery_count": count,
        "a2a_endpoint": a2a_endpoint,
        "agent_uri": agent_uri,
    }


def _resolve_registration_content(agent_uri: str) -> dict:
    if agent_uri.startswith("data:"):
        _, _, payload = agent_uri.partition(",")
        return json.loads(base64.b64decode(payload))

    if agent_uri.startswith(("http://", "https://", "ipfs://")):
        import httpx

        url = agent_uri
        if agent_uri.startswith("ipfs://"):
            url = "https://ipfs.io/ipfs/" + agent_uri.removeprefix("ipfs://")
        try:
            response = httpx.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            logger.warning("Could not resolve agentURI %s", agent_uri)
            return {}

    return {}


def build_a2a_service(
    endpoint: str,
    version: str = "0.3.0",
    a2a_skills: list[str] | None = None,
) -> dict:
    """Build an A2A services[] entry per erc-8004 best practices.

    a2a_skills is optional — the A2A AgentCard at `endpoint` is the primary
    skill advertisement; a2aSkills here is a redundant on-chain mirror for
    discovery without an HTTP round-trip.
    """
    service: dict = {"name": "A2A", "endpoint": endpoint, "version": version}
    if a2a_skills:
        service["a2aSkills"] = list(a2a_skills)
    return service


def build_mcp_service(
    endpoint: str,
    version: str = "2025-06-18",
    tools: list[str] | None = None,
    prompts: list[str] | None = None,
    resources: list[str] | None = None,
    capabilities: list[str] | None = None,
) -> dict:
    """Build an MCP services[] entry per erc-8004 best practices."""
    service: dict = {"name": "MCP", "endpoint": endpoint, "version": version}
    if tools:
        service["mcpTools"] = list(tools)
    if prompts:
        service["mcpPrompts"] = list(prompts)
    if resources:
        service["mcpResources"] = list(resources)
    if capabilities:
        service["capabilities"] = list(capabilities)
    return service


def build_oasf_service(
    skills: list[str] | None = None,
    domains: list[str] | None = None,
    endpoint: str = "",
    version: str = "0.8",
) -> dict:
    """Build an OASF services[] entry — the standardized place for an
    agent's general capabilities/domains, using the OASF schema framework
    (skills/domains), per erc-8004 best practices' Capabilities
    Classification convention. Not a top-level field.
    """
    service: dict = {"name": "OASF", "endpoint": endpoint, "version": version}
    if skills:
        service["skills"] = list(skills)
    if domains:
        service["domains"] = list(domains)
    return service


def build_registration_uri(
    name: str,
    description: str,
    services: list[dict],
    image: str | None = None,
    x402_support: bool | None = None,
    active: bool = True,
    registrations: list[dict] | None = None,
    supported_trust: list[str] | None = None,
) -> str:
    """Build an ERC-8004 registration file and return it as a fully on-chain
    `data:application/json;base64,...` URI (RFC 2397) — no IPFS pin or HTTPS
    host required for the metadata to remain resolvable.

    Only `name`, `description`, and `services` are required — every other
    field is caller-supplied and optional, omitted entirely when not given
    (never emitted with a placeholder). `services` is fully open: any
    well-formed entries the caller wants (A2A, MCP, OASF, or anything else —
    see build_a2a_service()/build_mcp_service()/build_oasf_service() for the
    three erc-8004 best-practices conventions, or hand-roll any other shape).

    Schema per https://github.com/erc-8004/best-practices and
    https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html.
    Capabilities/skills belong on the relevant services[] entry, never as a
    top-level field here.
    """
    registration: dict = {
        "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
        "name": name,
        "description": description,
    }
    if image is not None:
        registration["image"] = image
    registration["services"] = list(services)
    if x402_support is not None:
        registration["x402Support"] = x402_support
    registration["active"] = active
    if registrations:
        registration["registrations"] = list(registrations)
    if supported_trust:
        registration["supportedTrust"] = list(supported_trust)

    raw = json.dumps(registration, separators=(",", ":")).encode()
    return "data:application/json;base64," + base64.b64encode(raw).decode()


def build_registrations_entry(agent_id: int) -> dict:
    """Build the registrations[] self-reference entry — {agentId,
    agentRegistry} in CAIP-10-style eip155:{chainId}:{address} format, per
    the erc-8004 best-practices example. Added via an immediate
    setAgentURI() follow-up right after a fresh register() — agentId isn't
    known until registration succeeds (see register_agent()).
    """
    chain_id = network_config.get_chain_id()
    registry_address = Web3.to_checksum_address(_identity_registry_address())
    return {"agentId": agent_id, "agentRegistry": f"eip155:{chain_id}:{registry_address}"}


async def register(agent_uri: str, wallet_address: str) -> dict:
    """Call IdentityRegistry.register(agentURI) through WalletProvider.

    wallet_address identifies the calling agent's own wallet — the caller
    (ultimately the MCP server boundary, e.g. src/guild/server.py) resolves
    this from its own environment; this module never reads env vars itself,
    so it stays a plain, testable function of its inputs.

    Idempotent: if wallet_address already owns an agentId (per balanceOf()),
    no new transaction is broadcast — the cached or on-chain-recovered
    registration is returned instead. Does not require agent_uri to resolve
    at registration time; it's just an on-chain write of a URI string (same
    as registering a domain before hosting goes live).

    Returns:
        {"agent_id": int, "tx_hash": str, "agent_uri": str, "minted": bool}
        — minted is True only when this call actually broadcast a new
        register() transaction, False for either idempotent path (cache hit
        or event-log recovery).
    """
    w3 = _web3()
    identity = _identity_registry_contract(w3)

    if wallet_address:
        checksum = Web3.to_checksum_address(wallet_address)
        already_registered = identity.functions.balanceOf(checksum).call() > 0
        if already_registered:
            cached = _load_registration_cache().get(wallet_address.lower())
            if cached:
                return {**cached, "minted": False}
            recovered = _recover_registration_from_events(w3, identity, wallet_address)
            if recovered:
                return {**recovered, "minted": False}
            raise RegistrationStateError(
                f"balanceOf({wallet_address}) > 0 but no Registered event "
                "could be recovered — refusing to mint a second agentId"
            )
    else:
        logger.warning(
            "wallet_address not provided — skipping the idempotency check; "
            "register() will proceed unconditionally"
        )

    calldata = identity.encode_abi(abi_element_identifier="register", args=[agent_uri])
    tx: UnsignedTx = {
        "to": _identity_registry_address(),
        "data": calldata,
        "value": "0",
        "chainId": int(network_config.get_chain_id()),
    }

    wallet = get_wallet_provider()
    result = await wallet.sign(tx)
    tx_hash = result.tx_hash or ""

    receipt = await _get_receipt_with_retry(w3, tx_hash)
    events = identity.events.Registered().process_receipt(receipt)
    if not events:
        raise RegistrationStateError(f"No Registered event found in receipt for tx {tx_hash}")
    agent_id = events[0]["args"]["agentId"]

    record = {"agent_id": agent_id, "tx_hash": tx_hash, "agent_uri": agent_uri}
    if wallet_address:
        cache = _load_registration_cache()
        cache[wallet_address.lower()] = record
        _save_registration_cache(cache)
    return {**record, "minted": True}


async def update_registration_uri(agent_id: int, new_uri: str) -> str:
    """Call IdentityRegistry.setAgentURI(agentId, newURI) through WalletProvider.

    The update path for a registration metadata change (a new capability, a
    moved A2A endpoint) — never a second register() call, which would
    attempt (and fail, or worse, silently succeed) to mint a new agentId for
    a wallet that already has one.
    """
    w3 = _web3()
    identity = _identity_registry_contract(w3)
    calldata = identity.encode_abi(
        abi_element_identifier="setAgentURI", args=[agent_id, new_uri]
    )
    tx: UnsignedTx = {
        "to": _identity_registry_address(),
        "data": calldata,
        "value": "0",
        "chainId": int(network_config.get_chain_id()),
    }
    wallet = get_wallet_provider()
    result = await wallet.sign(tx)
    return result.tx_hash or ""


async def register_agent(
    name: str,
    description: str,
    services: list[dict],
    wallet_address: str,
    image: str | None = None,
    x402_support: bool | None = None,
    active: bool = True,
    registrations: list[dict] | None = None,
    supported_trust: list[str] | None = None,
) -> dict:
    """Register an agent's ERC-8004 identity, done right: register(), then
    immediately backfill the registrations[] self-reference ({agentId,
    agentRegistry}) via a setAgentURI() follow-up — agentId can't be known
    until after register() succeeds, so the on-chain record starts
    incomplete for one block and is patched immediately rather than left
    half-filled until some future update.

    wallet_address identifies the calling agent's own wallet (resolved by
    the caller from its own environment — see register()'s docstring; this
    module never reads env vars itself).

    Idempotent — a wallet that already owns an agentId (minted=False) skips
    the follow-up entirely; there is nothing to backfill. Every fresh
    registration is therefore two on-chain transactions (Registered, then
    URIUpdated), not one.

    Returns:
        {"agent_id": int, "agent_uri": str (final), "register_tx_hash": str,
         "update_tx_hash": str | None, "minted": bool}
    """
    initial_uri = build_registration_uri(
        name=name,
        description=description,
        services=services,
        image=image,
        x402_support=x402_support,
        active=active,
        registrations=registrations,
        supported_trust=supported_trust,
    )
    result = await register(initial_uri, wallet_address=wallet_address)

    if not result["minted"]:
        return {
            "agent_id": result["agent_id"],
            "agent_uri": result["agent_uri"],
            "register_tx_hash": result["tx_hash"],
            "update_tx_hash": None,
            "minted": False,
        }

    self_reference = build_registrations_entry(result["agent_id"])
    final_uri = build_registration_uri(
        name=name,
        description=description,
        services=services,
        image=image,
        x402_support=x402_support,
        active=active,
        registrations=[*(registrations or []), self_reference],
        supported_trust=supported_trust,
    )
    update_tx_hash = await update_registration_uri(result["agent_id"], final_uri)

    if wallet_address:
        cache = _load_registration_cache()
        cache[wallet_address.lower()] = {
            "agent_id": result["agent_id"],
            "tx_hash": result["tx_hash"],
            "agent_uri": final_uri,
        }
        _save_registration_cache(cache)

    return {
        "agent_id": result["agent_id"],
        "agent_uri": final_uri,
        "register_tx_hash": result["tx_hash"],
        "update_tx_hash": update_tx_hash,
        "minted": True,
    }


def give_feedback(
    task_type: str,
    deliverable_hash: str,
    acceptance_timestamp: int,
    payment_wei: int,
    guild_address: str,
    a2a_task_id: str,
) -> str:
    """Call ReputationRegistry.giveFeedback() with 6 fields.

    Caller must be the guild contract (via DAO proposal execution) — never
    an agent EOA, never the Specialist wallet (specs/10-technical-design.md
    §8 F2). Returns DeliveryRecorded event tx hash.

    The full flow is: reputation_propose submits an executable Moloch
    proposal encoding giveFeedback(); Gate 4 halts for human vote; on
    passing vote AgentFightClub.process(proposal_id) executes it with
    msg.sender = guild contract. This function is the stub seam for the
    final on-chain call — no raw private key is ever accepted.
    """
    raise NotImplementedError


def capture_snapshot(agent_id: int, filename: str) -> dict:
    """Read and save agent profile to ./logs/{filename}.json."""
    profile = read_profile(agent_id)
    path = NOTES_DIR / f"{filename}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2, default=str))
    return profile
