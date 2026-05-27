from pydantic_ai import Agent
from tools import grep, read_file, list_files
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent
from typing import Any

agent = Agent(
    "openai:gpt-5.5",
    tools=[list_files, grep, read_file],
    instructions=(
        "Search notes with list_files,grep,read_file. Cite files.\
            If evidence is missing, say no."
    ),
)


def preview(
    content: Any,
) -> str:  # gives a short preview of the content, if it's a list it shows the number of items and the first few items, otherwise it shows the first line of the content
    if isinstance(content, list):
        lines = "\n      ".join(str(item) for item in content)
        return f"{len(content)} results\n      {lines}" if content else "0 results"

    return str(content).splitlines()[0][:120]


def format_tool_result(  # formats the tool result for display, showing the tool name and a preview of the content
    event: FunctionToolResultEvent,
    tool_names: dict[str, str],
) -> str:
    tool_name = tool_names.get(event.tool_call_id, event.result.tool_name)
    return f"   <- {tool_name}: {preview(event.result.content)}"


async def run_with_visible_steps(
    question: str, debug: bool = False
) -> str:  # runs the agent with the given question and prints the steps taken by the agent, including tool calls and their results if debug is True
    print(f"\nQ: {question}")
    print("------agent steps-----")
    tool_names: dict[str, str] = {}
    async with agent.iter(
        question
    ) as run:  # iterates through the agent's execution steps
        async for node in run:  # for each node in the execution, if it's a tool call node, it listens to the tool call events and prints the tool name and arguments, and if debug is True, it also prints the tool results
            if Agent.is_call_tools_node(node):  # checks if the node is a tool call node
                async with node.stream(
                    run.ctx
                ) as tool_stream:  # streams the tool call events for the current node
                    async for event in tool_stream:  # for each event in the tool stream, if it's a FunctionToolCallEvent, it stores the tool name in the tool_names dictionary and prints the tool call, and if it's a FunctionToolResultEvent and debug is True, it prints the tool result using the format_tool_result function
                        if isinstance(event, FunctionToolCallEvent):
                            tool_names[event.tool_call_id] = (
                                event.part.tool_name
                            )  # stores the tool name in the tool_names dictionary using the tool_call_id as the key
                            print(
                                f"-> {event.part.tool_name}({event.part.args_as_json_str})"  # prints the tool call with the tool name and arguments, we need to use args_as_json_str to get the full arguments as a string, since args might be truncated in the event.part.args
                            )
                        elif (
                            debug and isinstance(event, FunctionToolResultEvent)
                        ):  # if debug is True and the event is a FunctionToolResultEvent, it prints the tool result using the format_tool_result function, which shows the tool name and a preview of the content
                            print(
                                format_tool_result(event, tool_names)
                            )  # the difference btw resultevent and callevent is that callevent is when the tool is called with the arguments, and resultevent is when the tool returns the result, so we can use the tool_call_id to match the result with the call and get the tool name from the tool_names dictionary
    print("-----done-----")
    return run.result.output


async def main():
    question = "Why does our nightly deploy job run at 03:47 UTC specifically?"
    answer = await run_with_visible_steps(question, debug=True)
    print(f"\nA: {answer}")


if __name__ == "__main__":
    await main()
