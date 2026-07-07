from app.services.clause_segmenter import segment_contract


def test_segment_contract_splits_arabic_numbered_clauses() -> None:
    text = """
    البند 1 يلتزم العامل بالدوام.
    البند 2 يجوز إنهاء العقد دون إشعار.
    """

    clauses = segment_contract(text)

    assert len(clauses) == 2
    assert clauses[0].id == 1
    assert "البند 2" in clauses[1].text
