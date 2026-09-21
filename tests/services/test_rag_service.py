import pytest
from app.services.rag_service import RAGService

async def test_ask_question_returns_string():
    service = RAGService()
    query = "Who killed Laura Palmer?"

    response = await service.ask_question(query)
    assert isinstance(response, str)