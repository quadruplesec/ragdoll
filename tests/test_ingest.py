import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.dependencies import get_rag_service

client = TestClient(app)

class MockRAGService:
    async def ingest_text(self, query: str):
        return {"status": "success"}

    async def ingest_file_stream(self, file_content: bytes, filename: str):
        yield '{"step": "upload", "status": "Saving file...", "progress": 10}'
        yield '{"step": "complete", "status": "Ingestion successful!", "progress": 100}'
        

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

def test_ingest_file_streaming(mock_rag_service):
    file_data = {"file": ("test.txt", b"Project Ragdoll text content.", "text/plain")}

    response = client.post("/ingest/file", files=file_data)

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    expected_output = (
        'data: {"step": "upload", "status": "Saving file...", "progress": 10}\n\n'
        'data: {"step": "complete", "status": "Ingestion successful!", "progress": 100}\n\n'
    )

    assert response.text == expected_output