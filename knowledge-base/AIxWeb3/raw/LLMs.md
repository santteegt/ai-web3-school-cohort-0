## Notes

- It's important to understand how a model handles tokens, context, patterns, and uncertainty before you can know when to trust it and when to verify it.
- The goal of learning LLMs is not to memorize model parameters. It is to build one judgment: **model output is a candidate result, not the fact itself; model capability is an entry point for reasoning, not the final verification.**
- **An LLM generates outputs that are probabilistically reasonable, not facts that are trustworthy by default.**
	- They can help you understand, summarize, generate, and plan, but they cannot independently serve as the source of truth, the permission judge, or the final executor
	- **Treat the model as a reasoning layer, not a truth source**: key facts must come from databases, APIs, logs, documentation sources, or other trusted systems.
	- **Turn outputs into checkable objects**: summaries, classifications, plans, and action suggestions should land in schemas, parameters, citations, or logs whenever possible, not only in natural language.
	- **Expose uncertainty early**: when the model does not know, the material is outdated, or context is insufficient, the system should degrade explicitly instead of inventing a smooth answer.
- **Concepts**
	- **Tokens**: a segment produced by the tokenizer.
		- Tokens directly affect three things: how much context can fit, how much a call costs, and whether the model can see key information completely
	- **Embeddings**: maps text, code, or another object into a vector so the system can measure whether two things are semantically close.
		- Good at helping you find relevant material
		- Not suitable for deciding whether a conclusion is correct on their own.
	- **Transformer**: core architecture with attention mechanism
		- It can attend to different positions in the input while generating, learning relationships between words, code, facts, and context.
		- Transformer models are good at finding patterns in context
		- But can also produce wrong summaries when context is missing or similar patterns mislead them.
		- **Transformers give models strong pattern-composition ability, but not final authority over facts**
	- **Hallucination**
		- Do not handle hallucination only by "writing a better prompt." A more reliable approach is to connect model output to external verification: source citations, schema validation, rule checks, human confirmation, and audit logs.
	- **Multimodal**: can process text, images, audio, video, or screenshots
		- multimodal input also needs boundaries via structured key judgements and trusted sources
- **Where It Fits in AI x Web3**
	- **LLMs sit in the understanding and generation layer of AI x Web3 systems** 
		- Turn user goals into discussable plans
		- Explain complex on-chain data in human language
		- Connect documents and code into executable thinking.
- **The closer an LLM gets to the execution layer, the more the system must turn its natural-language output into verifiable objects.**

## Must-read

* [OpenAI Text Generation Guide](https://platform.openai.com/docs/guides/text-generation): learn how LLMs receive input, generate text, and return structured content through APIs.
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer): see directly how different text, code, addresses, and JSON are split into tokens.
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings): understand the basic role of embeddings in search, clustering, and RAG.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762): the original Transformer paper, useful for building technical background around attention and modern model architecture.
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/): understand common risks such as Prompt Injection, sensitive information disclosure, and excessive agency from a security perspective.*