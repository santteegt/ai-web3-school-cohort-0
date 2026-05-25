## Notes

- It is a way for humans and AI Coding Agents to iterate software together
	- Humans own direction, constraints, and acceptance
	- Agents handle generation, modification, search, and part of the engineering actions
- The core of AI Coding is **shortening the engineering feedback loop**
- Once coding speed increases, the **real questions become**: can you describe the task clearly, review the result, control the change scope, and verify that no new bug was introduced?
	- If the feedback loop lacks tests, review, and version control, speed only amplifies disorder
- Vibe coding is NOT "coding by feeling"
	- YOU NEED to manage the repo, task, context, tests, and commit boundaries more clearly
	- **AI cannot take over engineering judgment for you**
- Recommendations:
	- **Tasks should be small**: easier it is for the Agent to produce reviewable results.
	- **Context should be accurate**: matters more than writing a long requirement.
	- **Verification should be hard**
- It is not suitable for unboundedly "rewriting the whole project."
	- **let Agents do more local patches and fewer untraceable large changes.**
- AI Coding is not only about "which model is strongest." You also need to manage models, API keys, context windows, tool permissions, proxy settings, cost, and logs.
	- A good configuration should be reusable by the team, not something every person tweaks casually on their own machine.
	- You need to connect AI Coding to the full engineering process and judge when the Agent should continue and when humans must stop and review.
		- Put AI Coding into normal engineering flow: issue, branch, commit, test, review, merge, release. **DO NOT let AI bypass these flows**
-  A good approach to let a Coding Agent to participate in the engineering process it to:
	- extract task boundaries from issues
	- search related files
	- generate the smallest patch
	- run tests and explain failures
	- supplement changelog or docs
	- write PR summary and verification notes
* **Where It Fits in AI x Web3**
	* Vibe Coding can significantly speed up exploration, especially for hackathons and early prototypes.
	* **But chain-related code is higher risk**
	* AI Coding can help write tests, explain ABI, and generate scripts, but high-risk actions must go through review, simulation, and multi-party confirmation
## Must-read

- [OpenAI Codex CLI Getting Started](https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started): learn the basics of Codex CLI.
- [OpenCLI](https://github.com/jackwener/OpenCLI): learn how Agents can call websites, browser sessions, desktop apps, and local tools through one CLI interface.
