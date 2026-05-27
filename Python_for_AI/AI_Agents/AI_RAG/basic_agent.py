from pydantic_ai import Agent
from tools import grep, read_file, list_files

agent = Agent(
    "openai:gpt-4o",
    tools=[list_files, grep, read_file],
    instructions=(
        "Search notes with list_files,grep,read_file. Cite files.\
            If evidence is missing, say no."
    ),
)


async def ask(question: str):
    return await agent.run(question)


async def main():
    question = "Why does our nightly deploy job run at 03:47 UTC specifically?"
    result = await ask(question)
    print(f"\nQ: {question}")
    print("A: ", result.output)
    print(f"\nUsage: {result.usage}")


if __name__ == "__main__":
    await main()
