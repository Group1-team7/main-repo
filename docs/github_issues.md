# Ready-To-Copy GitHub Issues

Copy each issue into GitHub Issues and assign it to the listed teammate. Keep the branch name in the issue body so the project board stays consistent.

## Issue 1: PERSON-1 Legal Data And Evaluation

**Assignee:** Osama Harrab (@osamaharrab)

**Branch:** `feature/person-1-legal-data-eval`

**Objective:** Replace placeholder legal knowledge with manually verified official Jordanian source snippets and expand evaluation coverage.

**Files owned:**

- `data/legal_knowledge/legal_snippets.jsonl`
- `data/legal_knowledge/source_manifest.csv`
- `data/kg_lite/legal_edges.csv`
- `eval/heldout_clauses.jsonl`
- `eval/evaluate.py`
- `eval/results.json`
- `eval/failure_cases.md`

**Tasks:**

- [ ] TODO[PERSON-1]: Replace each `MANUAL_FILL_FROM_OFFICIAL_SOURCE` placeholder with a short manually verified official Jordanian source snippet.
- [ ] TODO[PERSON-1]: Update `source_url`, `source_id`, `last_verified`, and `trust_level`.
- [ ] TODO[PERSON-1]: Expand heldout evaluation cases across all five risk types.
- [ ] TODO[PERSON-1]: Document false positives and false negatives in `eval/failure_cases.md`.

**Definition of done:**

- [ ] `python eval/evaluate.py` runs without crashing.
- [ ] No legal source is fake or unverified.
- [ ] No snippet provides legal advice or states that a clause is illegal.

**Do not edit without coordination:**

- `backend/app/services/risk_analyzer.py`
- `backend/app/routers/*`
- `web/*`

## Issue 2: PERSON-2 Text Cleaning, Segmentation, And Rules

**Assignee:** Afrah Alsnaid (@afrah24ali)

**Branch:** `feature/person-2-text-risk-rules`

**Objective:** Improve deterministic Arabic text preparation and risk detection while staying within the five approved risk types.

**Files owned:**

- `backend/app/services/text_cleaner.py`
- `backend/app/services/clause_segmenter.py`
- `backend/app/services/risk_analyzer.py`
- `backend/tests/test_clause_segmenter.py`
- `backend/tests/test_risk_analyzer.py`

**Tasks:**

- [ ] TODO[PERSON-2]: Improve segmentation for Arabic ordinal markers such as `البند الأول` and `البند الثاني`.
- [ ] TODO[PERSON-2]: Add tests for written salary amounts and Arabic duration wording.
- [ ] TODO[PERSON-2]: Tune false positives discovered by PERSON-1 evaluation.
- [ ] TODO[PERSON-2]: Keep the detector limited to the five approved risk types.

**Definition of done:**

- [ ] `pytest` runs from inside `backend`.
- [ ] Existing evaluation cases still run through `python eval/evaluate.py`.
- [ ] Risk reasons use safe wording such as "potential risk", "may be related", and "review with a qualified lawyer".

**Do not edit without coordination:**

- `data/legal_knowledge/legal_snippets.jsonl`
- `backend/app/routers/*`
- `web/*`

## Issue 3: PERSON-3 Backend API, Retrieval, Guardrails, And Metrics

**Assignee:** Osaid Ziad Alhawamdeh (@OsaidZiad04)

**Branch:** `feature/person-3-backend-guardrails`

**Objective:** Keep the FastAPI app stable, scoped, local-only for retrieval, and safe for educational use.

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

**Tasks:**

- [ ] TODO[PERSON-3]: Verify `uvicorn app.main:app --reload` starts from inside `backend`.
- [ ] TODO[PERSON-3]: Verify `POST /analyze-contract` accepts `contract_text` and `language: "ar"`.
- [ ] TODO[PERSON-3]: Ensure every successful API response includes a disclaimer.
- [ ] TODO[PERSON-3]: Add tests for unsafe chat prompts: sign/do-not-sign, illegal/legal, lawsuit, and sue questions.

**Definition of done:**

- [ ] FastAPI starts from inside `backend`.
- [ ] `/analyze-contract`, `/chat`, `/health`, `/metrics`, and `/legal-disclaimer` return disclaimers.
- [ ] Retrieval uses only `data/legal_knowledge/legal_snippets.jsonl` by `risk_type`.

**Do not edit without coordination:**

- `data/legal_knowledge/legal_snippets.jsonl`
- `eval/heldout_clauses.jsonl`
- `web/components/*`

## Issue 4: PERSON-4 Frontend, Docs, And Demo

**Assignee:** Yamen Ayman (@yamenayman)

**Branch:** `feature/person-4-frontend-docs-demo`

**Objective:** Keep the web UI usable for the demo and keep docs aligned with the educational, non-legal-advice scope.

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

**Tasks:**

- [ ] TODO[PERSON-4]: Confirm the frontend calls `NEXT_PUBLIC_API_BASE_URL`.
- [ ] TODO[PERSON-4]: Keep mock fallback data aligned with backend schemas.
- [ ] TODO[PERSON-4]: Keep disclaimer visible near analysis results and scoped chat.
- [ ] TODO[PERSON-4]: Finalize the demo script with one allowed chat question and one refused chat question.

**Definition of done:**

- [ ] `npm run build` runs from inside `web`.
- [ ] Demo instructions work with `data/sample_contracts`.
- [ ] UI copy does not claim to provide legal advice, determine legality, recommend signing, or draft lawsuits.

**Do not edit without coordination:**

- `backend/app/services/risk_analyzer.py`
- `backend/app/services/legal_retriever.py`
- `data/legal_knowledge/*`
- `eval/*`
