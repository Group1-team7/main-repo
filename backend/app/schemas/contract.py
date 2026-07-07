from typing import Literal

from pydantic import BaseModel, Field


class ContractAnalyzeRequest(BaseModel):
    contract_text: str = Field(..., min_length=1)
    language: Literal["ar"] = Field(
        default="ar",
        description="MVP language scope. Only Arabic pasted contract text is supported.",
    )


class Clause(BaseModel):
    id: int
    text: str
