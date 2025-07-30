import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.shared._httpx_utils import create_mcp_http_client
import os

MISRA_RULE_URL = "http://cisivi.lge.com:8060/files/copilot_md/common/Misracpp2008Guidelines_High_en.md"
LGEDV_RULE_URL = "/home/worker/src/copilot_md/LGEDVRuleGuide.md"


async def fetch_misra_rule(url: str) -> list[
    types.TextContent | types.ImageContent | types.AudioContent | types.EmbeddedResource
]:
    headers = {
        "User-Agent": "MCP MISRA Rule Fetcher"
    }
    async with create_mcp_http_client(headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return [types.TextContent(type="text", text=response.text)]


async def fetch_lgedv_rule(url: str) -> list[
    types.TextContent | types.ImageContent | types.AudioContent | types.EmbeddedResource
]:
    headers = {
        "User-Agent": "MCP LGEDV Rule Fetcher"
    }
    if url.startswith("http://") or url.startswith("https://"):
        async with create_mcp_http_client(headers=headers) as client:
            response = await client.get(url)
            response.raise_for_status()
            return [types.TextContent(type="text", text=response.text)]
    else:
        # Treat as local file path
        if not os.path.exists(url):
            raise FileNotFoundError(f"LGEDV rule file not found: {url}")
        with open(url, "r", encoding="utf-8") as f:
            text = f.read()
        return [types.TextContent(type="text", text=text)]


def create_messages(
    context: str | None = None, topic: str | None = None
) -> list[types.PromptMessage]:
    """Create the messages for the prompt."""
    messages = []

    # Add context if provided
    if context:
        messages.append(
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text", text=f"Here is some relevant context: {context}"
                ),
            )
        )

    # Add the main prompt
    prompt = "Please help me with "
    if topic:
        prompt += f"the following topic: {topic}"
    else:
        prompt += "whatever questions I may have."

    messages.append(
        types.PromptMessage(
            role="user", content=types.TextContent(type="text", text=prompt)
        )
    )

    return messages


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    app = Server("mcp-misra-tool")

    @app.call_tool()
    async def fetch_tool(
        name: str, arguments: dict
    ) -> list[
        types.TextContent
        | types.ImageContent
        | types.AudioContent
        | types.EmbeddedResource
    ]:
        if name == "fetch_misra_rule":
            url = arguments.get("url")
            if not url or not (url.startswith("http://") or url.startswith("https://")):
                url = MISRA_RULE_URL
            return await fetch_misra_rule(url)
        elif name == "fetch_lgedv_rule":
            url = arguments.get("url")
            if not url:
                url = LGEDV_RULE_URL
            return await fetch_lgedv_rule(url)
        else:
            raise ValueError(f"Unknown tool: {name}")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="fetch_misra_rule",
                description="Fetches the MISRA C++ 2008 rule markdown from remote server.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to fetch MISRA rule (optional, default is preset)",
                        }
                    },
                },
            ),
            types.Tool(
                name="fetch_lgedv_rule",
                description="Fetches the LGEDV rule markdown from remote server.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to fetch LGEDV rule (optional, default is preset)",
                        }
                    },
                },
            ),
        ]

    @app.list_prompts()
    async def list_prompts() -> list[types.Prompt]:
        return [
            types.Prompt(
                name="simple",
                description="[taikt] A simple prompt that can take optional context and topic "
                "arguments",
                arguments=[
                    types.PromptArgument(
                        name="context",
                        description="Additional context to consider",
                        required=False,
                    ),
                    types.PromptArgument(
                        name="topic",
                        description="Specific topic to focus on",
                        required=False,
                    ),
                ],
            ),
            types.Prompt(
                name="fetch_misra_rule",
                description="Fetch the MISRA C++ 2008 rule markdown from remote server.",
                arguments=[],
            ),
        ]

    @app.get_prompt()
    async def get_prompt(
        name: str, arguments: dict[str, str] | None = None
    ) -> types.GetPromptResult:
        if name == "simple":
            if arguments is None:
                arguments = {}
            return types.GetPromptResult(
                messages=create_messages(
                    context=arguments.get("context"), topic=arguments.get("topic")
                ),
                description="A simple prompt with optional context and topic arguments: this is your taikt",
            )
        elif name == "fetch_misra_rule":
            async with httpx.AsyncClient() as client:
                resp = await client.get(MISRA_RULE_URL)
                resp.raise_for_status()
                rule_content = resp.text
            return types.GetPromptResult(
                messages=[
                    types.PromptMessage(
                        role="system",
                        content=types.TextContent(type="text", text=rule_content),
                    )
                ],
                description="MISRA C++ 2008 rule markdown fetched from remote server.",
            )
        else:
            raise ValueError(f"Unknown prompt: {name}")

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.responses import Response
        from starlette.routing import Mount, Route

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
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="127.0.0.1", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0
