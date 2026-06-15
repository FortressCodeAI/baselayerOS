from fastapi import APIRouter
from .publish_pipeline import publish_pack

router = APIRouter()

@router.post("/api/publish/{pack_id}")
def publish(pack_id: str):
    result = publish_pack(pack_id)
    return result
