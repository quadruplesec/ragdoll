from fastapi import APIRouter
from app.api.models import IngestRequest, IngestResponse
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document_endpoint(request: IngestRequest):
    result = await rag_service.ingest_text(request.text)
    return IngestResponse(status=result["status"])