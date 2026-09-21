from fastapi import APIRouter
from app.api.models import AskRequest, AskResponse
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/ask", response_model=AskResponse)
async def ask_question_endpoint(request: AskRequest):
    answer = await rag_service.ask_question(request.query)
    return AskResponse(answer=answer)