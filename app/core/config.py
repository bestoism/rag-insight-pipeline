import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAG Insight Pipeline")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # Qdrant Config (Hybrid)
    QDRANT_PATH: str = os.path.join(BASE_DIR, "qdrant_data")
    QDRANT_URL: str = os.getenv("QDRANT_URL")         # <--- Baru
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY") # <--- Baru
    QDRANT_COLLECTION_NAME: str = "rag_documents"
    
    # Langfuse
    LANGFUSE_SECRET_KEY: str = os.getenv("LANGFUSE_SECRET_KEY")
    LANGFUSE_PUBLIC_KEY: str = os.getenv("LANGFUSE_PUBLIC_KEY")
    LANGFUSE_HOST: str = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

settings = Settings()