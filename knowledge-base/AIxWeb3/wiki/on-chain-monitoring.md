---
title: "On-Chain Monitoring"
type: concept
tags: [web3-foundations, security, observability]
source_count: 1
date_updated: "2026-05-25"
---

# On-Chain Monitoring

## Definition

On-chain monitoring is the real-time observation of blockchain transactions and contract state to detect anomalous or suspicious behavior after deployment. Unlike traditional server monitoring, on-chain monitoring tracks public transaction data — no private logs needed. It is the post-deployment security layer that complements pre-deployment audits.

## Key Points

- **Event-driven**: monitors subscribe to contract events via RPC WebSocket; alert when specific patterns are detected (large withdrawals, role changes, unusual call sequences)
- **OpenZeppelin Defender**: managed platform for monitoring, alerting, automated responses (Autotasks), and governance execution
- **Forta**: decentralized monitoring network; detection bots written by anyone; alerts on anomalous patterns across any EVM chain
- **Alert types**: admin role changes, large token flows, flash loan usage, contract pausing, oracle price spikes
- **Automated response**: monitoring can trigger automated pausing or circuit breakers via a Defender Autotask when thresholds are exceeded
- **AI × Web3**: AI agents monitoring on-chain state for anomalies; natural fit for AI pattern recognition applied to transaction streams
- **Post-exploit response**: even if an exploit succeeds, fast monitoring enables rapid protocol pause to limit further damage

## Related Concepts

- [[web3-security]] — monitoring is the post-deployment security layer
- [[contract-event]] — events are the raw input to monitoring systems
- [[observability]] — same principle as software observability; applied on-chain
- [[smart-contract]] — the monitored artifact
- [[data-pipeline]] — monitoring uses event-driven data pipelines
- [[rpc]] — WebSocket subscriptions for real-time event streaming

## Sources

- [[sources/web3-chapters]] — Chapter: Security
