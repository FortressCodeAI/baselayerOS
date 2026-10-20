def governance_check(payload):

    return {

        "step":
            "governance",

        "allowed":
            True
    }


def llm_execution(payload):

    prompt = payload.get(
        "prompt",
        ""
    )

    return {

        "step":
            "llm",

        "response":
            f"Governed response: {prompt}"
    }


WORKFLOW = [

    governance_check,

    llm_execution
]