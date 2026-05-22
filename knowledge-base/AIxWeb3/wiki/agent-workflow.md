---
title: "Agent Workflow"
type: concept
tags: [aixweb3-bridge, agent]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

An agent workflow defines the execution structure for an AI agent's task: which steps are automated end-to-end, which steps require human-in-the-loop confirmation, and how control flows between them. In AI × Web3, workflow design is especially critical because mistakes may be irreversible on-chain.

## Key Points

- Not all workflow steps should be automated: high-risk, irreversible, or compliance-sensitive steps should require human-in-the-loop checkpoints
- Workflow design answers four questions for each step: who initiates, who executes, who pays, who verifies, and who carries the risk
- The Prompt → Workflow → Agent spectrum means most tasks should be handled as structured workflows before considering full agent autonomy
- In Week 2 of the program, track selection involves mapping out a workflow for a specific AI × Web3 use case
- Common Web3 workflow pattern: agent retrieves data → proposes action → human confirms → agent executes on-chain → agent records receipt

## Related Concepts

- [[ai-agent]] — agents operate within workflow structures
- [[prompt-workflow-agent-boundary]] — workflow is the middle architecture between prompt and agent
- [[agent-handoff]] — handoffs occur at workflow step boundaries
- [[guardrails]] — guardrails enforce workflow rules at each step
- [[agent-wallet]] — wallet permissions are scoped to specific workflow steps
- [[machine-payment]] — payment steps within agent workflows

## Sources

- [[sources/aixweb3-school]] — agent workflow as AI × Web3 Bridge topic
- [[sources/program-structure]] — workflow design as Week 2 track exercise
