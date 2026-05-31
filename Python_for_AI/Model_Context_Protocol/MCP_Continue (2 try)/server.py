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


if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running on stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running on sse transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")
