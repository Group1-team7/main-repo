from fastapi import APIRouter

from app.monitoring.metrics import snapshot
from app.services.guardrails import DISCLAIMER

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "lawz-ai-jo-ultra-mvp",
        "disclaimer": DISCLAIMER,
    }


@router.get("/metrics")
def metrics() -> dict[str, int | str]:
    return {**snapshot(), "disclaimer": DISCLAIMER}
