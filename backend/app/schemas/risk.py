from typing import Literal

from pydantic import BaseModel, Field

RiskType = Literal[
    "termination_without_notice",
    "salary_unclear",
    "probation_unclear_or_long",
    "non_compete_overreach",
    "penalty_or_deduction_clause",
]

RiskLevel = Literal["low", "medium", "high"]


class LegalSnippet(BaseModel):
    risk_type: RiskType
    source_id: str
    source_title: str
    source_url: str
    snippet: str
    last_verified: str
    trust_level: str
    notes: str | None = None


class DetectedRisk(BaseModel):
    risk_id: str
    risk_type: RiskType
    risk_level: RiskLevel
    clause_id: int
    clause_text: str
    reason: str
    sources: list[LegalSnippet] = Field(default_factory=list)
    safe_recommendation: str
