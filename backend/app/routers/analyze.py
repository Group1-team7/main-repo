from fastapi import APIRouter, HTTPException

from app.monitoring.metrics import record_analyze
from app.schemas.contract import ContractAnalyzeRequest
from app.schemas.report import ReportResponse
from app.services.report_builder import build_report
from app.services.text_cleaner import clean_contract_text

router = APIRouter(tags=["analysis"])


@router.post("/analyze-contract", response_model=ReportResponse)
def analyze_contract(request: ContractAnalyzeRequest) -> ReportResponse:
    """Analyze pasted contract text using deterministic MVP rules."""
    cleaned = clean_contract_text(request.contract_text)
    if not cleaned:
        raise HTTPException(status_code=400, detail="contract_text cannot be empty")

    record_analyze()
    return build_report(cleaned)
