from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_contract_accepts_language_and_returns_disclaimer() -> None:
    response = client.post(
        "/analyze-contract",
        json={
            "contract_text": (
                "البند الأول: يتم تحديد الراتب لاحقاً حسب سياسة الشركة. "
                "البند الثاني: يجوز للشركة إنهاء العقد دون إشعار مسبق."
            ),
            "language": "ar",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["disclaimer"]
    assert body["clause_count"] == 2
    assert {risk["risk_type"] for risk in body["detected_risks"]} == {
        "salary_unclear",
        "termination_without_notice",
    }


def test_chat_refusal_includes_disclaimer() -> None:
    response = client.post(
        "/chat",
        json={"question": "Should I sign?", "contract_text": "نص عقد"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["refused"] is True
    assert body["disclaimer"]


def test_health_and_metrics_include_disclaimer() -> None:
    health = client.get("/health")
    metrics = client.get("/metrics")

    assert health.status_code == 200
    assert metrics.status_code == 200
    assert health.json()["disclaimer"]
    assert metrics.json()["disclaimer"]


def test_validation_error_includes_disclaimer() -> None:
    response = client.post("/analyze-contract", json={"contract_text": "نص", "language": "en"})

    assert response.status_code == 422
    assert response.json()["disclaimer"]
