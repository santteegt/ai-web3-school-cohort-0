## Notes
### Web3 Career Build

* Date: 05/22/26 16:18
* Source: https://web3career.build/en/programs/AI-Web3-School?tab=learning
* Tags: #

___

## Module A | AI Fundamentals: From LLMs to Agent Workflows

**Goal:** Build an understanding of what models are and how agent workflows operate, then get hands-on with API calls and mainstream AI coding tools.

### Core Concepts

1.  **How LLMs work at a basic level:** LLMs generate text probabilistically based on context: given an input, the model predicts the most likely next sequence of tokens. They excel at language understanding, code generation, and reasoning, but are poor at accurate factual recall, deterministic computation, and maintaining state across sessions.
2.  **The four control layers:** Context window is the model's "working memory" and controls how much information the model can see at any given time. System instructions set identity, tone, and behavioral boundaries. Prompt conveys the intent of the current task. Tool calling transforms the model from a talker into a doer.
3.  **Calling the LLM API hands-on:** MaaS lets you call top-tier models via API key on a per-token basis, no GPU required. Core parameters: `model`, `messages`, `temperature`, `max_tokens`. Start with the Quick Start guides from OpenAI, Anthropic, or GLM and get your first request.
4.  **The boundary between Prompt, Workflow, and Agent:** Prompt is letting the model answer, with the human making the decisions. Workflow is a predefined task pipeline where the model is one node and the path is fixed. Agent is the model planning autonomously, calling tools dynamically, and managing state across turns. These three differ fundamentally in failure modes, risk exposure, and debuggability.
5.  **The value and limits of AI coding tools:** Claude Code, Codex CLI, and Cursor can rapidly generate boilerplate, explain unfamiliar libraries, and accelerate prototyping. Code review, test design, and architectural decisions, however, cannot be delegated to them.
6.  **Why AI output must always be validated:** Factual errors are the most common trap: models fabricate information with full confidence, so critical facts must be verified externally. Models are equally unreliable with references, routinely inventing paper titles, URLs, and data sources, so never trust a link a model gives you. In longer contexts, reasoning drift becomes a risk where the logical chain quietly breaks down and conclusions diverge from the original premises, making segment-by-segment validation essential. When agents are involved, two additional failure modes emerge: execution overreach, where the agent acts beyond its authorized scope (requiring guardrails and human-in-the-loop checkpoints), and tool misuse, where the model invokes the wrong tool or passes incorrect parameters (requiring tracing to monitor execution).
7.  **Core technical components of an Agent:** State management: multiple nodes share read/write access to the same State object. Long-term memory: store and retrieve information across sessions. MCP: a unified connectivity protocol between LLMs and external tools. Skills: reusable high-level instruction sets supporting auto-discovery and dynamic generation. Tool calling: the model emits a structured request; the framework executes it and returns the result. Tracing: visualize the agent's execution chain. Guardrails: input/output validation rules; execution halts if violated. Handoff: transfer control after a subtask completes. Error recovery: retry, rollback, or escalate to human intervention on failure.
8.  **When do you actually need an agent?:** Use an agent when the goal is open-ended, multiple tools must collaborate, intermediate results determine the next step, or state must persist across sessions. Stick to simpler solutions when it's a one-off Q&A (use a prompt), the process is fixed (use a script), compliance is strict (use a human review node), or data determinism is critical (use a database query). The higher the complexity and risk, the more cautious you should be about over-agentifying.

### Recommended Materials / Reference Links

1.  [What is a Large Language Model?](https://www.youtube.com/watch?v=LPZh9BOjkQs) (Video): Build the minimal mental model of LLMs
2.  [Hugging Face LLM Course Chapter 1](https://huggingface.co/learn/llm-course/chapter1/1): Systematic understanding of how LLMs work
3.  [LLM API Getting Started](https://www.youtube.com/watch?v=mnJJPltybBM) (Video): Follow along and write your first API call
4.  [Anthropic: Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api): Official end-to-end API onboarding course
5.  [Z.ai API Developer Docs](https://docs.z.ai/api-reference/introduction): GLM MaaS API intro; OpenAI-compatible; first request in 5 minutes
6.  [Z.ai Coding Plan](https://z.ai/subscribe): Unlock full call quota across the GLM model family
7.  [Claude Code 101](https://anthropic.skilljar.com/claude-code-101): AI coding tool quick-start
8.  [AI Agent Fundamentals](https://www.youtube.com/watch?v=FwOTs4UxQS4) (Video): Foundational agent concepts
9.  [Microsoft: AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners): From concept to code; builds end-to-end agent intuition
10.  [OpenAI Agents SDK Intro](https://openai.github.io/openai-agents-python/): Understand how an agent framework organizes models, tools, and execution
11.  [LangGraph Overview](https://langchain-ai.github.io/langgraph/): Understand how agents are structured and orchestrated
12.  [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/): Agents, tool calling, skills, memory, and long-running execution
13.  [Zread.ai: OpenClaw](https://zread.ai/openclaw/openclaw) / [Hermes](https://zread.ai/NousResearch/hermes-agent): Understand the architectural shifts agents bring at the execution layer

___

