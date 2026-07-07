from app.schemas.contract import Clause
from app.services.risk_analyzer import analyze_risks


def test_detects_termination_without_notice() -> None:
    risks = analyze_risks(
        [Clause(id=1, text="يجوز لصاحب العمل إنهاء العقد في أي وقت دون إشعار.")]
    )

    assert [risk.risk_type for risk in risks] == ["termination_without_notice"]


def test_detects_salary_unclear_and_probation_long() -> None:
    risks = analyze_risks(
        [
            Clause(id=1, text="يحدد الراتب لاحقاً حسب تقدير الشركة."),
            Clause(id=2, text="تكون مدة التجربة ستة أشهر قابلة للتمديد."),
        ]
    )

    assert {risk.risk_type for risk in risks} == {
        "salary_unclear",
        "probation_unclear_or_long",
    }
