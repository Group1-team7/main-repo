from pydantic import BaseModel, Field

from app.schemas.risk import LegalSnippet


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    contract_text: str = ""


class ChatResponse(BaseModel):
    answer: str
    refused: bool
    citations: list[LegalSnippet] = Field(default_factory=list)
    disclaimer: str
