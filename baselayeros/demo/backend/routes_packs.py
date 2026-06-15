from fastapi import APIRouter
from baselayeros.runtime.server import PACK_REGISTRY

router = APIRouter()

@router.get("/api/packs")
def list_packs():
    return [
        {
            "id": p["meta"]["id"],
            "name": p["meta"].get("name"),
            "version": p["meta"].get("version"),
            "domain": p["meta"].get("domain", "finance"),
        }
        for p in PACK_REGISTRY.values()
    ]
