from __future__ import annotations
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base


class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    member_name = Column(String(255), nullable=False)
    member_id = Column(String(64), nullable=False, index=True)
    employer = Column(String(255), nullable=False)
    incident_date = Column(String(10), nullable=False)
    filed_date = Column(String(10), nullable=False)
    issue_summary = Column(Text, nullable=False)
    requested_remedy = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(32), nullable=False, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ReportSnapshot(Base):
    __tablename__ = "report_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    label = Column(String(255), nullable=False)
    payload = Column(Text, nullable=False)
