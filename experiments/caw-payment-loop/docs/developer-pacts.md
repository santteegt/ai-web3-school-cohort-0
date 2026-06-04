> ## Documentation Index
> Fetch the complete documentation index at: https://cobo.com/products/agentic-wallet/manual/llms.txt
> Use this file to discover all available pages before exploring further.

# Submit and manage pacts

> How to use pacts for task-level authorization — submit, poll, operate, and revoke.

Before your runtime can transfer tokens or call contracts, it needs an active pact. A pact is the agreement between the wallet owner and your runtime: it captures the program's intent, the execution plan, the policy boundaries the owner enforces, and when the authority ends. When the owner approves a pact, Cobo Agentic Wallet creates a scoped delegation with enforced policies so the runtime can operate — but only within the approved boundaries.

## How pacts work

The pact flow has three phases: **propose**, **approve**, **operate**.

```
1. Runtime proposes a pact
   └── "I want to DCA $500/week into ETH on Base for 3 months"
   └── Specifies: spending limits, allowed contracts, and completion conditions

2. You review and approve
   └── Pact appears in the Cobo Agentic Wallet app
   └── You see the intent, execution plan, and spending rules
   └── You can revise the policies before approving
   └── Approve → runtime gets scoped access. Reject → nothing happens.

3. Runtime operates within the pact
   └── Every transaction is checked against the pact's policies
   └── Exceeds a limit → denied with a clear reason
   └── Exceeds your threshold → paused for your approval
   └── Completion conditions are met or the owner revokes → access removed automatically
```

## What a pact contains

For the conceptual overview of the four elements, see [What is a pact](/products/agentic-wallet/manual/start-here/what-is-a-pact). The following table maps those elements to PactSpec fields:

| Field                     | What it controls                                                                                                                                                 |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Intent**                | A plain-language description of what the runtime wants to do — e.g., "DCA \$500/week into ETH on Base for 3 months"                                              |
| **Execution plan**        | A detailed markdown plan explaining the runtime's strategy, steps, and rationale — helps the owner understand *how* the program intends to accomplish the intent |
| **Policies**              | Spending rules — per-transaction limits, daily/weekly budgets, allowed chains/tokens/contracts                                                                   |
| **Completion conditions** | Conditions that end the pact automatically — e.g., after 12 transactions, \$6,000 total spent, or 90 days elapsed                                                |

### Example PactSpec

A DCA trader pact that allows weekly \$500 ETH purchases on Base for 3 months:

```json theme={null}
{
  "intent": "DCA $500/week into ETH on Base for 3 months",
  "execution_plan": "# Summary\nWeekly DCA: swap $500 USDC to ETH on Base via Uniswap V3.\n\n# Operations\n- Swap $500 USDC → ETH via Uniswap V3 on Base weekly\n\n# Risk Controls\n- Per-swap cap: $550 (includes slippage buffer)\n- Rolling 24h limit: $600, max 5 swaps",
  "policies": [
    {
      "name": "allow-uniswap-base",
      "type": "contract_call",
      "rules": {
        "effect": "allow",
        "when": {
          "chain_in": ["BASE_ETH"],
          "target_in": [{
            "chain_id": "BASE_ETH",
            "contract_addr": "0x2626664c2603336E57B271c5C0b26F421741e481"
          }]
        },
        "review_if": {
          "amount_usd_gt": "500"
        }
      }
    },
    {
      "name": "deny-excessive-spending",
      "type": "contract_call",
      "rules": {
        "effect": "allow",
        "when": {
          "chain_in": ["BASE_ETH"]
        },
        "deny_if": {
          "amount_usd_gt": "550",
          "usage_limits": {
            "rolling_24h": { "amount_usd_gt": "600", "tx_count_gt": 5 }
          }
        }
      }
    }
  ],
  "completion_conditions": [
    { "type": "time_elapsed", "threshold": "7776000" },
    { "type": "tx_count", "threshold": "12" }
  ]
}
```

For the full policies and completion conditions schema, see [Pact policies and completion conditions](/products/agentic-wallet/manual/reference/pact-policies).

## Pact lifecycle

A pact moves through these states:

```
  Submit ──► PENDING_APPROVAL
                  |
             ┌────┴────┐
      approved│        │rejected
             v        v
          ACTIVE   REJECTED
         ┌──┬──┐
         │  │  │
  done ◄─┘  │  └─► owner revokes ──► REVOKED
   v        v
COMPLETED  EXPIRED
```

| State              | What it means                                                                                                           |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `PENDING_APPROVAL` | Runtime submitted the pact. Waiting for owner approval in the Cobo Agentic Wallet app.                                  |
| `ACTIVE`           | Owner approved. The runtime now has a scoped delegation and API key to operate within the pact's boundaries.            |
| `REJECTED`         | Owner rejected the pact. No access was granted.                                                                         |
| `COMPLETED`        | A completion condition was met (e.g., 12 transactions completed). Access revoked automatically.                         |
| `EXPIRED`          | The pact expired because approval timed out or a time-based completion condition elapsed. Access revoked automatically. |
| `REVOKED`          | Owner revoked the pact manually. Access revoked immediately.                                                            |

When a pact reaches any terminal state (`COMPLETED`, `EXPIRED`, `REVOKED`), the delegation and its pact-scoped API key are both revoked. The runtime can no longer submit onchain operations.

## Pact, delegation, and policy relationship

When you approve a pact, Cobo Agentic Wallet creates the underlying infrastructure automatically:

```
Pact (what you approve)
  │
  ├── Delegation (scoped access grant)
  │     └── derived scope, wallet, operator, expiry
  │
  ├── Inline policies (spending rules)
  │     └── transfer limits, contract allowlists, rolling budgets
  │
  └── Pact-scoped API key (operator credential)
        └── bound to the delegation, returned only to the runtime
```

You don't need to create delegations or policies manually when using pacts — the pact does it for you.

## Submit a pact

The example below submits a simple one-time transfer pact that allows a single USDC transfer of up to \$101 on Base.

<Tabs>
  <Tab title="CLI">
    ```bash theme={null}
    caw pact submit \
      --intent "Transfer 100 USDC to 0xRecipient... on Base" \
      --original-intent "Send 100 USDC to 0xRecipient... on Base" \
      --execution-plan "# Summary
    Transfer 100 USDC to 0xRecipient... on Base.

    # Operations
    - Transfer 100 USDC to 0xRecipient... on BASE_ETH

    # Risk Controls
    - Per-tx cap: \$101
    - One-time transfer only" \
      --policies '[
        {
          "name": "usdc-transfer",
          "type": "transfer",
          "rules": {
            "effect": "allow",
            "when": {
              "chain_in": ["BASE_ETH"],
              "token_in": [{"chain_id": "BASE_ETH", "token_id": "BASE_USDC"}],
              "destination_address_in": [{"chain_id": "BASE_ETH", "address": "0xRecipient..."}]
            },
            "deny_if": {
              "amount_usd_gt": "101"
            }
          }
        }
      ]' \
      --completion-conditions '[{"type": "tx_count", "threshold": "1"}]'
    ```

    Required flags are `--intent`, `--execution-plan`, `--policies`, and `--completion-conditions`. The wallet UUID is resolved from the active wallet profile. The command prints a `pact_id` — save it to poll for approval and execute transactions.
  </Tab>

  <Tab title="Python SDK">
    ```python theme={null}
    from cobo_agentic_wallet import WalletAPIClient

    async with WalletAPIClient(base_url=API_URL, api_key=AGENT_API_KEY) as client:
        result = await client.submit_pact(
            wallet_id=WALLET_UUID,
            intent="Transfer 100 USDC to 0xRecipient... on Base",
            spec={
                "policies": [
                    {
                        "name": "usdc-transfer",
                        "type": "transfer",
                        "rules": {
                            "effect": "allow",
                            "when": {
                                "chain_in": ["BASE_ETH"],
                                "token_in": [{"chain_id": "BASE_ETH", "token_id": "BASE_USDC"}],
                                "destination_address_in": [{"chain_id": "BASE_ETH", "address": "0xRecipient..."}],
                            },
                            "deny_if": {
                                "amount_usd_gt": "101"
                            },
                        },
                    }
                ],
                "completion_conditions": [{"type": "tx_count", "threshold": "1"}],
                "execution_plan": (
                    "# Summary\n"
                    "Transfer 100 USDC to 0xRecipient... on Base.\n\n"
                    "# Operations\n"
                    "- Transfer 100 USDC to 0xRecipient... on BASE_ETH\n\n"
                    "# Risk Controls\n"
                    "- Per-tx cap: $101\n"
                    "- One-time transfer only"
                ),
            },
        )
        pact_id = result["pact_id"]
        print(f"Submitted: {pact_id}")
    ```
  </Tab>

  <Tab title="TypeScript SDK">
    ```typescript theme={null}
    import { PactsApi, Configuration } from '@cobo/agentic-wallet';

    const config = new Configuration({ apiKey: AGENT_API_KEY, basePath: API_URL });
    const pactsApi = new PactsApi(config);

    const pactResp = await pactsApi.submitPact({
      wallet_id: WALLET_UUID,
      intent: 'Transfer 100 USDC to 0xRecipient... on Base',
      spec: {
        policies: [
          {
            name: 'usdc-transfer',
            type: 'transfer',
            rules: {
              effect: 'allow',
              when: {
                chain_in: ['BASE_ETH'],
                token_in: [{ chain_id: 'BASE_ETH', token_id: 'BASE_USDC' }],
                destination_address_in: [{ chain_id: 'BASE_ETH', address: '0xRecipient...' }],
              },
              deny_if: {
                amount_usd_gt: '101',
              },
            },
          },
        ],
        completion_conditions: [{ type: 'tx_count', threshold: '1' }],
        execution_plan:
          '# Summary\nTransfer 100 USDC to 0xRecipient... on Base.\n\n' +
          '# Operations\n- Transfer 100 USDC to 0xRecipient... on BASE_ETH\n\n' +
          '# Risk Controls\n- Per-tx cap: $101\n- One-time transfer only',
      },
    });
    const pactId = pactResp.data.result.pact_id;
    console.log('Submitted:', pactId);
    ```
  </Tab>
</Tabs>

## Wait for approval

After submission, the pact is in `pending_approval` state. If the wallet is paired with the Cobo Agentic Wallet app, the owner must approve it there. If the wallet is not yet paired, it activates automatically.

Poll until the status changes:

<Tabs>
  <Tab title="CLI">
    ```bash theme={null}
    caw pact status --pact-id <PACT_ID>
    ```
  </Tab>

  <Tab title="Python SDK">
    ```python theme={null}
    import asyncio

    while True:
        pact = await client.get_pact(pact_id)
        status = pact["status"]
        if status == "active":
            break
        if status in ("rejected", "revoked", "expired"):
            raise RuntimeError(f"Pact {status} — cannot proceed")
        await asyncio.sleep(3)

    print("Pact active — ready to execute")
    ```
  </Tab>

  <Tab title="TypeScript SDK">
    ```typescript theme={null}
    const poll = async (): Promise<void> => {
      while (true) {
        const pact = (await pactsApi.getPact(pactId)).data.result;
        if (pact.status === 'active') break;
        if (['rejected', 'revoked', 'expired'].includes(pact.status ?? '')) {
          throw new Error(`Pact ${pact.status} — cannot proceed`);
        }
        await new Promise(res => setTimeout(res, 3000));
      }
    };
    await poll();
    ```
  </Tab>
</Tabs>

## Handle rejection

If the owner rejects the pact, offer to resubmit with a narrower scope — lower spend cap, shorter duration, or a tighter allowlist.

```python theme={null}
if pact["status"] == "rejected":
    # Submit a revised pact with narrower limits
    result = await client.submit_pact(
        wallet_id=WALLET_UUID,
        intent="Transfer 50 USDC to 0xRecipient... on Base",
        spec={
            "policies": [...],  # revised, narrower policy
            "completion_conditions": [{"type": "tx_count", "threshold": "1"}],
            "execution_plan": "...",
        },
    )
```

## Check pact status

<Tabs>
  <Tab title="CLI">
    ```bash theme={null}
    # Show full pact detail
    caw pact show --pact-id <PACT_ID>

    # Check status (also triggers lazy activation)
    caw pact status --pact-id <PACT_ID>

    # List all pacts
    caw pact list

    # List active pacts only
    caw pact list --status active
    ```
  </Tab>

  <Tab title="Python SDK">
    ```python theme={null}
    # Get a specific pact
    pact = await client.get_pact(pact_id)
    print(pact["status"])  # pending_approval, active, rejected, completed, expired, revoked

    # List pacts with status filter
    pacts = await client.list_pacts(status="active")
    ```
  </Tab>

  <Tab title="TypeScript SDK">
    ```typescript theme={null}
    // Get a specific pact
    const pact = (await pactsApi.getPact(pactId)).data.result;
    console.log(pact.status); // pending_approval, active, rejected, completed, expired, revoked

    // List pacts with status filter
    const pacts = (await pactsApi.listPacts('active')).data.result;
    ```
  </Tab>
</Tabs>

## Revoke a pact

<Tabs>
  <Tab title="CLI">
    ```bash theme={null}
    caw pact revoke --pact-id <PACT_ID>
    ```

    Revoking immediately revokes the delegation and invalidates the pact-scoped API key.
  </Tab>

  <Tab title="Python SDK">
    ```python theme={null}
    await client.revoke_pact(pact_id)
    ```
  </Tab>

  <Tab title="TypeScript SDK">
    ```typescript theme={null}
    await pactsApi.revokePact(pactId);
    ```
  </Tab>
</Tabs>

## Approval experience

When your runtime submits a pact, the owner receives a notification in the Cobo Agentic Wallet app. The approval screen shows:

* **Intent** — what the agent wants to do, in plain language
* **Execution plan** — the agent's detailed strategy and steps, so you understand the reasoning
* **Policy scope proposed** — what transactions and contract calls the pact would allow in practice
* **Spending rules** — per-transaction limits, daily budgets, allowed chains and contracts
* **Duration** — how long the pact lasts
* **Completion conditions** — what triggers automatic completion

You can **approve**, **reject**, or **revise before approving**. If the agent's proposed policies are too broad (or too narrow), you can adjust them directly before granting access — the agent will operate under your revised terms, not its original proposal. You can also revoke an active pact at any time.

## When to use pacts vs. manual delegation

| Scenario                                                               | Use                                                                   |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Agent needs temporary, scoped access for a specific task               | **Pact** — auto-expires, auto-revokes on completion                   |
| You want to review what the agent is asking for before granting access | **Pact** — the approval flow shows you exactly what's being requested |
| Permanent or long-lived delegation managed by an admin                 | **Manual delegation** — create directly via API or CLI                |
| Programmatic setup without human approval                              | **Manual delegation** — no approval step required                     |

## Pact events

Every pact records lifecycle events that you can query:

<Tabs>
  <Tab title="CLI">
    ```bash theme={null}
    caw pact events --pact-id <PACT_ID>
    ```
  </Tab>

  <Tab title="Python SDK">
    ```python theme={null}
    events = await client.list_pact_events(pact_id)
    for event in events.get("items", []):
        print(event["type"], event["created_at"])
    ```
  </Tab>

  <Tab title="TypeScript SDK">
    ```typescript theme={null}
    const events = (await pactsApi.listPactEvents(pactId)).data.result;
    for (const event of events.items ?? []) {
      console.log(event.type, event.created_at);
    }
    ```
  </Tab>
</Tabs>

Events include: `submitted`, `activated`, `rejected`, `completed`, `expired`, `revoked`. Each event records a timestamp and relevant details.

## Next steps

Once a pact is active, use it to execute transactions:

<CardGroup cols={2}>
  <Card title="Transfers" href="/products/agentic-wallet/manual/developer/transfers">
    Submit token transfers under an active pact.
  </Card>

  <Card title="Contract calls" href="/products/agentic-wallet/manual/developer/contract-calls">
    Call smart contracts under an active pact.
  </Card>

  <Card title="Policy Engine" icon="shield" href="/products/agentic-wallet/manual/security/policy-engine">
    Deep dive into policy rules — the spending limits enforced by pacts.
  </Card>
</CardGroup>
