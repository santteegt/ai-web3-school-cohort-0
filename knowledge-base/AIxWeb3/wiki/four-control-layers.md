---
title: "Four Control Layers"
type: concept
tags: [ai-foundations, llm, agent, prompt]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

The four control layers are the four mechanisms through which a developer or system controls what an LLM does in a given interaction: context window, system instructions, prompt, and tool calling. Each layer has a distinct authority level and purpose.

## Key Points

1. **Context window** — the model's "working memory"; controls how much information the model can see at any time
2. **System instructions** — set identity, tone, and behavioral boundaries; the highest-trust developer-controlled layer
3. **Prompt** — conveys the intent of the current task; session-scoped user or developer input
4. **Tool calling** — transforms the model from a talker into a doer; enables real-world action

- These four layers map to the [[five-layer-agent-context]] model (which adds the memory layer for agents)
- Understanding which layer to use for which constraint prevents prompt over-loading (putting security in prompts instead of code)

## Related Concepts

- [[context-window]] — the first control layer
- [[instruction]] — content of the system instructions layer
- [[prompt-design]] — the third control layer
- [[tool-calling]] — the fourth control layer
- [[five-layer-agent-context]] — extends this model with memory for agent contexts
- [[large-language-model]] — the entity the four layers control

## Sources

- [[sources/ai-fundamentals-introduction]] — four control layers definition
