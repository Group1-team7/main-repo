import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.schemas.contract import Clause  # noqa: E402
from app.services.risk_analyzer import analyze_risks  # noqa: E402

HELDOUT_PATH = ROOT / "eval" / "heldout_clauses.jsonl"
RESULTS_PATH = ROOT / "eval" / "results.json"


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def evaluate() -> dict:
    rows = read_jsonl(HELDOUT_PATH)
    cases = []
    correct = 0

    for row in rows:
        risks = analyze_risks([Clause(id=1, text=row["clause_text"])])
        predicted = sorted({risk.risk_type for risk in risks})
        expected = sorted(row["expected_risk_types"])
        is_correct = predicted == expected
        correct += int(is_correct)
        cases.append(
            {
                "id": row["id"],
                "expected_risk_types": expected,
                "predicted_risk_types": predicted,
                "correct": is_correct,
            }
        )

    accuracy = correct / len(rows) if rows else 0.0
    result = {
        "risk_detection_accuracy": accuracy,
        "total_cases": len(rows),
        "correct_cases": correct,
        "cases": cases,
        "notes": "TODO[PERSON-1]: Expand heldout set after manual data review.",
    }
    RESULTS_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    output = evaluate()
    print(f"risk_detection_accuracy={output['risk_detection_accuracy']:.3f}")
