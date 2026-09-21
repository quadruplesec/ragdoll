class RAGService:
    def __init__(self):
        pass

    async def ask_question(self, query: str) -> str:
        return "Who is Laura Palmer?"

    async def ingest_text(self, text: str) -> dict:
        return {"status": "success"}