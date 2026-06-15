from __future__ import annotations
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator


Status = Literal["draft", "filed", "investigating", "resolved", "closed"]


class GrievanceBase(BaseModel):
    member_name: str = Field(..., max_length=255)
    member_id: str = Field(..., max_length=64)
    employer: str = Field(..., max_length=255)
    incident_date: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$")
    filed_date: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$")
    issue_summary: str
    requested_remedy: str
    notes: Optional[str] = None

    @validator("filed_date")
    def filed_not_before_incident(cls, v: str, values: dict) -> str:
        incident = values.get("incident_date")
        if incident and v < incident:
            raise ValueError("filed_date cannot be before incident_date")
        return v


class GrievanceCreate(GrievanceBase):
    pass


class GrievanceUpdate(BaseModel):
    issue_summary: Optional[str] = None
    requested_remedy: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[Status] = None


class GrievanceRead(GrievanceBase):
    id: int
    status: Status
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportSummary(BaseModel):
    total_grievances: int
    by_status: dict[str, int]
    by_employer: dict[str, int]
    generated_at: datetime
