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
    ingested: bool = False

class DocumentIngestRequest(BaseModel):
    content: str
    title: str | None = None
    document_id: str | None = None
    metadata: dict[str, str] | None = None

class DocumentIngestResponse(BaseModel):
    document_id: str
    message: str
