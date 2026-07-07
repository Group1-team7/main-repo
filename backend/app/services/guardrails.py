import re

DISCLAIMER = (
    "Educational capstone MVP only. This output is not legal advice, does not decide "
    "whether a clause is legal or illegal, and should not be used as a sign/do-not-sign "
    "recommendation. Review any potential risk with a qualified lawyer in Jordan."
)

_UNSAFE_PATTERNS = [
    r"\bshould\s+i\s+sign\b",
    r"\bsign\s+or\s+not\b",
    r"\bis\s+this\s+illegal\b",
    r"\billegal\b",
    r"\blawsuit\b",
    r"\bsue\b",
    r"\bcan\s+i\s+sue\b",
    r"\blegal\s+advice\b",
    r"\bfinal\s+advice\b",
    r"هل\s+أوقع",
    r"هل\s+اوقع",
    r"أوقع\s+العقد",
    r"اوقع\s+العقد",
    r"غير\s+قانوني",
    r"مخالف\s+للقانون",
    r"ارفع\s+دعوى",
    r"دعوى",
    r"أقاضي",
    r"اقاضي",
    r"أستطيع\s+مقاضاة",
    r"استطيع\s+مقاضاة",
]

_ALLOWED_SCOPE_TERMS = [
    "summarize",
    "summary",
    "risk",
    "risks",
    "top",
    "salary",
    "termination",
    "probation",
    "non-compete",
    "non compete",
    "penalty",
    "deduction",
    "لخص",
    "تلخيص",
    "مخاطر",
    "الخطر",
    "أهم",
    "اهم",
    "راتب",
    "الأجر",
    "اجر",
    "إنهاء",
    "انهاء",
    "فصل",
    "تجربة",
    "اختبار",
    "عدم منافسة",
    "غرامة",
    "خصم",
    "اقتطاع",
]


def is_unsafe_legal_advice_question(question: str) -> bool:
    lowered = question.casefold()
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in _UNSAFE_PATTERNS)


def is_in_scope_contract_question(question: str) -> bool:
    lowered = question.casefold()
    return any(term.casefold() in lowered for term in _ALLOWED_SCOPE_TERMS)


def refusal_message() -> str:
    return (
        "I cannot provide final legal advice, decide whether something is illegal, "
        "recommend signing or not signing, draft a lawsuit, or advise whether to sue. "
        "I can summarize potential risks in the pasted contract and point to manually "
        "verified source snippets when they are available."
    )


def allowed_scope_message() -> str:
    return (
        "I can only answer scoped questions about the pasted contract: summarize "
        "potential risks, list top risks, or discuss salary, termination, probation, "
        "non-compete, penalties, or deductions."
    )
