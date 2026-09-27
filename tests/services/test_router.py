import pytest
from app.services.rag_service import RAGService
from langchain_community.llms.fake import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings

async def test_classify_query_direct():
    fake_embeddings = FakeEmbeddings(size=384)
    fake_llm = FakeListLLM(responses=["DIRECT"])
    
    rag_service = RAGService(
        embedding_function=fake_embeddings, 
        llm=fake_llm, 
        persist_directory=None
    )
    
    result = await rag_service.classify_query("Hello! What's up?")
    assert result == "DIRECT"

async def test_classify_query_rag():
    fake_embeddings = FakeEmbeddings(size=384)
    fake_llm = FakeListLLM(responses=["RAG"])
    
    rag_service = RAGService(
        embedding_function=fake_embeddings, 
        llm=fake_llm, 
        persist_directory=None
    )
    
    result = await rag_service.classify_query("Explain Project Ragdoll's architecture.")
    assert result == "RAG"