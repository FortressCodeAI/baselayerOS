# baselayeros/regulus/dashboard.py

from dataclasses import dataclass


from baselayeros.regulus.ui_flow import RegulusUIFlow
from baselayeros.regulus.audit_view import RegulusAuditView
from kali.audit_chain import AuditChain


@dataclass
class RegulusDashboard:
    """
    Simple Regulus dashboard renderer (HTML + CLI).
    """

    audit_chain: AuditChain

    def render_cli(self) -> str:
        flow = RegulusUIFlow.default().to_dict()
        audit_view = RegulusAuditView(self.audit_chain)

        lines: list[str] = []
        lines.append("=== Regulus Dashboard ===")
        lines.append("\nFlow:")
        for step in flow["steps"]:
            lines.append(f"- {step['id']}: {step['label']} — {step['description']}")

        lines.append("\nAudit Events:")
        lines.append(audit_view.pretty_print() or "(none)")

        return "\n".join(lines)

    def render_html(self) -> str:
        flow = RegulusUIFlow.default().to_dict()
        audit_view = RegulusAuditView(self.audit_chain).summarize()

        steps_html = "".join(
            f"<li><strong>{s['label']}</strong>: {s['description']}</li>"
            for s in flow["steps"]
        )

        events_html = "".join(
            f"<li>[{e['type'].upper()}] {e['detail']}</li>"
            for e in audit_view["events"]
        )

        return f"""
<!DOCTYPE html>
<html>
<head>
  <title>Regulus Dashboard</title>
</head>
<body>
  <h1>Regulus Dashboard</h1>

  <h2>Flow</h2>
  <ul>
    {steps_html}
  </ul>

  <h2>Audit Events</h2>
  <ul>
    {events_html or "<li>(none)</li>"}
  </ul>
</body>
</html>
""".strip()
