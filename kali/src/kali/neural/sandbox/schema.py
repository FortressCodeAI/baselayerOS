"""
Kali v1.0.0 — Neural Sandbox Schema

Defines allowed output structures for:
- explanations
- summaries
- interpretations

We keep it simple and strict for v1.0.0.
"""

from __future__ import annotations
from typing import Dict, Any


def validate_explanation(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure explanation has required fields.
    """
    if not isinstance(output, dict):
        return {
            "text": str(output),
            "format": "text",
        }

    # Required fields
    text = output.get("text")
    if not text:
        output["text"] = str(output)

    output.setdefault("format", "text")
    return output
