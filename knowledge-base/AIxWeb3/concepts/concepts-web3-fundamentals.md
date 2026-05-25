---
marp: true
theme: default
paginate: true
footer: "AI × Web3 School — Web3 Fundamentals Concept Cards"
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Web3 Fundamentals
## Concept Cards

AI × Web3 School · Cohort 0
2026-05-25

55 concepts · Cryptography · Wallet · Smart Contracts · Dev Stack · Network · Account Abstraction · DeFi · Oracle · Indexing · Security

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 🔐 Cryptography

---
<!-- Concept: Cryptography -->

# Cryptography

> Mathematical foundation enabling trustless ownership through hashing, key pairs, and signatures that replace central authority with cryptographic proof.

**Example:** Ethereum uses Keccak256 hashing and ECDSA signatures so you prove ownership of an account without sharing your private key.

**Boundary:** Cryptography secures *data integrity and ownership*, not *privacy* — transactions are cryptographically valid but publicly visible on-chain.

---
<!-- Concept: Hash Function -->

# Hash Function

> Deterministic one-way transform (SHA256/Keccak256) that maps any input to a fixed-length digest; identical inputs always produce identical hashes.

**Example:** Keccak256("hello") always returns the same 32-byte hash; changing one character produces a completely different hash (avalanche effect).

**Boundary:** Hash functions are *irreversible* — you cannot recover the original input from the digest, so they cannot encrypt secrets.

---
<!-- Concept: Public Key -->

# Public Key

> Shareable cryptographic output from an asymmetric key pair; Ethereum address is the last 20 bytes of Keccak256(public key); safe to distribute.

**Example:** Your Ethereum address 0x1234...abcd is derived from your public key; anyone can send you funds, but only your private key can spend them.

**Boundary:** A public key *proves you own the account* when you sign, but it does *not* grant spending rights — only the private key does.

---
<!-- Concept: Private Key -->

# Private Key

> 256-bit root secret that controls a blockchain account; the holder can authorize any transaction; exposure or sharing means loss of account control.

**Example:** MetaMask stores your private key locally; if you share it or import it into an untrusted app, attackers can drain your account instantly.

**Boundary:** A private key is *not the same as a seed phrase* — seed phrases (12–24 words) *generate* private keys via HD derivation paths, but are distinct.

---
<!-- Concept: Cryptographic Signature -->

# Cryptographic Signature

> Mathematical proof that a specific private key authorized a specific message, without revealing the key; every on-chain transaction is a signed message.

**Example:** When you sign a transaction in MetaMask, you prove you hold the private key without exposing it; the network verifies the signature and executes the tx.

**Boundary:** A valid signature *proves authorization*, not *execution* — the network still decides whether to accept the transaction based on nonce, balance, and gas.

---
<!-- Concept: Merkle Tree -->

# Merkle Tree

> Binary tree of hashes where the root hash compactly represents an entire dataset; Merkle proofs verify set membership in O(log n) steps instead of scanning all data.

**Example:** Bitcoin blocks use Merkle trees to prove a transaction is in the block using only ~10 hashes instead of scanning all 2,000 transactions.

**Boundary:** Merkle proofs prove *inclusion in a specific tree*, not *absence* — you cannot use a Merkle proof to show a transaction is *not* in a block.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 👛 Wallet

---
<!-- Concept: EOA (Externally Owned Account) -->

# EOA (Externally Owned Account)

> A blockchain account controlled entirely by a private key, with no on-chain code; can initiate transactions but cannot execute conditional logic.

**Example:** Your MetaMask wallet address (0x...) on Ethereum — you hold the private key, sign transactions, and control the funds directly.

**Boundary:** EOAs cannot react to incoming transactions autonomously; smart contracts can, but you don't control them with a single private key.

---
<!-- Concept: Mnemonic (Seed Phrase) -->

# Mnemonic (Seed Phrase)

> A 12 or 24-word BIP-39 sequence encoding master entropy; all private keys in your HD wallet derive from it via standardized derivation paths.

**Example:** One MetaMask seed phrase generates your Ethereum account 0, account 1, account 2… and the same accounts on Polygon, Arbitrum, and all EVM chains.

**Boundary:** Losing your seed phrase means losing ALL accounts derived from it forever; even one word missing makes recovery cryptographically infeasible.

---
<!-- Concept: Web3 Transaction -->

# Web3 Transaction

> A signed data package instructing the network to change on-chain state; includes nonce, recipient, value, calldata, and gas parameters; finalized once mined in a block.

**Example:** Swapping 1 ETH for USDC on Uniswap v3: your wallet signs a transaction with swap calldata, Uniswap's contract executes it, Ethereum records the state change.

**Boundary:** A signed transaction is NOT final until included in a confirmed block; mempool transactions can be dropped, replaced (EIP-1559), or reordered by MEV.

---
<!-- Concept: Gas -->

# Gas

> The unit measuring computational work to execute EVM operations; paid in ETH (gwei); EIP-1559 base fee is burned; L2 rollups reduce costs 10–100x.

**Example:** A simple ETH transfer costs ~21,000 gas; a Uniswap swap costs 100,000–200,000 gas; at 20 gwei per gas, that's $2–4 per swap on L1 at current prices.

**Boundary:** Gas price (gwei) and gas *limit* (units) are separate; paying high gwei doesn't guarantee fast inclusion if network demand is low.

---
<!-- Concept: Block Explorer -->

# Block Explorer

> A read-only web interface providing human-readable access to all on-chain data: transactions, blocks, addresses, contract code, events, and token balances.

**Example:** Etherscan — paste a transaction hash and see the sender, receiver, value transferred, gas used, and smart contract calls all in one page.

**Boundary:** Block explorers show only what's on-chain; off-chain data (prices, metadata in centralized databases) requires external APIs or oracles alongside on-chain facts.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 📜 Smart Contracts

---
<!-- Concept: Smart Contract -->

# Smart Contract

> A program deployed on a blockchain that executes deterministically when called; its state and code are public and immutable unless a proxy pattern enables upgrades.

**Example:** Uniswap's core contracts execute token swaps, track reserves, and emit logs — all visible and tamper-proof on Ethereum, auditable by anyone.

**Boundary:** "Immutable" does not mean behavior cannot change; proxy patterns like UUPS let developers swap the logic while keeping the same contract address.

---
<!-- Concept: Solidity -->

# Solidity

> The primary statically-typed language for writing Ethereum smart contracts; compiled by `solc` into EVM bytecode and a JSON ABI.

**Example:** OpenZeppelin's ERC-20 token implementation is written in Solidity and deployed across hundreds of projects on Ethereum and EVM-compatible chains.

**Boundary:** Solidity's runtime assumptions differ from general-purpose languages — integer overflow, gas limits, and lack of floating-point require careful design.

---
<!-- Concept: EVM (Ethereum Virtual Machine) -->

# EVM (Ethereum Virtual Machine)

> The sandboxed, deterministic runtime that executes smart contract bytecode identically on every Ethereum node; the same environment runs on EVM-compatible chains.

**Example:** A single `SSTORE` opcode writes to storage; every node executes it the same way, guaranteeing that all nodes reach the same consensus state.

**Boundary:** The EVM is not a general compute platform — it has no native support for randomness, external data, or async calls; these require oracles.

---
<!-- Concept: ABI (Application Binary Interface) -->

# ABI (Application Binary Interface)

> A JSON specification describing a contract's public interface: function signatures, parameter and return types, and emitted events; required to encode calls and decode responses.

**Example:** An ERC-20 ABI specifies `transfer(address, uint256)` and `Transfer(address, address, uint256)` event, so any wallet can interact with any token uniformly.

**Boundary:** The ABI is not the contract itself — it is interface metadata; the actual contract logic can behave differently than the ABI suggests if code is poorly written.

---
<!-- Concept: Contract Event -->

# Contract Event

> A log entry emitted during contract execution, stored in the transaction receipt (not contract storage), enabling off-chain systems to observe state changes without reading storage.

**Example:** A token transfer emits `Transfer(from, to, amount)`, which an indexer listens to and records in a database for instant UI updates without scanning all state.

**Boundary:** Events are not searchable directly on-chain — indexers like The Graph listen and store them; contract logic cannot read its own emitted events.

---
<!-- Concept: Contract Upgrade -->

# Contract Upgrade

> Proxy patterns (transparent, UUPS, beacon) that allow replacing a contract's logic while preserving its address, storage, and on-chain state.

**Example:** A DeFi project deploys a logic contract, then points a proxy at it; months later they deploy bug-fixed logic and update the proxy pointer — users keep the same address.

**Boundary:** Upgradeable contracts introduce a trust assumption — the upgrade admin key controls all future behavior; a single compromised key = full protocol takeover.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 🛠️ Dev Stack

---
<!-- Concept: Web3 Dev Stack -->

# Web3 Dev Stack

> Layered toolchain for building, testing, and deploying smart contracts and dApp frontends: Remix → Hardhat/Foundry → OpenZeppelin → viem/wagmi.

**Example:** Prototype a token in Remix, graduate to Hardhat with Chai tests, import OpenZeppelin's ERC-20 for production-grade code, then connect a React frontend using wagmi hooks.

**Boundary:** Each tool serves a specific phase — using Remix for production deployments or viem for smart contract logic inverts the stack's intent.

---
<!-- Concept: Remix IDE -->

# Remix IDE

> Browser-based Solidity development environment requiring zero local setup; deploy to a JavaScript VM or MetaMask-connected testnet directly from the browser.

**Example:** Write a Solidity contract at remix.ethereum.org, hit compile, deploy to Sepolia testnet by connecting MetaMask — no CLI or node_modules required.

**Boundary:** Remix is for rapid prototyping and learning, not multi-file production projects or CI/CD pipelines; graduate to Hardhat or Foundry for engineering work.

---
<!-- Concept: Hardhat -->

# Hardhat

> Node.js development environment for Ethereum: compile, test with Chai/Mocha, run a local Hardhat Network, and deploy contracts with TypeScript scripts.

**Example:** `npx hardhat compile` builds your contracts; `npx hardhat test` runs Chai unit tests against a local in-memory EVM; `npx hardhat run scripts/deploy.ts` deploys to Sepolia.

**Boundary:** Hardhat's JavaScript-first design is accessible but slower than Rust alternatives like Foundry for large test suites with thousands of cases.

---
<!-- Concept: Foundry -->

# Foundry

> Rust-based dev framework with Forge (Solidity tests + fuzzing), Cast (CLI chain interaction), Anvil (local EVM node), and Chisel (REPL); dramatically faster than Node.js alternatives.

**Example:** Write fuzz tests in Solidity with `forge test --fuzz-runs 10000`, query mainnet with `cast call`, spin up a forked local chain with `anvil --fork-url $RPC`.

**Boundary:** Foundry requires Rust, has steeper learning curve for Node.js developers; its speed advantage matters most for large test suites and security research workflows.

---
<!-- Concept: OpenZeppelin Contracts -->

# OpenZeppelin Contracts

> Audited, battle-tested Solidity library providing ERC-20, ERC-721, AccessControl, ReentrancyGuard, and upgradeable proxy base contracts.

**Example:** Inherit from `ERC20` to build a standard token in three lines; use `Ownable` and `AccessControl` to govern permissions without writing security-critical code from scratch.

**Boundary:** Using OpenZeppelin does not guarantee contract security — custom logic built on top still requires auditing; OZ libraries are a floor, not a ceiling.

---
<!-- Concept: viem / wagmi -->

# viem / wagmi

> viem: TypeScript library for low-level EVM interaction; wagmi: React hooks over viem for dApp frontends; the modern, tree-shakeable replacement for ethers.js.

**Example:** Use viem's `publicClient.readContract()` to fetch a token balance, or wagmi's `useReadContract()` hook in React to auto-update the UI on every block.

**Boundary:** wagmi binds viem to React — non-React projects should use viem directly; viem is transport-agnostic (HTTP, WebSocket, IPC).

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 🌐 Network

---
<!-- Concept: Blockchain Network -->

# Blockchain Network

> A permissionless peer-to-peer system where nodes independently verify and agree on a single canonical sequence of blocks via consensus, enabling trustless distributed state.

**Example:** Ethereum mainnet: thousands of independent nodes worldwide validate every transaction and block, reaching agreement without a central authority.

**Boundary:** Permissionless does not mean uncontrolled — nodes enforce strict protocol rules; anyone can join but must follow the consensus rules exactly.

---
<!-- Concept: Block -->

# Block

> A batched collection of transactions with a cryptographic header (parent hash, timestamp, proposer, state root, tx root) linking it to the previous block in the chain.

**Example:** Ethereum block 21,000,000 contains ~150 transactions, is produced every ~12 seconds, and its header includes the Keccak-256 hash of the previous block.

**Boundary:** A block is not final until enough subsequent blocks are added — reorgs can happen within a short window; on Ethereum PoS, true finality takes ~13 minutes (2 epochs).

---
<!-- Concept: Consensus -->

# Consensus

> The mechanism by which distributed, untrusting nodes reach agreement on which transactions happened and in what order, preventing double-spend and ensuring a single canonical chain.

**Example:** Ethereum validators propose, attest to, and finalize blocks; if the majority signs a block, it becomes canonical and dissenting nodes resync to that truth.

**Boundary:** Consensus guarantees *safety* (finalized history won't revert) but not *liveness* — the chain can stall if too many validators go offline simultaneously.

---
<!-- Concept: Proof of Stake (PoS) -->

# Proof of Stake (PoS)

> Ethereum's consensus since The Merge (Sept 2022): validators deposit 32 ETH, are randomly selected to propose blocks, and are slashed for misbehavior or double-signing.

**Example:** A validator stakes 32 ETH, earns ~3–4% annual yield by proposing blocks and attesting, but risks losing their entire stake if they equivocate (sign two conflicting blocks).

**Boundary:** PoS ties economic security to token holdings; it does not eliminate a wealthy attacker accumulating 51% of stake — the cost is now enormous, but not impossible.

---
<!-- Concept: Testnet -->

# Testnet

> A parallel blockchain network with the same protocol as mainnet but using valueless test tokens; designed for developers to safely experiment before paying mainnet gas.

**Example:** Sepolia is Ethereum's primary testnet — deploy contracts, run integration tests, and simulate scenarios there before mainnet; test ETH is free from faucets.

**Boundary:** Testnet behavior can diverge from mainnet in load patterns, MEV, and edge cases; a contract passing all Sepolia tests may still surface issues on mainnet under real conditions.

---
<!-- Concept: Layer 2 (L2) -->

# Layer 2 (L2)

> A scaling solution that executes transactions off the main chain but posts commitments and proofs to L1, inheriting its security while reducing gas costs 10–100x.

**Example:** Arbitrum and Optimism process user transactions on their sequencers, then post compressed bundles to Ethereum mainnet; users save $10–20 per transaction vs. L1.

**Boundary:** L2 security depends on L1 and the L2 bridge contract code — a critical bridge bug could drain user funds even though Ethereum itself is secure.

---
<!-- Concept: Rollup -->

# Rollup

> The dominant L2 architecture: a sequencer executes transactions in an EVM, batches them, posts compressed data plus a validity proof to Ethereum L1.

**Example:** Optimism processes 4,000+ TPS, batches transactions hourly, compresses data ~10x, and posts proofs to Ethereum — users get fast finality at a fraction of L1 cost.

**Boundary:** Rollups introduce a trusted sequencer risk — if the sequencer censors transactions, users must wait for force-include mechanisms; decentralized sequencers are still experimental.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 🔑 Account Abstraction

---
<!-- Concept: ERC-4337 (Account Abstraction) -->

# ERC-4337 (Account Abstraction)

> Ethereum standard enabling programmable smart account wallets via a UserOperation mempool and EntryPoint contract, without changes to the base protocol.

**Example:** Safe implements ERC-4337 modules enabling multisig approval, gas sponsorship, and session keys without modifying the Ethereum base layer.

**Boundary:** ERC-4337 does not replace EOAs — it adds an alternative path; most wallets still use EOA + smart contract, not pure smart accounts.

---
<!-- Concept: Smart Account -->

# Smart Account

> Contract-based wallet with programmable authorization: multisig, social recovery, passkeys, session keys, and gas sponsorship — unlike bare EOAs.

**Example:** A Safe multisig smart account requires 2-of-3 owner signatures for any transaction; no single key can drain the wallet unilaterally.

**Boundary:** Smart accounts cannot initiate transactions alone — they require a bundler (ERC-4337) or direct EOA caller; they are targets, not initiators.

---
<!-- Concept: Bundler -->

# Bundler

> Off-chain service collecting UserOperations from the ERC-4337 alt mempool, validating them, and submitting them as a single on-chain EntryPoint transaction.

**Example:** Pimlico Bundler aggregates 50 UserOperations into one `EntryPoint.handleOps()` call, amortizing base transaction costs across all users.

**Boundary:** Bundlers are not consensus-enforced — they are incentivized relayers; fee markets and MEV apply here just as with standard on-chain transactions.

---
<!-- Concept: Paymaster -->

# Paymaster

> ERC-4337 smart contract sponsoring gas fees on behalf of users or AI agents, enabling gasless UX or ERC-20 gas payment instead of ETH.

**Example:** Pimlico Paymaster sponsors gas during user onboarding; Stackup Paymaster accepts USDC instead of ETH for fees — the user never holds ETH.

**Boundary:** Paymasters must prepay or hold collateral in the EntryPoint to prevent griefing attacks — they are not free; someone bears the gas cost.

---
<!-- Concept: Session Key -->

# Session Key

> Limited-scope cryptographic key granted to AI agents or dApps with on-chain constraints: specific contracts, amount caps, and time bounds enforced by the smart account.

**Example:** Grant a Uniswap dApp a session key allowing only swaps up to $100 per transaction on that contract, expiring in 24 hours — no full key exposure.

**Boundary:** Session keys are enforced by smart account contract logic, not by key material itself; a compromised key cannot exceed the preset on-chain limits.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 💰 DeFi

---
<!-- Concept: DeFi (Decentralized Finance) -->

# DeFi (Decentralized Finance)

> An ecosystem of permissionless financial protocols on blockchains enabling lending, trading, yield generation, and stablecoins governed by smart contracts without intermediaries.

**Example:** Aave and Uniswap allow users to deposit ETH as collateral, borrow USDC, and swap tokens — all without KYC, bank account, or third-party approval.

**Boundary:** DeFi protocols are only as secure as their smart contract code — a bug can freeze or drain all user funds, and liquidations happen fast without warning.

---
<!-- Concept: ERC-20 Token -->

# ERC-20 Token

> Ethereum's standard fungible token interface: transfer, approve, allowance, balanceOf, totalSupply; enables uniform handling across wallets, DEXes, and lending protocols.

**Example:** USDC, DAI, and UNI are all ERC-20 tokens — you can send them to any Ethereum address and trade them on Uniswap using identical contract calls.

**Boundary:** ERC-20 does not enforce uniqueness or prevent token loss — if you send tokens to a contract that doesn't support them, they are permanently and irrecoverably lost.

---
<!-- Concept: AMM (Automated Market Maker) -->

# AMM (Automated Market Maker)

> A DEX that trades against a liquidity pool using a mathematical formula (x·y=k) instead of an order book; Uniswap pioneered this model on Ethereum.

**Example:** In a Uniswap ETH/USDC pool, swapping 10 ETH executes instantly against pool reserves — no counterparty needed; price set by the constant product formula.

**Boundary:** AMMs suffer slippage — larger trades move the price more; liquidity providers face impermanent loss if prices diverge from their deposit ratio.

---
<!-- Concept: DeFi Lending -->

# DeFi Lending

> Permissionless over-collateralized borrowing and lending governed by smart contracts (Aave, Compound); collateral value must exceed loan value; liquidation if health factor drops below 1.

**Example:** Deposit 2 ETH ($6,000) as collateral on Aave, borrow $4,000 USDC at 5% APY; if ETH drops to $2,000, your position gets liquidated automatically.

**Boundary:** Liquidation is not instantaneous — price volatility and network congestion can leave positions underwater before liquidators act; monitor health factor actively.

---
<!-- Concept: Stablecoin -->

# Stablecoin

> A cryptocurrency pegged to a reference value (usually USD): fiat-backed (USDC, USDT), crypto-collateralized (DAI), or algorithmic (FRAX); the primary DeFi unit of account.

**Example:** USDC is 1:1 backed by dollars in bank accounts; DAI is 150% collateralized by ETH and other crypto; both trade near $1 and are composable across DeFi protocols.

**Boundary:** Stablecoins can depeg under extreme stress or issuer insolvency; algorithmic stablecoins are most fragile — Terra/LUNA erased $40B in 2022 within days.

---
<!-- Concept: Liquidity -->

# Liquidity

> Capital deposited by liquidity providers into AMM pools or lending markets, enabling trading and borrowing; deeper liquidity means less price impact (lower slippage) per trade.

**Example:** Uniswap's ETH/USDC pool holds $500M in reserves — a $1M swap slips minimally; a $100M swap causes 10%+ price impact from shallow depth at that level.

**Boundary:** Liquidity can dry up during market crashes or when major LPs withdraw; concentrated liquidity (Uniswap v3) requires active management to avoid impermanent loss.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 🔮 Oracle

---
<!-- Concept: Oracle -->

# Oracle

> A system bridging off-chain data to on-chain smart contracts; blockchains cannot natively access external APIs, so oracles publish authenticated data contracts can read.

**Example:** Chainlink runs a decentralized node network fetching real-world asset prices, sports scores, and weather data and publishing them to contracts on Ethereum or Arbitrum.

**Boundary:** Oracles don't eliminate trust — they move it from a single API provider to the oracle network itself, which can still be compromised if nodes collude.

---
<!-- Concept: Price Feed -->

# Price Feed

> Oracle service publishing real-time asset prices on-chain by aggregating data from multiple independent nodes; updates on deviation threshold or heartbeat interval.

**Example:** Chainlink's ETH/USD feed collects prices from multiple exchanges, aggregates on-chain, and updates when price moves beyond 0.5% or after a 1-hour heartbeat.

**Boundary:** Even aggregated feeds can lag during extreme congestion; contracts relying on price feeds without freshness checks risk acting on stale prices.

---
<!-- Concept: Oracle Risk -->

# Oracle Risk

> Vulnerabilities from a contract's dependence on external oracle data: price manipulation, stale data, and centralization of the data source.

**Example:** A flash loan temporarily spikes an AMM's price; a lending protocol using that pool as its sole oracle allows over-borrowing or incorrect liquidations in the same transaction.

**Boundary:** Using multiple oracle providers or aggregation reduces but does not eliminate risk — synchronized market events or collusion can affect all sources simultaneously.

---
<!-- Concept: AI Oracle -->

# AI Oracle

> Emerging pattern where AI model outputs (predictions, classifications) are published verifiably on-chain via ZK proofs, TEEs, or oracle committees for contract use.

**Example:** An on-chain prediction market uses an AI oracle running inside an Intel SGX TEE; the TEE signs the inference result and posts a cryptographic attestation to a smart contract.

**Boundary:** AI oracle security depends on the integrity of the execution environment and model — adversarial inputs, model poisoning, or TEE compromise produce incorrect on-chain results.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 📊 Indexing

---
<!-- Concept: On-Chain Indexing -->

# On-Chain Indexing

> Extracting, transforming, and loading blockchain event data into queryable databases enables efficient aggregate queries that raw RPC calls cannot support.

**Example:** The Graph indexes Uniswap swap events, stores decoded token amounts and prices, then serves real-time pool analytics via GraphQL — no scanning millions of blocks.

**Boundary:** Indexers lag behind chain head by a few blocks; queries reflect indexed data, not real-time state; design systems to handle this latency.

---
<!-- Concept: Subgraph (The Graph) -->

# Subgraph (The Graph)

> A Graph Protocol indexing unit: manifest + AssemblyScript mappings that process contract events and expose a queryable GraphQL API over structured data.

**Example:** Aave's subgraph indexes Deposit and Repay events, maps them to User and LendingPool entities, and serves borrow rates and utilization via GraphQL.

**Boundary:** Subgraphs are chain-specific — a Uniswap subgraph on Ethereum differs from one on Arbitrum and must be deployed and maintained separately.

---
<!-- Concept: RPC (Remote Procedure Call) -->

# RPC (Remote Procedure Call)

> The JSON-RPC API exposed by Ethereum nodes for reading chain state and submitting transactions via methods like eth_call, eth_getLogs, and eth_sendRawTransaction.

**Example:** viem calls `eth_call` to read USDC.balanceOf(address) without modifying state; `eth_sendRawTransaction` broadcasts a signed swap transaction to the network.

**Boundary:** RPC is stateless and request-bound — a single call returns data at a specific block; historical range queries require archive nodes or an indexer like The Graph.

---
<!-- Concept: Data Pipeline -->

# Data Pipeline

> An Extract-Transform-Load process that reads raw blockchain events, decodes ABI-encoded data, and loads it into structured databases for analytics and AI agent context.

**Example:** Dune's pipeline extracts Uniswap V3 Swap events from logs, decodes token amounts and fees, and loads them into SQL tables queryable for volume analysis and ML training.

**Boundary:** Pipelines introduce latency — data freshness depends on block confirmation and indexer speed, typically 1–5 minutes behind real-time; design agents to handle stale context.

---

<!-- _class: lead -->
<!-- _paginate: false -->

# 🛡️ Security

---
<!-- Concept: Web3 Security -->

# Web3 Security

> Defensive practices for smart contracts: audits, static analysis, simulation, and monitoring; bugs in deployed contracts can be immediately and irreversibly exploited for financial gain.

**Example:** The Euler Finance hack (2023, $197M) was caught by on-chain monitoring within hours; Euler paused the protocol and recovered funds via negotiation — showing defense in depth works.

**Boundary:** Security is not a one-time audit event — it is a continuous practice spanning development (tests), deployment (audit), and production (monitoring, bug bounty).

---
<!-- Concept: Reentrancy -->

# Reentrancy

> A vulnerability where an external contract call re-enters the caller before its state is updated; The DAO hack (2016, $60M) is the canonical example.

**Example:** `withdraw()` sends ETH before updating balance → attacker's fallback re-calls `withdraw()` → balance never decrements → contract is drained recursively.

**Boundary:** Checks-Effects-Interactions pattern and OpenZeppelin's `ReentrancyGuard` prevent this — but "read-only reentrancy" in view functions used as price oracles is a newer, subtler variant.

---
<!-- Concept: Access Control -->

# Access Control

> Mechanisms restricting which addresses can call sensitive contract functions; OpenZeppelin's Ownable (single owner) and AccessControl (role-based) are standard implementations.

**Example:** A DeFi protocol uses `AccessControl` to separate MINTER_ROLE, PAUSER_ROLE, and UPGRADER_ROLE — each role can be held by a different multisig with independent signers.

**Boundary:** Access control is only as strong as the key securing the admin role — a single compromised owner key = full contract takeover; production contracts should use a Safe multisig.

---
<!-- Concept: Contract Audit -->

# Contract Audit

> Systematic security review of smart contract source code by expert researchers before mainnet deployment; standard gate for any protocol holding significant value.

**Example:** Trail of Bits or Code4rena competitive audits review Solidity source, test coverage, and deployment scripts; findings are categorized as Critical/High/Medium/Low/Informational.

**Boundary:** Audits reduce risk but cannot prove absence of all bugs — audited protocols (Euler, Compound, Curve) have still been exploited; audits are necessary but not sufficient.

---
<!-- Concept: Transaction Simulation -->

# Transaction Simulation

> Executing a transaction in a sandbox EVM (Anvil, Tenderly, mainnet fork) to preview gas cost, return values, state changes, and potential reverts before broadcasting.

**Example:** Tenderly simulates a complex DeFi strategy against mainnet state — showing exact token balance changes, gas cost, and revert reason — before the user signs anything.

**Boundary:** AI agents *must* simulate before signing; simulation against forked mainnet is realistic but may miss time-sensitive MEV or state changes that occur between simulation and execution.

---
<!-- Concept: On-Chain Monitoring -->

# On-Chain Monitoring

> Real-time observation of blockchain transactions to detect anomalous patterns after deployment; complements pre-deployment audits with post-deployment alerting.

**Example:** Forta bots monitor Aave for large withdrawal bursts, unusual liquidation volumes, or oracle price spikes; alerts trigger an OpenZeppelin Defender Autotask to pause the protocol.

**Boundary:** Monitoring catches anomalies after they happen — if an attack executes in one transaction, monitoring can alert but may not prevent the initial drain; combine with circuit breakers.

---

<!-- _class: lead -->
<!-- _paginate: false -->

## Sources

- **AI × Web3 School Handbook** · https://aiweb3.school/en/handbook/web3/
- **WCB Program Page** · https://web3career.build/en/programs/AI-Web3-School
- **Ethereum Docs** · https://ethereum.org/developers/docs/
- **OpenZeppelin Docs** · https://docs.openzeppelin.com/contracts
- **ERC-4337 Docs** · https://docs.erc4337.io/
- **The Graph Docs** · https://thegraph.com/docs/

---

<!-- _class: lead -->
<!-- _paginate: false -->

*Generated by AI × Web3 School Learning Agent (Sensei)*
*Wiki source: `knowledge-base/AIxWeb3/wiki/` · 55 concepts · 2026-05-25*
