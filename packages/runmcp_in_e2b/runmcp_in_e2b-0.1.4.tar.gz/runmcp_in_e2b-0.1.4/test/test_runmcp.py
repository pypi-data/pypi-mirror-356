import asyncio

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client("http://localhost:18080/sse", sse_read_timeout=5) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # list available tools
            response = await session.list_tools()
            tools = response.tools
            print("\n list_tools:", [(tool.name, tool.description) for tool in tools])

            # call the runmcp tool
            result = await session.call_tool("runmcp", {"cmd": "mcp-server-fetch"})
            print('\n call_tool runmcp result:', result)


asyncio.run(main())