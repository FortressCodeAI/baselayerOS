from __future__ import annotations

from typing import Any, Dict, List

from kali.engine import execute_workflow


def main() -> Dict[str, Any]:
    steps: List[Dict[str, Any]] = [
        {
            "action": "summarize_stream",
            "data": {"text": "First, summarize this long stream of governance events."},
            "capability_envelope": ["summarize_stream"],
        },
        {
            "action": "extract_entities",
            "data": {"text": "Then extract entities from the summarized governance stream."},
            "capability_envelope": ["extract_entities"],
        },
    ]

    return execute_workflow(steps, meta={"workflow": "governed_summary_pipeline"})
