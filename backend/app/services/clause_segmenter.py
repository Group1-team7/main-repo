import re
from collections.abc import Iterable

from app.schemas.contract import Clause
from app.services.text_cleaner import clean_contract_text

# TODO[PERSON-2]: Tune these boundaries against real Jordanian employment contracts.
_BOUNDARY_PATTERN = re.compile(
    r"\n{2,}|(?<=[.!؟?؛;])\s+|(?=(?:المادة|البند|(?<!\w)بند|Article)\s*[\d٠-٩]+)",
    flags=re.IGNORECASE,
)


def segment_contract(contract_text: str) -> list[Clause]:
    """Split pasted contract text into lightweight clause objects."""
    cleaned = clean_contract_text(contract_text)
    if not cleaned:
        return []

    parts = _split_parts(cleaned)
    clauses: list[Clause] = []
    for part in parts:
        candidate = part.strip(" \t\r\n-•*")
        if len(candidate) < 3:
            continue
        clauses.append(Clause(id=len(clauses) + 1, text=candidate))
    return clauses


def _split_parts(text: str) -> Iterable[str]:
    normalized = re.sub(r"\n\s*[-•*]\s*", "\n", text)
    parts = _BOUNDARY_PATTERN.split(normalized)
    if len(parts) <= 1 and len(text) > 350:
        return re.split(r"(?<=[.!؟?؛;])\s+", text)
    return parts
