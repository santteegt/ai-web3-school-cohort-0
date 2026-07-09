"""MCP Server Evaluation Harness

Evaluates MCP servers by running test questions against them using an
OpenAI-compatible LLM. Defaults to Z.AI (GLM-4.7) but works with any
OpenAI-compatible provider by changing --base-url and --model.

Requires: ZAI_API_KEY (or OPENAI_API_KEY) in the environment.
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
import traceback
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from connections import create_connection
from openai import OpenAI

DEFAULT_BASE_URL = "https://api.z.ai/api/paas/v4/"
DEFAULT_MODEL = "glm-4.7"

EVALUATION_PROMPT = """You are an AI assistant with access to tools.

When given a task, you MUST:
1. Use the available tools to complete the task
2. Provide summary of each step in your approach, wrapped in <summary> tags
3. Provide feedback on the tools provided, wrapped in <feedback> tags
4. Provide your final response, wrapped in <response> tags

Summary Requirements:
- In your <summary> tags, you must explain:
  - The steps you took to complete the task
  - Which tools you used, in what order, and why
  - The inputs you provided to each tool
  - The outputs you received from each tool
  - A summary for how you arrived at the response

Feedback Requirements:
- In your <feedback> tags, provide constructive feedback on the tools:
  - Comment on tool names: Are they clear and descriptive?
  - Comment on input parameters: Are they well-documented? Are required vs optional parameters clear?
  - Comment on descriptions: Do they accurately describe what the tool does?
  - Comment on any errors encountered during tool usage: Did the tool fail to execute? Did the tool return too many tokens?
  - Identify specific areas for improvement and explain WHY they would help
  - Be specific and actionable in your suggestions

Response Requirements:
- Your response should be concise and directly address what was asked
- Always wrap your final response in <response> tags
- If you cannot solve the task return <response>NOT_FOUND</response>
- For numeric responses, provide just the number
- For IDs, provide just the ID
- For names or text, provide the exact text requested
- Your response should go last"""


def parse_evaluation_file(file_path: Path) -> list[dict[str, Any]]:
    """Parse XML evaluation file with qa_pair elements."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        evaluations = []

        for qa_pair in root.findall(".//qa_pair"):
            question_elem = qa_pair.find("question")
            answer_elem = qa_pair.find("answer")

            if question_elem is not None and answer_elem is not None:
                evaluations.append({
                    "question": (question_elem.text or "").strip(),
                    "answer": (answer_elem.text or "").strip(),
                })

        return evaluations
    except Exception as e:
        print(f"Error parsing evaluation file {file_path}: {e}")
        return []


def extract_xml_content(text: str, tag: str) -> str | None:
    """Extract content from XML tags."""
    pattern = rf"<{tag}>(.*?)</{tag}>"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches[-1].strip() if matches else None


def convert_tools_to_openai(tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert MCP tool definitions to OpenAI function-calling format.

    MCP tools come as {name, description, input_schema}. OpenAI expects
    {type: "function", function: {name, description, parameters}}.
    """
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("input_schema", {"type": "object", "properties": {}}),
            },
        }
        for tool in tools
    ]


def _extract_tool_text(result: Any) -> str:
    """Extract human-readable text from an MCP call_tool result.

    MCP returns a list of content blocks (TextContent, etc.). We pull the
    .text field from each and join them. Falls back to JSON serialization.
    """
    if isinstance(result, list):
        parts: list[str] = []
        for block in result:
            if hasattr(block, "text"):
                parts.append(block.text)
            elif hasattr(block, "model_dump"):
                parts.append(json.dumps(block.model_dump(), default=str))
            else:
                parts.append(str(block))
        return "\n".join(parts) if parts else str(result)
    if isinstance(result, str):
        return result
    return json.dumps(result, indent=2, default=str)


async def agent_loop(
    client: OpenAI,
    model: str,
    question: str,
    tools: list[dict[str, Any]],
    connection: Any,
) -> tuple[str | None, dict[str, Any]]:
    """Run the agent loop with MCP tools via an OpenAI-compatible LLM."""
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": EVALUATION_PROMPT},
        {"role": "user", "content": question},
    ]

    response = await asyncio.to_thread(
        client.chat.completions.create,
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096,
        # For harder eval questions (multi-step reasoning), enable thinking:
        #   extra_body={"thinking": {"type": "enabled"}},
    )

    message = response.choices[0].message
    _append_assistant(messages, message)

    tool_metrics: dict[str, Any] = {}

    while response.choices[0].finish_reason == "tool_calls":
        for tool_call in message.tool_calls or []:
            tool_name = tool_call.function.name
            try:
                tool_input = json.loads(tool_call.function.arguments)
            except (json.JSONDecodeError, TypeError):
                tool_input = {}

            tool_start_ts = time.time()
            try:
                tool_result = await connection.call_tool(tool_name, tool_input)
                tool_response = _extract_tool_text(tool_result)
            except Exception as e:
                tool_response = f"Error executing tool {tool_name}: {e}\n"
                tool_response += traceback.format_exc()
            tool_duration = time.time() - tool_start_ts

            if tool_name not in tool_metrics:
                tool_metrics[tool_name] = {"count": 0, "durations": []}
            tool_metrics[tool_name]["count"] += 1
            tool_metrics[tool_name]["durations"].append(tool_duration)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_response,
            })

        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096,
            # For harder eval questions (multi-step reasoning), enable thinking:
            #   extra_body={"thinking": {"type": "enabled"}},
        )
        message = response.choices[0].message
        _append_assistant(messages, message)

    return message.content, tool_metrics


def _append_assistant(
    messages: list[dict[str, Any]], message: Any
) -> None:
    """Append an assistant message (with optional tool_calls) to the list."""
    msg: dict[str, Any] = {"role": "assistant", "content": message.content}
    if message.tool_calls:
        msg["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in message.tool_calls
        ]
    messages.append(msg)


async def evaluate_single_task(
    client: OpenAI,
    model: str,
    qa_pair: dict[str, Any],
    tools: list[dict[str, Any]],
    connection: Any,
    task_index: int,
) -> dict[str, Any]:
    """Evaluate a single QA pair with the given tools."""
    start_time = time.time()

    print(f"Task {task_index + 1}: Running task with question: {qa_pair['question']}")
    response, tool_metrics = await agent_loop(
        client, model, qa_pair["question"], tools, connection
    )

    response_value = extract_xml_content(response or "", "response")
    summary = extract_xml_content(response or "", "summary")
    feedback = extract_xml_content(response or "", "feedback")

    duration_seconds = time.time() - start_time

    return {
        "question": qa_pair["question"],
        "expected": qa_pair["answer"],
        "actual": response_value,
        "score": int(response_value == qa_pair["answer"]) if response_value else 0,
        "total_duration": duration_seconds,
        "tool_calls": tool_metrics,
        "num_tool_calls": sum(
            len(metrics["durations"]) for metrics in tool_metrics.values()
        ),
        "summary": summary,
        "feedback": feedback,
    }


REPORT_HEADER = """
# Evaluation Report

## Summary

- **Accuracy**: {correct}/{total} ({accuracy:.1f}%)
- **Average Task Duration**: {average_duration_s:.2f}s
- **Average Tool Calls per Task**: {average_tool_calls:.2f}
- **Total Tool Calls**: {total_tool_calls}

---
"""

TASK_TEMPLATE = """
### Task {task_num}

**Question**: {question}
**Ground Truth Answer**: `{expected_answer}`
**Actual Answer**: `{actual_answer}`
**Correct**: {correct_indicator}
**Duration**: {total_duration:.2f}s
**Tool Calls**: {tool_calls}

**Summary**
{summary}

**Feedback**
{feedback}

---
"""


async def run_evaluation(
    eval_path: Path,
    connection: Any,
    client: OpenAI,
    model: str,
) -> str:
    """Run evaluation with MCP server tools."""
    print("🚀 Starting Evaluation")

    raw_tools = await connection.list_tools()
    tools = convert_tools_to_openai(raw_tools)
    print(f"📋 Loaded {len(tools)} tools from MCP server")

    qa_pairs = parse_evaluation_file(eval_path)
    print(f"📋 Loaded {len(qa_pairs)} evaluation tasks")

    results = []
    for i, qa_pair in enumerate(qa_pairs):
        print(f"Processing task {i + 1}/{len(qa_pairs)}")
        result = await evaluate_single_task(
            client, model, qa_pair, tools, connection, i
        )
        results.append(result)

    correct = sum(r["score"] for r in results)
    accuracy = (correct / len(results)) * 100 if results else 0
    average_duration_s = (
        sum(r["total_duration"] for r in results) / len(results) if results else 0
    )
    average_tool_calls = (
        sum(r["num_tool_calls"] for r in results) / len(results) if results else 0
    )
    total_tool_calls = sum(r["num_tool_calls"] for r in results)

    report = REPORT_HEADER.format(
        correct=correct,
        total=len(results),
        accuracy=accuracy,
        average_duration_s=average_duration_s,
        average_tool_calls=average_tool_calls,
        total_tool_calls=total_tool_calls,
    )

    report += "".join([
        TASK_TEMPLATE.format(
            task_num=i + 1,
            question=qa_pair["question"],
            expected_answer=qa_pair["answer"],
            actual_answer=result["actual"] or "N/A",
            correct_indicator="✅" if result["score"] else "❌",
            total_duration=result["total_duration"],
            tool_calls=json.dumps(result["tool_calls"], indent=2),
            summary=result["summary"] or "N/A",
            feedback=result["feedback"] or "N/A",
        )
        for i, (qa_pair, result) in enumerate(zip(qa_pairs, results))
    ])

    return report


def parse_headers(header_list: list[str]) -> dict[str, str]:
    """Parse header strings in format 'Key: Value' into a dictionary."""
    headers = {}
    if not header_list:
        return headers

    for header in header_list:
        if ":" in header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        else:
            print(f"Warning: Ignoring malformed header: {header}")
    return headers


def parse_env_vars(env_list: list[str]) -> dict[str, str]:
    """Parse environment variable strings in format 'KEY=VALUE' into a dictionary."""
    env = {}
    if not env_list:
        return env

    for env_var in env_list:
        if "=" in env_var:
            key, value = env_var.split("=", 1)
            env[key.strip()] = value.strip()
        else:
            print(f"Warning: Ignoring malformed environment variable: {env_var}")
    return env


async def main():
    parser = argparse.ArgumentParser(
        description="Evaluate MCP servers using test questions (OpenAI-compatible LLM)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate with Z.AI defaults (GLM-4.7)
  python evaluation.py -t stdio -c uv -a run python run_server.py eval.xml

  # Evaluate with a custom OpenAI-compatible provider
  python evaluation.py -t stdio -c python -a server.py \\
      --base-url https://api.openai.com/v1 --model gpt-4o eval.xml

  # Evaluate an HTTP MCP server
  python evaluation.py -t http -u https://example.com/mcp eval.xml
        """,
    )

    parser.add_argument("eval_file", type=Path, help="Path to evaluation XML file")
    parser.add_argument(
        "-t", "--transport",
        choices=["stdio", "sse", "http"],
        default="stdio",
        help="Transport type (default: stdio)",
    )
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"LLM model name (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"OpenAI-compatible API base URL (default: {DEFAULT_BASE_URL})",
    )

    stdio_group = parser.add_argument_group("stdio options")
    stdio_group.add_argument("-c", "--command", help="Command to run MCP server (stdio only)")
    stdio_group.add_argument("-a", "--args", nargs="+", help="Arguments for the command (stdio only)")
    stdio_group.add_argument("-e", "--env", nargs="+", help="Environment variables in KEY=VALUE format (stdio only)")

    remote_group = parser.add_argument_group("sse/http options")
    remote_group.add_argument("-u", "--url", help="MCP server URL (sse/http only)")
    remote_group.add_argument("-H", "--header", nargs="+", dest="headers", help="HTTP headers in 'Key: Value' format (sse/http only)")

    parser.add_argument("-o", "--output", type=Path, help="Output file for evaluation report (default: stdout)")

    args = parser.parse_args()

    if not args.eval_file.exists():
        print(f"Error: Evaluation file not found: {args.eval_file}")
        sys.exit(1)

    api_key = os.getenv("ZAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set ZAI_API_KEY (or OPENAI_API_KEY) in the environment.")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=args.base_url)

    headers = parse_headers(args.headers) if args.headers else None
    env_vars = parse_env_vars(args.env) if args.env else None

    try:
        connection = create_connection(
            transport=args.transport,
            command=args.command,
            args=args.args,
            env=env_vars,
            url=args.url,
            headers=headers,
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"🔗 Connecting to MCP server via {args.transport}...")
    print(f"🤖 LLM: {args.model} @ {args.base_url}")

    async with connection:
        print("✅ Connected successfully")
        report = await run_evaluation(args.eval_file, connection, client, args.model)

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report)
            print(f"\n✅ Report saved to {args.output}")
        else:
            print("\n" + report)


if __name__ == "__main__":
    asyncio.run(main())
