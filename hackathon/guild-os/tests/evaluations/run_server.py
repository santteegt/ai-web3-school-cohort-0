#!/usr/bin/env python3
"""Wrapper to start the Orchestrator MCP server for evaluation.

Exists because the evaluation harness's argparse conflicts with the ``-m``
flag used by ``python -m src.orchestrator.server``.
"""

from src.orchestrator.server import main

if __name__ == "__main__":
    main()
