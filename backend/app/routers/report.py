from fastapi import APIRouter

from app.services.guardrails import DISCLAIMER

router = APIRouter(tags=["report"])


@router.get("/legal-disclaimer")
def legal_disclaimer() -> dict[str, str]:
    return {"disclaimer": DISCLAIMER}
