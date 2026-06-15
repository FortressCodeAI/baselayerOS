# baselayeros/companies/compliance/nodes/generate_calendar.py

from dataclasses import dataclass
from datetime import date, timedelta
from kali.refusal import refuse


@dataclass
class GenerateCalendar:
    """
    Deterministic compliance calendar generator.
    Produces a stub schedule of due dates.
    """

    def run(self) -> dict[str, str]:
        today = date.today()

        calendar = {
            "annual_report_due": str(today.replace(month=12, day=31)),
            "policy_review_due": str(today + timedelta(days=90)),
            "financial_statement_due": str(today + timedelta(days=30)),
        }

        if not calendar:
            refuse("Calendar generation failed", code="CALENDAR_EMPTY")

        return calendar
