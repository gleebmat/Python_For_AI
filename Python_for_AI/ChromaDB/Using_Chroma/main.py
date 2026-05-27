import chromadb
from pprint import pprint
import dotenv

chroma_client = chromadb.Client()
dotenv.load_dotenv()
collection = chroma_client.get_or_create_collection(name="documents")

collection.add(
    documents=[
        "This is a document about pineapples",
        "This is a document about oranges",
    ],
    ids=["id1", "id2"],
)

results = collection.query(query_texts=["This is a document about hawaii"], n_results=2)
pprint(results)
results = collection.query(
    query_texts=["This is a document about hawaii"],
    n_results=2,
    where_document={"$contains": "pineapple"},
)
pprint(results)
