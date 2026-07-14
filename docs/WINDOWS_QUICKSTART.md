# Windows Quickstart

Recommended path for teammates: Windows PowerShell + Docker Desktop + xAI API key.

Do not run this from WSL unless you know your Docker networking.

## 1. Install Docker Desktop

Install Docker Desktop for Windows and make sure it is running with Linux containers / WSL2 backend.

## 2. Prepare Your LLM Provider

The recommended fast path is xAI/Grok. You need a real `XAI_API_KEY` in `.env`.

Ollama is optional. Use it only if you set `LLM_PROVIDER=ollama`.

Optional Ollama setup:

```powershell
ollama pull qwen3:4b
ollama list
```

`jq` is optional on Windows and is not required for these commands.

## 3. Clone The Repo

```powershell
git clone <repo-url>
cd <repo-folder>
```

## 4. Copy The Env File

```powershell
Copy-Item .env.example .env
notepad .env
```

Set your xAI key:

```env
LLM_PROVIDER=xai
XAI_API_KEY=your_xai_api_key_here
XAI_BASE_URL=https://api.x.ai/v1
XAI_MODEL=grok-4.3
```

Keep LibreTranslate configured with the Docker service name:

```env
LIBRETRANSLATE_URL=http://libretranslate:5000
```

## 5. Run The Stack

```powershell
docker compose -p lawz-ai-jo up -d --build
```

## 6. Seed Weaviate

```powershell
docker compose -p lawz-ai-jo exec api python -m api.seed_weaviate
```

Optional KG seed:

```powershell
docker compose -p lawz-ai-jo exec -T api python -m api.seed_neo4j
```

## 7. Smoke Test The API

```powershell
curl.exe http://localhost:8001/readyz
curl.exe -X POST http://localhost:8001/rag/answer -H "Content-Type: application/json" -d "{\"question\":\"هل يجوز إنهاء عقد العمل بدون إشعار؟\",\"k\":5}"
curl.exe -X POST http://localhost:8001/kg/query -H "Content-Type: application/json" -d "{\"question\":\"ما المواد المرتبطة بإنهاء عقد العمل؟\"}"
curl.exe -X POST http://localhost:8001/translate -H "Content-Type: application/json" -d "{\"text\":\"يجوز للعامل إنهاء العقد في الحالات التي يحددها القانون.\"}"
```

## 8. Open The App

```text
http://localhost:3001
```

The first LibreTranslate start can take longer while language assets are prepared. If you use optional Ollama, `qwen3:4b` can take 2-4 minutes per question on local machines.

## If It Fails

Check Ollama, only when using `LLM_PROVIDER=ollama`:

```powershell
curl.exe http://localhost:11434/api/tags
```

Check API readiness:

```powershell
curl.exe http://localhost:8001/readyz
```

Check API logs:

```powershell
docker compose -p lawz-ai-jo logs api --tail=120
```

Check LibreTranslate:

```powershell
docker compose -p lawz-ai-jo ps libretranslate
```

Stop the stack:

```powershell
docker compose -p lawz-ai-jo down
```
