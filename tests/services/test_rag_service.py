import pytest
from app.services.rag_service import RAGService
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.llms.fake import FakeListLLM

@pytest.fixture
def rag_service():
    fake_embeddings = FakeEmbeddings(size=384)
    fake_llm = FakeListLLM(responses=["We all killed Laura Palmer."])
    return RAGService(
        embedding_function=fake_embeddings,
        llm=fake_llm,
        persist_directory=None
    )

async def test_ask_question_returns_string(rag_service):
    query = "Who killed Laura Palmer?"
    response = await rag_service.ask_question(query)
    assert isinstance(response, str)
    assert response == "We all killed Laura Palmer."


async def test_ingest_text_success(rag_service):
    documet_text = "The owls are not what they seem."
    result = await rag_service.ingest_text(documet_text)
    assert result == {"status": "success"}