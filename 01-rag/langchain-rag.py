from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Setup Local Models (Ollama)
embeddings = OllamaEmbeddings(model="qwen3-embedding:8b")
llm = ChatOllama(model="qwen3:8b", temperature=0)

# 2. Setup Vector Store (Qdrant)
# LangChain handles the collection creation and dimension matching (4096) automatically
vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="local_docs",
    url="http://localhost:6333",
)

# 3. The "Loader" Logic: Ingesting Data
def ingest_document(text):
    # Use LangChain's smart splitter instead of manual loops
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    docs = text_splitter.create_documents([text])
    
    # LangChain handles UUID generation and batching automatically
    vector_store.add_documents(docs)
    print(f"Ingested {len(docs)} chunks successfully.")

# 4. The "RAG Chain": Defining the Logic
# This defines the data flow: Question -> Retriever -> Prompt -> LLM -> String
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Define the retriever (Top-3 search)
retriever = vector_store.as_retriever(search_kwargs={"k": 10})

# LCEL (LangChain Expression Language) Chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# --- Execution ---
if __name__ == "__main__":
    # Ingest example
    raw_text = "The Fiber Go framework uses a Prefork feature to achieve high performance."
    # ingest_document(raw_text)
    
    # Ask question
    response = rag_chain.invoke("tell me about go fiber framework")
    print(f"\nAI Answer:\n{response}")