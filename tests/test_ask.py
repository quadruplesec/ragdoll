import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_rag_service

client = TestClient(app)

class MockRAGService:
        async def stream_question(self, query: str):
            tokens = ["I ", "am ", "dead ", "yet ", "I ", "live."]
            for token in tokens:
                yield token

@pytest.fixture
def mock_rag_service():
    app.dependency_overrides[get_rag_service] = lambda: MockRAGService()
    yield
    app.dependency_overrides.pop(get_rag_service, None) 
     
def test_ask_endpoint_success(mock_rag_service):
    payload = {"query": "Who killed Laura Palmer?"}
    response = client.post("/ask", json=payload)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    expected_output = "data: I \n\ndata: am \n\ndata: dead \n\ndata: yet \n\ndata: I \n\ndata: live.\n\n"
    assert response.text == expected_output