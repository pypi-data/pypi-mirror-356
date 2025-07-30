import logging
import os
import aiohttp
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from typing import Any, Dict, List

logger = logging.getLogger("robosystems_mcp")
logger.info("Starting RoboSystems MCP Server")


class RoboSystemsAPIClient:
    """HTTP client for RoboSystems API."""
    
    def __init__(self, base_url: str, api_key: str, graph_id: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.graph_id = graph_id
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from the API."""
        url = f"{self.base_url}/v1/{self.graph_id}/mcp/tools"
        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
            data = await response.json()
            return data.get('tools', [])
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool via the API."""
        url = f"{self.base_url}/v1/{self.graph_id}/mcp/call-tool"
        payload = {'name': name, 'arguments': arguments}
        async with self.session.post(url, json=payload) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
            data = await response.json()
            return data.get('result', {})


async def main():
    """Main MCP server entry point using HTTP API."""
    # Get configuration from environment
    base_url = os.getenv('ROBOSYSTEMS_API_URL', 'http://localhost:8000')
    api_key = os.getenv('ROBOSYSTEMS_API_KEY')
    graph_id = os.getenv('ROBOSYSTEMS_GRAPH_ID', 'default')
    
    if not api_key:
        raise ValueError("ROBOSYSTEMS_API_KEY environment variable is required")
    
    logger.info(f"Connecting to RoboSystems API at {base_url} for graph {graph_id}")
    
    async with RoboSystemsAPIClient(base_url, api_key, graph_id) as client:
        # Test connection
        try:
            tools = await client.get_tools()
            tool_names = [t.get('name', 'unknown') for t in tools]
            logger.info(f"Connected successfully. Available tools: {', '.join(tool_names)}")
        except Exception as e:
            logger.error(f"Failed to connect to API: {e}")
            raise

        server = Server("robosystems-mcp")

        @server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools from the API."""
            try:
                tools_data = await client.get_tools()
                tools = []
                for tool_data in tools_data:
                    tools.append(types.Tool(
                        name=tool_data['name'],
                        description=tool_data.get('description', ''),
                        inputSchema=tool_data.get('inputSchema', {})
                    ))
                return tools
            except Exception as e:
                logger.error(f"Error listing tools: {e}")
                return []

        @server.call_tool()
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
            """Handle tool execution via the API."""
            try:
                result = await client.call_tool(name, arguments or {})
                
                # Convert API response to MCP content
                if result.get('type') == 'text':
                    return [types.TextContent(type="text", text=result['text'])]
                else:
                    # Fallback: serialize as JSON
                    import json
                    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [types.TextContent(type="text", text=f"Error: {str(e)}")]

        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("Server running with stdio transport")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="robosystems-mcp",
                    server_version="0.2.10",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
