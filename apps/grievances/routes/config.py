from __future__ import annotations
from fastapi import APIRouter
from ..config.settings import settings

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/info")
def get_info() -> dict:
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "database_url": settings.database_url,
    }
