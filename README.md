# Lawz AI JO Ultra-MVP

Group 1 Team 7 Capstone project inside the existing `main-repo`.

Lawz AI JO Ultra-MVP is a 6-day educational capstone scaffold for a Jordanian employment contract first-pass risk checker. It accepts pasted Arabic employment contract text, segments it into clauses, detects five predefined potential risk types with deterministic rules, retrieves placeholder legal snippets from a local JSONL file, and returns a structured report with citations and a disclaimer.

This is not a legal product and does not provide legal advice.

## MVP Scope

Supported risk types:

- `termination_without_notice`
- `salary_unclear`
- `probation_unclear_or_long`
- `non_compete_overreach`
- `penalty_or_deduction_clause`

The system must use safe wording such as "potential risk", "may be related", and "review with a qualified lawyer". It must not say a clause is illegal, recommend signing or not signing, draft lawsuits, or provide final legal advice.

## Repository Layout

- `backend/`: FastAPI app, services, schemas, metrics, and pytest tests.
- `web/`: simple Next.js/React TypeScript frontend.
- `data/`: sample contracts, placeholder legal knowledge JSONL, lightweight CSV edges.
- `eval/`: heldout clauses, evaluation script, results file, and failure notes.
- `docs/`: architecture, limitations, disclaimer, demo, assignments, and issue planning.

## Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend endpoints:

- `GET /health`
- `GET /metrics`
- `GET /legal-disclaimer`
- `POST /analyze-contract`
- `POST /chat`

Example:

```bash
curl -X POST http://localhost:8000/analyze-contract ^
  -H "Content-Type: application/json" ^
  -d "{\"contract_text\":\"يجوز لصاحب العمل إنهاء العقد دون إشعار.\"}"
```

## Frontend Setup

```bash
cd web
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend calls `NEXT_PUBLIC_API_BASE_URL` and falls back to mock data if the backend is unavailable.

## Docker Compose

```bash
docker compose up
```

This starts:

- API at `http://localhost:8000`
- Web app at `http://localhost:3000`

## Tests and Evaluation

Run backend tests:

```bash
cd backend
pytest
```

Run evaluation from the repo root:

```bash
python eval/evaluate.py
```

The script prints `risk_detection_accuracy` and writes `eval/results.json`.

## Team Workflow

- PERSON-1: Legal data + evaluation.
- PERSON-2: Text cleaning + clause segmentation + risk rules.
- PERSON-3: Backend API + retrieval + guardrails + metrics.
- PERSON-4: Frontend + docs + demo.

Branch rules:

- Do not commit directly to `main`.
- Use feature branches like `feature/legal-snippets`, `feature/risk-rules`, or `fix/chat-guardrails`.
- Open a PR for each meaningful change.
- Require two teammate approvals before merging.
- Keep PRs small enough to review during daily sync.

## Legal Data Rule

`data/legal_knowledge/legal_snippets.jsonl` contains placeholder records only. Teammates must manually fill snippets from official Jordanian sources and update `source_url`, `source_id`, `last_verified`, and `trust_level`. Do not invent citations or use unverified legal snippets in the final demo.

## Legal Disclaimer

Educational capstone MVP only. This output is not legal advice, does not decide whether a clause is legal or illegal, and should not be used as a sign/do-not-sign recommendation. Review any potential risk with a qualified lawyer in Jordan.
