from pydantic import BaseModel, Field
from pydantic_ai import Agent
from tools import grep, read_file, list_files


class Citation(BaseModel):
    file: str = Field(
        description="Relative path to the markdown file, e.g.\
                   '03-incident-2024-q3.md'"
    )
    quote: str = Field(
        description="The exact line(s) from the file that support the claim"
    )
    line_number: int = Field(
        description="The line number in the file where the quote appears"
    )


class SearchAnswer(BaseModel):
    answer: str = Field(description="The answer in plain English")
    citations: list[Citation] = Field(
        description="Files and quotes that support the answer"
    )


agent = Agent(
    "openai:gpt-5.5",
    tools=[list_files, grep, read_file],
    output_type=SearchAnswer,
    instructions=(
        "Search notes with list_files,grep,read_file. Cite files.\
            If evidence is missing, say no."
    ),
)


async def main():

    result = await agent.run(
        "Why does our nightly deploy job run at 03:47 UTC specifically?"
    )
    answer = result.output

    print(f"Answer: {answer.answer}")
    print("Citations:")
    for citation in answer.citations:
        print(f"  - {citation.file}:{citation.line_number}")
        print(f" {citation.quote}")


if __name__ == "__main__":
    await main()
