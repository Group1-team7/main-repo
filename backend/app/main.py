import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import analyze, chat, health, report
from app.services.guardrails import DISCLAIMER


def _cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="Lawz AI JO Ultra-MVP",
    version="0.1.0",
    description=(
        "Educational capstone MVP for first-pass Jordanian employment contract "
        "risk triage. This service does not provide legal advice."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(chat.router)
app.include_router(report.router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "disclaimer": DISCLAIMER},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "disclaimer": DISCLAIMER},
    )


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Lawz AI JO Ultra-MVP",
        "status": "ok",
        "disclaimer": DISCLAIMER,
    }
