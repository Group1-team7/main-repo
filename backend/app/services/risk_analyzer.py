import re
from collections.abc import Callable, Sequence

from app.schemas.contract import Clause
from app.schemas.risk import DetectedRisk, RiskLevel, RiskType

RISK_TYPES: tuple[RiskType, ...] = (
    "termination_without_notice",
    "salary_unclear",
    "probation_unclear_or_long",
    "non_compete_overreach",
    "penalty_or_deduction_clause",
)

_RECOMMENDATIONS: dict[RiskType, str] = {
    "termination_without_notice": (
        "Review notice-period wording with a qualified lawyer before relying on it."
    ),
    "salary_unclear": (
        "Ask a qualified reviewer to confirm whether salary amount, payment timing, "
        "and allowances are clear enough."
    ),
    "probation_unclear_or_long": (
        "Review probation duration and extension language with a qualified lawyer."
    ),
    "non_compete_overreach": (
        "Review the scope, duration, geography, and work restrictions with a qualified lawyer."
    ),
    "penalty_or_deduction_clause": (
        "Review any deduction, penalty, or liquidated amount with a qualified lawyer."
    ),
}

_REASONS: dict[RiskType, str] = {
    "termination_without_notice": (
        "The clause mentions ending employment with wording that may remove or weaken notice."
    ),
    "salary_unclear": (
        "The clause discusses salary or compensation but may leave amount, timing, or method unclear."
    ),
    "probation_unclear_or_long": (
        "The clause mentions a probation period that may be unclear, extendable, or longer than expected."
    ),
    "non_compete_overreach": (
        "The clause mentions non-compete or post-employment restrictions that may be broad."
    ),
    "penalty_or_deduction_clause": (
        "The clause mentions deductions, penalties, or fixed compensation that may need review."
    ),
}

_LEVELS: dict[RiskType, RiskLevel] = {
    "termination_without_notice": "high",
    "salary_unclear": "medium",
    "probation_unclear_or_long": "medium",
    "non_compete_overreach": "high",
    "penalty_or_deduction_clause": "medium",
}

_ARABIC_NUMBERS = {
    "واحد": 1,
    "واحدة": 1,
    "شهر": 1,
    "شهرين": 2,
    "اثنين": 2,
    "إثنين": 2,
    "اثنان": 2,
    "ثلاث": 3,
    "ثلاثة": 3,
    "اربع": 4,
    "أربع": 4,
    "اربعة": 4,
    "أربعة": 4,
    "خمس": 5,
    "خمسة": 5,
    "ست": 6,
    "ستة": 6,
    "سبع": 7,
    "سبعة": 7,
    "ثمان": 8,
    "ثمانية": 8,
    "تسع": 9,
    "تسعة": 9,
    "عشر": 10,
    "عشرة": 10,
}


def analyze_risks(clauses: Sequence[Clause]) -> list[DetectedRisk]:
    """Detect only the five approved MVP risk types using deterministic rules."""
    # TODO[PERSON-2]: Expand rules only after evaluation examples expose a real miss.
    detected: list[DetectedRisk] = []

    detectors: dict[RiskType, Callable[[str], bool]] = {
        "termination_without_notice": _is_termination_without_notice,
        "salary_unclear": _is_salary_unclear,
        "probation_unclear_or_long": _is_probation_unclear_or_long,
        "non_compete_overreach": _is_non_compete_overreach,
        "penalty_or_deduction_clause": _is_penalty_or_deduction_clause,
    }

    for clause in clauses:
        for risk_type in RISK_TYPES:
            if detectors[risk_type](clause.text):
                detected.append(
                    DetectedRisk(
                        risk_id=f"{risk_type}-{clause.id}",
                        risk_type=risk_type,
                        risk_level=_LEVELS[risk_type],
                        clause_id=clause.id,
                        clause_text=clause.text,
                        reason=_REASONS[risk_type],
                        safe_recommendation=_RECOMMENDATIONS[risk_type],
                    )
                )

    return detected


def _is_termination_without_notice(text: str) -> bool:
    lowered = text.casefold()
    has_termination = _contains_any(
        lowered,
        ["إنهاء", "انهاء", "فسخ", "فصل", "ينهي", "terminate", "termination", "dismiss"],
    )
    weak_notice = _contains_any(
        lowered,
        [
            "دون إشعار",
            "دون اشعار",
            "بدون إشعار",
            "بدون اشعار",
            "فوري",
            "في أي وقت",
            "في اي وقت",
            "without notice",
            "immediate",
        ],
    )
    return has_termination and weak_notice


def _is_salary_unclear(text: str) -> bool:
    lowered = text.casefold()
    has_salary = _contains_any(
        lowered,
        ["راتب", "الأجر", "الاجر", "أجر", "اجر", "تعويض", "بدل", "salary", "wage"],
    )
    if not has_salary:
        return False

    unclear = _contains_any(
        lowered,
        [
            "يحدد لاحقا",
            "يحدد لاحقاً",
            "حسب تقدير",
            "حسب الشركة",
            "غير محدد",
            "يتم الاتفاق عليه",
            "as determined",
            "to be agreed",
            "not specified",
        ],
    )
    deduction_context = _contains_any(
        lowered,
        ["خصم", "اقتطاع", "حسم", "غرامة", "penalty", "deduction"],
    )
    if deduction_context and not unclear:
        return False

    missing_amount = not _has_numeric_amount(text)
    return unclear or missing_amount


def _is_probation_unclear_or_long(text: str) -> bool:
    lowered = text.casefold()
    if not _contains_any(lowered, ["تجربة", "اختبار", "probation", "trial period"]):
        return False

    if _contains_any(
        lowered,
        ["قابلة للتمديد", "قابل للتمديد", "تمديد", "غير محددة", "غير محدد", "extendable"],
    ):
        return True

    months = _extract_duration_months(lowered)
    return months is None or months > 3


def _is_non_compete_overreach(text: str) -> bool:
    lowered = text.casefold()
    has_non_compete = _contains_any(
        lowered,
        [
            "عدم منافسة",
            "منافسة",
            "العمل لدى شركة أخرى",
            "العمل لدى شركة اخرى",
            "non-compete",
            "non compete",
            "competitor",
        ],
    )
    broad_scope = _contains_any(
        lowered,
        [
            "أي مكان",
            "اي مكان",
            "داخل وخارج الأردن",
            "داخل وخارج الاردن",
            "جميع القطاعات",
            "أي نشاط",
            "اي نشاط",
            "لمدة سنتين",
            "لمدة ثلاث",
            "لمدة 2",
            "لمدة 3",
            "دائما",
            "دائماً",
            "anywhere",
            "worldwide",
            "all sectors",
            "two years",
            "three years",
        ],
    )
    post_employment = _contains_any(
        lowered,
        ["بعد انتهاء", "بعد إنهاء", "بعد انهاء", "post-employment", "after termination"],
    )
    return has_non_compete and (broad_scope or post_employment)


def _is_penalty_or_deduction_clause(text: str) -> bool:
    lowered = text.casefold()
    return _contains_any(
        lowered,
        [
            "غرامة",
            "خصم",
            "اقتطاع",
            "حسم",
            "جزاء",
            "تعويض مقطوع",
            "من الراتب",
            "penalty",
            "deduction",
            "liquidated damages",
        ],
    )


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term.casefold() in text for term in terms)


def _has_numeric_amount(text: str) -> bool:
    return bool(
        re.search(
            r"(\d+|[٠-٩]+)\s*(دينار|د\.أ|jd|jod|dinar|ديناراً|دينارا)?",
            text,
            flags=re.IGNORECASE,
        )
    )


def _extract_duration_months(text: str) -> int | None:
    numeric_match = re.search(
        r"(\d+|[٠-٩]+)\s*(شهر|أشهر|اشهر|months?|سنة|سنوات|year|years)",
        text,
        flags=re.IGNORECASE,
    )
    if numeric_match:
        value = int(numeric_match.group(1).translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")))
        unit = numeric_match.group(2).casefold()
        return value * 12 if unit in {"سنة", "سنوات", "year", "years"} else value

    for word, value in _ARABIC_NUMBERS.items():
        if word in text and _contains_any(text, ["شهر", "أشهر", "اشهر"]):
            return value

    if _contains_any(text, ["سنة", "سنوات"]):
        for word, value in _ARABIC_NUMBERS.items():
            if word in text:
                return value * 12

    return None
