import json
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP(
    name="Knowledge Base",
    host="0.0.0.0",
    port=8050,
    env={**os.environ},
)


@mcp.tool()
def get_knowledge_base() -> str:
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "data", "kb.json")
        with open(kb_path, "r") as f:
            kb_data = json.load(
                f
            )  # Assuming the knowledge base is stored in a JSON file,we load it and return its content as a string

        kb_text = "Here is the retrieved knowledge base:\n"
        if isinstance(kb_data, list):
            for i, item in enumerate(kb_data, 1):
                if isinstance(item, dict):
                    question = item.get("question", "Unknown question")
                    answer = item.get("answer", "Unknown answer")
                else:
                    question = f"Item {i}"
                    answer = str(item)
                kb_text += f"Q{i}: {question}\n"
                kb_text += f"A{i}: {answer}\n"
        else:
            kb_text += f"Knowledge base content:\n{json.dumps(kb_data, indent=2)}\n"

        return kb_text
    except FileNotFoundError:
        return "Knowledge base file not found."
    except json.JSONDecodeError:
        return "Error decoding knowledge base file."
    except Exception as e:
        return f"An error occurred while retrieving the knowledge base: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
