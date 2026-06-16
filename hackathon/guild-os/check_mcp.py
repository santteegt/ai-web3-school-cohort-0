"""Quick check of MCP SDK API."""
from mcp.server import Server
import mcp.types as types

r = types.CallToolResult(content=[types.TextContent(type="text", text="hello")])
print("type:", type(r))
print("fields:", list(r.model_fields))
print("content[0].text:", r.content[0].text)

# Check if .root exists
print("has root:", hasattr(r, "root"))

# Check Server request_handlers
s = Server("test")
print("server name:", s.name)
print("server request_handlers type:", type(s.request_handlers))
