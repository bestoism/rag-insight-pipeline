import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Ganti ke HuggingFace
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.core.config import settings

# 1. Setup Embeddings Model 
def get_embedding_model():
    # Model 'all-MiniLM-L6-v2' akan didownload sekali ke komputer
    # Ukuran vectornya adalah 384 dimensi
    print("Loading local embedding model...")
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Setup Qdrant Client
def get_qdrant_client():
    client = QdrantClient(path=settings.QDRANT_PATH)
    return client

# 3. Fungsi Utama
async def index_document(text: str, filename: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.create_documents([text], metadatas=[{"source": filename}])
    
    print(f"Generated {len(chunks)} chunks from {filename}")

    embeddings = get_embedding_model()
    client = get_qdrant_client()
    
    # PENTING: Ukuran vector all-MiniLM-L6-v2 adalah 384
    if not client.collection_exists(settings.QDRANT_COLLECTION_NAME):
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.QDRANT_COLLECTION_NAME,
        embedding=embeddings,
    )
    
    vector_store.add_documents(documents=chunks)
    
    return len(chunks)