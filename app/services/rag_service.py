import os
import json
import io
from pypdf import PdfReader
from operator import itemgetter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from app.core.llm_factory import get_llm


class RAGService:
    def __init__(self, embedding_function=None, llm=None, persist_directory="./chroma_data"):
        self.embeddings = embedding_function or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.vectorstore = Chroma (
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

        existing_data = self.vectorstore.get()
        existing_docs = existing_data.get("documents", [])

        if existing_docs:
            self.keyword_retriever = BM25Retriever.from_texts(existing_docs)
            self.keyword_retriever.k = 4
        else:
            self.keyword_retriever = None

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

        def dynamic_retriever(query: str):
            dense_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
            if self.keyword_retriever:
                ensemble = EnsembleRetriever(
                    retrievers=[dense_retriever, self.keyword_retriever],
                    weights=[0.5,0.5]
                )
                return ensemble.invoke(query)
            return dense_retriever.invoke(query)

        rag_prompt = PromptTemplate.from_template(
            "Use the following pieces of retrieved context to answer the question.\n\nContext: {context}\n\nQuestion: {query}\n\nAnswer:"
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": itemgetter("query") | RunnableLambda(dynamic_retriever) | format_docs, "query": itemgetter("query")}
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
        return result.strip().upper().replace("*", "").replace(".","")

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
        all_docs = self.vectorstore.get()["documents"]
        self.keyword_retriever = BM25Retriever.from_texts(all_docs)
        self.keyword_retriever.k = 4
        return {"status": "success"}

    async def ingest_file_stream(self, file_content: bytes, filename: str):
        yield json.dumps({"step": "upload", "status": "Saving file...", "progress": 10})

        text = ""

        if file_content.startswith(b"%PDF-"):
            yield json.dumps({"step": "parse", "status": "Extracting text from PDF...", "progress": 30})
            try:
                pdf_reader = PdfReader(io.BytesIO(file_content))
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            except Exception:
                yield json.dumps({"step": "error", "status": "Corrupted or invalid PDF file.", "progress": 0})
                return

        else:
            yield json.dumps({"step": "parse", "status": "Reading text file...", "progress": 30})
            try:
                text = file_content.decode("utf-8")
            except UnicodeDecodeError:
                yield json.dumps({"step": "error", "status": "File encoding is not valid UTF-8 and is not a valid PDF.", "progress": 0})
                return

        if not text.strip():
            yield json.dumps({"step": "error", "status": "No readable text found in the file", "progress": 0})
            return

        yield json.dumps({"step": "chunk", "status": "Splitting text into chunks...", "progress": 50})
        chunks = self.text_splitter.split_text(text)

        yield json.dumps({"step": "embed", "status": "Generating vectors and updating BM25...", "progress": 80})
        self.vectorstore.add_texts(texts=chunks)

        all_docs = self.vectorstore.get()["documents"]
        self.keyword_retriever = BM25Retriever.from_texts(all_docs)
        self.keyword_retriever.k = 4

        yield json.dumps({"step": "complete", "status": "Ingestion successful!", "progress": 100})
                