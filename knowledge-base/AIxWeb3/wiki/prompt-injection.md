---
title: "Prompt Injection"
type: concept
tags: [ai-foundations, prompt, context, security]
source_count: 2
date_updated: "2026-05-22"
---

## Definition

Prompt injection is an attack where adversarial content in the model's input — a webpage, retrieved document, user message, or tool result — attempts to override or subvert the system's original instructions, causing the model to take unintended actions.

## Key Points

- Especially dangerous in agent scenarios with access to private internal systems: a model that browses the web and then executes actions could be hijacked via a malicious webpage
- **Prevention requires defense-in-depth**, not just better prompts:
  - Mark external content as untrusted data (zone isolation)
  - Perform parameter verification before tool calls
  - Force sensitive actions through an allowlist and human approval
  - Never hand secrets, primary permissions, or irreversible actions to the model
- Prompt injection exploits the **five-layer context model failure**: untrusted content from the knowledge or fact layer is treated as instruction-layer authority
- In AI × Web3 contexts, a wallet-connected agent that reads governance forum posts could be injected via a malicious proposal
- Indirect prompt injection (via retrieved documents or tool results) is harder to detect than direct injection (via user messages)

## Related Concepts

- [[information-governance]] — proper zone separation is the primary structural defense
- [[five-layer-agent-context]] — injection exploits layer boundary failures
- [[context-engineering]] — isolating untrusted content is a core context engineering task
- [[guardrails]] — system-level defense that catches injected instructions before execution
- [[verification-chain]] — the full chain that must hold even if injection bypasses the prompt
- [[ai-security]] — prompt injection is a key attack surface in the AI security track

## Sources

- [[sources/prompt]] — prompt injection definition, prevention actions
- [[sources/context]] — zone isolation as structural defense
