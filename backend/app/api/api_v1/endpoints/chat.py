from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter()
service = ChatService()

@router.post("/query", response_model=ChatResponse)
async def query_chat(request: ChatRequest):
    response = await service.handle_query(request)
    return response
