"""
Deterministic credit risk evaluation module.

Action: credit_risk.evaluate

Inputs:
    income: number
    credit_score: number
    existing_debt: number

Output:
    {
        "decision": "APPROVED" | "REVIEW" | "DECLINED",
        "reason": string
    }

Rules:
    - DECLINED if credit_score < 580
    - REVIEW if credit_score < 670 or debt-to-income ratio > 0.4
    - APPROVED otherwise
"""

def evaluate(payload: dict) -> dict:
    income = payload.get("income")
    credit_score = payload.get("credit_score")
    existing_debt = payload.get("existing_debt")

    # Basic validation
    if not isinstance(income, (int, float)) or income <= 0:
        return {
            "decision": "DECLINED",
            "reason": "Invalid or missing income"
        }

    if not isinstance(credit_score, (int, float)):
        return {
            "decision": "DECLINED",
            "reason": "Invalid or missing credit score"
        }

    if not isinstance(existing_debt, (int, float)) or existing_debt < 0:
        return {
            "decision": "DECLINED",
            "reason": "Invalid or missing existing debt"
        }

    # Deterministic rules
    if credit_score < 580:
        return {
            "decision": "DECLINED",
            "reason": "Credit score below minimum threshold"
        }

    dti = existing_debt / income

    if credit_score < 670:
        return {
            "decision": "REVIEW",
            "reason": "Credit score in manual review band"
        }

    if dti > 0.4:
        return {
            "decision": "REVIEW",
            "reason": "Debt-to-income ratio exceeds 40%"
        }

    return {
        "decision": "APPROVED",
        "reason": "Meets all deterministic criteria"
    }
