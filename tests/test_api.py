from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """
    Test apakah endpoint root (/) mengembalikan status 200 dan pesan healthy
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# Nanti bisa tambah test upload/query di sini