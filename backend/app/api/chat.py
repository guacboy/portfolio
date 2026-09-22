from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.rag.chat import answer

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = answer(request.message)
    return ChatResponse(answer=result.answer, sources=result.sources)
