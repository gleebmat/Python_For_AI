from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",
    port=8050,
)


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


async def start_mcp(transport: str):
    if transport == "stdio":
        logging.info("Running server with stdio transport")
        await mcp.run_stdio_async()
    elif transport == "sse":
        logging.info("Running server with sse transport")
        await mcp.run_sse_async()
    else:
        raise ValueError(f"Unsupported transport: {transport}")


if __name__ == "__main__":
    TRANSPORT = "stdio"

    try:
        asyncio.get_running_loop()
        import nest_asyncio

        nest_asyncio.apply()  # Required for some interactive environments
        asyncio.create_task(start_mcp(TRANSPORT))
    except RuntimeError:
        asyncio.run(start_mcp(TRANSPORT))
