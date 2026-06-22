from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.document import (
    DocumentCreate,
    DocumentIngestRequest,
    DocumentIngestResponse,
    DocumentUploadResponse,
)
from app.services.file_service import FileService
from app.services.document_service import DocumentService

router = APIRouter()
file_service = FileService()
document_service = DocumentService()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    try:
        metadata = await file_service.save_document(file)
    except ValueError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    return DocumentUploadResponse(**metadata)

@router.post("/ingest", response_model=DocumentIngestResponse)
def ingest_document(payload: DocumentIngestRequest):
    try:
        result = document_service.ingest_text(
            content=payload.content,
            title=payload.title,
            document_id=payload.document_id,
            metadata=payload.metadata,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return DocumentIngestResponse(**result)
