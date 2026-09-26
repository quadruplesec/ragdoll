import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.llms.fake import FakeListLLM

from app.core.llm_factory import get_llm


class RAGService:
    def __init__(self, embedding_function=None, llm=None, persist_directory="./chroma_data"):
        self.embeddings = embedding_function or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.vectorstore = Chroma (
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

        if llm:
            self.llm = llm
        else:
            provider = os.getenv("LLM_PROVIDER", "ollama")
            self.llm = get_llm(provider)

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever()
        )

    async def ask_question(self, query: str) -> str:
        response = await self.qa_chain.ainvoke({"query": query})
        return response["result"]

    async def ingest_text(self, text: str) -> dict:
        chunks = self.text_splitter.split_text(text)
        self.vectorstore.add_texts(texts=chunks)
        return {"status": "success"}