import asyncio

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client



async def main():
    async with sse_client("http://localhost:18080/sse", sse_read_timeout=5) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            # List available tools
            response = await session.list_tools()
            tools = response.tools
            print("\nlist tools:", [(tool.name, tool.description) for tool in tools])

            # Call the fetch tool
            result = await session.call_tool("runmcp", {"cmd": "mcp-server-fetch"})
            print(f'--- call runmcp result ---: {result}')


asyncio.run(main())