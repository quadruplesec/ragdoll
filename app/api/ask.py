from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.api.models import AskRequest, AskResponse
from app.services.rag_service import RAGService
from app.api.dependencies import get_rag_service

router = APIRouter()
@router.post("/ask")
async def ask_question_endpoint(
    request: AskRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    async def event_generator():
        async for token in rag_service.stream_question(request.query):
            yield f"data: {token}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )