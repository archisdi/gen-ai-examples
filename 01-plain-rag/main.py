import uuid

import ollama
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# 1. Configuration
DB_CLIENT = QdrantClient("http://localhost:6333")
COLLECTION_NAME = "local_docs"
EMBED_MODEL = "qwen3-embedding:8b"
LLM_MODEL = "qwen3:8b"

def init_db():
    """Create collection with 4096 dimensions (Qwen3-Embedding:8b default)."""
    if not DB_CLIENT.collection_exists(COLLECTION_NAME):
        DB_CLIENT.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=4096, distance=Distance.COSINE),
        )

# 2. Ingestion: Breaking text into chunks and storing vectors
def chunk_text(text, size=600, overlap=100):
    chunks = []
    for i in range(0, len(text), size - overlap):
        chunks.append(text[i : i + size])
    return chunks

def ingest_data(doc_id, text):
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        # Generate embedding locally via Ollama
        response = ollama.embed(model=EMBED_MODEL, input=chunk)
        vector = response["embeddings"][0]
        
        # Store in Qdrant
        point_id = str(uuid.uuid4())
        DB_CLIENT.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id, 
                    vector=vector, 
                    payload={"text": chunk}
                )
            ],
        )
    print(f"Stored {len(chunks)} chunks for document {doc_id}.")

# 3. Retrieval: Finding relevant text
def get_context(query, limit=3):
    # Vectorize the user query
    query_vector = ollama.embed(model=EMBED_MODEL, input=query)["embeddings"][0]
    
    # Search Qdrant
    results = DB_CLIENT.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )
    
    # Extract the original text from the payload
    return [hit.payload["text"] for hit in results.points]

# 4. Generation: Producing the final answer
def ask_local_rag(question):
    context_list = get_context(question)
    context_text = "\n---\n".join(context_list)

    print(f"Retrieved Context:\n{context_text}\n")
    
    prompt = f"""Use the provided context to answer the question.
If the information is not in the context, say you do not know.

Context:
{context_text}

Question: {question}
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# --- Run ---
if __name__ == "__main__":
    init_db()
    
    # Example data (Software engineering focus)
    data = "The Go HTTP server 'Chi' is optimized for zero memory allocation."
    ingest_data(1, data)
    
    # Query
    result = ask_local_rag("Which Go server is optimized for zero memory allocation?")
    print(f"\nQwen3 Answer:\n{result}")