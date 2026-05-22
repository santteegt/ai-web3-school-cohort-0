## Notes

* A Prompt is the interface design between you and the model
* An executable communication protocol that includes:
	* task goals
	* input boundaries
	* output formats
	* failure handling
	* security rules
* **The value of a prompt lies in turning a vague task into a work instruction that the model can execute stably
* If a prompt has no boundaries, the model will naturally "complete" the missing information
* **A good prompt is not about making the model more confident, but about letting the model stop at the right time.**
* **First principles**
	* **Prompts are soft constraints, not security boundaries**
		* Real boundaries must be borne by code, permissions, verification, and auditing
		* The prompt should be responsible for expressing the task, and the system should be responsible for executing constraints.
	* **Instruction layers must be clear**: System rules, developer rules, user goals, and retrieved content should not be mixed together.
	- **Output formats must be machine-verifiable**: Critical results should as much as possible be carried by JSON schemas, function parameters, or explicit fields.
	- **High-risk actions cannot rely solely on prompt interception**: Actions such as writing to a database, sending messages, calling external tools, executing payments, or signing must also undergo code-layer verification and human checks.
- A prompt should not bear the burden of security alone. A more stable chain is:
	1. Prompt defines the task and output format.
	2. Context provides trusted data and source boundaries.
	3. Model generates an explanation or candidate action.
	4. Code verifies the schema and business rules.
	5. Guard / simulation checks the on-chain impact.
	6. Human check confirms high-risk actions.
- **Concepts**
	- **Instruction**: task rule given to the model. It should answer: 
			- what is your role
			- what are you to complete
			- what are you prohibited from doing
			- how to handle uncertain information
			- what form the output should take.
		- Instructions must specifically distinguish between "explanation" and "execution."
		- **A practical way to write an instruction is to split it into four segments**:
			- Task Goal
			- Available Inputs
			- Prohibited Behaviors
			- Output Format and Failure Format
	- **Few-Shot**: the model imitate the judgment method and output format of the examples.
		- But few-shot also brings maintenance costs -> **they are test assets that must be maintained together with evaluation sets**
	- **Structured Output**: the model return results on a schema-constrained format.
		- It is important for application development because subsequent systems process explicit fields, not prose
	- **Prompt injection**: it is especially dangerous in Agent scenarios with access to private internal systems. Preventive actions include:
		- Mark external content as untrusted data.
		- Perform parameter verification before tool calls.
		- Force sensitive actions to go through an allowlist and human approval.
		- Do not hand over secrets, primary permissions, and irreversible actions to the model.
- **Where It Fits in AI x Web3**
	- Prompts sit between user goals and model behavior.

## Must-read

- [OpenAI Prompting Guide](https://platform.openai.com/docs/guides/prompting): Understand prompt management, variables, versions, and team collaboration.
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering): See practical methods for clear instructions, examples, context organization, and output formats.
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs): Suitable for connecting model outputs to subsequent code, tools, and verification processes.
- [OpenAI Safety Best Practices](https://platform.openai.com/docs/guides/safety-best-practices): See basic suggestions for model applications in security, abuse prevention, and pre-launch checks.