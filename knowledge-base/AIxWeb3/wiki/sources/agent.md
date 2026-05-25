---
title: "Agent"
type: source
tags: [ai-foundations, agent, tool-use, planning, state-management]
source_file: "raw/Agent.md"
source_hash: "sha256:3f074253dac7b4d37fba126712d84a6dfe4ff8a4b161ba8f500658555c223fcd"
date_ingested: "2026-05-24"
---

## Summary

This source deepens the concept of AI agents beyond basic definitions, framing them as constrained execution loops rather than autonomous systems. Its central thesis is that agent design is about giving the execution loop clear boundaries — not making the model more human-like. The source introduces the division of labor model (model proposes, system limits, user approves), emphasizes that agent state must be externalized and queryable, and provides the 8-step AI × Web3 agent architecture as a stable reference pattern.

## Key Concepts

- [[ai-agent]] — redefined as a constrained execution loop with goal, tools, state, permissions, and stop conditions
- [[tool-calling]] — tool use makes agents dangerous; tools must declare input schema, permission scope, side effects, and logging
- [[agent-planning]] — model generates candidate plan; system must verify before execution; each step must be classified as read or write
- [[state-management]] — state must be externalized, queryable, recoverable, auditable — not hidden in prompt history
- [[agent-reflection]] — self-checking mechanism to correct intermediate steps; improves quality but cannot be the final safety judgment
- [[agent-stop-conditions]] — explicit criteria for halting execution: goal reached, budget exceeded, information lacking, risk boundary crossed
- [[multi-agent-systems]] — multiple agents dividing complex workflows; amplifies coordination problems
- [[aixweb3-agent-architecture]] — 8-step pattern: goal → plan → split read/write → policy check → simulation → user confirmation → wallet execution → log
- [[guardrails]] — the system limits action space; the model never authorizes its own actions
- [[prompt-injection]] — tools make prompt injection dangerous (malicious webpage can trigger wrong action, not just wrong answer)

## Notable Points

- "Tools are more dangerous than answers" — an agent that acts on a wrong answer creates real-world consequences, not just incorrect text.
- "The most dangerous design is giving an Agent vague goals, broad tools, long-term memory, and large-asset permissions at the same time."
- "Self-checking can improve quality; deterministic checking is what can carry risk." — reflection is not a substitute for code-enforced guardrails.
