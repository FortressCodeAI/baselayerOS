# baselayeros/regulus/timeline.py

from dataclasses import dataclass
from typing import List, Dict, Any

from kali.audit_chain import AuditChain


@dataclass
class DecisionTimeline:
    """
    Builds a simple chronological timeline of Regulus-related events.
    """

    audit_chain: AuditChain

    def build(self) -> List[Dict[str, Any]]:
        timeline: List[Dict[str, Any]] = []

        for event in self.audit_chain.events:
            timeline.append(
                {
                    "type": event.event_type,
                    "detail": event.detail,
                    "timestamp": getattr(event, "timestamp", None),
                }
            )

        return timeline

    def pretty_print(self) -> str:
        lines: List[str] = ["=== Regulus Decision Timeline ==="]
        for e in self.build():
            ts = e["timestamp"] or "no-ts"
            lines.append(f"[{ts}] {e['type'].upper()}: {e['detail']}")
        return "\n".join(lines)
