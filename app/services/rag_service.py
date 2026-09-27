import os

from operator import itemgetter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch
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

        kb_desc = os.getenv("KNOWLEDGE_BASE_DESCRIPTION", "private documents and domain-specific knowledge")
        
        prompt_text = (
            "You are a strict semantic routing agent. Classify the user query into exactly one of these two categories:\n\n"
            "1. RAG: Select this if the query asks for specific facts or relates to this domain: " + kb_desc + ".\n"
            "2. DIRECT: Select this if the query is a greeting, conversational pleasantry, or general world knowledge.\n\n"
            "Output ONLY the exact word RAG or DIRECT, with absolutely no other text, markdown, or punctuation.\n\n"
            "Query: {query}\n"
            "Classification:"
        )
        
        self.classifier_prompt = PromptTemplate.from_template(prompt_text)
        self.classifier_chain = self.classifier_prompt | self.llm | StrOutputParser()

        rag_prompt = PromptTemplate.from_template(
            "Use the following pieces of retrieved context to answer the question.\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": itemgetter("query") | self.vectorstore.as_retriever() | format_docs, "query": itemgetter("query")}
            | rag_prompt
            | self.llm
            | StrOutputParser()
        )

        direct_prompt = PromptTemplate.from_template("""
You are a helpful AI assistant. Answer the following user query directly.
Query: {query}
Answer:
""")

        direct_chain = (
            {"query": itemgetter("query")}
            | direct_prompt
            | self.llm
            | StrOutputParser()
        )

        self.qa_chain = RunnableBranch(
            (lambda x: x["classification"] == "RAG", rag_chain),
            direct_chain
        )

    async def classify_query(self, query: str) -> str:
        result = await self.classifier_chain.ainvoke({"query": query})
        return result.strip().upper()

    async def ask_question(self, query: str) -> str:
        classification = await self.classify_query(query)
        return await self.qa_chain.ainvoke({"query": query, "classification": classification})

    async def stream_question(self, query: str):
        classification = await self.classify_query(query)
        async for chunk in self.qa_chain.astream({"query": query, "classification": classification}):
            yield chunk

    async def ingest_text(self, text: str) -> dict:
        chunks = self.text_splitter.split_text(text)
        self.vectorstore.add_texts(texts=chunks)
        return {"status": "success"}