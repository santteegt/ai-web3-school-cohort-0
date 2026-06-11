"""Check MCP server handler registration and call_tool dispatch."""
import asyncio
import json
import mcp.types as types
from mcp.server import Server


def create_test_server():
    server = Server("test")

    @server.list_tools()
    async def list_tools():
        return [types.Tool(
            name="test_tool",
            description="A test",
            inputSchema={"type": "object", "properties": {}, "required": []},
        )]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        return [types.TextContent(type="text", text=json.dumps({"ok": True}))]

    return server


async def main():
    server = create_test_server()
    print("Handler keys:", list(server.request_handlers.keys()))

    # Use the actual type as key
    call_handler = server.request_handlers.get(types.CallToolRequest)
    print("call_handler:", call_handler)

    # Build a proper request
    request = types.CallToolRequest(
        method="tools/call",
        params=types.CallToolRequestParams(
            name="test_tool",
            arguments={},
        ),
    )
    result = await call_handler(request)
    print("result type:", type(result))
    print("result:", result)

    # The result is ServerResult - it wraps the actual result
    # Check what's inside
    print("has root:", hasattr(result, "root"))
    if hasattr(result, "root"):
        print("root type:", type(result.root))
        inner = result.root
        print("inner:", inner)
        if hasattr(inner, "content"):
            print("inner.content[0]:", inner.content[0])
            if hasattr(inner.content[0], "text"):
                print("inner.content[0].text:", inner.content[0].text)


asyncio.run(main())
