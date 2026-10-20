"""
Kali v1.0.0 — HTTP API Interface

Minimal FastAPI-based HTTP API for Kali.

Endpoints:
- POST /govern
"""

from __future__ import annotations
from typing import Dict, Any

from fastapi import FastAPI, HTTPException

from kali.core.logging import get_logger
from kali.operators.request_operator import RequestOperator
from run_kali import build_kali_operator


app = FastAPI(title="Kali Governance Operator API", version="1.0.0")

logger = get_logger("api")
operator = build_kali_operator()
request_op = RequestOperator(logger=logger)


@app.post("/govern")
async def govern(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a full governance cycle on the given request.
    """
    try:
        normalized = request_op.normalize(request)
        result = operator.process(normalized)
        return result
    except Exception as e:
        logger.error("api_error", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
