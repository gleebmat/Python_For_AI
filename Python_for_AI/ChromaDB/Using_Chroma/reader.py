import pandas as pd
from dotenv import load_dotenv
import chromadb.utils.embedding_functions as embedding_functions
import os
import chromadb
from pprint import pprint

load_dotenv()
chroma_client = chromadb.PersistentClient(path="./vectordb")
articles = pd.read_csv("Articles.csv", encoding="ISO-8859-1")
articles

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small",
)
subset = 600
articles = articles[:subset]

documents_list = articles["Article"].to_list()
ids = [f"id{x}" for x in articles.index.to_list()]
vectors = openai_ef(documents_list)


collection = chroma_client.get_or_create_collection(name="articles")
collection.add(documents=documents_list, ids=ids, embeddings=vectors)
collection.count()
query = "football match"
query_embeddings = openai_ef([query])
result = collection.query(query_embeddings=query_embeddings, n_results=3)
pprint(result)
