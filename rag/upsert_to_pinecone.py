import os
from openai import OpenAI
from pinecone import Pinecone
import markdown
import hashlib


# --- Configure your API keys ---
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# --- Initialize Pinecone ---
pinecone_client = Pinecone(
    api_key=PINECONE_API_KEY
)
INDEX_NAME = 'rag-example-index'  
# Assuming the index has already been created in Pinecone
index = pinecone_client.Index(INDEX_NAME)

def upsert_to_pinecone(text,metadata):
    response = client.embeddings.create(input=text,model="text-embedding-3-small")
    embedding = response.data[0].embedding

    metadata['content'] = text
    hash_object = hashlib.md5(text.encode())
    id = hash_object.hexdigest()

    index.upsert(
         vectors = [
           {  
            "id": id,
            "values": embedding,
            "metadata": metadata
           }
         ]
    )

# upsert_to_pinecone('The capital of Poland is Warsaw', metadata={'Category':'Geography'})
# upsert_to_pinecone('Robert Lewandowski is a big data engineer', metadata={'Category':'Linkedin'})
