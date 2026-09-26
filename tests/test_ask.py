import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_rag_service

client = TestClient(app)

class MockRAGService:
        async def ask_question(self, query: str):
            return "I am dead yet I live."

@pytest.fixture
def mock_rag_service():
    app.dependency_overrides[get_rag_service] = lambda: MockRAGService()
    yield
    app.dependency_overrides.pop(get_rag_service, None) 
     
def test_ask_endpoint_success(mock_rag_service):
    payload = {"query": "Who killed Laura Palmer?"}
    response = client.post("/ask", json=payload)

    assert response.status_code == 200
    assert response.json() == {"answer": "I am dead yet I live."}