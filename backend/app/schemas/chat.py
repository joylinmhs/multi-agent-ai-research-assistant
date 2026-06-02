from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None
    user_id: str | None = None

class SourceReference(BaseModel):
    document_id: str
    page_number: int | None = None
    snippet: str
    confidence: float

class ChatResponse(BaseModel):
    answer: str
    summary: str | None = None
    sources: List[SourceReference] = []
    confidence: float = 0.0
    session_id: str | None = None
