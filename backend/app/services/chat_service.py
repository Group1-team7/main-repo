from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.risk import DetectedRisk, LegalSnippet, RiskType
from app.services.guardrails import (
    DISCLAIMER,
    allowed_scope_message,
    is_in_scope_contract_question,
    is_unsafe_legal_advice_question,
    refusal_message,
)
from app.services.report_builder import build_report
from app.services.text_cleaner import clean_contract_text

TOPIC_TO_RISK_TYPES: dict[str, list[RiskType]] = {
    "salary": ["salary_unclear"],
    "راتب": ["salary_unclear"],
    "الأجر": ["salary_unclear"],
    "اجر": ["salary_unclear"],
    "termination": ["termination_without_notice"],
    "إنهاء": ["termination_without_notice"],
    "انهاء": ["termination_without_notice"],
    "فصل": ["termination_without_notice"],
    "probation": ["probation_unclear_or_long"],
    "تجربة": ["probation_unclear_or_long"],
    "اختبار": ["probation_unclear_or_long"],
    "non-compete": ["non_compete_overreach"],
    "non compete": ["non_compete_overreach"],
    "عدم منافسة": ["non_compete_overreach"],
    "penalty": ["penalty_or_deduction_clause"],
    "deduction": ["penalty_or_deduction_clause"],
    "غرامة": ["penalty_or_deduction_clause"],
    "خصم": ["penalty_or_deduction_clause"],
}


def answer_chat(request: ChatRequest) -> ChatResponse:
    question = request.question.strip()

    if is_unsafe_legal_advice_question(question):
        return ChatResponse(
            answer=refusal_message(),
            refused=True,
            citations=[],
            disclaimer=DISCLAIMER,
        )

    if not is_in_scope_contract_question(question):
        return ChatResponse(
            answer=allowed_scope_message(),
            refused=True,
            citations=[],
            disclaimer=DISCLAIMER,
        )

    if not clean_contract_text(request.contract_text):
        return ChatResponse(
            answer=(
                "Please paste the employment contract text first. I can only discuss "
                "potential risks found in the pasted contract."
            ),
            refused=False,
            citations=[],
            disclaimer=DISCLAIMER,
        )

    report = build_report(request.contract_text)
    selected_risks = _select_risks_for_question(question, report.detected_risks)
    answer = _build_scoped_answer(question, report.detected_risks, selected_risks)
    return ChatResponse(
        answer=answer,
        refused=False,
        citations=_dedupe_sources(selected_risks),
        disclaimer=DISCLAIMER,
    )


def _select_risks_for_question(
    question: str, detected_risks: list[DetectedRisk]
) -> list[DetectedRisk]:
    lowered = question.casefold()
    requested_types: set[RiskType] = set()

    for keyword, risk_types in TOPIC_TO_RISK_TYPES.items():
        if keyword.casefold() in lowered:
            requested_types.update(risk_types)

    if not requested_types:
        return detected_risks

    return [risk for risk in detected_risks if risk.risk_type in requested_types]


def _build_scoped_answer(
    question: str,
    all_risks: list[DetectedRisk],
    selected_risks: list[DetectedRisk],
) -> str:
    lowered = question.casefold()
    wants_top = "top" in lowered or "أهم" in question or "اخطر" in question

    risks_to_show = selected_risks
    if wants_top:
        risks_to_show = sorted(
            selected_risks or all_risks,
            key=lambda risk: {"high": 3, "medium": 2, "low": 1}[risk.risk_level],
            reverse=True,
        )[:3]

    if not risks_to_show:
        return (
            "The MVP rules did not flag a matching potential risk in the pasted "
            "contract. This is not a legal conclusion; review the contract with a "
            "qualified lawyer for legal interpretation."
        )

    lines = [
        "Potential risks found in the pasted contract:",
    ]
    for risk in risks_to_show:
        lines.append(
            f"- {risk.risk_type} ({risk.risk_level}) in clause {risk.clause_id}: "
            f"{risk.reason}"
        )
    lines.append(
        "Use these points as a review checklist and discuss them with a qualified lawyer."
    )
    return "\n".join(lines)


def _dedupe_sources(risks: list[DetectedRisk]) -> list[LegalSnippet]:
    seen: set[str] = set()
    citations: list[LegalSnippet] = []
    for risk in risks:
        for source in risk.sources:
            key = f"{source.risk_type}:{source.source_id}"
            if key not in seen:
                citations.append(source)
                seen.add(key)
    return citations
