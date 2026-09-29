from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.api.models import IngestRequest, IngestResponse
from app.services.rag_service import RAGService
from app.api.dependencies import get_rag_service

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
async def ingest_document_endpoint(
    request: IngestRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    result = await rag_service.ingest_text(request.text)
    return IngestResponse(status=result["status"])

@router.post(
    "/ingest/file",
    responses={
        200: {
            "description": "Server-Sent Events stream providing ingestion progress.",
            "content": {"text/event-stream": {}}
        }
    }
)
async def ingest_file_endpoint(
    file: UploadFile = File(...),
    rag_service: RAGService = Depends(get_rag_service)
):
    allowed_types = ["application/pdf", "text/plain", "text/markdown", "text/csv"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail=f"Media type {file.content_type} not allowed.")

    file_content = await file.read()

    async def event_generator():
        async for chunk in rag_service.ingest_file_stream(file_content, file.filename):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )