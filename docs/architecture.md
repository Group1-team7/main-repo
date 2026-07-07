# Architecture

Lawz AI JO Ultra-MVP is a 6-day educational capstone scaffold for first-pass Jordanian employment contract risk triage. It is not a legal product and does not provide legal advice.

## Flow

1. User pastes Arabic employment contract text in the web UI.
2. FastAPI receives `POST /analyze-contract`.
3. `text_cleaner.py` normalizes whitespace and hidden characters.
4. `clause_segmenter.py` splits the text into simple clauses.
5. `risk_analyzer.py` applies deterministic rules for exactly five risk types.
6. `legal_retriever.py` retrieves local JSONL snippets by `risk_type`.
7. `report_builder.py` returns summary, clause count, detected risks, citations, safe recommendation, and disclaimer.
8. `chat_service.py` only answers scoped questions and refuses legal-advice requests.

## Components

- `backend/app/routers`: FastAPI routes.
- `backend/app/services`: deterministic MVP logic.
- `data/legal_knowledge/legal_snippets.jsonl`: placeholder local knowledge base.
- `eval/evaluate.py`: rule accuracy check over heldout clauses.
- `web`: Next.js frontend with backend calls and mock fallback.

## Constraints

- No legal advice, no illegal/legal determinations, no sign/do-not-sign recommendation.
- No lawsuit drafting or sue/not-sue advice.
- No PDF parsing in the MVP.
- No fine-tuning, external vector database, or Neo4j.
- Legal snippets must be manually filled from official Jordanian sources only.

## TODO Owners

- TODO[PERSON-1]: Fill verified legal snippets and expand evaluation.
- TODO[PERSON-2]: Improve cleaning, segmentation, and risk rules.
- TODO[PERSON-3]: Harden API, retrieval, guardrails, and metrics.
- TODO[PERSON-4]: Polish frontend, docs, and demo flow.
