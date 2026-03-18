from __future__ import annotations

from fastapi import APIRouter

from app.services.normalize_service import normalize_steps

router = APIRouter(tags=["normalize"])


@router.post("/normalize")
def normalize(limit: int = 100, since_id: int = 0):
    return normalize_steps(limit=limit, since_id=since_id)
