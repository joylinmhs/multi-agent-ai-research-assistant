from pydantic import BaseModel, Field
from typing import List

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None
    user_id: str | None = None
    document_id: str | None = None
    previous_answer: str | None = None

class SourceReference(BaseModel):
    document_id: str
    page_number: int | None = None
    snippet: str
    confidence: float

class ChatResponse(BaseModel):
    answer: str
    summary: str | None = None
    sources: List[SourceReference] = Field(default_factory=list)
    confidence: float = 0.0
    session_id: str | None = None
