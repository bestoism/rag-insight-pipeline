import os
from dotenv import load_dotenv

load_dotenv()

# Dapatkan base directory project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAG Insight Pipeline")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    
    # Qdrant Path (Sekarang pakai Absolute Path)
    QDRANT_PATH: str = os.path.join(BASE_DIR, "qdrant_data")
    
    QDRANT_COLLECTION_NAME: str = "rag_documents"
    EMBEDDING_MODEL_NAME: str = "models/embedding-001" 

settings = Settings()