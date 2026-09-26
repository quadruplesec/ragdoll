import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_rag_service

client = TestClient(app)

class MockRAGService:
        async def ingest_text(self, query: str):
            return {"status": "success"}

@pytest.fixture
def mock_rag_service():
    app.dependency_overrides[get_rag_service] = lambda: MockRAGService()
    yield
    app.dependency_overrides.pop(get_rag_service, None) 

def test_ingest_endpoint_success(mock_rag_service):
    payload = {"text": "Twin Peaks rocks!"}
    response = client.post("/ingest", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "success"}