from dataclasses import dataclass
from typing import Dict, Any, List

from kali.audit_chain import AuditChain


@dataclass
class RegulusAuditView:
    """
    Visualizes Regulus decisions and audit chain events.
    """

    audit_chain: AuditChain

    def summarize(self) -> Dict[str, Any]:
        events = [
            {
                "type": e.event_type,
                "detail": e.detail,
                "timestamp": getattr(e, "timestamp", None),
            }
            for e in self.audit_chain.events
        ]

        return {
            "total_events": len(events),
            "events": events,
        }

    def pretty_print(self) -> str:
        lines: List[str] = []
        for e in self.audit_chain.events:
            lines.append(f"[{e.event_type.upper()}] {e.detail}")
        return "\n".join(lines)
