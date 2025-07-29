import click

import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport

from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import Response

import uvicorn

async def run_mcp_in_e2b(cmd: str) -> str:
    mcp_server_url = "http://127.0.0.1:12020/sse"
    print(f"run uvx {cmd} in e2b, url={mcp_server_url}")
    return mcp_server_url


@click.command()
@click.option("--port", default=18080, help="Port to listen on for SSE")
def main(port: int) -> int:
    app = Server("runmcp_in_e2b")

    @app.call_tool()
    async def runmcp(
        name: str, arguments: dict
    )-> list[types.TextContent]:
        print("=== recv call_tool runmcp ===")

        if name != "runmcp":
            raise ValueError(f"Unknown tool: {name}")
        if "cmd" not in arguments:
            raise ValueError("Missing required argument 'url'")

        print(f"call run_mcp_in_e2b({arguments["cmd"]})")
        result = await run_mcp_in_e2b(arguments["cmd"])

        return [types.TextContent(type="text",text=result)]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="runmcp",
                description="Run Mcp Server in E2B Sandbox",
                inputSchema={
                    "type": "object",
                    "required": ["cmd"],
                    "properties": {
                        "cmd": {
                            "type": "string",
                            "description": "Run Mcp by uvx command, not inculde uvx",
                        }
                    },
                },
            )
        ]


    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        async with sse.connect_sse(
                request.scope, request.receive, request._send
        ) as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )
        return Response()

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

    print(f"MCP Server runmcp_in_e2b run on localhost port={port}")
    uvicorn.run(starlette_app, host="localhost", port=port)

    return 0

if __name__ == '__main__':
    main()
