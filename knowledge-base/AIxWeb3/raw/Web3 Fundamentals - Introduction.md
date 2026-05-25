## Notes

### Web3 Career Build

* Date: 05/25/26 16:45
* Source: https://web3career.build/en/programs/AI-Web3-School?tab=learning
* Tags: #

___

## Module B | Web3 Fundamentals: Accounts, Wallets, Signatures, and On-Chain Execution

### Core Concepts

- The relationship among accounts, addresses, and wallets: a wallet is not an ordinary account; it is the entry point to private keys, security responsibility, and on-chain actions.
- What seed phrases, private keys, and addresses are, and why seed phrases and private keys must never be exposed.
- Privacy and security baselines for AI × Web3 builders: an address is not the same as anonymity, a signature is not the same as ordinary login, and authorization is not the same as transfer; AI agents should not directly touch private keys / seed phrases, and actions involving signatures, approvals, transfers, or contract writes must keep human confirmation.
- The relationship between signatures and transactions: signing is not simply “clicking confirm”; it authorizes a specific action.
- What Gas is, and why on-chain execution has costs, can fail, and requires waiting for confirmation.
- L1 / L2 and execution costs.
- How smart contracts differ from ordinary backend logic: state is public, execution is public, upgrade permissions can be checked, and some contracts cannot be changed.
- The difference between mainnets and testnets: learning and experiments should be completed on testnets first.
- How block explorers, wallet prompts, and transaction receipts help you understand on-chain behavior.
- Advanced extension: account abstraction, smart accounts, multisig, Safe, ERC-4337, and OpenZeppelin Contracts, and why they become key infrastructure for AI × Web3.
- From wallets to AI-native accounts: recovery, authorization, and security boundaries, including private keys, seed phrases, social recovery, email recovery, account abstraction, session keys, permission limits, and human confirmation.

### Recommended Materials / Reference Links

- [Ethereum Accounts docs](https://ethereum.org/developers/docs/accounts/): understand accounts and addresses.
- [MetaMask Getting Started](https://support.metamask.io/start/getting-started-with-metamask/): understand wallet usage and security responsibilities.
- [Ethereum Development Documentation](https://ethereum.org/developers/docs/): the main entry point for Ethereum learning paths.
- [How Web3 Works](https://docs.google.com/presentation/d/1NUeO115bLnz0V8aejx9bYqQTaDrznTjhgbCkn-pK1a0/edit?usp=sharing): Week 1 supplemental Web3 fundamentals material that helps students understand how accounts, transactions, Gas, contract execution, and on-chain state jointly make up Web3 operations.
- [Remix IDE](https://remix.ethereum.org/): entry point for minimal contract interaction.
- [Sepolia Faucet](https://cloud.google.com/application/web3/faucet/ethereum/sepolia): get test tokens.
- [Hardhat Getting Started](https://hardhat.org/docs/getting-started) / [Foundry](https://github.com/foundry-rs/foundry): more engineering-oriented entry points for contract development.
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts): reusable contract components and security practices.
- [Safe Overview](https://docs.safe.global/home/overview) / [ERC-4337 docs](https://docs.erc4337.io/): understand smart accounts, multisig, and permission control.
- [viem](https://viem.sh/) / [wagmi](https://wagmi.sh/): entry points for on-chain reads and writes from frontends and scripts.

___