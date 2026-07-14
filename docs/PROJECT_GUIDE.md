# Lawz AI JO Project Guide

This guide explains the Lawz AI JO capstone project in enough detail for teammates, reviewers, and future PDF export.

## 1. Project Overview

Lawz AI JO is a focused Arabic Retrieval-Augmented Generation (RAG) assistant for Jordanian labor-law information. It accepts an Arabic question, retrieves relevant legal chunks from Weaviate, builds a grounded Arabic prompt, calls the configured LLM provider, and returns an Arabic answer with backend-generated citations.

The project is intentionally small. It is not a broad legal chatbot. It demonstrates a clean RAG workflow with Docker services, xAI/Grok or optional Ollama generation, a Neo4j Text2Cypher proof of concept, self-hosted answer translation, observability, and evaluation tooling.

## 2. Problem Statement

Jordanian labor-law information can be hard to search and summarize for non-specialists. The project provides a simple interface where a user can ask a labor-law information question in Arabic and receive a short grounded explanation with references to retrieved source chunks.

The answer is informational only. It is not a final legal opinion and does not replace official legal texts or a qualified lawyer.

## 3. Scope

The project does:

- Accept Arabic labor-law information questions.
- Embed the question with `intfloat/multilingual-e5-small`.
- Retrieve relevant legal chunks from Weaviate.
- Apply a simple lexical overlap rerank on top of vector retrieval.
- Build a grounded Arabic prompt from retrieved context.
- Call xAI/Grok by default, with Ollama available as an optional local provider.
- Return an Arabic answer, backend citations, retrieved chunk previews, confidence, and disclaimer.
- Provide a separate Neo4j Text2Cypher Knowledge Graph endpoint.
- Provide self-hosted Arabic-to-English answer translation through LibreTranslate.
- Expose health, readiness, metrics, and structured logs.
- Provide a simple Next.js web UI.
- Provide a smoke evaluation script.

## 4. Non-scope

The project does not include:

- PDF upload.
- DOCX parsing.
- Contract review.
- Risk scoring.
- LangChain.
- OpenAI or Groq API calls.
- Broad legal chatbot behavior.
- Production legal-advice workflows.

## 5. Architecture

```text
User
  -> Web UI on http://localhost:3001
  -> FastAPI on http://localhost:8001
  -> Weaviate on http://localhost:8081
  -> retrieved legal chunks
  -> xAI/Grok or Ollama
  -> Arabic answer with backend citations
  -> optional LibreTranslate English translation
```

Docker Compose runs Weaviate, Neo4j, LibreTranslate, the FastAPI API, and the web UI. Ollama is optional and does not run in Docker; when enabled, the API container connects to host Ollama through:

```text
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

## 6. File-by-file Explanation

### `api/main.py`

Creates the FastAPI application. It defines:

- `GET /healthz` for basic API health.
- `GET /readyz` for Weaviate, Neo4j, and selected LLM provider readiness checks.
- `POST /rag/answer` for the main RAG answer endpoint.
- `POST /kg/query` for the Knowledge Graph Text2Cypher endpoint.
- `POST /translate` for Arabic-to-English machine translation.
- CORS settings for the web UI.
- Observability middleware and metrics setup.

The routes catch LLM, KG, and translation errors and return clean API responses.

### `api/settings.py`

Defines environment-driven settings using Pydantic settings. Important values include Weaviate URL/class, embedding model, retrieval limits, xAI/Ollama provider settings, Neo4j settings, LibreTranslate settings, API URL, web URL, and CORS origin.

### `api/models.py`

Defines Pydantic request and response models:

- `RAGRequest`
- `Citation`
- `RetrievedChunk`
- `RAGResponse`
- `KGRequest`
- `KGResponse`
- `HealthResponse`
- `ReadyResponse`
- `TranslateRequest`
- `TranslateResponse`

These models keep the API response shape explicit and testable.

### `api/deps.py`

Small dependency module that exposes `get_settings` and `Settings` for FastAPI dependency injection.

### `api/rag.py`

Contains the core RAG flow:

1. Normalize and embed the user question.
2. Query Weaviate using a near-vector search.
3. Convert vector distance to an approximate score.
4. Rerank using a small lexical overlap bonus.
5. Build a grounded Arabic prompt from the top retrieved chunks.
6. Call the generator.
7. Clean the answer.
8. Build backend citations and retrieved chunk previews.

Citations are created by the backend from retrieved chunks. The LLM is not trusted to invent or format citations.

### `api/generator.py`

Calls the configured LLM provider through HTTP using `httpx`.

Supported providers:

- `xai` / `grok`, using the OpenAI-compatible chat completions API at `XAI_BASE_URL`.
- `ollama`, using the local `/api/chat` endpoint.

It removes `<think>...</think>` blocks from model output and returns an abstention message if the output is empty.

### `api/kg.py`

Implements the Neo4j Text2Cypher proof of concept. It builds schema-bounded Cypher with the configured LLM, validates read-only Cypher, executes it against Neo4j, and serializes records, nodes, relationships, generated Cypher, and an Arabic summary.

### `api/translation.py`

Calls LibreTranslate for Arabic-to-English answer translation. Translation is a UI convenience only; the Arabic answer remains the authoritative legal-language response.

### `api/observability.py`

Defines:

- Prometheus counters, histograms, and gauges.
- Request ID middleware.
- Structured JSON request logging.
- Metrics middleware.
- `/metrics` ASGI app mount.

Metric labels are bounded and do not include user questions or request IDs.

### `api/seed_weaviate.py`

Seeds Weaviate from `api/seed_chunks.json`. It:

1. Reads and validates seed chunks.
2. Connects to Weaviate.
3. Deletes the existing `LegalChunk` class if present.
4. Creates a schema with external vectors and cosine distance.
5. Embeds chunk text with `intfloat/multilingual-e5-small`.
6. Batch inserts chunks with vectors.
7. Prints a short summary.

Known successful seed summary:

```text
class: LegalChunk
chunks_loaded: 73
embedding_model: intfloat/multilingual-e5-small
first_chunk_id: official_labor_law_art_002_p01
last_chunk_id: betterwork_guide_page_067
```

### `api/seed_neo4j.py`

Seeds the Neo4j proof-of-concept graph from `api/seed_graph.json`.

### `api/seed_chunks.json`

JSON array containing the legal chunks used for Weaviate seeding. Each chunk includes:

- `chunk_id`
- `source_name`
- `reference`
- `topic`
- `text`
- `source_page`
- `source_type`
- `jurisdiction`
- `embedding_text`

The current seed file contains 73 legal chunks.

### `data/rag_smoke.json`

Small smoke evaluation fixture. It contains 5 Arabic test questions and expected topic/reference hints where available.

### `data/kg_questions.json`

Knowledge Graph evaluation fixture. It starts empty until reviewed question/gold Cypher pairs are added.

### `eval_rag_smoke.py`

Command-line smoke evaluation script. It calls the live API, measures latency, checks answer presence, citation presence, abstention count, retrieval hits when expected chunk IDs exist, and reference hits when expected reference text exists.

Default output:

```text
outputs/rag_smoke_results.json
```

### `docker-compose.yml`

Defines the local stack:

- `weaviate` on host port `8081`.
- `neo4j` on host ports `7474` and `7687`.
- `api` on host port `8001`.
- `libretranslate` as an internal Docker service on port `5000`.
- `web` on host port `3001`.

It also maps `host.docker.internal` so the API container can reach host Ollama when `LLM_PROVIDER=ollama`.

### `api/Dockerfile`

Builds the Python API image. It installs CPU-only Torch first, then installs `requirements.txt`, copies the API package and seed script, and starts Uvicorn.

### `web/pages/index.js`, `web/pages/rag.js`, and `web/pages/kg.js`

Next.js pages for the home screen, RAG assistant, and KG assistant. The RAG and KG result views include:

- Arabic legal answer display.
- Citations or graph entities where available.
- Retrieved evidence or technical details.
- Copy answer action.
- English translation action through `web/components/TranslationToggle.js`.

### `web/package.json`

Defines the web dependencies and scripts:

- `next`
- `react`
- `react-dom`
- `npm run dev`
- `npm run build`
- `npm run start`

### `seed_weaviate.sh`

Small helper script that runs:

```bash
python -m api.seed_weaviate
```

On Windows, teammates can run the Python module directly inside the API container instead:

```powershell
docker compose -p lawz-ai-jo exec api python -m api.seed_weaviate
```

### `README.md`

Primary teammate-facing setup document. It is Windows-first and includes ports, prerequisites, setup commands, troubleshooting, evaluation, and GitHub safety notes.

## 7. Runtime Flow

### User Question

The user enters an Arabic labor-law information question in the web UI or sends it directly to:

```text
POST /rag/answer
```

Example:

```json
{
  "question": "هل يجوز إنهاء عقد العمل بدون إشعار؟",
  "k": 5
}
```

### Question Embedding

The API formats the question for the E5 embedding model:

```text
query: {question}
```

It embeds the question using `intfloat/multilingual-e5-small`.

### Weaviate Retrieval

The API queries the `LegalChunk` class in Weaviate using near-vector search. It asks for legal chunk fields plus vector distance metadata.

### Reranking

The API combines:

- Vector score from Weaviate distance.
- Small lexical overlap bonus from normalized Arabic question terms and chunk text/topic/reference.

This stays simple and avoids cross-encoders or additional ML models.

### Prompt Building

The API builds a grounded Arabic prompt from the top retrieved chunks. The prompt tells the model:

- Use only retrieved legal texts.
- Do not invent references.
- Do not provide final legal advice.
- Say clearly when context is insufficient.
- Do not output `<think>`.

### Configured LLM Generation

The default fast path is xAI/Grok:

```text
LLM_PROVIDER=xai
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-4.3
```

Ollama remains available as an optional local provider:

```text
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=qwen3:4b
```

### Response With Backend Citations

The API returns:

- `answer`
- `citations`
- `confidence`
- `retrieved_chunks`
- `disclaimer`

Citations are created from retrieved chunks, not from the LLM output.

## 8. Models

### Embedding Model

```text
intfloat/multilingual-e5-small
```

This model supports multilingual retrieval and works well with E5 prefixes:

- `query:` for user questions.
- `passage:` for legal chunks.

### Generator

```text
xAI/Grok by default, Ollama qwen3:4b as an optional local provider
```

The xAI path is the recommended fast path. The Ollama path runs locally through Ollama and can be slow on typical laptops.

## 9. Data

### Legal Chunks

Current seed data:

```text
api/seed_chunks.json
```

Count:

```text
73 legal chunks
```

### Weaviate Class

Class name:

```text
LegalChunk
```

Schema fields:

- `chunk_id`
- `source_name`
- `reference`
- `topic`
- `text`
- `source_page`
- `source_type`
- `jurisdiction`

Vectors are provided externally by the API seeding script. Weaviate does not vectorize text by itself.

### Citation Fields

Each citation returned by the API includes:

- `chunk_id`
- `source_name`
- `reference`
- `topic`
- `source_page`

### Knowledge Graph Data

Neo4j seed data lives in:

```text
api/seed_graph.json
```

It is loaded by:

```bash
python -m api.seed_neo4j
```

### Translation Data

LibreTranslate stores downloaded or prepared language assets in the Docker volume:

```text
libretranslate_models
```

## 10. How To Run On Windows

Recommended path for teammates: Windows PowerShell + Docker Desktop + xAI API key.

Do not run this from WSL unless you know your Docker networking. `jq` is optional on Windows; the documented commands do not require it.

```powershell
git clone <repo-url>
cd <repo-folder>
Copy-Item .env.example .env
notepad .env
```

Set a real `XAI_API_KEY` in `.env`. Keep this value when the API runs through Docker Compose:

```env
LIBRETRANSLATE_URL=http://libretranslate:5000
```

Optional Ollama setup:

```powershell
ollama pull qwen3:4b
ollama list
curl.exe http://localhost:11434/api/tags
```

Use Ollama only if `.env` sets `LLM_PROVIDER=ollama`.

```powershell
docker compose -p lawz-ai-jo up -d --build
docker compose -p lawz-ai-jo ps

curl.exe http://localhost:8001/healthz
curl.exe http://localhost:8001/readyz

docker compose -p lawz-ai-jo exec api python -m api.seed_weaviate
docker compose -p lawz-ai-jo exec -T api python -m api.seed_neo4j

curl.exe -X POST http://localhost:8001/rag/answer -H "Content-Type: application/json" -d "{\"question\":\"هل يجوز إنهاء عقد العمل بدون إشعار؟\",\"k\":5}"
curl.exe -X POST http://localhost:8001/kg/query -H "Content-Type: application/json" -d "{\"question\":\"ما المواد المرتبطة بإنهاء عقد العمل؟\"}"
curl.exe -X POST http://localhost:8001/translate -H "Content-Type: application/json" -d "{\"text\":\"يجوز للعامل إنهاء العقد في الحالات التي يحددها القانون.\"}"
```

Open:

```text
http://localhost:3001
```

## 11. How To Run On Linux

Create `.env` and set `XAI_API_KEY`:

```bash
cp .env.example .env
$EDITOR .env
```

Keep this value when the API runs through Docker Compose:

```env
LIBRETRANSLATE_URL=http://libretranslate:5000
```

Optional Ollama setup:

```bash
ollama pull qwen3:4b
curl http://localhost:11434/api/tags
```

Start the stack:

```bash
docker compose -p lawz-ai-jo up -d --build
docker compose -p lawz-ai-jo ps
```

Check readiness:

```bash
curl http://localhost:8001/healthz
curl http://localhost:8001/readyz
```

Seed:

```bash
docker compose -p lawz-ai-jo exec api python -m api.seed_weaviate
docker compose -p lawz-ai-jo exec -T api python -m api.seed_neo4j
```

Ask:

```bash
curl -X POST http://localhost:8001/rag/answer \
  -H "Content-Type: application/json" \
  -d '{"question":"هل يجوز إنهاء عقد العمل بدون إشعار؟","k":5}'

curl -X POST http://localhost:8001/kg/query \
  -H "Content-Type: application/json" \
  -d '{"question":"ما المواد المرتبطة بإنهاء عقد العمل؟"}'

curl -X POST http://localhost:8001/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"يجوز للعامل إنهاء العقد في الحالات التي يحددها القانون."}'
```

## 12. Troubleshooting History

### Docker Ports Already Taken

Issue: Docker ports `8001`, `8081`, and `3001` were already taken by old `docker-proxy` processes from another Docker context.

Fix: Checked Docker contexts and stopped old main-repo containers that were still holding the ports.

Useful commands:

```bash
docker context ls
docker ps
docker compose -p <old-project-name> down
```

### Compose File Had `api` At Root Level

Issue: `docker-compose.yml` once had `api` at the root level and failed with:

```text
additional properties 'api' not allowed
```

Fix: Ensured `api` is nested under the top-level `services:` key.

### `/metrics` Redirects

Issue: `GET /metrics` returned a `307` redirect to `/metrics/`.

Fix: Use:

```bash
curl -L http://localhost:8001/metrics
```

or:

```bash
curl http://localhost:8001/metrics/
```

On Windows PowerShell, use `curl.exe`.

### Local Eval Missing `httpx`

Issue: The local evaluation script failed in `.venv` because `httpx` was missing.

Fix:

```bash
python -m pip install httpx
```

### Slow Generation

Issue: Optional `qwen3:4b` generation was slow, taking around 2-4 minutes per answer.

Fix: Use a longer timeout for evaluation:

```bash
python eval_rag_smoke.py --api-url http://localhost:8001 --timeout 300 --output outputs/rag_smoke_results.json
```

### Translation Unavailable

Issue: `POST /translate` returns `503`.

Fix: Check the `libretranslate` container and confirm the API container uses the Docker service URL:

```env
LIBRETRANSLATE_URL=http://libretranslate:5000
```

Use `http://localhost:5000` only when the API itself runs directly on the host.

### xAI Not Ready

Issue: `/readyz` reports that the LLM provider is not ready.

Fix: Confirm `.env` contains a real xAI key and the expected model settings:

```env
LLM_PROVIDER=xai
XAI_API_KEY=xai-...
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-4.3
```

## 13. Known Limitations

- Not legal advice.
- Small legal corpus.
- Small smoke evaluation.
- Optional local generation can be slow.
- Machine translation is convenience-only and may need review.
- Confidence score is approximate.
- LLM wording may need legal review.

## 14. Future Work

- Add 50+ hand-labeled evaluation questions.
- Improve confidence scoring.
- Explore faster generation options.
- Add a smaller model option.
- Improve frontend loading and progress feedback.
- Add a dataset card.
- Add reviewed KG evaluation fixtures.
- Add optional contract upload later.
- Add optional report export later.
- Explore possible hosted deployment.

## 15. Appendix: Key Commands

### Start

```powershell
docker compose -p lawz-ai-jo up -d --build
```

### Stop

```powershell
docker compose -p lawz-ai-jo down
```

### Stop And Delete Volumes

```powershell
docker compose -p lawz-ai-jo down -v
```

### Check Services

```powershell
docker compose -p lawz-ai-jo ps
```

### API Health

```powershell
curl.exe http://localhost:8001/healthz
curl.exe http://localhost:8001/readyz
```

### Ollama Health

```powershell
curl.exe http://localhost:11434/api/tags
```

Only needed when using `LLM_PROVIDER=ollama`.

### Seed Weaviate

```powershell
docker compose -p lawz-ai-jo exec api python -m api.seed_weaviate
```

### Seed Neo4j

```powershell
docker compose -p lawz-ai-jo exec -T api python -m api.seed_neo4j
```

### Ask A Question

```powershell
curl.exe -X POST http://localhost:8001/rag/answer -H "Content-Type: application/json" -d "{\"question\":\"هل يجوز إنهاء عقد العمل بدون إشعار؟\",\"k\":5}"
```

### Ask The Knowledge Graph

```powershell
curl.exe -X POST http://localhost:8001/kg/query -H "Content-Type: application/json" -d "{\"question\":\"ما المواد المرتبطة بإنهاء عقد العمل؟\"}"
```

### Translate Text

```powershell
curl.exe -X POST http://localhost:8001/translate -H "Content-Type: application/json" -d "{\"text\":\"يجوز للعامل إنهاء العقد في الحالات التي يحددها القانون.\"}"
```

### Metrics

```powershell
curl.exe -L http://localhost:8001/metrics
```

### API Logs

```powershell
docker compose -p lawz-ai-jo logs api --tail=120
```

### Smoke Evaluation

```powershell
python eval_rag_smoke.py --api-url http://localhost:8001 --timeout 300 --output outputs/rag_smoke_results.json
```
