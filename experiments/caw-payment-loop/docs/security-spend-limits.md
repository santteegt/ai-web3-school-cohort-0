> ## Documentation Index
> Fetch the complete documentation index at: https://cobo.com/products/agentic-wallet/manual/llms.txt
> Use this file to discover all available pages before exploring further.

# Spend limits

> Per-transaction caps, rolling window counters, and review thresholds that bound how much an agent can move.

Spend limits are the quantitative controls in a pact's policies. They answer the question: even if an operation is the right type and goes to the right address, is it within the agreed financial bounds?

Spend limits are set in the `policies` field of a PactSpec at submission time and are fixed once the pact is activated. They are evaluated after permission checks and policy rule matching on every operation.

## Three limit types

### Per-transaction cap

A hard limit on the value of any single operation. If a transfer or contract call would exceed this value, it is denied immediately — regardless of rolling window state.

The cap can be expressed in USD (`amount_usd_gt`) or in the token's transfer unit (`amount_gt`). For USD limits, the engine converts using current market prices; if the price feed is unavailable for a token, the USD limit is not evaluated and the operation proceeds.

### Rolling window counter

Tracks cumulative activity over a sliding time window. Available windows: 1 hour, 24 hours, 7 days, 30 days. Each window can limit cumulative USD value, cumulative token amount, or transaction count — or any combination.

Rolling windows are not calendar-based. A 24-hour window tracks the last 24 hours backward from the moment of each operation, not from midnight. This provides consistent protection across all hours of the day.

Multiple windows can be active at once. An operation must pass all applicable counters before it can proceed.

### Review threshold

A soft escalation trigger instead of a hard block. When a transfer exceeds the threshold, the operation is held for owner review rather than denied. The agent receives a `PENDING_APPROVAL` response and can poll for the outcome. Operations below the threshold proceed automatically.

## How limits compose

A single operation must pass all applicable limits. A \$400 transfer may be within the per-transaction cap, but if the 24-hour counter is nearly full, it can still be denied on the rolling limit. Conversely, a transfer within the rolling budget can be blocked by the per-transaction cap.

When a limit is hit, the denial response includes the current counter value, the limit, and when the window will have enough capacity again — giving the agent enough information to decide whether to wait, reduce the amount, or surface the block to the user.

## Further reading

* [Policy engine](/products/agentic-wallet/manual/security/policy-engine) — how spend limits fit into the three-stage evaluation pipeline
* [Address allowlists](/products/agentic-wallet/manual/security/address-allowlists) — how to restrict which addresses an agent can send to
