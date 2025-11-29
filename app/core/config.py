import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAG Insight Pipeline")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # Placeholder for future keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")

settings = Settings()