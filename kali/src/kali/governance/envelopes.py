from __future__ import annotations
from typing import Any, Dict, List

def apply_envelopes(action: str, data: Dict[str, Any], envelopes: List[str]) -> Dict[str, Any]:
    governed = dict(data)

    if "priority_collapse" in envelopes:
        governed = _priority_collapse(governed)

    if "summarize_stream" in envelopes:
        governed = _summarize(governed)

    if "extract_entities" in envelopes:
        governed = _extract_entities(governed)

    return governed

def _priority_collapse(data: Dict[str, Any]) -> Dict[str, Any]:
    items = data.get("items")
    if not isinstance(items, list):
        return data
    collapsed = sorted(items, key=lambda x: x.get("priority", 0), reverse=True)
    return {"items": collapsed[:5]}

def _summarize(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("text")
    if not isinstance(text, str):
        return data
    return {"summary": text[:200] + "..."} if len(text) > 200 else {"summary": text}

def _extract_entities(data: Dict[str, Any]) -> Dict[str, Any]:
    text = data.get("text")
    if not isinstance(text, str):
        return data
    tokens = text.split()
    entities = [t.strip(",.") for t in tokens if t[:1].isupper()]
    return {"entities": entities, "original": text}
