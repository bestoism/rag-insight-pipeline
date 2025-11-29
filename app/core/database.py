from qdrant_client import QdrantClient
from app.core.config import settings

_qdrant_client_instance = None

def get_qdrant_client():
    """
    Factory function untuk mendapatkan client Qdrant.
    Otomatis memilih antara Cloud (URL) atau Local (Path).
    Menggunakan Singleton pattern agar koneksi efisien.
    """
    global _qdrant_client_instance
    
    if _qdrant_client_instance is None:
        # Logika Pemilihan:
        # Jika ada QDRANT_URL dan bukan localhost, pakai mode Cloud
        if settings.QDRANT_URL and "localhost" not in settings.QDRANT_URL:
            print("🌐 Connecting to Qdrant Cloud...")
            _qdrant_client_instance = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY
            )
        else:
            print("📂 Using Local Qdrant Storage...")
            _qdrant_client_instance = QdrantClient(path=settings.QDRANT_PATH)
            
    return _qdrant_client_instance