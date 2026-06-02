from pydantic import BaseModel

class DocumentCreate(BaseModel):
    filename: str
    content_type: str
    size: int
    uploaded_by: str | None = None

class DocumentUploadResponse(BaseModel):
    filename: str
    message: str
    document_id: str
