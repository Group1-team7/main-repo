from app.schemas.report import ReportResponse
from app.schemas.risk import DetectedRisk, RiskLevel
from app.services.clause_segmenter import segment_contract
from app.services.guardrails import DISCLAIMER
from app.services.legal_retriever import retrieve_snippets
from app.services.risk_analyzer import analyze_risks
from app.services.text_cleaner import clean_contract_text

SAFE_RECOMMENDATION = (
    "Treat the flagged items as a first-pass review checklist only. Do not make a "
    "final decision from this report; review the contract and cited source snippets "
    "with a qualified lawyer."
)


def build_report(contract_text: str) -> ReportResponse:
    cleaned = clean_contract_text(contract_text)
    clauses = segment_contract(cleaned)
    risks_with_sources = [
        _attach_sources(risk)
        for risk in analyze_risks(clauses)
    ]

    return ReportResponse(
        contract_summary=_summary(len(clauses), len(risks_with_sources)),
        clause_count=len(clauses),
        detected_risks=risks_with_sources,
        overall_risk_level=_overall_risk_level(risks_with_sources),
        safe_recommendation=SAFE_RECOMMENDATION,
        disclaimer=DISCLAIMER,
    )


def _attach_sources(risk: DetectedRisk) -> DetectedRisk:
    return risk.model_copy(update={"sources": retrieve_snippets(risk.risk_type)})


def _summary(clause_count: int, risk_count: int) -> str:
    return (
        f"تم تحليل النص كعقد عمل لأغراض تعليمية أولية. تم تقسيمه إلى "
        f"{clause_count} بند/بنود، وتم رصد {risk_count} مؤشر/مؤشرات "
        "على مخاطر محتملة ضمن نطاق القواعد الخمس المحددة."
    )


def _overall_risk_level(risks: list[DetectedRisk]) -> RiskLevel:
    if any(risk.risk_level == "high" for risk in risks):
        return "high"
    if any(risk.risk_level == "medium" for risk in risks):
        return "medium"
    return "low"
