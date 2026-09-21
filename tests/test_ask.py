from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_endpoint_success(monkeypatch):
    async def mock_ask_question(self, query: str):
        return "Who is Laura Palmer?"

    monkeypatch.setattr("app.api.ask.RAGService.ask_question", mock_ask_question)

    payload = {"query": "Who killed Laura Palmer?"}

    response = client.post("/ask", json=payload)

    assert response.status_code == 200
    assert response.json() == {"answer": "Who is Laura Palmer?"}