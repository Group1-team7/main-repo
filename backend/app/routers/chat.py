from fastapi import APIRouter

from app.monitoring.metrics import record_chat
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import answer_chat

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    response = answer_chat(request)
    record_chat(refused=response.refused)
    return response
