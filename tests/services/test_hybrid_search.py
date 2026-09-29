import pytest
from app.services.rag_service import RAGService
from langchain_community.llms.fake import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings

async def test_hybrid_search_initialization():
    fake_embeddings = FakeEmbeddings(size=384)
    fake_llm = FakeListLLM(responses=["RAG"])

    rag_service = RAGService(
        embedding_function=fake_embeddings,
        llm=fake_llm,
        persist_directory=None
    )

    await rag_service.ingest_text("BM25 and ChromaDB working together.")

    assert hasattr(rag_service, "keyword_retriever")
    assert rag_service.keyword_retriever is not None

    