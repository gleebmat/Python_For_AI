import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI


nest_asyncio.apply()

load_dotenv()


class MCPOpenAIClient:
    def __init__(self, model: str = "gpt-4o"):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI()
        self.model = model
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self, server_script_path: str = "server.py"):
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
        )
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        tools_result = await self.session.list_tools()
        print("\nConnected to server with tools")
        for tool in tools_result.tools:
            print(f" - {tool.name}: {tool.description}")

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str) -> str:
        tools = await self.get_mcp_tools()

        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}],
            tools=tools,
            tool_choice="auto",
        )
        assistant_message = response.choices[0].message
        messages = [{"role": "user", "content": query}, assistant_message]

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                result = await self.session.call_tool(
                    tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments),
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.content[0].text,
                    }
                )
                if tool_call.function.name == "get_knowledge_base":
                    messages.append(
                        {"role": "system", "content": result.content[0].text}
                    )
                final_response = await self.openai_client.chat.completions.create(
                    model=self.model, messages=messages, tools=tools, tool_choice="auto"
                )

                return final_response.choices[0].message.content

            return assistant_message.content

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPOpenAIClient()
    await client.connect_to_server("server.py")

    query = "What is our company's vacation policy"

    print(f"\nQuery: {query}")

    response = await client.process_query(query)

    print(f"\nResponse: {response}")

    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
