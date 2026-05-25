## Notes

* Frameworks organize models, tools, state, retrieval, evaluation, and deployment into a maintainable system
	* Choosing the wrong framework often implies issues with debug it, test it, or even replace it
* When building production systems:
	* prompts need version management
	* tool calls need schemas
	* Agents need state
	* failures need retries
	* user feedback needs to enter evaluation
	* online behavior needs tracing
* Frameworks do not guarantee model correctness, but they can help you split complex systems into clearer modules
* The most important judgment when choosing a frameworks is ****which layer of complexity does it help you manage, and which complexity does it hide?****
	* A framework expresses system boundaries
	* Understand the workflow first, then decide whether to use a framework
	* Major mistake -> **bend product logic around a framework**
	* **A steadier path** is to first draw inputs, state, tools, outputs, evaluation, and failure paths, then decide which parts deserve a framework.
		* But be careful with "abstracting too early."
		* Wrapping everything in chains and agents without having a clearer picture of your workflow can make later debugging harder.
	* Recommendations:
		* **Keep simple flows simple**: single model call, retrieval and output format do not require a framework
		* **Long workflows need explicit state**: multi-step tasks, tool calls, human confirmation, and failure recovery **should have queryable state, not only chat history.**
		* **Frameworks must be exit-able**: if it makes it hard to change models, vector databases, or deployment methods, the long-term cost will be high. It should not decide product boundaries for you.
* **A framework is not the only abstraction layer**
	* If a  model itself is good at tool calling, JSON mode, long context, and reasoning also affects system design
	* A model with stable tool-calling ability can reduce a lot of parsing and fallback cost
	* conversely, when model capability is unstable, even a good framework needs many guards
* **Frameworks**
	* **LangChain**: it covers model integration, prompts, tool calls, retrievers, agents, output parsers, and other modules
		* It is a component library that helps you compose capabilities
		* useful for quickly connecting model capabilities to external systems,
		* useful for learning common components of AI applications
	* **LangGraph**: leans more toward DAG-based workflows and state machines
		* Represents an Agent or multi-step task as a graph
			* nodes execute actions
			* edges control flow
			* state records the process
		* An explicit graph is more reliable than a long prompt history when a workflow requires:
			* multiple tool calls, retries, human confirmation
			* branching
			* recovery
			* long-running execution
		* Useful when you care about which step the task is on, whether it can recover, and where to resume after failure
	* **OpenAI Agents SDK**: it turns common engineering problems in Agent workflows into composable structures
		* You can use it to organize:
			- Agent instructions and tools
			- handoff between multiple Agents
			- tool calls and structured output
			- guardrails and runtime tracing
	* **DSPy**: focuses on writing prompt / LM **pipelines as optimizable programs**
		* **DSPy do not tune prompts only by feel; bring tasks, data, and metrics into the system**
		* It asks you to define inputs, outputs, modules, and metrics clearly, then **use optimizers to improve prompts or calling strategies**
		* Useful when you have a clear dataset, evaluation metric, and repeatable task
			* e.g. classification, extraction, Q&A, rerank, or complex reasoning chains.
	* **Hermes**: is a model / agent ecosystem oriented around tool calling and structured output, rather than a general-purpose framework
		* When looking at agents like Hermes, do not look only at benchmark scores. Look at whether it can reliably produce the structured output and tool-call format you need.
* **Learning Agents**
	* Learning Agent means a system can improve from feedback, logs, evaluation results, or user corrections.
		* does not necessarily mean training the model
		* it can also mean updating prompts, adjusting retrievers, adding rules, or improving test sets.
	* In production, the most common mistake is turning online feedback directly into behavior changes
		* This can introduce data pollution, unauthorized learning, and unexplained changes.
	* **Learning ability should enter the evaluation loop first, then the production system.**
	* A steadier process is:
		1. Record failure cases.
		2. Label causes manually or with rules.
		3. Add them to eval / regression sets.
		4. Modify prompts, retrieval, tools, or model configuration.
		5. Release only after tests pass.
* **Where It Fits in AI x Web3**
	* Frameworks are responsible for connecting model capabilities to product workflows in AI x Web3
		* reading context, calling tools, generating structured actions
		* recording traces, and entering eval
	* A framework can organize an Agent; it cannot take asset risk on behalf of the user
		* should not replace permissions, signatures, tx simulation, and account rules
	* AI Framework manages prompts, tools, state, eval, and traces.
	- Web3 infra manages accounts, signatures, contracts, txs, and on-chain state.
	- Product layer defines user goals, permission boundaries, confirmation flows, and failure handling.

## Must-read

- [LangChain Agents Docs](https://docs.langchain.com/oss/python/langchain-agents): see how LangChain organizes models, tools, and agent loops
- [LangGraph Docs](https://docs.langchain.com/langgraph): official docs for the basic model of stateful Agents and workflows.
- [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents-sdk/): see the SDK's core concepts and implementation approach.
- [DSPy Documentation](https://dspy.ai/): learn core concepts such as signatures, modules, and optimizers.
- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs/): learn the Hermes Agent toolchain from Nous Research.
- [Nous Hermes Function Calling](https://github.com/NousResearch/Hermes-Function-Calling): see examples of how the Hermes family handles function calling and JSON output.

