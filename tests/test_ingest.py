from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_endpoint_success(monkeypatch):
    async def mock_ingest_text(self, text: str):
        return {"status": "success"}

    monkeypatch.setattr("app.api.ingest.RAGService.ingest_text", mock_ingest_text)

    payload = {"text": "Twin Peaks rocks!"}

    response = client.post("/ingest", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "success"}