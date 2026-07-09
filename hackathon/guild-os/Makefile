.PHONY: test lint inspect eval

test:
	uv run pytest tests/

lint:
	uv run ruff check src/ tests/

inspect:
	npx @modelcontextprotocol/inspector uv run python -m src.orchestrator.server

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
