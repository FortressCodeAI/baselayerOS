def evaluate_risk(data):

    risk = "low"

    if (
        "production"
        in data.get(
            "target",
            ""
        ).lower()
    ):
        risk = "high"

    return {

        "step":
            "risk_assessment",

        "risk":
            risk
    }


def compliance_review(data):

    return {

        "step":
            "compliance_review",

        "approved":
            True
    }


def approval_decision(data):

    risk = (
        evaluate_risk(
            data
        )["risk"]
    )

    return {

        "step":
            "approval",

        "approved":
            risk != "high"
    }


WORKFLOW = [

    evaluate_risk,

    compliance_review,

    approval_decision
]