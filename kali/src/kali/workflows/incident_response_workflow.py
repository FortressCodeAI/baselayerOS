def classify_alert(data):

    text = data.get(
        "alert",
        ""
    ).lower()

    severity = "low"

    if (
        "unauthorized"
        in text
    ):
        severity = "high"

    return {

        "step":
            "classification",

        "severity":
            severity
    }


def response_plan(data):

    return {

        "step":
            "response",

        "action":
            "escalate"
    }


WORKFLOW = [

    classify_alert,

    response_plan
]