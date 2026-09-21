import pytest
from app.services.rag_service import RAGService
from langchain_community.embeddings import FakeEmbeddings

@pytest.fixture
def rag_service():
    fake_embeddings = FakeEmbeddings(size=384)
    return RAGService(embedding_function=fake_embeddings, persist_directory=None)

async def test_ask_question_returns_string(rag_service):
    query = "Who killed Laura Palmer?"

    response = await rag_service.ask_question(query)
    assert isinstance(response, str)

async def test_ingest_text_success(rag_service):
    documet_text = "The owls are not what they seem."

    result = await rag_service.ingest_text(documet_text)
    assert result == {"status": "success"}