## Notes

- **AI behavior that cannot be measured repeatedly cannot be improved reliably.**
- AI system outputs are probabilistic, and user questions are open-ended.
- Without evals:
	- changes to prompts, models, RAG, Agents, and tool calls can only be judged by subjective trial use
	- regression problems will eventually slow the team down
	- You change one prompt; some questions improve while others get worse
	- you switch models; average performance improves, but a critical scenario fails
	- you add RAG; answers become longer, but citations become less accurate.
- The goal of learning eval is not to make a beautiful report. It is to let the team answer: **did this change make key tasks more reliable? Did it introduce new failure modes?**
	- using explicit samples, metrics, grading methods, and regression tests to decide whether the system really got better
	- **Test tasks first, not only models**: users care whether the whole chain completes the task
	- **Protect key failure cases first**: high-risk errors, common questions, and edge cases should enter the regression set.
	- **Evaluation should stay close to the product**: the further it is from real input, the more eval becomes self-comfort
- **Concepts**
	- **Harness**: is the framework that runs evals
		- The value of a harness is **repeatability**
			-  Without repeatable evals, it is hard to compare prompts, models, retrieval strategies, etc
		- It feeds samples, calls the system, collects outputs, runs graders, and records results
		- Minimal harness components:
			- input samples
			- expected outputs or grading rules
			- system version under test
			- model and parameter configuration
			- run logs
			- result report
	- **Golden Set**: the key is to cover real tasks and key failure modes
		- 30-100 high-quality samples are often more than useful
		- **Every time you fix an important bug, consider turning it into a regression sample.**
		- A Golden Set should include:
			- common normal questions
			- boundary questions
			- questions easy to misjudge
			- high-risk questions
			- historical bugs
			- real user feedback samples
	- **LLM-as-Judge**: it works for evaluating open-ended answers, such as summary quality, completeness, format following, and source citation.
		- However, judge models also have bias, miss issues, and can be influenced by output style
		- A steadier approach is:
			- Use rule scoring for fields that can be judged automatically.
			- Use LLM judge for open-ended quality.
			- Keep human spot checks for high-risk samples.
			- Regularly calibrate consistency between judge and human scoring.
	- **Regression**: tests fixes historical problems in place and reruns them for every change.
		- A practical workflow:
			1. A user reports an error.
			2. Reproduce and record the input.
			3. Label the expected output or refusal condition.
			4. Add it to the regression set.
			5. Run it before every release afterward.
	- **Observability**: ability to observe system behavior online.
		- While evals happens before release, observability happens during real use
			- so you know where real users fail, and what to add to the golden set
		- You should record at least:
			- input type and source
			- retrieval results
			- tool calls
			- model output
			- errors and retries
			- user feedback
			- cost and latency
- **Where It Fits in AI x Web3**
	- Eval is even more important in AI x Web3 systems because errors can affect assets, permissions, governance judgment, and on-chain execution
	- Eval does not replace transaction simulation and permission control
	- It helps you continuously discover where the system is unreliable
	- You should especially evaluate:
		- do tx explanations are accurate?
		- do risk warnings miss issues
		- do tool-call parameters go out of bounds?
		- whether the system can refuse uncertain requests
		- ca it identify Prompt Injection
		- whether citations and sources are traceable
		- whether high-risk actions require human check

## Must-read

- [OpenAI Evals API Reference](https://platform.openai.com/docs/api-reference/evals?api-mode=chat): see how the OpenAI platform creates and runs evals.
- [OpenAI: How evals drive the next chapter in AI](https://openai.com/index/evals-drive-next-chapter-of-ai/): understand why evals matter from a product and business perspective.
- [OpenAI Evals GitHub](https://github.com/openai/evals): open-source eval framework and examples, useful for understanding benchmark / grader organization.
- [LangSmith Evaluation Docs](https://docs.smith.langchain.com/evaluation): learn about datasets, experiments, feedback, and tracing for LLM applications.
- [RAGAS Documentation](https://docs.ragas.io/): useful for learning answer quality, context relevance, and faithfulness evaluation in RAG scenarios.
