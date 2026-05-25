---
title: "Contract Audit"
type: concept
tags: [web3-foundations, security]
source_count: 1
date_updated: "2026-05-25"
---

# Contract Audit

## Definition

A contract audit is a systematic security review of smart contract source code by expert security researchers before mainnet deployment. Auditors look for known vulnerability patterns (reentrancy, access control flaws, oracle manipulation, integer issues), logic errors, and design flaws. Audits are the primary quality gate for production DeFi protocols.

## Key Points

- **Not a guarantee**: audits reduce risk but cannot prove absence of all bugs; audited protocols have still been exploited
- **Scope**: auditors review Solidity source code, test coverage, deployment scripts, and protocol design; may also review off-chain components
- **Static analysis**: tools like Slither (Trail of Bits) and Mythril automate detection of known patterns; used as pre-audit and in CI
- **Formal verification**: mathematically proving that a contract satisfies a specification; used for critical components (voting, token transfers)
- **Audit firms**: Trail of Bits, OpenZeppelin, Sherlock, Code4rena (competitive audits); competitive audits pool many researchers
- **Bug bounty**: post-launch bug bounty programs (Immunefi) provide ongoing financial incentive for white-hat reporting
- **Timing**: audit after code is feature-complete and test coverage is high; auditing unfinished code is wasteful
- **Remediation**: audit report lists findings by severity (critical, high, medium, low, info); fixes require re-audit of changed code

## Related Concepts

- [[web3-security]] — audit is a core security practice
- [[smart-contract]] — the artifact being audited
- [[openzeppelin]] — audited library that reduces code needing custom audit
- [[tx-simulation]] — pre-audit: simulate behavior under edge cases
- [[foundry]] — fuzz testing finds issues before audit
- [[contract-upgrade]] — upgradeable contracts need audit for each logic version

## Sources

- [[sources/web3-chapters]] — Chapter: Security
