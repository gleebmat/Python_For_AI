from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_postgres.vectorstores import PGVector

load_dotenv()
loader = TextLoader("state_of_the_union.txt", encoding="utf-8")
documents = loader.load()
print(documents)
print(len(documents))

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)

texts = text_splitter.split_documents(documents)
print(texts[0])
type(texts)

embeddings = OpenAIEmbeddings()
vector = embeddings.embed_query("testing")
len(vector)  # 1536

doc_vectors = embeddings.embed_documents([t.page_content for t in texts[:5]])
doc_vectors

CONNECTION_STRING = "postgresql+psycopg://postgres:7007@localhost:5433/vector_db"
COLLECTION_NAME = "state_of_union_vectors"

db = PGVector.from_documents(
    embedding=embeddings,
    documents=texts,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
)


query = "what is said about rocknroll?"
result = db.similarity_search_with_score(query, k=2)
print(embeddings.embed_query(query))
print(result)
