from pathlib import Path

from app.services.legal_retriever import retrieve_snippets


def test_retrieve_snippets_by_risk_type(tmp_path: Path) -> None:
    kb = tmp_path / "legal_snippets.jsonl"
    kb.write_text(
        '{"risk_type":"salary_unclear","source_id":"MANUAL_VERIFY_TEST",'
        '"source_title":"MANUAL_FILL_FROM_OFFICIAL_SOURCE","source_url":"MANUAL_FILL_FROM_OFFICIAL_SOURCE",'
        '"snippet":"MANUAL_FILL_FROM_OFFICIAL_SOURCE","last_verified":"MANUAL_VERIFY",'
        '"trust_level":"placeholder_unverified"}\n',
        encoding="utf-8",
    )

    snippets = retrieve_snippets("salary_unclear", kb)

    assert len(snippets) == 1
    assert snippets[0].source_id == "MANUAL_VERIFY_TEST"
