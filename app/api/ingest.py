from fastapi import APIRouter, Depends
from app.api.models import IngestRequest, IngestResponse
from app.services.rag_service import RAGService
from app.api.dependencies import get_rag_service

router = APIRouter()
rag_service = RAGService()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document_endpoint(
    request: IngestRequest,
    rag_services: RAGService = Depends(get_rag_service)
):
    result = await rag_service.ingest_text(request.text)
    return IngestResponse(status=result["status"])