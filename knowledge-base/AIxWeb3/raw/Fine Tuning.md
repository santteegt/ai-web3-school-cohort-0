## Notes

- It is useful for scenarios where a model needs to learn a certain format, style, domain task, or behavior pattern more consistently
- The value of fine-tuning is to make the model more consistent on a class of tasks, not to make it magically know the latest facts.
	- It should have data, evaluation, and a clear goal properly defined
		- **Have evals before fine-tuning**: otherwise you do not know whether the tuned model improved or only became smoother on a few samples.
		- **Fix data before fixing the model**: bad data trains bad habits more stably.
		- **Do not use fine-tuning to store real-time knowledge**
- However, in real engineering, fine-tuning is often not the first step. You should first ask:
	- Is the prompt unclear?
	- Is context missing?
	- Did retrieval fail to get the right material?
	- Does the output format lack a schema?
	- Is the model itself not capable enough?
	- Is there already an eval proving the problem is stable?
- Fine-tuning can make the model look more like your data, but it does not automatically bring factual correctness, permission safety, reliable citations, or safe tool calling
- **Concepts**
	- **Supervised Fine-Tuning (SFT)**: uses input and expected-output samples to teach the model how to answer a certain class of tasks.
		- It is suitable for:
			- fixed-format output
			- specific tone or style
			- specific task flows
			- domain terminology and answer habits
			- tool-call style
		- SFT is very sensitive to data quality
	- **Low Rank Adaptation (LoRA)**: is a parameter-efficient fine-tuning method. Instead of updating all model parameters, it trains smaller adapter parameters, reducing training cost and VRAM requirements.
		- Commonly used for open-source model fine-tuning
		- Fits teams with limited resources who want to quickly experiment on specific tasks
		- It educes experiment cost, but it is not magic
		- Task definition, data quality, and evaluation still determine the final result
		- LoRA is a subset of PEFT
	- **Parameter-Efficient Fine-Tuning (PEFT)**: adapt a model to a task or domain through smaller parameter changes.
		- Suitable scenarios:
			- a large model where full fine-tuning is too expensive
			- a clearly scoped task
			- a medium-sized dataset
			- a need to test multiple adapter versions in parallel
	- **Dataset**: the core asset of fine-tuning
		- It needs a clear task definition, input sources, output standards, quality checks, and split strategy
		- There are training, validation, test & regression sets
	- **Overfitting**: happens when the model memorizes training data too tightly and performs worse on new samples
		- validation and training sets are too similar
		- training runs for too many epochs
		- model looks good on your prepared examples, but falls apart when real users ask questions
* **Where It Fits in AI x Web3**
	* Fine-tuning can be used for specific tasks such as transaction-explanation style, governance-summary format, risk-label output, contract-comment style, and tool-call style
	* Fine-tuning can make the model understand your task format better, but **it cannot directly turn the model into a trusted execution layer**
## Must-read

- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning): learn fine-tuning use cases, data format, and training flow.
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/index): learn parameter-efficient fine-tuning methods such as LoRA and adapters.
- [Unsloth Docs](https://unsloth.ai/docs): understand a lightweight fine-tuning path that is closer to hands-on practice.
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685): the original LoRA paper, useful for understanding low-rank adaptation.
- [TRL Documentation](https://huggingface.co/docs/trl/index): learn tools for SFT, preference optimization, and related training flows.
- [OpenAI Evals API Reference](https://platform.openai.com/docs/api-reference/evals?api-mode=chat): use evals before and after fine-tuning to determine whether performance actually improved.
