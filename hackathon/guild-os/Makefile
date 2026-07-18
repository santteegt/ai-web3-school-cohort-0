.PHONY: test lint coverage inspect eval

test:
	uv run pytest tests/ --cov=src --cov-report=term-missing

lint:
	uv run ruff check src/ tests/

# Same as `test`, plus an HTML report for local drill-down. No
# --cov-fail-under — coverage is reported, not gated (several src/ files,
# e.g. still-stubbed orchestrator tools, are expected to be under-covered
# right now; a hard threshold would be noise, not signal, at this stage).
coverage:
	uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html
	@echo "HTML report: htmlcov/index.html"

inspect:
	npx @modelcontextprotocol/inspector uv run python -m src.orchestrator.server

# Run with the calling agent's own AGENT_WALLET_* env loaded — this is the
# one-time invocation mechanism for both the Specialist's and the
# Orchestrator's ERC-8004 registration (see src/guild/server.py).
inspect-guild:
	npx @modelcontextprotocol/inspector uv run python -m src.guild.server

# Phase 4 evaluation — requires ZAI_API_KEY (or OPENAI_API_KEY) in the environment.
# Uses GLM-4.7 via Z.AI by default. Override with --model and --base-url.
# Spawns the MCP server as a subprocess and runs 10 QA pairs through the LLM.
eval:
	uv run python tests/evaluations/evaluation.py \
		tests/evaluations/orchestrator_eval.xml \
		-t stdio \
		-c uv \
		-a run python tests/evaluations/run_server.py \
		-o output/eval_report.md
