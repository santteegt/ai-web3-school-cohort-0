## Notes

- MCP tries to standardize the connection between models and external tools, data sources, and application context
- It solves how the model uses external capabilities in a describable, reusable, discoverable and manageable way
	- What capabilities a server exposes
	- what the input schema is and what result it returns
	- which actions have side effects
- MCP aims to abstract this connection layer into a protocol
	- the client interacts with the model
	- the server exposes **resources, tools, and prompts**
- **Tools need schemas**: otherwise tool calls become natural-language parameter guessing
- **Permissions must also hold outside the protocol**: real authorization, audit, and isolation still need to be implemented by the system
- **Errors must be transmissible**: returned clearly instead of leaving the model to guess.
- **Server**: provides capabilities so AI clients can read information or call actions
	- I can expose resources, tools, prompts, and more
	- Design boundaries:
		- which resources are exposed
		- which tools are read-only and which have side effects
		- whether parameter schemas are clear
		- how errors are returned
		- whether user authorization is required
		- where logs and audits are recorded
- **Client**: connects the model and MCP servers
	- Discovers server capabilities
	- Gives tool information to the model
	- Turns model-generated call requests back into protocol messages
	- Handles user confirmation, permission prompts, session isolation, and tool-call display
- **Tool Schema**: describes a tool's name, purpose, parameters, return value, and constraints
	- If a tool schema is vague, the model will fill gaps with wrong parameters
	- A good tool schema should explain:
		- when this tool should be used
		- what each parameter means
		- which fields are required
		- whether it changes external state
		- what is returned on failure
- **Permission**: is the most underestimated issue when MCP enters real products
	- Before an MCP server exposes capability, it should define its permission model
	- Different tool calls have different risk levels
	- Permission should at least distinguish:
		- read-only vs write
		- current-session authorization vs long-term authorization
		- whether user confirmation is required
		- whether sensitive information can be accessed
		- whether external side effects are created
		- whether the action is revocable and auditable
- **Where It Fits in AI x Web3**
	- MCP can serve as the interface layer for Agents connecting to on-chain tools and developer tools
	- MCP itself is not a wallet-security solution
		- MCP handles tool discovery and call format
		- Web3 account system handles final permission and execution boundaries
## Must-read

* [Model Context Protocol Architecture](https://modelcontextprotocol.io/docs/learn/architecture): official architecture explanation for understanding the division of labor between client, server, tools, and resources.
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2024-11-05/basic/index): the protocol source text, useful for message formats and JSON-RPC basics.
- [OpenAI MCP Overview](https://platform.openai.com/docs/mcp/overview): understand how the OpenAI API / ChatGPT ecosystem connects to MCP servers.
- [Claude Code MCP Docs](https://docs.claude.com/en/docs/claude-code/overview): see how MCP is used in local developer tools.
- [GitHub: modelcontextprotocol/mcp-docs](https://github.com/modelcontext-protocol/mcp-docs): the official docs repository, useful for tracking documentation and specification changes.

