import json
from pathlib import Path

from pydantic import ValidationError

from app.schemas.risk import LegalSnippet, RiskType

DEFAULT_KB_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "legal_knowledge"
    / "legal_snippets.jsonl"
)


def load_legal_snippets(kb_path: str | Path = DEFAULT_KB_PATH) -> list[LegalSnippet]:
    """Load manually curated legal snippets from local JSONL."""
    path = Path(kb_path)
    if not path.exists():
        return []

    snippets: list[LegalSnippet] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            snippets.append(LegalSnippet.model_validate(json.loads(line)))
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(f"Invalid legal snippet at {path}:{line_number}") from exc
    return snippets


def retrieve_snippets(
    risk_type: RiskType,
    kb_path: str | Path = DEFAULT_KB_PATH,
) -> list[LegalSnippet]:
    """Return snippets matching a risk type. No semantic search in the MVP."""
    # TODO[PERSON-1]: Replace placeholders with manually verified official snippets.
    # TODO[PERSON-3]: Add cache invalidation if the JSONL grows during demos.
    return [snippet for snippet in load_legal_snippets(kb_path) if snippet.risk_type == risk_type]
