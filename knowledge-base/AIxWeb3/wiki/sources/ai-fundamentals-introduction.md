---
title: "AI Fundamentals - Introduction"
type: source
tags: [ai-foundations, llm, agent, tool-calling, prompt, workflow]
source_file: "raw/AI Fundamentals - Introduction.md"
source_hash: "sha256:559c38e2a16b2bfab24e69841564b8e0198954c918e4f86af6a797af3770a762"
date_ingested: "2026-05-22"
---

## Summary

This source covers the foundational concepts of AI and agent workflows from Module A of the AI × Web3 School bootcamp. It establishes the mental model for how LLMs work probabilistically, the four control layers (context window, system instructions, prompt, tool calling), and the critical distinction between Prompt, Workflow, and Agent architectures. The source emphasizes that AI output must always be validated because models hallucinate with confidence. It also catalogs the core technical components of production-grade agents.

## Key Concepts

- [[large-language-model]] — generates text probabilistically; excels at language, code, reasoning; unreliable for factual recall
- [[four-control-layers]] — context window, system instructions, prompt, tool calling
- [[prompt-workflow-agent-boundary]] — three distinct architectures with different failure modes
- [[tool-calling]] — transforms the model from talker to doer
- [[ai-agent]] — model planning autonomously, calling tools, managing state across turns
- [[state-management]] — multiple nodes share read/write access to the same State object
- [[agent-memory]] — store and retrieve information across sessions
- [[mcp]] — unified connectivity protocol between LLMs and external tools
- [[guardrails]] — input/output validation; execution halts if violated
- [[agent-handoff]] — transfer control after a subtask completes
- [[ai-agent-tracing]] — visualize agent execution chain
- [[hallucination]] — models fabricate information with full confidence
- [[maas]] — Model-as-a-Service: call top-tier models via API key per token

## Notable Points

- "Prompt is letting the model answer, with the human making decisions. Workflow is a predefined task pipeline. Agent is the model planning autonomously." — three fundamentally different failure modes and risk profiles.
- Execution overreach and tool misuse are agent-specific failure modes that require guardrails and tracing, beyond just prompt validation.
- "Use an agent when the goal is open-ended, multiple tools must collaborate, intermediate results determine the next step, or state must persist across sessions."
