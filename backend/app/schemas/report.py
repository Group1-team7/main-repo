from pydantic import BaseModel, Field

from app.schemas.risk import DetectedRisk, RiskLevel


class ReportResponse(BaseModel):
    contract_summary: str
    clause_count: int
    detected_risks: list[DetectedRisk] = Field(default_factory=list)
    overall_risk_level: RiskLevel
    safe_recommendation: str
    disclaimer: str
