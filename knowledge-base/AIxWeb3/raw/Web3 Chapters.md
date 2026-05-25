
### Cryptography | handbook | AI x Web3 School

* Date: 05/25/26 16:19
* Source: https://aiweb3.school/en/handbook/web3/cryptography/
* Tags: #

___

## Cryptography

> In Web3, "accounts," "signatures," "addresses," and "ownership" are all built on cryptography. You do not need to become a cryptography researcher first, but you must know which actions prove identity, which actions authorize assets, and which things cannot be recovered once lost.

## Why Learn This

Many Web3 beginners understand wallets as account systems, signatures as login confirmations, and addresses as usernames. This becomes dangerous later, because on-chain systems do not have centralized customer support or password recovery like the traditional internet.

Cryptography here is not abstract theory; it is the product boundary. Private keys control assets, signatures express authorization, hashes fix data, and Merkle Trees let large amounts of data be verified efficiently.

**Understanding basic cryptography is about knowing when you must not "click confirm."**

This section does not require you to derive elliptic-curve formulas. A more realistic goal is: when you see a wallet popup, signature request, transaction hash, Merkle proof, or contract verification, you can judge what it is proving.

## First Principles

> **On-chain identity is not issued to you by a platform; it is determined by whether you can prove control of a private key.**

Web3 account systems turn "who has permission" from a centralized database record into a verifiable mathematical relationship. The benefit is openness, composability, and no platform permission. The cost is that users and applications must take key and signature risks more explicitly.

-   **Private key is control**: losing the private key usually means losing control; leaking it means others gain control.
-   **Signature is authorization evidence**: signed content must be human-readable, not only an unreadable data string.
-   **Hash is commitment**: a hash cannot recover the original content, but it can verify whether data was changed.

## Concepts

### Hash

**Difficulty: Beginner.** First understand that a hash turns arbitrary data into a fixed-length fingerprint, used to verify whether data is consistent.

A hash function maps input data into a fixed-length output. Ideally, changing even one character in the input produces a completely different output. On-chain systems commonly use hashes to identify transactions, blocks, data commitments, and contract bytecode.

A hash is not encryption. It usually cannot be "decrypted back to the original text." Its purpose is identity and integrity verification. For example, when you receive contract source code, you can use a hash or compilation result to check whether it matches deployed on-chain code.

Common uses include:

-   Transaction hash: locate a transaction.
-   Block hash: locate a block.
-   Contract bytecode hash: check whether deployed code is consistent.
-   Data commitment: publish the hash first, then reveal the original content later so others can verify it was not changed.

### Public Key

**Difficulty: Beginner.** A public key can be public. It is used to derive addresses or verify signatures, but it is not your login password.

Public Key is public information paired with a private key. Others can use the public key to verify that a signature came from the corresponding private key, but they cannot derive the private key from the public key.

In Ethereum contexts, users usually see addresses rather than full public keys. An address can be understood as a shorter identifier derived from the public key. Addresses can be public; private keys must never be public.

An address is not identity itself. It is only an identifier for a verifiable control relationship. It is meaningless that an address "looks official"; what matters is whether it comes from a trusted source and matches contract docs, the official website, and explorer verification information.

### Private Key

**Difficulty: Beginner.** A private key is account control itself. Any action that exposes it to webpages, screenshots, logs, or chat tools is extremely dangerous.

Private Key is used to generate signatures and prove that you control an account. In the traditional internet, leaked passwords can often be recovered or reset. In Web3, once a private key leaks, attackers can directly move assets or authorize malicious contracts.

Wallets, seed phrases, hardware wallets, multisigs, and account abstraction are all solving the same core problem: how to make key control safer, more recoverable, and more suitable for real users.

Basic private-key management rules are simple:

-   Do not screenshot it.
-   Do not upload it to cloud drives.
-   Do not paste it into webpages.
-   Do not send it to AI tools or customer support.
-   Do not put it in code repositories or `.env.example`.
-   Do not use your main wallet to test unfamiliar dApps.

### Signature

**Difficulty: Intermediate.** A signature is not a "login popup"; it is authorization proof over a specific message or transaction.

A Signature is generated by using the private key over a message. Verifiers can use the public key or address to check whether the signature is valid, confirming that the authorization came from the corresponding account.

The easiest place for signatures to go wrong is that users cannot understand what they are signing. Products should show readable content whenever possible, such as signing purpose, domain, chain ID, contract address, amount, expiration time, and risk warning. For Agents, signatures need permission boundaries even more; the model should not be able to freely trigger high-risk authorization.

### Merkle Tree

**Difficulty: Intermediate.** A Merkle Tree uses hashes to organize large amounts of data so that you can verify one piece of data belongs to the whole set with only a small proof.

A Merkle Tree hashes many pieces of data layer by layer until it produces one root. As long as the root is recorded in a trusted place, a user can use a Merkle proof to prove "my data is in this batch" without downloading all data.

It is common in airdrop lists, light clients, state proofs, and verifiable data structures. Understanding Merkle Trees helps you understand why blockchains can organize large amounts of state into verifiable structures.

## Where It Fits in AI x Web3

If an AI Agent wants to explain transactions, judge authorization, generate on-chain actions, or help users manage permissions, it must understand signature and key boundaries. A model can explain that "this approval appears to approve a token allowance," but it cannot keep private keys for users, and it must not push signatures when users do not understand the content.

Further, AI output itself may need to be signed, hashed, or recorded as audit evidence: what advice an Agent gave under what input, whether the user confirmed it, and whether the execution result matched the advice.

## Minimum Practice

Do a signature observation exercise:

1.  Create a test wallet with no real assets.
2.  In a test environment, initiate a normal transfer or message signature.
3.  In the block explorer or wallet UI, observe the address, transaction hash, signature prompt, and chain ID.
4.  Write down which information can be public and which must never be public.
5.  Compare the difference between "signing a message" and "sending a transaction."

Do not use your main wallet for practice. Do not paste seed phrases or private keys into any webpage, chat tool, or code repository.

## Further Reading

-   [Ethereum: Cryptography](https://ethereum.org/en/developers/docs/cryptography/): understand hashes, public/private keys, and signatures from the Ethereum perspective.
-   [Ethereum Accounts](https://ethereum.org/en/developers/docs/accounts/): understand accounts, addresses, externally owned accounts, and contract accounts.
-   [Ethereum Transactions](https://ethereum.org/en/developers/docs/transactions/): continue with how signatures enter transaction structure.
-   [EIP-712](https://eips.ethereum.org/EIPS/eip-712): learn typed structured data signing and why readable signatures matter for user safety.

___


### Wallet | handbook | AI x Web3 School

* Date: 05/25/26 16:19
* Source: https://aiweb3.school/en/handbook/web3/wallet/#minimum-practice
* Tags: #

___

## Wallet

> A wallet is not Web3's "login button." It is the entry point where users manage accounts, sign authorizations, send transactions, switch networks, and confirm risks. Product quality often first shows up in whether wallet interactions are clear.

## Why Learn This

Web3 applications cannot avoid wallets. Users connect wallets, read addresses, sign messages, send transactions, approve tokens, and switch networks at the wallet boundary. Treating the wallet only as an SDK integration makes it easy to ignore safety and experience problems.

A successful wallet connection does not mean the user understands the next action. The real questions are: does the user know which chain they are on, which contract they are interacting with, which asset they authorized, how much gas they will pay, and whether recovery is possible after failure?

**The wallet is the final confirmation interface before user intent enters on-chain execution.**

In products, wallet interactions should at least distinguish three types of actions:

-   **Connect wallet**: the application reads address and network; this does not mean it can move assets.
-   **Sign message**: the user proves control of an address, possibly for login, authorization, or order creation.
-   **Send transaction**: the user requests a change to on-chain state, which may transfer funds, approve tokens, call contracts, or pay gas.

These three actions have completely different risks. Page copy, button states, and confirmation prompts should also be different.

## First Principles

> **A wallet manages on-chain control, not "account profile data."**

In traditional login systems, platforms can reset passwords, ban accounts, and recover state. In wallet systems, control comes from private keys or smart-account rules. Applications can request connection and signature, but should not assume they own the user's account.

-   **Connection is not asset authorization**: reading an address and initiating a transaction are two completely different permission layers.
-   **Signatures must be explainable**: users need to know the purpose of the signature, not only see hexadecimal data.
-   **Network is context**: the same address can have different assets and state on different chains.

## Concepts

### EOA

**Difficulty: Beginner.** First understand that the most common wallet account is an externally owned account controlled by a private key.

EOA means Externally Owned Account. It is controlled by a private key. It can sign messages, initiate transactions, pay gas, and call contracts. Most browser wallets and mobile wallets create this type of account for users by default.

EOAs are simple, general, and widely compatible with the ecosystem, but they have obvious limits: private-key loss is hard to recover from, permissions are hard to split, automation is weak, and user experience is often interrupted by gas, network switching, and signature popups.

### Mnemonic

**Difficulty: Beginner.** A mnemonic is a high-risk secret used to recover a wallet. It is not an ordinary verification code, and no application should ask for it.

A Mnemonic is usually a set of words used to recover private keys inside a wallet. It exists to make backup easier for users, but it also makes phishing attacks easier to disguise as "enter your seed phrase to recover your account."

Any webpage, support agent, AI Agent, form, or script asking you to input a mnemonic should be treated as dangerous by default. Real products should not ask users to hand seed phrases to the application.

Do not design flows like "enter mnemonic to connect wallet" in a product. The correct approach is to let users recover accounts inside the wallet application, then let the dApp request wallet connection.

### Transaction

**Difficulty: Intermediate.** A transaction is a formal request to change on-chain state. Once successfully included on-chain, it usually cannot be casually rolled back like a database record.

A Transaction can be a transfer or a contract method call. The wallet asks the user to confirm transaction content, chain, contract address, gas, and possible asset changes. The application should explain this information as clearly as possible.

A common misunderstanding is treating "clicking a button" as the transaction itself. In reality, the button only initiates a request; the transaction still goes through wallet confirmation, signing, broadcasting, inclusion, and execution. Every step can fail.

The frontend should at least display or handle these states:

-   waiting for the user to confirm in the wallet
-   user rejected signature
-   transaction broadcasted, waiting for block confirmation
-   transaction succeeded
-   transaction failed or reverted
-   transaction pending for too long, requiring retry or explorer guidance

### Gas

**Difficulty: Beginner.** Gas is the cost of on-chain execution. It affects both user payment and whether the transaction can be processed in time.

Gas pays for network execution and storage resources. Users usually pay gas fees when sending transactions. If gas estimation is wrong, the network is congested, or balance is insufficient, a transaction may fail or get stuck.

Products should not only show "confirm transaction." They should tell the user roughly how much it costs, which asset pays the fee, whether fees may still be consumed on failure, and whether retry is possible.

### Explorer

**Difficulty: Beginner.** A block explorer is the window through which users and developers view on-chain facts, but it is not the chain itself.

Explorers can show addresses, transactions, contracts, events, token transfers, and execution state. For users, they confirm whether a transaction succeeded; for developers, they help debug failures, verify contracts, and trace state.

If an AI product cites on-chain information, it should ideally provide an explorer link or transaction hash so users can verify it themselves instead of only trusting the model summary.

When reading a transaction, check at least:

-   Status: success or failure.
-   From / To: who initiated it and which address was called.
-   Method: which contract method was called.
-   Value: whether native asset was transferred directly.
-   Token Transfers: whether token transfers happened.
-   Logs: which events the contract emitted.
-   Gas Used: how much gas was actually consumed.

## Where It Fits in AI x Web3

When an AI Agent wants to enter on-chain execution, it eventually hits the wallet boundary. It can help explain transactions, prepare parameters, check risks, and generate operation plans, but signatures and permissions cannot be casually handed to the model.

A more reasonable design is: AI handles understanding and assistance, the wallet handles confirmation and authorization, and a policy contract or smart account enforces execution constraints. This gives users AI efficiency while preserving control over assets and permissions.

## Minimum Practice

Create a wallet-interaction map:

1.  Use a test wallet to connect to a testnet dApp.
2.  Record the full flow: connect wallet, switch network, sign message, send transaction, view explorer.
3.  Mark which actions only read information and which actions change on-chain state.
4.  Write the key information the user should see at each step.
5.  Consider which actions must retain human confirmation if assisted by an AI Agent.

## Further Reading

-   [MetaMask Wallet Docs](https://docs.metamask.io/wallet/): learn developer interfaces for wallet connection, accounts, signatures, and transaction requests.
-   [Ethereum Accounts](https://ethereum.org/en/developers/docs/accounts/): understand the basic difference between EOAs and contract accounts.
-   [Ethereum Transactions](https://ethereum.org/en/developers/docs/transactions/): learn transaction structure, signatures, and execution flow.
-   [WalletConnect Docs](https://docs.walletconnect.network/): understand cross-wallet connections and session management.
-   [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193): an important interface standard for wallet Provider APIs.

___


### Smart Contract | handbook | AI x Web3 School

* Date: 05/25/26 16:20
* Source: https://aiweb3.school/en/handbook/web3/smart-contract/#minimum-practice
* Tags: #

___

## Smart Contract

> A smart contract is not a "legal contract that executes automatically." It is a program deployed on-chain. It puts rules, assets, and state into a publicly verifiable execution environment, and also exposes bugs, permissions, and upgrade risks to everyone.

## Why Learn This

Many core Web3 product logics live in smart contracts: tokens, NFTs, DEXs, lending, governance, staking, airdrops, and account abstraction. Frontends can be replaced, backends can be refactored, but once a contract is deployed, modification cost and risk are usually much higher than ordinary application code.

Learning smart contracts is not about immediately writing complex protocols. It is about building judgment first: which rules belong on-chain, how contracts store state, how calls change state, how interfaces can be composed by other applications, and why testing and audits cannot be skipped.

**Smart contracts turn rules into public infrastructure, and bugs into public risk.**

A tiny example is enough to start: a counter contract stores one `count`. Anyone calls `increment()`, and `count` increases by one. Although simple, this already contains the core ideas: state variables, external calls, transaction execution, gas cost, event logs, and block-explorer visibility.

Real protocols simply scale this model up: balances, collateral, loans, orders, votes, permissions, and upgrade information are all more complex on-chain state.

## First Principles

> **A contract's value comes from verifiable execution, not from code that "looks clever."**

Smart contracts let anyone inspect rules, call interfaces, and verify state changes. This openness brings composability, but also attack surface. You are not writing ordinary functions; you are writing programs that manage real assets and public state.

-   **State is publicly inspectable**: on-chain state is not a private database field; much of it can be seen by everyone.
-   **Calls have cost and order**: every execution is affected by gas, block ordering, and external state.
-   **Permissions must be explicit**: who can mint, pause, upgrade, or withdraw cannot rely on default trust.

## Concepts

### Solidity

**Difficulty: Beginner.** Solidity is the most common contract language in the EVM ecosystem. Use it first to understand how on-chain programs are written and constrained.

Solidity looks like an ordinary programming language, but it runs in a completely different environment. Contract state is written on-chain, function calls may consume gas, and permission mistakes can directly affect asset safety.

When learning Solidity, do not only look at syntax. More important are chain-specific concepts such as storage, `msg.sender`, modifiers, events, external calls, revert, and access control.

A minimal contract looks like this:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Counter {
    uint256 public count;

    event CountChanged(uint256 newCount);

    function increment() external {
        count += 1;
        emit CountChanged(count);
    }
}
```

Here, `count` is on-chain state, `increment()` is a write operation that changes state, and `event` is a log external systems can index. A frontend can read `count()` without user signature, but calling `increment()` usually requires wallet signature and gas payment.

### EVM

**Difficulty: Intermediate.** The EVM is the contract execution environment. It determines how code is deployed, called, charged, and isolated.

EVM means Ethereum Virtual Machine. Solidity code is compiled into EVM bytecode, deployed on-chain, and executed by nodes.

Understanding the EVM helps explain many phenomena: why gas exists, why storage is expensive, why external calls are risky, and why the same contract can be deployed to many EVM-compatible chains.

### ABI

**Difficulty: Beginner.** ABI is the interface description between applications and contracts. Without ABI, frontends and tools cannot easily call contracts correctly.

ABI means Application Binary Interface. It describes a contract's functions, parameters, return values, and events. Frontend SDKs, scripts, block explorers, and AI tools can use ABI to understand how to encode calldata and decode results.

For AI x Web3, ABI is also important context for Agents to understand contract capabilities. But ABI only tells you "what can be called"; it does not guarantee "whether calling it is safe."

For example, if a contract has `transfer(address to, uint256 amount)`, the ABI tells tools that the function needs an address and a number. It does not automatically tell you:

-   whether `to` is a malicious address;
-   whether `amount` should be an integer scaled by token decimals;
-   whether this call will trigger an external contract;
-   whether the current account has enough balance or allowance;
-   whether the function is paused or permission-restricted.

So ABI is a machine-readable interface, not a safety manual.

### Event

**Difficulty: Beginner.** Events are indexable logs that contracts leave for external systems. They are important data sources for frontends, indexers, and analytics tools.

Contracts can emit events during execution. Events do not become contract-readable state like storage, but they are very suitable for external systems to track what happened, such as transfers, order creation, parameter updates, and permission changes.

Many product pages do not scan contract storage every time. They build a query-friendly data layer by indexing events.

For example, an NFT marketplace may emit:

-   `OrderCreated`
-   `OrderCancelled`
-   `OrderFilled`

Frontend order lists, user histories, and dashboards often do not read all orders one by one from the contract. They build query databases by indexing these events.

### Upgrade

**Difficulty: Advanced.** Contract upgrades are a tradeoff between safety, governance, and product iteration. They cannot be treated only as a switch for "fixing bugs later."

Some contracts are immutable after deployment; some retain upgrade capability through proxies, governance, or multisigs. Immutability is closer to "fixed rules," but bug fixes are hard. Upgradeability is more flexible, but introduces admin permission, governance attack, and user-trust issues.

Product documentation should clearly state whether a contract is upgradeable, who holds upgrade permission, whether there is a timelock, and how users can monitor changes.

To judge upgrade risk, ask four questions directly:

-   Who holds upgrade permission: a single EOA, multisig, DAO, or timelock contract?
-   Can users see the upgrade proposal and new implementation address in advance?
-   Can an upgrade change asset transfer, withdrawal, pause, or permission logic?
-   If an admin key leaks, what is the worst outcome?

If a protocol says "the contract has been audited" but does not explain upgrade permissions, the security statement is still incomplete.

## How a Call Happens

Take "user clicks the vote button" as an example. The full chain usually is:

1.  The frontend reads the wallet address and current network.
2.  The frontend encodes `vote(proposalId)` calldata using ABI.
3.  The wallet shows transaction information and asks the user to confirm signing.
4.  The transaction is broadcast to an RPC node.
5.  Validators include the transaction in a block.
6.  The EVM executes contract logic; success updates state and emits events, failure reverts.
7.  The frontend watches the transaction receipt and updates page state.
8.  The indexer reads events and updates history or dashboards.

This is why smart-contract development cannot focus only on Solidity files. You need to understand wallets, RPC, block explorers, frontend SDKs, events, and indexing layers at the same time.

## Common Mistakes

-   **Mixing `view` functions with write transactions**: reading state does not require signature; changing state usually requires a transaction.
-   **Not handling decimals**: a token `amount` is usually not the human-visible "1.5"; it is an integer scaled by decimals.
-   **Testing only the success path**: permission failure, insufficient balance, repeated calls, expiration, and paused state all need tests.
-   **Treating owner as always trustworthy**: when owner permission is too broad, users are really trusting the admin.
-   **Ignoring event design**: without events, frontend history, indexing, and audits become much harder later.

## Where It Fits in AI x Web3

When AI Agents enter on-chain execution, smart contracts should carry final rules and constraints instead of handing all judgment to the model. A model can help users understand ABI, generate call parameters, explain transaction results, and write test cases, but contracts enforce execution boundaries.

A steady design is usually: AI gives suggestions and orchestration, the wallet confirms authorization, the contract performs verifiable execution, and monitoring records results. Even if AI output is unstable, the on-chain rules still have clear boundaries.

## Minimum Practice

Do a minimal contract-reading exercise:

1.  Find a simple ERC-20 or NFT contract with verified source code.
2.  In a block explorer, view source code, ABI, events, and recent transactions.
3.  Identify which functions change state and which only read state.
4.  Identify permission functions, such as owner, admin, pause, mint, burn, upgrade.
5.  Identify the most important event and explain which type of user action it corresponds to.
6.  Explain in one sentence: what is the most important risk boundary of this contract?

## Further Reading

-   [Solidity Documentation](https://docs.soliditylang.org/): learn the Solidity language, types, contract structure, and security notes.
-   [Ethereum Smart Contracts](https://ethereum.org/en/developers/docs/smart-contracts/): understand basic smart-contract concepts from Ethereum developer docs.
-   [Ethereum Virtual Machine](https://ethereum.org/en/developers/docs/evm/): understand how the EVM executes contract code.
-   [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/): learn common secure contract libraries and standard implementations.
-   [OpenZeppelin Upgrades](https://docs.openzeppelin.com/upgrades-plugins/): understand proxy upgrade patterns and related risks.

___


### Dev Stack | handbook | AI x Web3 School

* Date: 05/25/26 16:20
* Source: https://aiweb3.school/en/handbook/web3/dev-stack/#minimum-practice
* Tags: #

___

## Dev Stack

> The Web3 dev stack is not a random list of tool names. It is an engineering chain from writing contracts, testing contracts, deploying contracts, connecting wallets, calling contracts, and monitoring results. Tool choice should make on-chain development more verifiable, reproducible, and less accident-prone.

## Why Learn This

Writing a Web3 demo is easy: connect a wallet, call a contract, send a transaction. But once you build a real project, you immediately meet contract compilation, tests, deployment scripts, environment variables, RPC, frontend SDKs, chain switching, contract verification, permission management, and monitoring.

The purpose of the dev stack is not to collect more tools. It is to turn development into a repeatable system. A project should at least be runnable locally, reproducible in tests, recorded in deployment, explicit in frontend calls, and traceable in contract addresses.

**The clearer the toolchain, the more controllable on-chain execution becomes.**

You can split a minimal development chain into six steps:

1.  Write the contract locally or in a browser IDE.
2.  Compile the contract to get bytecode and ABI.
3.  Deploy the contract to a local chain or testnet.
4.  Write tests for core state changes and permission boundaries.
5.  Use contract address and ABI in the frontend to read or send transactions.
6.  Verify source code, transactions, and events in a block explorer.

If any step is missing, it becomes debugging cost later. For example, a wrong ABI in the frontend causes parameter encoding errors; deployment addresses without version records make it unclear which contract users are interacting with; tests that only cover the happy path easily miss permissions and failure branches.

## First Principles

> **The core of a Web3 toolchain is to move irreversible execution into testable, simulatable, and reviewable processes before it happens.**

Once an on-chain transaction succeeds, regret is expensive. Development tools should expose errors as early as possible in local environments, testnets, simulations, and code review, rather than after mainnet launch.

-   **Reproduce locally first**: contract logic, deployment scripts, and frontend calls should all run locally or on testnets.
-   **Version addresses and ABI**: the exact contract the frontend calls must be traceable.
-   **Security libraries are not audits**: OpenZeppelin and similar libraries reduce basic risk, but composition logic still needs your own verification.

## Concepts

### Remix

**Difficulty: Beginner.** Remix is useful for quickly understanding Solidity, deploying small contracts, and observing contract-call flows.

Remix is a Solidity IDE in the browser. It can write, compile, deploy, and debug contracts, making it suitable for onboarding, teaching, prototyping, and quick verification.

Its advantage is low setup cost; you do not need a full engineering project first. But real projects still need Git, test frameworks, deployment scripts, and CI, otherwise collaboration and reproduction become difficult.

You can treat Remix as a "contract lab." It is best for:

-   quickly pasting Solidity code and checking whether it compiles
-   deploying contracts in JavaScript VM or testnets and observing constructors, calls, and events
-   using Deploy & Run to understand the difference between `read` and `write` calls

Remix is not a long-term replacement for an engineered repo. Once a project enters multi-person collaboration, contracts should move into a Git repository, with tests and deployment flows fixed through Hardhat or Foundry.

### Hardhat

**Difficulty: Intermediate.** Hardhat fits JavaScript/TypeScript projects and connects contract development with tests, scripts, and frontend engineering.

Hardhat provides a local development network, compilation, testing, deployment scripts, and a plugin ecosystem. For frontend teams, it fits naturally with TypeScript, ethers, and CI.

The point of learning Hardhat is not memorizing commands. It is understanding how local chain, testnet, deployment scripts, contract verification, and environment variables form a complete development flow.

Hardhat is more like a "contract engineering framework." A typical repo includes:

-   `contracts/`: Solidity source code.
-   `test/`: TypeScript or Solidity tests.
-   `ignition/` or `scripts/`: deployment modules and scripts.
-   `hardhat.config.ts`: networks, compiler, plugins, and variable configuration.
-   `artifacts/`: generated ABI, bytecode, and metadata.

If your project needs tight collaboration with frontend, backend, and CI, Hardhat usually makes the flow easier to stabilize than Remix alone.

### Foundry

**Difficulty: Intermediate.** Foundry leans toward command line and Solidity-native testing, and is suited for intensive contract development and fast feedback.

Common Foundry tools include `forge`, `cast`, and `anvil`. It can write tests in Solidity, runs fast, and is useful for fuzz testing, script deployment, and on-chain state interaction.

If you care more about contract logic, test depth, and command-line workflow, Foundry is a very important tool.

Common Foundry entry points:

-   `forge test`: run contract tests.
-   `forge build`: compile contracts.
-   `anvil`: start a local test chain.
-   `cast call`: read on-chain contracts.
-   `cast send`: send transaction calls to contracts.

It is especially good for training the habit of "write tests first, then change contracts." For safety-sensitive contracts, quickly running unit tests, fuzz tests, and fork tests is more reliable than clicking through a UI a few times.

### OpenZeppelin

**Difficulty: Intermediate.** OpenZeppelin provides common contract standards and safety components, but does not replace review of business logic.

OpenZeppelin Contracts includes common modules such as ERC-20, ERC-721, AccessControl, Ownable, and Pausable. Mature libraries reduce duplicated work and avoid many basic implementation mistakes.

The danger is the illusion that "using a library means safe." Permission composition, upgrade patterns, parameter settings, external calls, and economic design can still fail.

A common example: you can use OpenZeppelin's ERC-20 implementation for a token, but you still decide who can mint, whether it can pause, whether ownership can transfer, and whether upgrade permissions have a timelock. These are product decisions the library does not make for you.

Related Topic

-   [Smart Contract](https://aiweb3.school/en/handbook/web3/smart-contract/): first understand contract state, ABI, events, and upgrade risk.
-   [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/): official contract library docs for ERC implementations, AccessControl, Ownable, Pausable, and other modules.
-   [OpenZeppelin Upgrades](https://docs.openzeppelin.com/upgrades-plugins/): understand proxy upgrade flows and upgrade-risk boundaries.

### viem / wagmi

**Difficulty: Intermediate.** viem and wagmi mainly solve frontend-chain interaction: reading contracts, writing contracts, managing accounts, handling networks, and caching.

viem is a TypeScript Ethereum interface library focused on type safety and low-level call capability. wagmi targets React applications and provides wallet connection, account state, contract reads/writes, and hooks.

When frontends connect to chains, the easiest issue is inconsistent state: wallet network, frontend config, contract address, RPC return values, and transaction pending state can all drift. Good SDKs reduce complexity, but they cannot design user flow for you.

In the frontend, separate at least four kinds of state:

-   whether the wallet is connected
-   which chain the user is currently on
-   whether contract-read results are loading or stale
-   whether a write transaction is waiting for signature, broadcasted, waiting for confirmation, succeeded, or failed

If these states are mixed into one button, users cannot tell whether they are "connecting wallet," "signing authorization," or "waiting for the transaction to land."

## How a Concrete Toolchain Fits Together

Suppose you want to build a minimal voting contract. You can combine tools like this:

1.  Write the first version of `Voting.sol` in Remix to confirm syntax and basic call flow.
2.  Move the contract into a Hardhat or Foundry repo.
3.  Write tests for creating votes, duplicate voting, vote ending, and non-admin operation failure.
4.  Deploy to a local chain and record address and ABI.
5.  Use viem or wagmi in the frontend: read candidates, initiate voting transaction, show pending and confirmed states.
6.  After deploying to a testnet, verify source code in a block explorer and check whether events can be queried correctly.

This flow looks slower than "write a page and call the contract directly," but it exposes errors earlier. The time-consuming part of Web3 projects is often not writing the first version, but discovering after launch that the contract address is wrong, ABI does not match, permissions were not tested, or transaction states were not handled.

## Where It Fits in AI x Web3

AI can significantly improve Web3 development efficiency: explaining ABI, generating deployment scripts, adding tests, debugging failed transactions, and summarizing contract permissions. But once AI enters the dev stack, verification flow needs to be even clearer.

If an Agent can run `forge test`, read deployment config, call `cast`, or generate frontend contract-call code, it must be constrained by repo workflow, tests, permissions, and secret management. On-chain development is not ordinary code generation; high-risk commands require human confirmation.

## Minimum Practice

Build a minimal Web3 development chain:

1.  Use Remix to deploy a tiny counter contract containing `count()`, `increment()`, and a `CountChanged` event.
2.  Create a local project with Hardhat or Foundry, and write tests for initial value and state change after `increment()`.
3.  Record contract address, ABI, deployment network, deployer account, and transaction hash.
4.  Use viem or wagmi to read `count()` from the frontend, then initiate one `increment()` transaction.
5.  Confirm in a block explorer or local logs that the event was emitted correctly.
6.  Write down which information in this chain must enter version control, and which must stay in `.env` or secret management.

## Further Reading

-   [Remix Documentation](https://remix-ide.readthedocs.io/): a browser-IDE entry point for Solidity compilation, deployment, and debugging.
-   [Hardhat Documentation](https://hardhat.org/docs): learn TypeScript/JavaScript contract development, testing, and deployment.
-   [Foundry Book](https://book.getfoundry.sh/): learn `forge`, `cast`, `anvil`, and Solidity-native testing workflows.
-   [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/): see common contract standards, safety components, and access-control modules.
-   [viem Documentation](https://viem.sh/): learn TypeScript-based chain reads, transaction sending, and contract calls.
-   [wagmi Documentation](https://wagmi.sh/): learn wallet connection, account state, and contract interaction in React applications.

___


### Network | handbook | AI x Web3 School

* Date: 05/25/26 16:21
* Source: https://aiweb3.school/en/handbook/web3/network/#minimum-practice
* Tags: #

___

## Network

> In Web3, a "network" is not abstract background. It is the base environment that determines whether transactions can be included, whether state can sync, how fees arise, how long confirmation takes, and how L2s and mainnet divide responsibilities.

## Why Learn This

Many Web3 problems look like frontend or wallet problems on the surface, but are actually network problems underneath: users switch to the wrong chain, RPC latency, pending transactions, insufficient testnet assets, L2 withdrawal waits, or inconsistent state between the block explorer and the frontend.

Understanding Network means knowing which layers a transaction passes through from wallet signature to final user visibility: wallet, RPC, mempool, block, consensus, execution, confirmation, indexing, and explorer.

**An on-chain application does not directly write a database. It submits requests to a public state machine that advances by blocks and is maintained by network consensus.**

## First Principles

> **The core of a blockchain network is not "storing data," but letting mutually distrusting participants agree on state changes.**

In ordinary applications, a server can directly update a database. In on-chain systems, transactions must be propagated, executed, included, verified, and confirmed by nodes. This process brings public verifiability, but also latency, fees, and finality issues.

-   **Blocks are the sync rhythm**: state does not update continuously every millisecond; it advances in batches by blocks.
-   **Consensus is the trust source**: users trust the state not because one company decides it, but because the network reaches agreement by rules.
-   **Network choice changes experience**: mainnet, testnets, and L2s differ in fees, speed, security assumptions, and tooling support.

## Concepts

### Block

**Difficulty: Beginner.** A block is the unit in which transactions are submitted and ordered in batches.

A block usually contains a transaction list, a reference to the previous block, state root, timestamp, gas usage, and consensus-related information. After transactions enter a block, nodes execute them and update global state.

When looking at blocks, the point is not to memorize fields, but to understand three things:

-   Transactions have order, and order affects results.
-   Blocks have gas limits, so network throughput is not unlimited.
-   New blocks reference previous blocks, forming verifiable history.

### Consensus

**Difficulty: Intermediate.** Consensus is the mechanism by which the network decides "which history is valid."

Different nodes receive transactions, blocks, and network messages. Consensus lets these nodes form a shared view of block order and state changes without a central database.

For application developers, consensus affects:

-   how many confirmations a transaction should wait before being considered safe
-   whether blocks may be briefly reorganized, meaning the frontend should not assume finality too early
-   whether state reads may be delayed when nodes fail or RPC behaves abnormally

### PoS

**Difficulty: Intermediate.** PoS uses staking and penalties to organize validators, replacing PoW mining to maintain network security.

Ethereum currently uses Proof of Stake. Validators stake ETH to participate in block proposal and attestation, and incorrect behavior can be penalized. Ordinary users do not necessarily need to run validators, but they should understand that network security is not "free"; it comes from economic stake, client implementations, and node participation.

PoS also explains why block time, finality, validators, staking, and slashing appear in network-layer discussions.

### Testnet

**Difficulty: Beginner.** Testnets are used to test contracts, frontends, and transaction flows in environments close to real chains.

Testnet assets have no real economic value, but they help you verify deployment scripts, wallet connections, RPC configuration, contract calls, explorer verification, and frontend state handling.

Testnets cannot replace mainnet security review. The reason is simple: testnet liquidity, MEV, attack incentives, asset scale, and user behavior are all different. Testnets are suitable for testing processes, not proving that economic mechanisms are safe.

When building a project, record at least:

-   which testnet it is deployed on
-   contract addresses and deployment transactions
-   which RPC is used
-   how the frontend switches chain id
-   where test assets come from

### L2

**Difficulty: Intermediate.** L2 is a network layer that balances mainnet security with lower cost.

Layer 2 usually executes many transactions outside mainnet, then submits results or proofs back to mainnet. For users, common L2 advantages are lower fees and faster confirmation; but they also introduce bridges, withdrawal delays, sequencers, and cross-chain state synchronization.

Product design cannot only say "supports Ethereum." If multiple L2s are supported, the product should clearly show the current network, which chain assets are on, how long bridging takes, and whether contract addresses differ.

### Rollup

**Difficulty: Advanced.** Rollup is the mainstream L2 scaling path. It moves execution off L1 or onto L2, then submits data and results to L1.

Common rollup types include optimistic rollups and zero-knowledge rollups. They differ in proof method, withdrawal delay, data availability, developer experience, and ecosystem tooling.

For builders, start with one judgment: rollups reduce per-transaction cost, but do not remove on-chain system complexity. You still need to handle cross-chain assets, RPC, explorers, contract addresses, bridge risks, and user confirmation.

## Where It Fits in AI x Web3

If an AI Agent needs to read on-chain state or execute transactions, it must know which network it is operating on. Mainnet and testnet, L1 and L2, different chain ids, and different contract addresses cannot be guessed by the model.

A safer approach is to have tools return structured network information: chain id, RPC source, block height, transaction hash, confirmation count, and explorer link. The Agent summary should cite these verifiable fields instead of only saying "the transaction succeeded."

## Minimum Practice

Track one testnet transaction:

1.  Claim a small amount of test ETH on a testnet.
2.  Use a test wallet to send a transfer or call a simple contract.
3.  Check transaction status, block number, gas used, from, to, and logs in a block explorer.
4.  Record how long the transaction takes from pending to confirmed.
5.  Switch to another network and observe whether the same address has different balance and transaction history.

After finishing, write down: if this flow were assisted by an AI Agent, which fields must be read by tools, and which descriptions can be generated by the model.

## Further Reading

-   [Ethereum Blocks](https://ethereum.org/en/developers/docs/blocks/): understand how blocks organize transactions and state changes.
-   [Ethereum Networks](https://ethereum.org/en/developers/docs/networks/): learn about mainnet, testnets, and network IDs.
-   [Ethereum Proof-of-Stake](https://ethereum.org/en/developers/docs/consensus-mechanisms/pos/): learn Ethereum's current consensus mechanism.
-   [Ethereum Layer 2](https://ethereum.org/en/layer-2/): understand L2 from user and developer perspectives.
-   [Ethereum Rollups](https://ethereum.org/en/developers/docs/scaling/#rollups): continue with why rollups are the mainstream scaling path.

___


### Account Abstraction | handbook | AI x Web3 School

* Date: 05/25/26 16:21
* Source: https://aiweb3.school/en/handbook/web3/account-abstraction/#minimum-practice
* Tags: #

___

## Account Abstraction

> Account Abstraction releases "how an account verifies operations, who pays gas, and which permissions can execute automatically" from the fixed EOA model, making wallets more like programmable account systems.

## Why Learn This

Ordinary EOA wallets have clear limits: users must manage private keys, must pay gas with the native token, signatures are coarse-grained, automation is hard, and recovery experience is unfriendly.

Account Abstraction tries to turn accounts into smart contracts so accounts can define their own verification logic and execution policies. This can support multisig, social recovery, gas sponsorship, session keys, spending limits, batched transactions, and finer-grained permissions.

**The core of account abstraction is not "gasless transactions," but expanding account control from a single private key into programmable rules.**

## First Principles

> **When the account itself is programmable, permission can move from "has private key / no private key" to "what action is allowed under what condition."**

This is especially important for AI x Web3. An Agent should not hold the user's main private key, and should not have unlimited transaction permission. A better approach is to give the Agent an action space that is limitable, expirable, revocable, and auditable.

-   **Verification logic is customizable**: accounts can verify operations with multisig, Passkeys, social recovery, or module rules.
-   **Payment logic is customizable**: gas can be paid by the user, the application, a paymaster, or another asset.
-   **Permissions can be minimized**: session keys can allow only specific contracts, amounts, time windows, and methods.

## Concepts

### ERC-4337

**Difficulty: Intermediate.** ERC-4337 is one of the most important account-abstraction standards in the Ethereum ecosystem. It uses an alt mempool and EntryPoint to implement smart-account transaction flow.

In ERC-4337, users do not directly send ordinary transactions. They create a `UserOperation`. Bundlers collect these operations and submit them to the on-chain EntryPoint contract. EntryPoint then calls the smart account's validation and execution logic.

A simplified flow:

1.  The user or application generates a `UserOperation`.
2.  The smart account validates signature, nonce, balance, or policy.
3.  The Bundler packages and submits the operation.
4.  EntryPoint calls the account to execute the target action.
5.  A Paymaster may sponsor gas.

### Smart Account

**Difficulty: Intermediate.** A Smart Account is an account controlled by a contract. It can put permissions, recovery, batched execution, and policies into account logic.

EOA validation logic is basically fixed: whoever has the private key can sign. A Smart Account can define:

-   large transfers require multiple signatures
-   small transactions can pass automatically
-   certain dApps can call within a limited allowance
-   lost wallets can be recovered through guardians or devices
-   transactions can be batched to reduce user confirmations

Risk also increases. The smart account itself is a contract, so contract bugs, module permissions, upgrade logic, and external dependencies all become account risks.

### Bundler

**Difficulty: Intermediate.** A Bundler collects `UserOperation`s, simulates validation, and submits them to EntryPoint.

In ERC-4337, a Bundler is similar to a transaction packaging service, but it handles `UserOperation`s rather than ordinary transactions directly sent by wallets. A Bundler needs to judge whether an operation is valid, whether it can pay gas, and whether it will fail during execution.

For applications, Bundler is an infrastructure dependency. If the Bundler is unstable, user operations may get stuck. If simulation is insufficient, failed operations cause experience and cost problems.

### Paymaster

**Difficulty: Intermediate.** Paymaster allows a third party to pay gas for user operations, or lets users bear fees with non-native assets.

Paymaster is often used for onboarding: new users without ETH can still complete their first operation. It can also be used for campaign subsidies, subscriptions, whitelisted transactions, or in-app gas abstraction.

But Paymaster is not free lunch. It needs risk control:

-   Which methods are sponsored?
-   What is each user's limit?
-   Are target contracts restricted?
-   How are spam and arbitrage prevented?
-   Who bears the cost of failed operations?

### Session Key

**Difficulty: Advanced.** A Session Key is temporary permission for an application or Agent, and should not be treated as the user's main private key.

A Session Key can be limited by time, contract, method, spending amount, and chain.

This is a key basis for Agent Wallets. You do not want an AI Agent to interrupt users for signatures every time, and you do not want it to have unlimited permissions. Session Keys provide a middle state: the Agent can automatically execute low-risk actions, while high-risk actions still require user confirmation.

## Where It Fits in AI x Web3

Account Abstraction is an important base for AI Agents executing on-chain. Without account abstraction, Agents often remain at "give suggestions" or "ask users to sign every step." With Smart Accounts, Paymasters, and Session Keys, Agents can execute automatically within a constrained scope.

But the more automated it becomes, the clearer the policy must be: what can be called, what the amount limit is, when it expires, who can revoke it, where logs are stored, and how failure is handled. Account abstraction does not make AI freer; it wraps AI freedom in rules.

## Minimum Practice

Design an Agent Session Key policy:

1.  Choose a concrete scenario, such as "rebalance a small amount of testnet assets at most once per hour."
2.  Specify allowed contract addresses and methods.
3.  Set amount limits, expiration time, chain ID, and maximum transaction count.
4.  Write which actions must return to the user's wallet for confirmation.
5.  Explain how to revoke the session key and audit what it executed.

The point is not to deploy a full AA wallet immediately, but to learn how to split permission from "allow everything" into verifiable rules.

## Further Reading

-   [EIP-4337](https://eips.ethereum.org/EIPS/eip-4337): the account-abstraction standard text.
-   [ERC-4337 Documentation](https://docs.erc4337.io/): understand EntryPoint, Bundler, Paymaster, and Smart Account from a developer perspective.
-   [Ethereum Account Abstraction](https://ethereum.org/en/roadmap/account-abstraction/): understand why account abstraction matters from the Ethereum roadmap perspective.
-   [Safe Smart Accounts](https://docs.safe.global/): learn how multisig and smart accounts are used in real projects.
-   [Rhinestone Smart Sessions](https://docs.rhinestone.dev/smart-wallet/smart-sessions/overview): learn session keys, permission policies, and modular smart-account design.

___


### Decentralized Finance（DeFi） | handbook | AI x Web3 School

* Date: 05/25/26 16:21
* Source: https://aiweb3.school/en/handbook/web3/defi/#minimum-practice
* Tags: #

___

## Decentralized Finance（DeFi）

> DeFi is an open financial system built on smart contracts. It lets assets, trading, lending, stablecoins, and liquidity be combined through protocols, and it also lets risk propagate along protocol dependency chains.

## Why Learn This

Many AI x Web3 projects touch DeFi: transaction interpretation, yield strategies, risk monitoring, liquidation alerts, automated rebalancing, asset management, and protocol data analysis. Even if you are not building a financial product, you need to understand basic concepts such as tokens, liquidity, prices, lending, and oracles.

The hard part of DeFi is not only "whether the contract can run," but how assets and mechanisms affect each other. A simple-looking swap may involve AMM curves, slippage, liquidity depth, fees, MEV, and price oracles.

**The core of DeFi is not "removing intermediaries," but turning financial rules into on-chain protocols that are composable, verifiable, and attackable.**

## First Principles

> **DeFi protocols manage asset state, not only application interfaces.**

In traditional finance, much state lives in institutional ledgers. DeFi puts balances, collateral, debt, liquidity, trading, and liquidation into contract systems. Transparency improves, but mechanism errors, price shocks, and external dependencies are exposed faster.

-   **Assets are protocol inputs**: token standards, decimals, approvals, and balances all affect protocol behavior.
-   **Liquidity determines executability**: having a price does not mean a trade can execute; executing does not mean it executes cheaply.
-   **Composability amplifies risk**: when one protocol breaks, many protocols depending on it may be affected.

## Concepts

### Token

**Difficulty: Beginner.** Token is the asset unit of DeFi, but different tokens vary greatly in standard, precision, permissions, and risk.

ERC-20 is the most common fungible token standard. User balances, transfers, approvals, trading, and lending usually revolve around tokens.

When looking at a token, do not only look at name and icon. Check at least:

-   whether the contract address is correct
-   what the decimals value is
-   total supply and issuance permission
-   whether it can be paused, frozen, minted, or upgraded
-   whether it has special transfer tax or blacklist logic

Wrong token addresses and decimals handling are very common risk sources in DeFi frontends and Agent tools.

### AMM

**Difficulty: Intermediate.** AMM replaces traditional order books with liquidity pools and pricing formulas, allowing users to trade directly with contracts.

In AMMs such as Uniswap, users deposit two assets into a pool, traders swap one asset for another, and price is determined by pool state and formula. The deeper the liquidity, the smaller the price impact for the same trade size in general.

Several key AMM concepts:

-   **Slippage**: the gap between expected price and actual execution price.
-   **Liquidity provider**: provides assets to the pool, earns fees, and bears impermanent loss.
-   **Price impact**: large trades change pool ratios and worsen execution price.
-   **MEV risk**: transaction ordering can be exploited, for example in sandwich attacks.

### Lending

**Difficulty: Intermediate.** Lending protocols put deposits, borrowing, collateral ratios, interest rates, and liquidation rules into contracts.

Users can deposit assets to earn interest, or collateralize assets to borrow another asset. Whether a loan can remain open depends on collateral value, debt value, liquidation threshold, and oracle prices.

Lending-protocol risk is often not a single point:

-   collateral price drops quickly
-   oracle price is delayed or abnormal
-   insufficient liquidity causes liquidation failure
-   parameters are set too aggressively
-   dependent assets depeg or contracts break

If AI gives lending suggestions, it must explain collateral ratio, health factor, liquidation price, and price source. It cannot only say "higher yield."

### Stablecoin

**Difficulty: Intermediate.** Stablecoins are the unit of account and settlement base in DeFi, but "stable" comes from different mechanisms and is not guaranteed by nature.

Common stablecoins may be backed by fiat reserves, over-collateralized crypto assets, algorithmic mechanisms, or hybrid structures. Their risks also differ: reserve transparency, redemption ability, collateral volatility, governance parameters, regulation, and liquidity all affect stability.

When looking at a stablecoin, ask:

-   What maintains the peg?
-   Who can issue and burn?
-   Where are reserves or collateral?
-   Who bears loss during depeg?
-   How deep is liquidity in major pools?

### Liquidity

**Difficulty: Beginner.** Liquidity determines whether assets can be bought, sold, borrowed, liquidated, or exited at reasonable prices.

In DeFi, if "price" is not backed by liquidity, it is only a number on the screen. A token marked at $1 does not mean you can sell a large position at $1.

Liquidity problems show up as:

-   swap slippage increases
-   lending liquidation becomes hard
-   oracle prices are easier to manipulate
-   LP withdrawals increase protocol risk
-   cross-protocol strategies cannot exit in time

## Where It Fits in AI x Web3

When AI enters DeFi, the safest starting point is information organization and risk assistance: explaining transactions, summarizing positions, monitoring liquidation, identifying abnormal prices, and drafting strategies. The truly high-risk part is automatic execution: swaps, lending, leverage, approvals, cross-chain actions, and liquidation.

If an Agent executes DeFi operations, it needs at least amount limits, protocol allowlists, slippage caps, simulation results, oracle checks, human confirmation, and post-transaction audit records.

## Minimum Practice

Break down one DeFi transaction:

1.  Choose a public swap transaction hash.
2.  In a block explorer, inspect input token, output token, route, slippage, and fee.
3.  Find the pool or router contract involved.
4.  Explain how much asset the user actually received and how it differed from the expected price.
5.  Write which limits must be set if an AI Agent executes similar trades.

## Further Reading

-   [Ethereum DeFi](https://ethereum.org/en/defi/): understand DeFi concepts and risks from a user perspective.
-   [ERC-20 Token Standard](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/): understand the basic interface of fungible tokens.
-   [Uniswap Docs](https://developers.uniswap.org/docs/get-started/concepts/how-uniswap-works): learn how AMMs and liquidity pools work.
-   [Aave Developers](https://aave.com/docs/developers/overview): developer entry point and core concepts for lending protocols.
-   [Chainlink Data Feeds](https://docs.chain.link/data-feeds): understand how price data enters on-chain systems in DeFi.

___


### Oracle | handbook | AI x Web3 School

* Date: 05/25/26 16:21
* Source: https://aiweb3.school/en/handbook/web3/oracle/#minimum-practice
* Tags: #

___

## Oracle

> A blockchain cannot naturally know what happens outside the chain. An Oracle brings external information such as prices, weather, match results, proof of reserves, randomness, or computation results on-chain in a way contracts can use.

## Why Learn This

Many on-chain protocols depend on external data. Lending protocols need asset prices, derivatives need index prices, insurance protocols need event outcomes, and RWA protocols need reserves and asset status.

Oracle is the bridge between on-chain systems and the outside world. A bridge brings capability, but also risk: wrong data sources, delayed updates, price manipulation, feed interruption, and aggregation bugs can directly affect contract execution.

**An oracle is not a "real-world API." It is a data submission and verification mechanism that on-chain contracts are willing to trust.**

## First Principles

> **Contracts can only execute based on data visible on-chain, so once external data enters the chain, it becomes part of protocol rules.**

If a lending protocol uses a price feed to judge liquidation, then the feed's update frequency, data sources, aggregation method, and abnormal-case handling all affect user asset safety.

-   **Data sources are trust boundaries**: who provides data, who aggregates it, and who can update it must be clear.
-   **Latency becomes risk**: when prices move quickly, old data can cause wrong liquidation or bad debt.
-   **Abnormal cases need protection**: contracts should handle stale prices, extreme jumps, and paused feeds.

## Concepts

### Price Feed

**Difficulty: Beginner.** Price Feed is the most common oracle form, providing asset prices to contracts.

DeFi protocols use price feeds to calculate collateral ratios, liquidation lines, swap limits, borrowing capacity, and net asset value. A price looks like a number, but behind it are data sources, update time, precision, aggregation method, and abnormal handling.

When reading a price, check at least:

-   which asset pair the feed represents
-   what the decimals value is
-   whether the update time is too old
-   whether the returned value is abnormal
-   whether the feed address on the current chain is correct

### Data Feed

**Difficulty: Intermediate.** Data Feed includes not only prices, but also proof of reserves, interest rates, macro data, sports results, or other off-chain information.

Whenever contract execution depends on off-chain data, ask the same questions: where does data come from, how is it updated, who can submit it, whether it is verifiable, and what happens when it is wrong.

For example, RWA protocols may need reserve data; insurance protocols may need disaster or flight status; games may need randomness or match results. Contracts cannot directly know any of these by themselves.

### Oracle Risk

**Difficulty: Advanced.** Oracle Risk is the systemic risk introduced when off-chain data enters on-chain execution.

Common risks include:

-   data source manipulation
-   delayed feed updates
-   aggregator nodes offline
-   decimals or unit misunderstanding
-   low-liquidity asset price attacks
-   contracts not checking stale prices
-   opaque oracle upgrade or permission changes

Oracle risk often compounds with DeFi risk. A wrong price feed can cause wrong liquidations, bad debt, arbitrage, and losses in asset pools.

### AI Oracle

**Difficulty: Advanced.** AI Oracle is a direction where model inference, scoring, classification, or generation results are submitted to on-chain systems.

It is more complex than ordinary price feeds because AI output is usually not a simple objective number. "Is this content violating rules," "is this task complete," or "is this address high risk" may all involve model version, input data, prompt, evaluation standard, and dispute handling.

If you design an AI Oracle, consider at least:

-   whether input data is traceable
-   whether model version and prompt are recorded
-   whether output can be reviewed
-   whether challenge or arbitration is allowed
-   what on-chain consequences wrong output causes

## Where It Fits in AI x Web3

Oracle is one of the key bridges in AI x Web3. AI Agents need to read on-chain and off-chain data; if contracts use AI results, model output must also become on-chain data that is verifiable or disputable.

But do not imagine AI Oracle as "whatever the model says, the contract executes." A more reasonable approach is: AI produces a result, the system records sources and confidence, and high-risk scenarios introduce human-in-the-loop, challenge periods, multi-party validation, or economic penalties.

## Minimum Practice

Run a price-feed risk check:

1.  Find an on-chain ETH/USD or BTC/USD price feed.
2.  Check feed address, decimals, latest price, and update time.
3.  Think through which protocol actions would be affected if this price were delayed by 30 minutes.
4.  Write which conditions a contract should check when reading this feed.
5.  Then design an AI Oracle output scenario and list the required input, model version, and dispute process records.

## Further Reading

-   [Ethereum Oracles](https://ethereum.org/en/developers/docs/oracles/): understand why oracles exist and how off-chain data enters on-chain systems.
-   [Chainlink Data Feeds](https://docs.chain.link/data-feeds): learn developer usage of price and data feeds.
-   [Chainlink Data Feeds API Reference](https://docs.chain.link/data-feeds/api-reference): see common interfaces such as AggregatorV3Interface.
-   [Pyth Docs](https://docs.pyth.network/): learn another type of low-latency price oracle network.
-   [UMA Optimistic Oracle](https://docs.uma.xyz/developers/optimistic-oracle): learn the idea of optimistic oracles with challenge mechanisms.

___


### Indexing | handbook | AI x Web3 School

* Date: 05/25/26 16:21
* Source: https://aiweb3.school/en/handbook/web3/indexing/#minimum-practice
* Tags: #

___

## Indexing

> On-chain data is public, but that does not mean it is easy to use. Indexing organizes blocks, transactions, events, and contract state into structured data that products, analytics tools, and AI Agents can query quickly.

## Why Learn This

A contract can emit many events, and a chain produces large numbers of blocks and transactions every day. You can read directly through RPC, but if you want user history, leaderboards, protocol dashboards, risk monitoring, or Agent context, you need a stable data indexing layer.

Indexing does not solve "whether data exists"; it solves "whether data can be queried quickly, accurately, and replayably according to product needs."

**The chain is the source of truth; the indexing layer is the usable data layer.**

## First Principles

> **Products need problem-oriented data models, not raw block streams.**

Blockchains organize data by blocks and transactions, but users and products care about "this address's position," "this protocol's TVL," "whether this order was filled," or "which actions this Agent executed." The indexing layer turns underlying facts into these query objects.

-   **Events are an important entry point**: contract events are the main signals indexers use to build state.
-   **RPC is not a database**: RPC is good for reading chain state and sending transactions, not for all complex historical queries.
-   **Indexing must be replayable**: when contracts upgrade, reorgs happen, or bugs are fixed, data may need to be rebuilt from a certain block.

## Concepts

### Event Indexing

**Difficulty: Beginner.** Event Indexing listens to contract logs and organizes on-chain actions into queryable records.

For example, a contract emits `Transfer`, `OrderCreated`, `Deposit`, `Withdraw`, or `VoteCast`; the indexer can turn these events into database tables or search indexes. The frontend can then query "all orders for a user" or "recent deposits for a pool."

When designing events, consider future queries:

-   whether the event contains key addresses
-   whether indexed parameters are needed
-   whether business state can be reconstructed from events
-   failed transactions do not emit success events
-   whether events remain compatible after contract upgrades

### Subgraph

**Difficulty: Intermediate.** A Subgraph declaratively describes how to index contract events and expose queries through GraphQL.

A The Graph subgraph usually includes three parts: contracts and events to listen to, mapping from events to entities, and GraphQL schema. It is useful for building protocol data APIs such as token, pool, swap, position, and vote.

The value of Subgraph is that developers do not have to write the entire indexer from scratch. But it still needs maintenance: contract-address changes, event-structure changes, reorgs, sync delays, and schema design all affect data quality.

### RPC

**Difficulty: Beginner.** RPC is the interface between applications and nodes, used to read chain state, query logs, estimate gas, and send transactions.

RPC is important, but it is not a universal indexing service. You can use `eth_call` to read current contract state, `eth_getLogs` to query event logs, and `eth_sendRawTransaction` to broadcast transactions. But if you frequently scan large historical logs, public RPC can easily rate-limit or slow down.

Common RPC problems include:

-   rate limits
-   node not synced
-   archive data unavailable
-   different RPCs returning inconsistent data
-   query block range too large
-   unstable WebSocket connections

### Data Pipeline

**Difficulty: Advanced.** Data Pipeline combines on-chain data, off-chain data, indexing results, and business events into a data system for analysis, monitoring, and AI use.

A complete pipeline may include:

-   RPC or node data source
-   event listener
-   ABI decoding
-   database writes
-   reorg handling
-   data validation and compensation jobs
-   API / GraphQL / vector store
-   dashboard, alert, and Agent context

AI x Web3 projects especially need to care about data sources. If an Agent receives stale indexes or wrongly decoded results, stronger downstream reasoning will still be built on wrong facts.

## Where It Fits in AI x Web3

AI Agents need context, and on-chain context usually comes from the indexing layer. Transaction history, contract events, user positions, protocol state, and risk signals are not suitable to search from raw blocks every time.

A good indexing layer should provide Agents with structured, sourced, timestamped, replayable data. The model explains and reasons; the indexing layer provides facts.

## Minimum Practice

Design an event index:

1.  Choose a simple contract, such as voting, counter, or NFT mint.
2.  List the events it should emit.
3.  Design one query table, such as `votes`, `transfers`, or `mints`.
4.  Mark which event parameter or transaction field each column comes from.
5.  Write how to handle reorgs, duplicate events, and contract upgrades.

Then ask: if this data is used by an AI Agent, which source fields and update times must be attached?

## Further Reading

-   [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/): understand the low-level interface for reading chain state, querying logs, and sending transactions.
-   [Ethereum Events and Logs](https://ethereum.org/en/developers/docs/apis/backend/#events): understand how backends listen to on-chain events.
-   [The Graph Subgraphs](https://thegraph.com/docs/en/subgraphs/overview/): learn schema, mappings, and query patterns for subgraphs.
-   [Substreams Documentation](https://substreams.streamingfast.io/): understand another high-throughput on-chain data pipeline approach.
-   [Dune Docs](https://docs.dune.com/): useful for SQL analysis of on-chain data and dashboard building.

___


### Security | handbook | AI x Web3 School

* Date: 05/25/26 16:22
* Source: https://aiweb3.school/en/handbook/web3/security/#minimum-practice
* Tags: #

___

## Security

> Web3 security is not asking someone to audit code once before launch. It is a full engineering process from contract design, permissions, tests, transaction simulation, monitoring, emergency pause, to permission revocation.

## Why Learn This

The cost of errors in on-chain systems is higher than in ordinary applications. Once a contract is deployed, assets may already be inside the protocol, attackers can directly interact with public interfaces, and transaction execution results usually cannot be casually rolled back.

Security is not only the auditor's job. Product, frontend, backend, contracts, operations, and AI Agents all affect safety boundaries: a wrong authorization button, an unlimited approval, an unrestricted Agent tool, or an unsimulated transaction can all become incident entry points.

**The core of Web3 security is not "having no bugs," but blocking predictable risks as much as possible before execution and quickly discovering and containing damage after execution.**

## First Principles

> **On-chain systems are exposed to a public adversarial environment by default, and every callable path should be treated as attack surface.**

Ordinary backends can rely on permissions, network isolation, manual rollback, and database repair. Contracts are different: code is public, state is public, funds are public, and attackers can repeatedly simulate and front-run.

-   **Permissions must be minimized**: owner, admin, upgrade, pause, and withdraw all need clear boundaries.
-   **Simulate before execution**: whether a transaction can succeed, which assets it changes, and which contracts it calls should be seen in advance whenever possible.
-   **Monitor after launch**: security does not end at deployment; abnormal transfers, parameter changes, failed transactions, and price movements need continuous observation.

## Concepts

### Reentrancy

**Difficulty: Intermediate.** Reentrancy is a classic vulnerability where a contract is called again before an external call has finished, allowing state to be reused repeatedly.

The most common pattern is: a contract transfers funds to an external address or calls an external contract before updating internal balances. A malicious contract can re-enter the original function in the callback and withdraw repeatedly before the balance is zeroed.

Defense ideas include:

-   Use Checks-Effects-Interactions: check first, update state second, make external calls last.
-   Use reentrancy guards on high-risk functions.
-   Avoid calling untrusted contracts before state is updated.
-   Test multi-contract interactions, not only single functions.

### Access Control

**Difficulty: Intermediate.** Access Control determines who can execute sensitive actions. It is one of the most common and underestimated parts of contract security.

Sensitive actions include mint, burn, pause, upgrade, withdraw, setOracle, setFee, setRouter, and changeOwner. Any overly broad permission can let admins or attackers rewrite protocol rules.

When checking permissions, do not only ask "is there `onlyOwner`?" Ask further:

-   Is the owner an EOA, multisig, or governance contract?
-   Is there a timelock?
-   Can roles grant each other?
-   Are permission changes emitted as events?
-   Who controls emergency pause and resume?
-   What is the worst outcome if the private key leaks?

### Audit

**Difficulty: Intermediate.** Audit is external security review, not a safety certificate.

Audits can find problems in design, implementation, and tests, but they cannot guarantee a protocol is always safe. Audit scope, code version, dependency version, deployment parameters, upgrade permissions, and post-launch changes all affect conclusions.

When reading an audit report, check at least:

-   which commits and contracts were covered
-   which issues were fixed and which risks the project accepted
-   whether economic mechanisms and external dependencies were covered
-   whether it includes test suggestions and deployment notes
-   whether deployed code matches audited code

### Simulation

**Difficulty: Intermediate.** Simulation is a transaction rehearsal before sending, used to discover execution failure, abnormal asset changes, and permission overreach.

Before a user or Agent signs, the system can simulate the transaction: which contract is called, which tokens will move out, what will be received, approximate gas, whether it reverts, and whether approval changes are triggered.

Simulation cannot replace security audits, because real chain state may change before the transaction is included. But it can block many obvious errors: wrong chain ID, wrong contract address, abnormal approval amount, excessive slippage, insufficient balance, or unexpected method calls.

### Monitoring

**Difficulty: Advanced.** Monitoring is the post-launch security awareness layer, used to discover anomalies and trigger responses.

On-chain monitoring can watch:

-   large transfers or withdrawals
-   admin permission changes
-   contract upgrades
-   oracle price anomalies
-   many failed transactions
-   rapid TVL outflows
-   unexpected events
-   Agents repeatedly triggering high-risk tools

Monitoring alone is not enough. What works is "monitoring + response": who receives alerts, who can pause, who confirms false positives, and what the recovery flow is.

## Where It Fits in AI x Web3

AI makes security boundaries more complex. Agents can explain contracts, generate transactions, call tools, and execute strategies, but they may also misread context, be affected by Prompt Injection, call the wrong tool, or generate dangerous transactions.

So AI x Web3 security design should separate model output from on-chain execution: models can suggest, tools return facts, policies limit permissions, simulation rehearses results, human check confirms high-risk actions, and monitoring records execution consequences.

## Minimum Practice

Build a transaction security checklist:

1.  Choose a public contract-call transaction.
2.  Inspect from, to, method, value, token transfers, logs, and gas used.
3.  Judge whether this transaction changes permissions, assets, or key protocol parameters.
4.  Write which simulation and human checks are needed if this transaction is initiated by an Agent.
5.  Write which events or anomaly metrics should be monitored after launch.

## Further Reading

-   [Solidity Security Considerations](https://docs.soliditylang.org/en/latest/security-considerations.html): official security notes for building contract-security foundations.
-   [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/5.x): learn common security components, access control, and standard contract implementations.
-   [OpenZeppelin Utils](https://docs.openzeppelin.com/contracts/5.x/api/utils): see utilities such as `ReentrancyGuard`, `Pausable`, and `Nonces`.
-   [Ethereum Smart Contract Security](https://ethereum.org/en/developers/docs/smart-contracts/security/): understand common security practices from Ethereum developer docs.
-   [Tenderly Simulations](https://docs.tenderly.co/simulations): learn how transaction simulation and execution traces help diagnose risk.

___
