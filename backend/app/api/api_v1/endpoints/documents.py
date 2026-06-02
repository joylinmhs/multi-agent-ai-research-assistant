from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.document import DocumentCreate, DocumentUploadResponse
from app.services.file_service import FileService

router = APIRouter()
service = FileService()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    metadata = await service.save_document(file)
    return DocumentUploadResponse(**metadata)
