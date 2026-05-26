# EOA vs. Smart Account vs. Multisig: Permission & Control Comparison

*All facts drawn from the wiki knowledge base at `knowledge-base/AIxWeb3/wiki/`.*
*Generated: 2026-05-26 | Agent: Sensei (Claude via Cowork)*

---

## Comparison Table

| Dimension | EOA | Smart Account (ERC-4337) | Multisig Account (e.g., Safe) |
|---|---|---|---|
| **Who holds control** | Whoever holds the private key — no exceptions. One key = total account authority. | The account contract itself enforces control. The root owner key authorizes policy changes; session keys can delegate bounded sub-authority. | M-of-N keyholders collectively. No single key has unilateral power. |
| **Who can initiate transactions** | Only the private key holder. All on-chain transactions must originate from an EOA (or a bundler acting on behalf of a UserOperation). | The owner key, or a session key within its permitted scope, submits a `UserOperation` to the bundler → EntryPoint. The contract's `validateUserOp` decides what passes. | Any one of the N signers can *propose* a transaction, but it cannot execute until M signers have confirmed it on-chain. |
| **Multiple approvals supported** | No. Single key, single signature — no threshold logic exists. | Optionally yes. Smart accounts can implement M-of-N validation in `validateUserOp`, or delegate to Safe modules for multisig. | Yes — this is the core design. M-of-N is enforced by the contract; execution is blocked until the threshold is met. |
| **Recovery, limits, automation policies** | None. If the private key is lost, the account is permanently inaccessible. No limits, no automation rules. | Full support: social/email recovery via trusted guardians; session keys with per-contract allowlists, amount caps, and time bounds; passkey (biometric) auth; gas sponsorship via paymasters. | Limited by default. Safe supports modules that can add timelocks, spending limits, and ERC-4337 compatibility, but this requires explicit module installation. Recovery requires a new key rotation agreed on by M signers. |
| **Typical use cases** | Personal wallets (MetaMask, Rainbow), individual developer accounts, on-chain transaction originators. AI agents should **not** use bare EOAs. | AI agent wallets with session key delegation, dApps granting scoped DeFi access, onboarding flows with gasless UX, any system requiring programmable authorization. | DAO and protocol treasuries, production smart contract admin/upgrade authority, team funds requiring shared approval, replacing single-owner admin keys with a safer threshold. |
| **Main risk points** | Single point of failure: private key leak, loss, or theft = total, irreversible loss. No recovery path. No way to limit blast radius post-compromise. | Admin key compromise exposes the ability to change the account's entire validation policy. Bugs in custom `validateUserOp` logic can bypass intended restrictions. Session key scope misconfiguration can over-grant. | Coordination overhead: transactions stall if M signers are unavailable. Key management complexity scales with N. Signer collusion (M signers act maliciously together) can drain funds. Smart contract bugs in the Safe itself (historically audited and rare, but non-zero). |

---

## Security Boundaries

### EOA — The Narrowest Boundary

The security perimeter of an EOA is exactly as wide as its private key. The wiki is explicit: *"anyone with the private key can do anything the account can do."* There is no on-chain enforcement layer, no fallback, and no second opinion. A compromised EOA key means instant, unrestricted access — and because EOAs have no recovery mechanism, the loss is permanent. This makes bare EOAs unacceptable for high-value accounts or AI agent use.

### Smart Account — Programmable Boundary

Smart accounts push the security boundary from a single secret into on-chain contract logic. The `validateUserOp` function is the enforcement point: it decides whether an incoming operation is valid before it ever executes. This makes the boundary programmable — you can express rules like *"this session key may only call contract X, with a max of 100 USDC per transaction, and only until block timestamp T."* The wiki notes this is exactly why smart accounts are *"the primary trust boundary for AI agents operating on-chain."* The risk shifts from key loss to admin key compromise (which would allow rewriting the entire validation policy) and logic bugs in the contract itself.

### Multisig — Distributed Boundary

Multisig accounts distribute the security boundary across multiple independent keyholders. No single compromised key enables unauthorized execution — an attacker would need to compromise M distinct keys simultaneously. The wiki highlights this pattern explicitly in the context of access control: *"use a Safe multisig as the contract owner → requires M-of-N signers for any admin action; standard practice for production contracts."* The boundary is robust against individual key compromise but introduces coordination risk: it cannot respond instantly, and collusion among M signers is the ultimate attack vector.

---

## Suitable Scenarios

**Use an EOA when:** You need a simple personal wallet for everyday transactions, you're a developer signing test transactions, or you need a lightweight on-chain identity. Keep balances low and treat the private key as the entire security model — because it is.

**Use a Smart Account when:** You're building AI agents that need to act on-chain autonomously within defined limits (session keys). You want gas abstraction, passkey authentication, or social recovery. You need a trust boundary that can evolve without changing your address — add new rules, revoke stale session keys, or upgrade validation logic in-place.

**Use a Multisig when:** You're managing a shared treasury, acting as admin of a deployed smart contract, or running a DAO. Any situation where *"a single human error or compromise should not be catastrophic"* calls for multisig. The wiki is specific: using a Safe multisig as the contract owner is the *standard practice for production contracts* precisely because it eliminates the single admin key as a single point of failure.

---

## Layered Architecture Note

These three are not mutually exclusive. A production setup might look like: a **Safe multisig** as the root owner of a **smart account**, with **session keys** granted to AI agents for bounded daily operations, and an **EOA** used only as one of the M signers in the multisig — never holding funds directly. This is the architecture the wiki recommends for AI × Web3 systems.

---

## Wiki Sources

- [`wiki/eoa.md`](../knowledge-base/AIxWeb3/wiki/eoa.md)
- [`wiki/smart-account.md`](../knowledge-base/AIxWeb3/wiki/smart-account.md)
- [`wiki/erc-4337.md`](../knowledge-base/AIxWeb3/wiki/erc-4337.md)
- [`wiki/session-key.md`](../knowledge-base/AIxWeb3/wiki/session-key.md)
- [`wiki/agent-wallet.md`](../knowledge-base/AIxWeb3/wiki/agent-wallet.md)
- [`wiki/access-control.md`](../knowledge-base/AIxWeb3/wiki/access-control.md)
- [`wiki/private-key.md`](../knowledge-base/AIxWeb3/wiki/private-key.md)
- [`wiki/web3-security.md`](../knowledge-base/AIxWeb3/wiki/web3-security.md)
