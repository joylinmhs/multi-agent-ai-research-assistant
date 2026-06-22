from functools import lru_cache

from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()

@router.post("/query", response_model=ChatResponse)
async def query_chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    response = await service.handle_query(request)
    return response
