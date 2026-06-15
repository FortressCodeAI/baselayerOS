from __future__ import annotations
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from collections.abc import Generator
from sqlalchemy.orm import Session

from apps.grievances.database import SessionLocal
from apps.grievances.schemas import (
    GrievanceCreate,
    GrievanceRead,
    GrievanceUpdate,
)
from apps.grievances.models import Grievance
from apps.grievances.repositories import (
    create_grievance,
    list_grievances,
    get_grievance,
)
from apps.grievances.engine.context import EngineContext
from apps.grievances.runtime import apply_command
from apps.grievances.attachment.storage import save_attachment
from apps.grievances.assistant.llm_adapter import LLMAdapter

router = APIRouter(prefix="/grievances", tags=["grievances"])
llm = LLMAdapter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=GrievanceRead)
def create(payload: GrievanceCreate, db: Session = Depends(get_db)) -> GrievanceRead:
    g = Grievance(**payload.model_dump(), status="draft")
    stored = create_grievance(db, g)
    return GrievanceRead.model_validate(stored)


@router.get("/", response_model=List[GrievanceRead])
def list_all(db: Session = Depends(get_db)) -> List[GrievanceRead]:
    return [GrievanceRead.model_validate(g) for g in list_grievances(db)]


@router.get("/{grievance_id}", response_model=GrievanceRead)
def get_one(grievance_id: int, db: Session = Depends(get_db)) -> GrievanceRead:
    g = get_grievance(db, grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Grievance not found")
    return GrievanceRead.model_validate(g)


@router.patch("/{grievance_id}", response_model=GrievanceRead)
def update(
    grievance_id: int,
    payload: GrievanceUpdate,
    db: Session = Depends(get_db),
) -> GrievanceRead:
    g = get_grievance(db, grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Grievance not found")

    ctx = EngineContext(actor="api", run_id=f"update-{grievance_id}")
    cmd = {"type": "update_fields", "payload": payload.model_dump(exclude_unset=True)}
    g = apply_command(db, ctx, g, cmd)
    return GrievanceRead.model_validate(g)


@router.post("/{grievance_id}/transition/{event}", response_model=GrievanceRead)
def transition(
    grievance_id: int,
    event: str,
    db: Session = Depends(get_db),
) -> GrievanceRead:
    g = get_grievance(db, grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Grievance not found")

    ctx = EngineContext(actor="api", run_id=f"transition-{grievance_id}")
    cmd = {"type": "transition", "payload": {"event": event}}
    g = apply_command(db, ctx, g, cmd)
    return GrievanceRead.model_validate(g)


@router.post("/{grievance_id}/attachments")
def upload_attachment(
    grievance_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    g = get_grievance(db, grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Grievance not found")
    
    filename = file.filename or f"attachment-{grievance_id}"
    path = save_attachment(grievance_id, filename, file.file)
    return {"path": str(path)}


@router.post("/{grievance_id}/summary")
def summarize(grievance_id: int, db: Session = Depends(get_db)) -> dict:
    g = get_grievance(db, grievance_id)
    if not g:
        raise HTTPException(status_code=404, detail="Grievance not found")
    summary = llm.summarize_grievance(
        {
            "member_name": g.member_name,
            "member_id": g.member_id,
            "employer": g.employer,
            "issue_summary": g.issue_summary,
            "requested_remedy": g.requested_remedy,
        }
    )
    return {"summary": summary}
