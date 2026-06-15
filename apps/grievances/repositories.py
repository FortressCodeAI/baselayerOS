from __future__ import annotations
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from apps.grievances.models import Grievance, ReportSnapshot


def create_grievance(db: Session, g: Grievance) -> Grievance:
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


def get_grievance(db: Session, grievance_id: int) -> Optional[Grievance]:
    stmt = select(Grievance).where(Grievance.id == grievance_id)
    return db.scalar(stmt)


def list_grievances(
    db: Session, limit: int = 100, offset: int = 0
) -> List[Grievance]:
    stmt = (
        select(Grievance)
        .order_by(Grievance.filed_date.desc(), Grievance.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt))


def update_grievance(db: Session, g: Grievance) -> Grievance:
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


def count_by_status(db: Session) -> dict[str, int]:
    stmt = select(Grievance.status, func.count(Grievance.id)).group_by(
        Grievance.status
    )
    result: Result = db.execute(stmt)

    # Each row is a Row object -> row[0], row[1]
    return {row[0]: row[1] for row in result}


def count_by_employer(db: Session) -> dict[str, int]:
    stmt = select(Grievance.employer, func.count(Grievance.id)).group_by(
        Grievance.employer
    )
    result: Result = db.execute(stmt)

    return {row[0]: row[1] for row in result}


def create_report_snapshot(db: Session, label: str, payload: str) -> ReportSnapshot:
    snap = ReportSnapshot(label=label, payload=payload)
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap
