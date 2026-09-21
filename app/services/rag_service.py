from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGService:
    def __init__(self, embedding_function=None, persist_directory="./chroma_data"):
        self.embeddings = embedding_function or HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.vectorstore = Chroma (
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )

    async def ask_question(self, query: str) -> str:
        return "Who is Laura Palmer?"

    async def ingest_text(self, text: str) -> dict:
        chunks = self.text_splitter.split_text(text)
        self.vectorstore.add_texts(texts=chunks)
        return {"status": "success"}