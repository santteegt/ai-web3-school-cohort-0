## Notes
* **Context is the information space the model can see, use, and be influenced by in a current session**
	* The system must decide what enters context, with what identity, and how it exits after expiration.
* The **hard part** is to separate **system rules, user goals, historical state, tool results, and external documents.**
* If the context is wrong, missing, or outdated, even a strong model will produce unreliable answers => **context design problems**
	* treating an untrusted webpage as a system instruction,
	* treating old docs as the latest rules,
	* treating a user wish as fact
	* leaking the previous task state into the next task
	* if the model cannot see the real tool result, it can only guess
* Context is not simply long-text concatenation. It is an information governance problem
	* You need to **label each type of information by source, freshness, permission, and trust level**
	* Otherwise the model will process "what the user said," "what a webpage wrote," "what the chain returned," and "what the system requires"
	* **Trusted sources must be explicitly marked**: system state, user input, retrieved documents, and tool results should be placed in separate zones.
	- **Context must be refreshable**: state, configuration, permissions, prices, versions, and task progress cannot be cached for a long time and then reused as if still current.
	- **Memory must be revocable**: user preferences and historical tasks can improve the experience, but they must not become hidden permissions or permanent identity assumptions.
- A reliable Agent context include these layers:
	- **Instruction layer**: system rules, tool-use rules, prohibitions.
	- **Task layer**: user goal and current session parameters.
	- **Fact layer**: on-chain state, tool results, simulation.
	- **Knowledge layer**: documents, standards, forums, historical cases.
	- **Memory layer**: user preferences and project configuration.
- **The clearer the layers, the easier it becomes to do permission control, Prompt Injection defense, and audit.**
- **Concepts**
	- **Context window**: max amount of context a model can process in one request
		- Longer context windows does not imply the model will use every detail perfectly.
			- Problem: "the model saw it but did not focus on the right thing."
		- In real products, the context window should be used **together with retrieval, summarization, and structured data**
			- Key state should be provided directly
			- Long documents should be fetched on demand
			- Low-trust content should be isolated and labeled
	- **Context Engineering**: is the design of how context enters the model
		- Its goal is to **let the model work at the right information layer.**
		- Includes:
			- choosing data sources
			- ordering, trimming, labeling sources
			- isolating untrusted content
			- deciding which information must be re-queried every time
		- A stable tool-using Agent context should include:
			- current task state
			- tool return values
			- relevant logs or evidence
			- trusted data sources
			- external check results
			- the user's original intent
			- system prohibitions and output schema
	- **Memory**: information retained across requests
		- e.g. user preferences, historical tasks, commonly used wallets, project configuration, and previous analysis results
		- Memory can make an Agent smoother to use, but it also introduces hidden risk
			- e.g. remember that "the user has high risk tolerance" and loosen confirmation on high-risk transactions.
		- Memory cannot replace real-time authorization
			- **Any memory related to identity, permissions, assets, or external side effects must be rebound to the current session and current authorization.**
	- **Knowledge Base**: is an external repository the system can retrieve from
		- Good at solving model knowledge staleness
		- It does not automatically guarantee correctness
		- It needs to maintain source, update time, version, applicable network, and deprecation status
		- A knowledge base should at least record
			- document source and URL
			- last update time
			- applicable protocol version
			- applicable version or runtime environment
			- whether it comes from an official source or a third party
			- whether human review is needed
- **Where It Fits in AI x Web3**
	- Context is the entry point connecting models with real systems
	- AI is responsible for reasoning while context determines whether the model sees user imagination, outdated documentation, or verifiable on-chain facts

## Must-read

* [OpenAI Text Generation Guide](https://platform.openai.com/docs/guides/text-generation): understand model inputs, message roles, outputs, and context management basics.
* [LangChain Retrieval Documentation](https://docs.langchain.com/oss/python/integrations/retrievers/index): learn how different retrievers send external knowledge into model context.