from __future__ import annotations
from datetime import datetime
import json

from fastapi import APIRouter, Depends
from collections.abc import Generator
from sqlalchemy.orm import Session

from apps.grievances.database import SessionLocal
from apps.grievances.repositories import (
    count_by_status,
    count_by_employer,
    create_report_snapshot,
)
from apps.grievances.schemas import ReportSummary

router = APIRouter(prefix="/reports", tags=["reports"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/summary", response_model=ReportSummary)
def summary(db: Session = Depends(get_db)) -> ReportSummary:
    by_status = count_by_status(db)
    by_employer = count_by_employer(db)
    total = sum(by_status.values())
    payload = {
        "total_grievances": total,
        "by_status": by_status,
        "by_employer": by_employer,
        "generated_at": datetime.utcnow().isoformat(),
    }
    create_report_snapshot(db, "summary", json.dumps(payload, separators=(",", ":")))
    return ReportSummary(
        total_grievances=total,
        by_status=by_status,
        by_employer=by_employer,
        generated_at=datetime.utcnow(),
    )
