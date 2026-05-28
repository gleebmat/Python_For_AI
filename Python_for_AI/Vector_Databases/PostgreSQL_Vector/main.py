import psycopg2
import numpy as np
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

texts = [
    "Type:Desktop,OS:Ubuntu,GPU:NVIDIA,CPU:AMD,RAM:64GB,SSD:2TB",
    "Type:Desktop,OS:Manjaro,GPU:NVIDIA,CPU:Intel,RAM:32GB,SSD:1TB",
    "Type:Laptop,OS:Windows,GPU:NVIDIA,CPU:Intel,RAM:16GB,SSD:512GB",
    "Type:Laptop,OS:Ubuntu,GPU:NVIDIA,CPU:AMD,RAM:16GB,SSD:512GB",
    "Type:Desktop,OS:Ubuntu,GPU:NVIDIA,CPU:AMD,RAM:32GB,SSD:1TB",
    "Type:Desktop,OS:Fedora,GPU:NVIDIA,CPU:Intel,RAM:64GB,SSD:2TB",
    "Type:Laptop,OS:Windows,GPU:NVIDIA,CPU:Intel,RAM:16GB,SSD:512GB",
    "Type:Laptop,OS:Ubuntu,GPU:NVIDIA,CPU:AMD,RAM:16GB,SSD:512GB",
    "Type:Desktop,OS:Mac OS,GPU:NVIDIA,CPU:AMD,RAM:32GB,SSD:1TB",
    "Type:Desktop,OS:Windows,GPU:NVIDIA,CPU:Intel,RAM:64GB,SSD:2TB",
]
embeddings = OpenAIEmbeddings(
    api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-small"
)
embedding_list = []
for text in texts:
    embedding_list.append(embeddings.embed_query(text))


conn = psycopg2.connect("dbname=vector_db user=postgres password=7007 port=5432")
cur = conn.cursor()
for i in range(len(embedding_list)):
    embedding = embedding_list[i]
    content = texts[i]
    cur.execute(
        "INSERT INTO items (content,embedding) VALUES (%s,%s::vector)",
        (content, embedding),
    )
conn.commit()
cur.close()
conn.close()

new_text = "Type: Desktop,OS:Arch Linux,GPU:NVIDIA,CPU:AMD,RAM:64GB,SSD:2TB"
new_embedding = embeddings.embed_query(new_text)
conn = psycopg2.connect("dbname=vector_db user=postgres password=postgres port=5432")
cur = conn.cursor()
cur.execute(
    "SELECT id,content FROM items ORDER BY embedding <-> %s::vector LIMIT 5",
    (new_embedding,),
)
result = cur.fetchall()
for row in result:
    print(row)
cur.close()
conn.close()
