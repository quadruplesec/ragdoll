from fastapi import APIRouter, Depends
from app.api.models import AskRequest, AskResponse
from app.services.rag_service import RAGService
from app.api.dependencies import get_rag_service

router = APIRouter()
rag_service = RAGService()

@router.post("/ask", response_model=AskResponse)
async def ask_question_endpoint(
    request: AskRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    answer = await rag_service.ask_question(request.query)
    return AskResponse(answer=answer)