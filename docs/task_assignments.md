# Task Assignments

This file maps the four sprint roles to named teammates, branch names, owned files, TODO checklist, definition of done, and files they must not edit without a coordinating PR comment.

## PERSON-1: Osama Harrab (@osamaharrab)

**Role:** Legal data + evaluation

**Branch name:** `feature/person-1-legal-data-eval`

**Files owned:**

- `data/legal_knowledge/legal_snippets.jsonl`
- `data/legal_knowledge/source_manifest.csv`
- `data/kg_lite/legal_edges.csv`
- `eval/heldout_clauses.jsonl`
- `eval/evaluate.py`
- `eval/results.json`
- `eval/failure_cases.md`

**TODO checklist:**

- TODO[PERSON-1]: Replace every `MANUAL_FILL_FROM_OFFICIAL_SOURCE` placeholder with a manually verified official Jordanian source snippet.
- TODO[PERSON-1]: Update `source_url`, `source_id`, `last_verified`, and `trust_level` after verification.
- TODO[PERSON-1]: Expand `eval/heldout_clauses.jsonl` to include representative true positives and true negatives for all five risk types.
- TODO[PERSON-1]: Record misses and false positives in `eval/failure_cases.md`.

**Definition of done:**

- All legal snippets remain short, manually verified, and from official Jordanian sources only.
- `python eval/evaluate.py` runs from the repo root and writes `eval/results.json`.
- No snippet gives legal advice or states that a clause is legal or illegal.

**Files they must not edit without coordination:**

- `backend/app/services/risk_analyzer.py`
- `backend/app/routers/*`
- `web/*`
- `docs/demo_script.md`

## PERSON-2: Afrah Alsnaid (@afrah24ali)

**Role:** Text cleaning + clause segmentation + risk rules

**Branch name:** `feature/person-2-text-risk-rules`

**Files owned:**

- `backend/app/services/text_cleaner.py`
- `backend/app/services/clause_segmenter.py`
- `backend/app/services/risk_analyzer.py`
- `backend/tests/test_clause_segmenter.py`
- `backend/tests/test_risk_analyzer.py`

**TODO checklist:**

- TODO[PERSON-2]: Improve Arabic clause segmentation using examples from `data/sample_contracts`.
- TODO[PERSON-2]: Tune only the five approved deterministic risk rules.
- TODO[PERSON-2]: Add pytest cases for Arabic ordinal clauses, written amounts, and false positives.
- TODO[PERSON-2]: Keep wording limited to "potential risk" and "may be related" in user-facing reasons.

**Definition of done:**

- `pytest` passes from inside `backend`.
- The five risk types remain exactly the approved MVP list.
- No rule says a clause is illegal or gives sign/do-not-sign advice.

**Files they must not edit without coordination:**

- `data/legal_knowledge/legal_snippets.jsonl`
- `backend/app/routers/*`
- `web/*`
- `docs/github_issues.md`

## PERSON-3: Osaid Ziad Alhawamdeh (@OsaidZiad04)

**Role:** Backend API + retrieval + guardrails + metrics

**Branch name:** `feature/person-3-backend-guardrails`

**Files owned:**

- `backend/app/main.py`
- `backend/app/routers/*`
- `backend/app/schemas/*`
- `backend/app/services/legal_retriever.py`
- `backend/app/services/report_builder.py`
- `backend/app/services/chat_service.py`
- `backend/app/services/guardrails.py`
- `backend/app/monitoring/metrics.py`
- `backend/tests/test_api_contract.py`
- `backend/tests/test_legal_retriever.py`

**TODO checklist:**

- TODO[PERSON-3]: Keep every API response shape carrying a disclaimer.
- TODO[PERSON-3]: Add regression tests for unsafe chat refusals.
- TODO[PERSON-3]: Keep retrieval local JSONL by `risk_type`; do not add an external vector database for the Ultra-MVP.
- TODO[PERSON-3]: Keep metrics lightweight and privacy-safe.

**Definition of done:**

- `uvicorn app.main:app --reload` starts from inside `backend`.
- `POST /analyze-contract` accepts `contract_text` and `language: "ar"`.
- Unsafe chat questions are refused with a disclaimer and no legal advice.

**Files they must not edit without coordination:**

- `data/legal_knowledge/legal_snippets.jsonl`
- `eval/heldout_clauses.jsonl`
- `web/components/*`
- `docs/demo_script.md`

## PERSON-4: Yamen Ayman (@yamenayman)

**Role:** Frontend + docs + demo

**Branch name:** `feature/person-4-frontend-docs-demo`

**Files owned:**

- `web/app/*`
- `web/components/*`
- `web/lib/*`
- `web/package.json`
- `web/tsconfig.json`
- `docs/architecture.md`
- `docs/demo_script.md`
- `docs/legal_disclaimer.md`
- `docs/limitations.md`
- `docs/task_assignments.md`
- `docs/github_issues.md`
- `README.md`

**TODO checklist:**

- TODO[PERSON-4]: Keep the frontend mock response aligned with the backend response schema.
- TODO[PERSON-4]: Keep disclaimer text visible in the analysis view and chat responses.
- TODO[PERSON-4]: Prepare the demo flow using `data/sample_contracts`.
- TODO[PERSON-4]: Keep docs clear that this is an educational MVP, not a legal product.

**Definition of done:**

- `npm run build` passes from inside `web`.
- The UI can call the backend and falls back to mock data if the backend is unavailable.
- No user-facing UI copy claims to provide legal advice.

**Files they must not edit without coordination:**

- `backend/app/services/risk_analyzer.py`
- `backend/app/services/legal_retriever.py`
- `data/legal_knowledge/*`
- `eval/*`
