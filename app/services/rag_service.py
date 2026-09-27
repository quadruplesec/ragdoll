import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

        prompt = PromptTemplate.from_template("""
Use the following pieces of retrieved context to answer the question.
Context: {context}
Question: {question}
Answer:
"""
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        self.qa_chain = (
            {"context": self.vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    async def ask_question(self, query: str) -> str:
        return await self.qa_chain.ainvoke(query)

    async def stream_question(self, query: str):
        async for chunk in self.qa_chain.astream(query):
            yield chunk

    async def ingest_text(self, text: str) -> dict:
        chunks = self.text_splitter.split_text(text)
        self.vectorstore.add_texts(texts=chunks)
        return {"status": "success"}